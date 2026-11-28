#!/usr/bin/env python3
"""Static site builder (standard library only).

    python build.py            # regenerate all pages + sitemap.xml
    python build.py --check    # exit 1 if generated files differ from what is on disk

Sources live in src/:
  layout.html   shared page shell (head, header, footer, floating buttons)
  i18n.json     shared strings (nav, footer, ...) per language
  pages.json    page list + sitemap settings
  pages/<name>.<lang>.html   per-page content (see the header comment in each file)
  lastmod.json  generated: sitemap <lastmod> dates (updated only when a page's output changes)

Output (committed, served as plain static files): <name>.html and en/<name>.html, sitemap.xml
"""
import datetime
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE_URL = "https://drsehamsalem.com"
LANGS = ("ar", "en")


def load_json(p):
    return json.loads(p.read_text(encoding="utf-8"))


def parse_page(text):
    """Return (front_matter dict, head_extra str, main html str)."""
    m = re.match(r"\s*<!--\n(.*?)\n-->\n", text, re.S)
    if not m:
        raise ValueError("page is missing its front-matter comment")
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    rest = text[m.end():]
    head = ""
    h = re.search(r"<!-- head -->\n(.*?)\n<!-- /head -->\n", rest, re.S)
    if h:
        head = h.group(1)
        rest = rest[: h.start()] + rest[h.end():]
    return meta, head, rest.strip()


def page_url(lang, name):
    base = SITE_URL + ("/en/" if lang == "en" else "/")
    return base if name == "index" else f"{base}{name}.html"


def render(layout, i18n, pages, lang, name):
    t = i18n[lang]
    meta, head_extra, main = parse_page((SRC / "pages" / f"{name}.{lang}.html").read_text(encoding="utf-8"))
    root = t["root"]
    main = main.replace("{{root}}", root)

    def link(page, label, active=False):
        a = f'<a class="nav-link{" active" if active else ""}" href="{page}.html"'
        return a + (' aria-current="page"' if active else "") + f">{label}</a>"

    nav_items = "\n".join(
        f'              <li class="nav-item">{link(p, t["nav"][p], p == name)}</li>' for p in t["nav"]
    )
    footer_links = "\n".join(
        f'              <li><a href="{p}.html">{t["nav"][p]}</a></li>' for p in t["nav"]
    ) + f'\n              <li><a href="appointment.html">{t["footer_book"]}</a></li>'

    file_name = f"{name}.html"
    ar_href = file_name if lang == "ar" else f"../{file_name}"
    en_href = f"en/{file_name}" if lang == "ar" else file_name
    toggle = []
    for code, label, href in (("ar", "عربي", ar_href), ("en", "EN", en_href)):
        cur = ' class="active" aria-current="true"' if code == lang else ""
        toggle.append(
            f'            <a href="{href}"{cur} lang="{code}" hreflang="{code}" data-lang-switch="{code}">{label}</a>'
        )

    scripts = "".join(
        f'    <script src="{root}assets/js/{s.strip()}"></script>\n'
        for s in meta.get("scripts", "").split(",")
        if s.strip()
    )
    ctx = dict(
        lang=lang,
        dir=t["dir"],
        root=root,
        title=html.escape(meta["title"], quote=False),
        title_attr=html.escape(meta["title"]),
        description_attr=html.escape(meta["description"]),
        canonical=page_url(lang, name),
        url_ar=page_url("ar", name),
        url_en=page_url("en", name),
        site_url=SITE_URL,
        head_extra=(head_extra + "\n") if head_extra else "",
        lang_toggle="\n".join(toggle),
        nav_items=nav_items,
        footer_links=footer_links,
        main=main,
        scripts=scripts,
    )
    for k, v in t.items():
        if isinstance(v, str):
            ctx.setdefault(k, v)
    for k, v in t["social"].items():
        ctx[f"social_{k}"] = v

    out = layout
    # head_extra / scripts / main may contain "{{" themselves, so fill them last.
    late = {k: ctx.pop(k) for k in ("head_extra", "scripts", "main")}
    out = re.sub(r"{{(\w+)}}", lambda m: str(ctx[m.group(1)]) if m.group(1) in ctx else m.group(0), out)
    for k, v in late.items():
        out = out.replace("{{" + k + "}}", v)
    left = re.findall(r"{{\w+}}", out)
    if left:
        raise ValueError(f"{lang}/{name}: unresolved placeholders {set(left)}")
    return out


def build_sitemap(pages, outputs, lastmod_path, today):
    prev = load_json(lastmod_path) if lastmod_path.exists() else {}
    new = {}
    for p in pages:
        n = p["name"]
        digest = hashlib.sha256("".join(outputs[(lang, n)] for lang in LANGS).encode()).hexdigest()
        old = prev.get(n, {})
        new[n] = {"hash": digest, "lastmod": old["lastmod"] if old.get("hash") == digest else today}
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for lang in LANGS:
        for p in pages:
            n = p["name"]
            lines += [
                "  <url>",
                f"    <loc>{page_url(lang, n)}</loc>",
                f"    <lastmod>{new[n]['lastmod']}</lastmod>",
                f"    <changefreq>{p['changefreq']}</changefreq>",
                f"    <priority>{p['priority']}</priority>",
            ]
            for hl, u in (("ar", page_url("ar", n)), ("en", page_url("en", n)), ("x-default", page_url("ar", n))):
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{hl}" href="{u}"/>')
            lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n", new


def main():
    check = "--check" in sys.argv
    today = datetime.date.today().isoformat()
    if "--date" in sys.argv:
        today = sys.argv[sys.argv.index("--date") + 1]
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    i18n = load_json(SRC / "i18n.json")
    pages = load_json(SRC / "pages.json")

    outputs = {}
    files = {}
    for lang in LANGS:
        for p in pages:
            n = p["name"]
            outputs[(lang, n)] = render(layout, i18n, pages, lang, n)
            files[ROOT / ("en" if lang == "en" else "") / f"{n}.html"] = outputs[(lang, n)]

    lastmod_path = SRC / "lastmod.json"
    sitemap, lastmod = build_sitemap(pages, outputs, lastmod_path, today)
    files[ROOT / "sitemap.xml"] = sitemap
    files[lastmod_path] = json.dumps(lastmod, indent=2) + "\n"

    changed = [p for p, c in files.items() if not p.exists() or p.read_text(encoding="utf-8") != c]
    if check:
        for p in changed:
            print("out of date:", p.relative_to(ROOT))
        sys.exit(1 if changed else 0)
    for p, c in files.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        if p in changed:
            p.write_text(c, encoding="utf-8")
    print(f"built {len(outputs)} pages; {len(changed)} files changed")


if __name__ == "__main__":
    main()
