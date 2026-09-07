/* Sherry Guo — small interactions. Plain JS, no dependencies.
   Everything here is optional: the page reads fine with JS off,
   and nothing moves when the visitor prefers reduced motion. */
(function () {
  'use strict';

  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 0. autoplay off for reduced motion ---------- */

  if (reduce) {
    document.querySelectorAll('video[autoplay]').forEach(function (v) {
      v.removeAttribute('autoplay');
      v.pause();
    });
  }

  /* ---------- 2. the photo has mass ----------
     Drag the print and let go; it springs back with a bit of overshoot
     and tilts with its own velocity. A small physics joke. */

  var snap = document.querySelector('.snap');
  if (snap && !reduce) {
    var img = snap.querySelector('img');
    if (img) img.draggable = false;
    var TILT0 = -1.4, K = 0.045, DAMP = 0.86;
    var x = 0, y = 0, vx = 0, vy = 0, tilt = TILT0;
    var held = false, gx = 0, gy = 0, lx = 0, ly = 0, anim = 0;

    function paint() {
      snap.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) rotate(' + tilt.toFixed(2) + 'deg)';
    }
    function settle() {
      if (held) { anim = 0; return; }
      vx += -K * x; vy += -K * y;
      vx *= DAMP; vy *= DAMP;
      x += vx; y += vy;
      tilt += ((TILT0 + vx * 0.9) - tilt) * 0.25;
      paint();
      if (Math.abs(x) + Math.abs(y) + Math.abs(vx) + Math.abs(vy) > 0.15) anim = requestAnimationFrame(settle);
      else { x = y = vx = vy = 0; tilt = TILT0; paint(); anim = 0; }
    }

    snap.classList.add('snap--live');
    snap.addEventListener('pointerdown', function (e) {
      if (e.button) return;
      held = true;
      gx = e.clientX - x; gy = e.clientY - y; lx = e.clientX; ly = e.clientY;
      snap.setPointerCapture(e.pointerId);
      snap.classList.add('snap--held');
      if (anim) { cancelAnimationFrame(anim); anim = 0; }
      e.preventDefault();
    });
    snap.addEventListener('pointermove', function (e) {
      if (!held) return;
      vx = e.clientX - lx; vy = e.clientY - ly;
      lx = e.clientX; ly = e.clientY;
      x = e.clientX - gx; y = e.clientY - gy;
      tilt += ((TILT0 + vx * 0.6) - tilt) * 0.3;
      paint();
    });
    function drop() {
      if (!held) return;
      held = false;
      snap.classList.remove('snap--held');
      if (!anim) anim = requestAnimationFrame(settle);
    }
    snap.addEventListener('pointerup', drop);
    snap.addEventListener('pointercancel', drop);
  }

  /* ---------- 3. a character that does what it wants ----------
     Config comes from window.SPRITE (written by build.py when
     _src/content/sprite.yml exists). Sheet layout: one row per
     animation, frames left to right, all frames the same size.
       { src, w, h, fps, scale, anims: { idle: [row, n], walk: [row, n],
         sit: [row, n], look: [row, n] } }
     The character walks along the bottom of the window. Clicking is a
     suggestion: sometimes it comes over, sometimes it just looks at you. */

  var cfg = window.SPRITE;
  if (cfg && !reduce && innerWidth >= 700) {
    var el = document.createElement('div');
    el.className = 'roam';
    el.setAttribute('aria-hidden', 'true');
    el.title = 'Suggest something. No promises.';
    var scale = cfg.scale || 1;
    var W = cfg.w * scale, H = cfg.h * scale;
    el.style.width = W + 'px';
    el.style.height = H + 'px';
    el.style.backgroundImage = 'url(' + cfg.src + ')';
    el.style.backgroundSize = (cfg.cols * W) + 'px auto';
    document.body.appendChild(el);

    var px = Math.min(innerWidth - W - 40, Math.max(40, innerWidth * 0.62));
    var dir = 1, anim = 'idle', frame = 0, fclock = 0, until = 0, dest = null;
    var SPEED = (cfg.speed || 60) * scale; // px per second
    var last = performance.now();

    function rand(a, b) { return a + Math.random() * (b - a); }
    function set(a, dur) { if (cfg.anims[a]) { anim = a; frame = 0; } until = dur; }
    function draw() {
      var row = cfg.anims[anim][0];
      el.style.backgroundPosition = (-frame * W) + 'px ' + (-row * H) + 'px';
      el.style.transform = 'translateX(' + px.toFixed(1) + 'px) scaleX(' + dir + ')';
    }
    function decide() {
      var r = Math.random();
      if (r < 0.45) { dest = rand(40, innerWidth - W - 40); dir = dest > px ? 1 : -1; set('walk', 1e9); }
      else if (r < 0.75) set('idle', rand(2, 5));
      else set('sit', rand(4, 9));
    }
    function loop(now) {
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      fclock += dt;
      var n = cfg.anims[anim][1];
      if (fclock > 1 / (cfg.fps || 10)) { fclock = 0; frame = (frame + 1) % n; }
      if (anim === 'walk' && dest !== null) {
        px += dir * SPEED * dt;
        if ((dir > 0 && px >= dest) || (dir < 0 && px <= dest)) { px = dest; dest = null; set('idle', rand(1, 3)); }
      } else {
        until -= dt;
        if (until <= 0) decide();
      }
      draw();
      requestAnimationFrame(loop);
    }

    // Suggestions. The character listens about half the time.
    document.addEventListener('click', function (e) {
      if (e.target.closest('a, button, input, textarea, label, video, .snap')) return;
      var tx = Math.min(innerWidth - W - 40, Math.max(40, e.clientX - W / 2));
      dir = tx > px ? 1 : -1;
      if (Math.random() < 0.5) { dest = tx; set('walk', 1e9); }
      else { dest = null; set('look', rand(1.2, 2)); }
    });
    // Looks at the cursor when it comes close, then loses interest.
    addEventListener('mousemove', function (e) {
      if (anim === 'walk' || anim === 'look') return;
      var cx = px + W / 2;
      if (Math.abs(e.clientX - cx) < 140 && innerHeight - e.clientY < H + 60 && Math.random() < 0.02) {
        dir = e.clientX > cx ? 1 : -1;
        set('look', rand(1, 2));
      }
    }, { passive: true });

    set('idle', rand(1, 3));
    requestAnimationFrame(loop);
  }

  /* ---------- 4. for whoever opens the console ---------- */

  try {
    console.log('%cgg. Plain HTML, one CSS file, this script. Source: https://github.com/SherryGuo8023/SherryGuo8023.github.io', 'color:#c6303e');
  } catch (e) { /* no console, no problem */ }
})();
