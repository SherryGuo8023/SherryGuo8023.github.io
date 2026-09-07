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

DESCRIPTION = "Yunjia Guo: game developer and AI researcher. Technical lead at Kotoko AI."


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

def build_home(base, projects, pubs):
    pc = next(p for p in projects if p["slug"] == "1bside")
    mobile = next(p for p in projects if p["slug"] == "bside-mobile")
    rest = [p for p in projects if p["slug"] not in ("1bside", "bside-mobile")]

    def duo(p, img, links, text):
        ls = "".join(f'<li><a href="{esc(u)}">{esc(l)}</a></li>' for l, u in links)
        return f"""<div class="duo__item">
  <a href="{base}/portfolio/{p['slug']}/"><img class="duo__img" src="/images/{img}" alt=""></a>
  <h3 class="duo__title"><a href="{base}/portfolio/{p['slug']}/">{esc(p['title'])}</a></h3>
  <p class="duo__when">{esc(p['years'])}</p>
  <p>{text}</p>
  <ul class="duo__links">{ls}</ul>
</div>"""

    body = f"""
<section class="hero">
  <div>
    <h1 class="hero__title">Game developer and AI researcher.</h1>
    <p class="hero__lede">I lead engineering at <a href="https://www.kotoko.ai/">Kotoko AI</a>, where we make games built around AI characters: Bside for PC on Steam, and Bside Mobile on iOS and Android. Before that I worked on combat systems at Tencent and procedural cities at NetEase, and studied physics.</p>
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
    <p>Two games under one name, built for different platforms. Characters and the character creator are shared; the games are not.</p>
  </div>
  <div class="duo">
    {duo(pc, 'bside-keyart.jpg', [("Steam", "https://store.steampowered.com/app/3649950/Bside/")],
         "A multiplayer social world with no NPCs. Every character belongs to a player and is run by a multi-agent LLM runtime; players steer with a whisper rather than a joystick. Steam Early Access since October 2025.")}
    {duo(mobile, 'bside-mobile-home.jpg', [("App Store", "https://apps.apple.com/us/app/bside/id6757434275"), ("Google Play", "https://play.google.com/store/apps/details?id=com.kotoko.bside")],
         "Create a character, then raise it. It posts about its day, goes on adventures on its own, appears in your own videos, and talks when you want it to. On iOS and Android since March 2026.")}
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
    <p>Research on LLM-driven characters in games.</p>
  </div>
  {papers_list(pubs)}
  <p style="margin-top:1.2rem"><a href="{base}/publications/">Abstracts</a></p>
</section>

<section class="section" id="background">
  <div class="section__head">
    <h2>Background</h2>
  </div>
  <ul class="road">
    <li><time>2023 – now</time><p><b>Kotoko AI.</b> Technical lead for Dobit, Bside for PC and Bside Mobile, and the LLM character systems underneath them.</p></li>
    <li><time>2022 – 2023</time><p><b>Tencent Games, TiMi Studios.</b> Character, control, camera and ability framework systems in Unreal Engine 4 for an AAA open-world action game; Unity work on other titles.</p></li>
    <li><time>2020 – 2021</time><p><b>NetEase Games.</b> Procedural urban generation in Houdini; stylised rendering for an online multiplayer demo.</p></li>
    <li><time>2019 – 2021</time><p><b>Utrecht University</b>, MSc Game and Media Technology. Procedural content generation and crowd simulation.</p></li>
    <li><time>2015 – 2019</time><p><b>University of Chinese Academy of Sciences</b>, BSc Physics, minor in mathematics. Superconductor research at the Institute of Physics, a summer at the Max Planck Institute for Solid State Research, and a thesis on machine learning for topological materials.</p></li>
  </ul>
  <p style="margin-top:1.2rem"><a href="{base}/cv/">Full CV</a>. Finalist, Innovator Award, Women in Tech Awards 2026.</p>
</section>

<section class="section" id="outside">
  <div class="section__head">
    <h2>Outside work</h2>
  </div>
  <div class="aside2">
    <div class="prose">
      <p>I play a lot: RTS, shooters, puzzle games, roguelikes, idle games. StarCraft II most of all, as Zerg. Overwatch's sound design is what got me into game development. I keep an eye on new releases on Steam and itch.io; recent favourites include Balatro, Stacklands, A Dance of Fire and Ice, Chillquarium, the Rusty Lake series, There Is No Game, Melvor Idle, BattleBlock Theater and Risk of Rain.</p>
    </div>
    <div>
      <div class="catpile">
        <img src="/images/cats/guagua.jpg" alt="Guagua" width="104" height="104">
        <img src="/images/cats/lily.jpg" alt="Lily" width="104" height="104">
        <img src="/images/cats/spot.jpg" alt="Spot" width="104" height="104">
      </div>
      <p>We rescue street cats, get them neutered and find them homes. Guagua, Lily and Spot stayed. <a href="{base}/cats/">More about the cats</a>.</p>
    </div>
  </div>
</section>

<section class="section" id="contact">
  <div class="section__head">
    <h2>Contact</h2>
    <p>Messages go straight to my inbox. Email is optional.</p>
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
  <p class="lede">Research on LLM-driven characters in games.</p>
</header>
{papers_list(pubs, with_summary=True)}
"""
    return page(base, title="Papers", body=body, current="/publications/")


def build_cv(base, pubs):
    fm, text = front_matter(read(os.path.join(CONTENT, "cv.md")))
    html_body = md(text, base).replace("<!-- PUBLICATIONS -->", papers_list(pubs))
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
  <p class="lede">Messages go straight to my inbox. Email is optional.</p>
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

    write(out, "index.html", build_home(base, projects, pubs))
    write(out, "portfolio/index.html", build_projects_index(base, projects))
    for p in projects:
        write(out, f"portfolio/{p['slug']}/index.html", build_project(base, p))
    write(out, "publications/index.html", build_pubs(base, pubs))
    write(out, "cv/index.html", build_cv(base, pubs))
    write(out, "cats/index.html", build_cats(base))
    write(out, "contact/index.html", build_contact(base))
    write(out, "404.html", build_404(base))
    shutil.copyfile(os.path.join(HERE, "style.css"), os.path.join(out, "style.css"))
    print(f"built into {out} with base '{base or '/'}'")


if __name__ == "__main__":
    main()
