"""Build the static site.

    python _src/build.py                 # writes to the repo root (live site)
    python _src/build.py --out new --base /new   # preview build under /new/

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
    ("Say hi", "/contact/"),
]


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
    desc = esc(description or "Yunjia (Sherry) Guo: game developer and AI researcher building games where the characters think for themselves.")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/images/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Caveat:wght@500&display=swap">
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
  <span>No template, no tracking, no cookies.</span>
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


def authors_html(names):
    out = []
    for n in names:
        out.append(f"<b>{esc(n)}</b>" if n == "Yunjia Guo" else esc(n))
    return ", ".join(out)


def paper_html(p, base, with_summary):
    title = esc(p["title"])
    if p.get("url"):
        title = f'<a href="{esc(p["url"])}">{title}</a>'
    venue = esc(p["venue"])
    status = esc(p["status"])
    summary = f'<p class="paper__summary">{esc(p["summary"].strip())}</p>' if with_summary else ""
    return f"""<li class="paper" id="{esc(p['id'])}">
  <h3 class="paper__title">{title}</h3>
  <p class="paper__authors">{authors_html(p['authors'])}</p>
  <p class="paper__venue">{venue}. {status.capitalize()}, {p['year']}.</p>
  {summary}
</li>"""


def papers_list(pubs, base, with_summary=False):
    return '<ul class="papers">' + "".join(paper_html(p, base, with_summary) for p in pubs) + "</ul>"


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
    return f"""<div id="sent" class="sent" hidden>Thanks, your message is on its way.</div>
<form id="contact" class="form" action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
  <input type="hidden" name="subject" value="New message from sherryguo8023.github.io">
  <input type="hidden" name="from_name" value="Personal website">
  <input type="hidden" name="redirect" value="{redirect}">
  <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off" style="display:none">
  <label for="c-name">Your name</label>
  <input id="c-name" type="text" name="name" required>
  <label for="c-email">Email, if you'd like a reply</label>
  <input id="c-email" type="email" name="email">
  <label for="c-msg">Message</label>
  <textarea id="c-msg" name="message" required></textarea>
  <button type="submit">Send message</button>
</form>
<script>
if (new URLSearchParams(location.search).get('sent') === '1') {{
  document.getElementById('sent').hidden = false;
  document.getElementById('contact').hidden = true;
}}
</script>"""


# ---------------------------------------------------------------- pages

def build_home(base, projects, pubs):
    bside = projects[0]
    rest = projects[1:]
    stores = "".join(
        f'<li><a href="{esc(u)}">{esc(l)}<span>{esc(note)}</span></a></li>'
        for l, u, note in [
            ("Steam", "https://store.steampowered.com/app/3649950/Bside/", "PC"),
            ("App Store", "https://apps.apple.com/us/app/bside/id6757434275", "iOS"),
            ("Google Play", "https://play.google.com/store/apps/details?id=com.kotoko.bside", "Android"),
            ("bside.zone", "https://www.bside.zone/", "official site"),
        ]
    )
    body = f"""
<section class="hero">
  <div>
    <h1 class="hero__title">I make games where the characters have minds of their own.</h1>
    <p class="hero__lede">Yunjia Guo, Sherry to most people. Game developer and AI researcher, technical lead at <a href="https://www.kotoko.ai/">Kotoko AI</a>, physicist by training, cat person by conviction.</p>
    <ul class="hero__links">
      <li><a href="{base}/portfolio/">What I've built</a></li>
      <li><a href="{base}/publications/">What I've written</a></li>
      <li><a href="https://www.linkedin.com/in/yunjiaguo/">LinkedIn</a></li>
    </ul>
  </div>
  <figure class="snap">
    <img src="/images/me.jpg" alt="Yunjia Guo sitting on a bench by a river on an overcast, windy day" width="1536" height="1152">
    <figcaption>me, on a windy day</figcaption>
  </figure>
</section>

<section class="section" id="now">
  <div class="section__head">
    <h2>Right now: Bside</h2>
    <p>A social simulation game on Steam, iOS and Android where every character is driven by a language model. I have led its engineering from the first prototype through international launch, across three generations of client, server and character systems.</p>
  </div>
  <a href="{base}/portfolio/1bside/"><img class="feature__img" src="/images/bside-keyart.jpg" alt="Bside key art" width="1600" height="900"></a>
  <div class="feature__body">
    <div>
      <h3 class="feature__title"><a href="{base}/portfolio/1bside/">{esc(bside['title'])}</a></h3>
      <p>{esc(bside['tagline'])} Players create characters with their own looks, backstory and personality, then watch them live, talk and act in a shared world, on PC and on their phones. The hard part, and the part I care about, is keeping open-ended model behaviour controllable, executable and meaningful inside a live multiplayer game.</p>
      <p><a href="{base}/portfolio/1bside/">More about Bside</a></p>
    </div>
    <ul class="feature__stores">{stores}</ul>
  </div>
</section>

<section class="section" id="projects">
  <div class="section__head">
    <h2>Earlier work</h2>
    <p>From AI companions back to procedural cities, crowd simulation and a physics thesis that used BERT on chemical formulas.</p>
  </div>
  <ul class="rows">{''.join(project_row(p, base) for p in rest)}</ul>
</section>

<section class="section" id="papers">
  <div class="section__head">
    <h2>Papers</h2>
    <p>What we learned building Bside, written down for the HCI and game AI communities.</p>
  </div>
  {papers_list(pubs, base)}
  <p style="margin-top:1.2rem"><a href="{base}/publications/">Abstracts and details</a></p>
</section>

<section class="section" id="road">
  <div class="section__head">
    <h2>The road here</h2>
    <p>Physics first, then games, then the two together.</p>
  </div>
  <ul class="road">
    <li><time>2023 – now</time><p><b>Kotoko AI</b>, CTO and hands-on technical lead. Bside, Dobit, and the LLM character systems underneath them.</p></li>
    <li><time>2022 – 2023</time><p><b>Tencent Games, TiMi Studios.</b> Core character, control, camera and ability framework systems in Unreal Engine 4 for an AAA open-world action game, plus Unity work.</p></li>
    <li><time>2020 – 2021</time><p><b>NetEase Games.</b> Procedural urban generation in Houdini, then stylised rendering for an online multiplayer demo.</p></li>
    <li><time>2019 – 2021</time><p><b>Utrecht University</b>, MSc Game and Media Technology. Procedural content generation and crowd simulation.</p></li>
    <li><time>2015 – 2019</time><p><b>University of Chinese Academy of Sciences</b>, BSc Physics, minor in mathematics. Superconductors and ARPES at the Institute of Physics, a summer at the Max Planck Institute for Solid State Research, and a thesis on machine learning for topological materials.</p></li>
  </ul>
  <p style="margin-top:1.2rem"><a href="{base}/cv/">Full CV</a>. Finalist for the Innovator Award at the Women in Tech Awards 2026.</p>
</section>

<section class="section" id="off">
  <div class="section__head">
    <h2>Off the clock</h2>
  </div>
  <div class="aside2">
    <div class="prose">
      <p>I play a lot. RTS, shooters, puzzle games, roguelikes, idle games. StarCraft II is the one I keep coming back to; I main Zerg and will defend Sarah Kerrigan to anyone. Overwatch's sound design is the reason I went into games in the first place, and AlphaStar beating humans at my favourite game is the reason I believe games are where AI gets tested for real.</p>
      <p>On Steam and itch.io I look for new releases and play them properly. A few favourites among many: Balatro, Stacklands, A Dance of Fire and Ice, Chillquarium, the Rusty Lake series, There Is No Game, Melvor Idle, BattleBlock Theater, Risk of Rain.</p>
    </div>
    <div>
      <div class="catpile">
        <img src="/images/cats/guagua.jpg" alt="Guagua" width="104" height="104">
        <img src="/images/cats/lily.jpg" alt="Lily" width="104" height="104">
        <img src="/images/cats/spot.jpg" alt="Spot" width="104" height="104">
        <span class="catpile__note">Guagua, Lily, Spot</span>
      </div>
      <p>We rescue street cats, get them neutered, and find them homes. Three of them decided they were already home. <a href="{base}/cats/">The cats</a>.</p>
    </div>
  </div>
</section>

<section class="section" id="hi">
  <div class="section__head">
    <h2>Say hi</h2>
    <p>Games, AI characters, research, cats. Messages land in my inbox.</p>
  </div>
  {contact_form(base)}
</section>
"""
    return page(base, title=None, body=body, current="/")


def build_projects_index(base, projects):
    body = f"""
<header class="pagehead">
  <h1>Projects</h1>
  <p class="lede">Seven things, in the order I would show them to you.</p>
</header>
<ul class="rows">{''.join(project_row(p, base) for p in projects)}</ul>
"""
    return page(base, title="Projects", body=body, current="/portfolio/")


def build_project(base, p):
    links = "".join(f'<li><a href="{esc(u)}">{esc(l)}</a></li>' for l, u in (p.get("links") or []))
    meta = f'<li>{esc(p["years"])}</li><li>{esc(p["role"])}</li>{links}'
    body = f"""
<header class="pagehead">
  <h1>{esc(p['title'])}</h1>
  <p class="lede">{esc(p['tagline'])}</p>
  <ul class="meta">{meta}</ul>
</header>
<img class="hero-img" src="/images/{p['hero']}" alt="">
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
  <p class="lede">Research from building Bside, at the meeting point of games and HCI.</p>
</header>
{papers_list(pubs, base, with_summary=True)}
"""
    return page(base, title="Papers", body=body, current="/publications/")


def build_cv(base, pubs):
    fm, text = front_matter(read(os.path.join(CONTENT, "cv.md")))
    html_body = md(text, base).replace("<!-- PUBLICATIONS -->", papers_list(pubs, base))
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
  <h1>Say hi</h1>
  <p class="lede">Games, AI characters, research, cats. Messages land in my inbox.</p>
</header>
{contact_form(base)}
"""
    return page(base, title="Say hi", body=body, current="/contact/")


def build_404(base):
    body = f"""
<header class="pagehead">
  <h1>Nothing here.</h1>
  <p class="lede">The page moved or never existed. <a href="{base}/">Back to the start</a>.</p>
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
