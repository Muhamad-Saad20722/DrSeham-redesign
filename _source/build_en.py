"""Generate the English (LTR) site in site/en/ from the Arabic pages in site/, using en_dict.EN.
Fails loudly if any Arabic text is left untranslated (patient reviews, which stay in Arabic on purpose, are exempt)."""
import glob, html, os, re, sys
from en_dict import EN

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
OUT = os.path.join(ROOT, 'en')
os.makedirs(OUT, exist_ok=True)
AR_RE = re.compile(r'[؀-ۿ]')
EXACT = {k: v for k, v in EN.items() if not k.endswith('…')}
PREFIX = sorted(((k[:-1], v) for k, v in EN.items() if k.endswith('…')), key=lambda kv: -len(kv[0]))
missing = []


def tr(text):
    """Translate a (stripped, unescaped) string or return None."""
    if text in EXACT:
        return EXACT[text]
    for p, v in PREFIX:
        if text.startswith(p):
            return v
    return None


def sub_text(m, page):
    tag, raw = m.group(1), m.group(2)
    if 'lang="ar"' in tag:
        return m.group(0)
    txt = html.unescape(raw)
    if not AR_RE.search(txt):
        return m.group(0)
    core = txt.strip()
    if len(core) <= 1:
        return m.group(0)
    new = tr(core)
    if new is None:
        missing.append((page, core))
        return m.group(0)
    lead = txt[:len(txt) - len(txt.lstrip())]
    trail = txt[len(txt.rstrip()):]
    return tag + lead + html.escape(new, quote=False) + trail


def sub_attr(m, page):
    name, raw = m.group(1), m.group(2)
    txt = html.unescape(raw)
    if not AR_RE.search(txt):
        return m.group(0)
    new = tr(txt.strip())
    if new is None:
        missing.append((page, txt))
        return m.group(0)
    return f'{name}="{html.escape(new, quote=True)}"'


for path in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    page = os.path.basename(path)
    s = open(path, encoding='utf8').read()

    # drop the AR->EN auto-redirect script, switch document language/direction
    s = re.sub(r'<script id="lang-redirect">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('<html lang="ar" dir="rtl">', '<html lang="en" dir="ltr">')

    # JSON-LD (home page only)
    def jsonld(m):
        b = m.group(0)
        for a, e in [('شارع عباس العقاد، المنطقة الأولى، مدينة نصر', 'Abbas El Akkad St., First District, Nasr City'),
                     ('استشارية أمراض الصدر والحساسية والدرن (السل)', 'Consultant in chest diseases, allergy and tuberculosis (TB)'),
                     ('مدينة نصر', 'Nasr City'), ('د. سهام سالم', 'Dr. Seham Salem')]:
            b = b.replace(a, e)
        return b
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', jsonld, s, flags=re.S)

    # translate attributes first, then text nodes, never touching <script>/<style>
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', s, flags=re.S)
    for i in range(0, len(parts), 2):
        seg = parts[i]
        seg = re.sub(r'\b(alt|aria-label|placeholder|title|content)="([^"]*)"', lambda m: sub_attr(m, page), seg)
        seg = re.sub(r'(<[^<>]+>)([^<>]+)(?=<)', lambda m: sub_text(m, page), seg)
        parts[i] = seg
    s = ''.join(parts)

    # language switcher + alternates (done after translation so the Arabic label is kept)
    s = s.replace(f'<a class="lang-switch order-lg-3" href="en/{page}" hreflang="en" lang="en" data-lang-switch="en" aria-label="Switch to English"><i class="bi bi-translate"></i><span>EN</span></a>',
                  f'<a class="lang-switch order-lg-3" href="../{page}" hreflang="ar" lang="ar" data-lang-switch="ar" aria-label="التبديل إلى العربية"><i class="bi bi-translate"></i><span>عربي</span></a>')
    s = s.replace(f'<link rel="alternate" hreflang="ar" href="{page}">', f'<link rel="alternate" hreflang="ar" href="../{page}">')
    s = s.replace(f'<link rel="alternate" hreflang="en" href="en/{page}">', f'<link rel="alternate" hreflang="en" href="{page}">')

    # assets live one level up; LTR Bootstrap build
    s = re.sub(r'(href|src|content)="assets/', r'\1="../assets/', s)
    s = s.replace('bootstrap.rtl.min.css', 'bootstrap.min.css')

    # direction-sensitive bits
    s = s.replace('bi-arrow-left', 'bi-arrow-right')
    s = s.replace('bi-chevron-right', '@@CHEV').replace('bi-chevron-left', 'bi-chevron-right').replace('@@CHEV', 'bi-chevron-left')
    s = s.replace(' style="direction:rtl;font-size:1rem"', ' style="font-size:1rem"').replace(' style="direction:rtl"', '')
    s = s.replace('text-md-start', 'text-md-end')

    open(os.path.join(OUT, page), 'w', encoding='utf8').write(s)

if missing:
    print('UNTRANSLATED:')
    for p, t in missing:
        print(' ', p, '|', t[:90])
    sys.exit(1)
print('English site built:', len(glob.glob(os.path.join(OUT, '*.html'))), 'pages')
