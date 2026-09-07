"""Build the static site.

    python _src/build.py                          # writes to the repo root (live site)
    python _src/build.py --out new --base /new    # preview build under /new/

Content lives in _src/content. Images live in /images at the site root.
Requires: pip install markdown pyyaml
"""
import argparse
import html
import io
import os
import re
import shutil

import markdown
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONTENT = os.path.join(HERE, "content")
SITE_URL = "https://sherryguo8023.github.io"
WEB3FORMS_KEY = "9f416cc0-9fbb-496c-b33e-6d7fe7a76b90"

NAV = [
    ("Projects", "/portfolio/"),
    ("Papers", "/publications/"),
    ("CV", "/cv/"),
    ("Cats", "/cats/"),
    ("Contact", "/contact/"),
]

DESCRIPTION = "Yunjia Guo — I make AI characters that live inside games."


def esc(s):
    return html.escape(str(s), quote=True)


def read(path):
    return io.open(path, encoding="utf-8").read()


def front_matter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}, text
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]


def md(text, base):
    text = text.replace("{{img}}", "/images").replace("{{base}}", base)
    return markdown.markdown(text, extensions=["extra"])


# ---------------------------------------------------------------- layout

def page(base, *, title, body, current=None, description=""):
    nav = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == current else ""
        nav.append(f'<li><a href="{base}{href}"{cur}>{label}</a></li>')
    full_title = "Yunjia Guo" if title is None else f"{title} – Yunjia Guo"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description or DESCRIPTION)}">
<link rel="icon" href="/images/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&display=swap">
<link rel="stylesheet" href="{base}/style.css">
</head>
<body>
<header class="wrap top">
  <a class="top__name" href="{base}/">Yunjia Guo</a>
  <nav aria-label="Main"><ul class="top__nav">{''.join(nav)}</ul></nav>
</header>
<main class="wrap">
{body}
</main>
<footer class="wrap foot">
  <span>Yunjia Guo, 2026</span>
</footer>
<script>
if (matchMedia('(prefers-reduced-motion: reduce)').matches) {{
  document.querySelectorAll('video[autoplay]').forEach(function (v) {{ v.removeAttribute('autoplay'); v.pause(); }});
}}
</script>
</body>
</html>
"""


def write(out, rel, content):
    path = os.path.join(out, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="\n").write(content)


# ---------------------------------------------------------------- content

def load_projects():
    items = []
    for name in os.listdir(os.path.join(CONTENT, "projects")):
        if not name.endswith(".md"):
            continue
        fm, body = front_matter(read(os.path.join(CONTENT, "projects", name)))
        fm["body"] = body
        items.append(fm)
    items.sort(key=lambda p: p["order"])
    return items


def load_pubs():
    return yaml.safe_load(read(os.path.join(CONTENT, "publications.yml")))


def load_talks():
    return yaml.safe_load(read(os.path.join(CONTENT, "talks.yml")))


def talks_list(talks):
    items = []
    for t in talks:
        links = " ".join(f'<a href="{esc(u)}">{esc(l)}</a>' for l, u in (t.get("links") or []))
        items.append(f"""<li class="paper">
  <h3 class="paper__title">{esc(t['title'])}</h3>
  <p class="paper__venue">{esc(t['event'])}, {t['year']}.</p>
  <p class="paper__summary">{esc(t['summary'])} {links}</p>
</li>""")
    return '<ul class="papers">' + "".join(items) + "</ul>"


def paper_html(p, with_summary):
    title = esc(p["title"])
    if p.get("url"):
        title = f'<a href="{esc(p["url"])}">{title}</a>'
    summary = f'<p class="paper__summary">{esc(p["summary"].strip())}</p>' if with_summary else ""
    return f"""<li class="paper" id="{esc(p['id'])}">
  <h3 class="paper__title">{title}</h3>
  <p class="paper__venue">{esc(p['role'])}. {esc(p['venue'])}. {esc(p['status']).capitalize()}, {p['year']}.</p>
  {summary}
</li>"""


def papers_list(pubs, with_summary=False):
    return '<ul class="papers">' + "".join(paper_html(p, with_summary) for p in pubs) + "</ul>"


def project_row(p, base):
    return f"""<li class="row">
  <a href="{base}/portfolio/{p['slug']}/" tabindex="-1" aria-hidden="true"><img class="row__thumb" src="/images/{p['thumb']}" alt=""></a>
  <div>
    <h3 class="row__title"><a href="{base}/portfolio/{p['slug']}/">{esc(p['title'])}</a></h3>
    <p class="row__tagline">{esc(p['tagline'])}</p>
  </div>
  <span class="row__when">{esc(p['years'])}</span>
</li>"""


def contact_form(base):
    redirect = f"{SITE_URL}{base}/contact/?sent=1"
    return f"""<div id="sent" class="sent" hidden>Sent. Thank you.</div>
<form id="contact" class="form" action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
  <input type="hidden" name="subject" value="New message from sherryguo8023.github.io">
  <input type="hidden" name="from_name" value="Personal website">
  <input type="hidden" name="redirect" value="{redirect}">
  <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="display:none">
  <label for="c-name">Name</label>
  <input id="c-name" type="text" name="name" required>
  <label for="c-email">Email (optional, for a reply)</label>
  <input id="c-email" type="email" name="email">
  <label for="c-msg">Message</label>
  <textarea id="c-msg" name="message" required></textarea>
  <button type="submit">Send</button>
</form>
<script>
if (new URLSearchParams(location.search).get('sent') === '1') {{
  document.getElementById('sent').hidden = false;
  document.getElementById('contact').hidden = true;
}}
</script>"""


# ---------------------------------------------------------------- pages

def build_home(base, projects, pubs, talks):
    mobile = next(p for p in projects if p["slug"] == "bside")
    pc = next(p for p in projects if p["slug"] == "1bside")
    rest = [p for p in projects if p["slug"] not in ("bside", "1bside")]

    def duo(p, img, links, text, video=None):
        ls = "".join(f'<li><a href="{esc(u)}">{esc(l)}</a></li>' for l, u in links)
        if video:
            media = f'<video class="duo__img" autoplay muted loop playsinline preload="metadata" poster="/images/{img}" src="{video}"></video>'
        else:
            media = f'<img class="duo__img" src="/images/{img}" alt="">'
        return f"""<div class="duo__item">
  <a href="{base}/portfolio/{p['slug']}/">{media}</a>
  <h3 class="duo__title"><a href="{base}/portfolio/{p['slug']}/">{esc(p['title'])}</a></h3>
  <p class="duo__when">{esc(p['years'])}</p>
  <p>{text}</p>
  <ul class="duo__links">{ls}</ul>
</div>"""

    body = f"""
<section class="hero">
  <div>
    <h1 class="hero__title">I make AI characters that live inside games.</h1>
    <p class="hero__lede">They post about their day, wander into trouble, and sometimes listen when you tell them not to. I build the systems that keep them alive at <a href="https://www.kotoko.ai/">Kotoko AI</a>, and write about it when something interesting happens.</p>
    <ul class="hero__links">
      <li><a href="{base}/portfolio/">Projects</a></li>
      <li><a href="{base}/publications/">Papers</a></li>
      <li><a href="https://www.linkedin.com/in/yunjiaguo/">LinkedIn</a></li>
    </ul>
  </div>
  <figure class="snap">
    <img src="/images/me.jpg" alt="Yunjia Guo" width="1536" height="1152">
  </figure>
</section>

<section class="section" id="bside">
  <div class="section__head">
    <h2>Bside</h2>
    <p>Two games, one character creator. One lives on your phone; the other lives on your desktop and on Steam. The characters cross between them.</p>
  </div>
  <div class="duo">
    {duo(mobile, 'bside-mobile-home.jpg', [("App Store", "https://apps.apple.com/us/app/bside/id6757434275"), ("Google Play", "https://play.google.com/store/apps/details?id=com.kotoko.bside")],
         "Create a character, raise it, and watch it develop a life of its own. It posts about its day, goes on adventures, and shows up in your videos. iOS and Android.")}
    {duo(pc, 'bside-keyart.jpg', [("Steam", "https://store.steampowered.com/app/3649950/Bside/")],
         "A multiplayer world where every character belongs to a real player and nobody holds a joystick. You whisper suggestions; they decide whether to listen. On Steam.",
         video="/video/bside-desktop-mate.mp4")}
  </div>
</section>

<section class="section" id="projects">
  <div class="section__head">
    <h2>Earlier work</h2>
  </div>
  <ul class="rows">{''.join(project_row(p, base) for p in rest)}</ul>
</section>

<section class="section" id="papers">
  <div class="section__head">
    <h2>Papers</h2>
    <p>What happens when you give game characters a language model and let go of the script.</p>
  </div>
  {papers_list(pubs)}
  <p style="margin-top:1.2rem"><a href="{base}/publications/">Abstracts</a></p>
</section>

<section class="section" id="talks">
  <div class="section__head">
    <h2>Talks</h2>
  </div>
  {talks_list(talks)}
</section>

<section class="section" id="background">
  <div class="section__head">
    <h2>Background</h2>
  </div>
  <ul class="road">
    <li><time>2026</time><p>Finalist, Innovator Award, Women in Tech Awards.</p></li>
    <li><time>2023 – now</time><p><b>Kotoko AI.</b> Building and shipping the AI character systems behind Bside, Desktop Mate, and Dobit.</p></li>
    <li><time>2022 – 2023</time><p><b>Tencent Games, TiMi Studios.</b> Combat systems, character controllers, cameras. Shipped Metal Slug: Awakening; worked on two titles that got cancelled before you could play them.</p></li>
    <li><time>2020 – 2021</time><p><b>NetEase Games.</b> Procedural cities in Houdini, stylised rendering. Credits on Once Human.</p></li>
    <li><time>2019 – 2021</time><p><b>Utrecht University</b>, MSc Game and Media Technology.</p></li>
    <li><time>2015 – 2019</time><p><b>University of Chinese Academy of Sciences</b>, BSc Physics.</p></li>
  </ul>
  <p style="margin-top:1.2rem"><a href="{base}/cv/">Full CV</a></p>
</section>

<section class="section" id="outside">
  <div class="section__head">
    <h2>Outside work</h2>
  </div>
  <div class="aside2">
    <div class="prose">
      <p>Zerg main in StarCraft II, D.Va main in the original Overwatch. Overwatch's sound design is the reason I got into making games. I play everything, though, from big releases to whatever surfaces on itch.io.</p>
      <p>Piano since childhood, currently teaching myself electric guitar.</p>
    </div>
    <div>
      <div class="catpile">
        <img src="/images/cats/guagua.jpg" alt="Guagua" width="104" height="104">
        <img src="/images/cats/lily.jpg" alt="Lily" width="104" height="104">
        <img src="/images/cats/spot.jpg" alt="Spot" width="104" height="104">
      </div>
      <p>We rescue street cats, get them fixed, and find them homes. Three of them refused to leave. <a href="{base}/cats/">More about the cats</a>.</p>
    </div>
  </div>
</section>

<section class="section" id="contact">
  <div class="section__head">
    <h2>Contact</h2>
    <p>Always happy to talk about research, games, or cats. Messages land straight in my inbox.</p>
  </div>
  {contact_form(base)}
</section>
"""
    return page(base, title=None, body=body, current="/")


def build_projects_index(base, projects):
    body = f"""
<header class="pagehead">
  <h1>Projects</h1>
</header>
<ul class="rows">{''.join(project_row(p, base) for p in projects)}</ul>
"""
    return page(base, title="Projects", body=body, current="/portfolio/")


def build_project(base, p):
    links = "".join(f'<li><a href="{esc(u)}">{esc(l)}</a></li>' for l, u in (p.get("links") or []))
    meta = f'<li>{esc(p["years"])}</li><li>{esc(p["role"])}</li>{links}'
    hero_cls = "hero-img img--phone" if p.get("hero_phone") else "hero-img"
    body = f"""
<header class="pagehead">
  <h1>{esc(p['title'])}</h1>
  <p class="lede">{esc(p['tagline'])}</p>
  <ul class="meta">{meta}</ul>
</header>
<img class="{hero_cls}" src="/images/{p['hero']}" alt="">
<div class="prose">
{md(p['body'], base)}
<hr>
<p><a href="{base}/portfolio/">All projects</a></p>
</div>
"""
    return page(base, title=p["title"], body=body, current="/portfolio/", description=p["tagline"])


def build_pubs(base, pubs):
    body = f"""
<header class="pagehead">
  <h1>Papers</h1>
  <p class="lede">What happens when you give game characters a language model and let go of the script.</p>
</header>
{papers_list(pubs, with_summary=True)}
"""
    return page(base, title="Papers", body=body, current="/publications/")


def build_cv(base, pubs, talks):
    fm, text = front_matter(read(os.path.join(CONTENT, "cv.md")))
    html_body = md(text, base).replace("<!-- PUBLICATIONS -->", papers_list(pubs)).replace("<!-- TALKS -->", talks_list(talks))
    body = f"""
<header class="pagehead">
  <h1>CV</h1>
</header>
<div class="prose">
{html_body}
</div>
"""
    return page(base, title="CV", body=body, current="/cv/")


def build_cats(base):
    fm, text = front_matter(read(os.path.join(CONTENT, "cats.md")))
    body = f"""
<header class="pagehead">
  <h1>{esc(fm['title'])}</h1>
  <p class="lede">{esc(fm['lede'])}</p>
</header>
<div class="prose prose--wide">
{md(text, base)}
</div>
"""
    return page(base, title="Cats", body=body, current="/cats/")


def build_contact(base):
    body = f"""
<header class="pagehead">
  <h1>Contact</h1>
  <p class="lede">Always happy to talk about research, games, or cats. Messages land straight in my inbox.</p>
</header>
{contact_form(base)}
"""
    return page(base, title="Contact", body=body, current="/contact/")


def build_404(base):
    body = f"""
<header class="pagehead">
  <h1>Page not found</h1>
  <p class="lede"><a href="{base}/">Back to the start</a>.</p>
</header>
"""
    return page(base, title="Not found", body=body)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=ROOT, help="output directory (default: repo root)")
    ap.add_argument("--base", default="", help="URL prefix, e.g. /new for a preview build")
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    base = args.base.rstrip("/")

    projects = load_projects()
    pubs = load_pubs()
    talks = load_talks()

    write(out, "index.html", build_home(base, projects, pubs, talks))
    write(out, "portfolio/index.html", build_projects_index(base, projects))
    for p in projects:
        write(out, f"portfolio/{p['slug']}/index.html", build_project(base, p))
    write(out, "publications/index.html", build_pubs(base, pubs))
    write(out, "cv/index.html", build_cv(base, pubs, talks))
    write(out, "cats/index.html", build_cats(base))
    write(out, "contact/index.html", build_contact(base))
    write(out, "404.html", build_404(base))
    shutil.copyfile(os.path.join(HERE, "style.css"), os.path.join(out, "style.css"))
    print(f"built into {out} with base '{base or '/'}'")


if __name__ == "__main__":
    main()
