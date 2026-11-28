# Dr. Seham Salem Clinic Website

A modern static website for Dr. Seham Salem's chest, allergy, and tuberculosis clinic in Nasr City, Cairo. The project includes Arabic and English versions, appointment booking UI, contact information, patient testimonials, service listings, and WhatsApp/phone call CTAs.

## Overview

This website is built as a lightweight static HTML/CSS/JS project with Arabic and English pages. It is designed for medical marketing and patient booking, with a responsive layout and strong conversion-focused calls to action.

## Features

- Arabic landing page and clinic content
- English translation pages under `en/`
- Services overview and specialty sections
- Medical articles page
- Patient testimonials and FAQ sections
- Contact page with clinic details and directions
- Appointment form UI for booking requests
- WhatsApp and phone direct contact buttons
- Bootstrap-based responsive design
- SEO metadata and social sharing tags

## Project Structure

```text
DrSeham-redesign/
├── build.py                    # static site generator (python build.py)
├── src/                        # layout, i18n strings, page sources
├── index.html                  # Arabic homepage (generated)
├── services.html               # Arabic services page
├── articles.html               # Arabic medical articles page
├── testimonials.html           # Arabic testimonials page
├── contact.html                # Arabic contact page
├── appointment.html            # Arabic appointment page
├── sitemap.xml                 # Search-engine sitemap
├── robots.txt                  # Crawling instructions
├── en/                         # English versions of pages
│   ├── index.html
│   ├── services.html
│   ├── articles.html
│   ├── testimonials.html
│   ├── contact.html
│   └── appointment.html
├── assets/
│   ├── css/
│   ├── fonts/
│   ├── img/
│   └── js/
├── README.md
└── .gitignore
```

## Technologies

- HTML5
- CSS3
- Bootstrap
- JavaScript

## Local Development

Because this is a static website, you can run it locally without a framework.

### Run a local server

The testimonials page loads `assets/data/reviews.json` with `fetch()`, so serve the folder over HTTP
(opening the file directly via `file://` will not load the reviews):

```bash
python -m http.server 8000   # then open http://localhost:8000
```

## Adding a patient review

Edit `assets/data/reviews.json` and add one line, the page builds the cards automatically (AR + EN):

```json
{"name": "اسم ا.", "text": "نص الرأي", "rating": 5}
```

`rating` is optional (default 5, range 1-5). The avatar letter is taken from the first letter of `name`.


## Build (templates)

The 12 HTML pages and `sitemap.xml` are **generated** from `src/` by a dependency-free Python script
(Python 3.8+). Do not edit the generated `*.html` files by hand; edit the sources and rebuild:

```bash
python build.py          # regenerate pages + sitemap.xml
python build.py --check  # CI-friendly: fails if the generated files are out of date
```

| What to change | Where |
| --- | --- |
| Header, footer, floating buttons, `<head>` | `src/layout.html` |
| Shared texts (menu, footer, labels) in AR / EN | `src/i18n.json` |
| Page content (title, description, body) | `src/pages/<page>.<ar\|en>.html` |
| Add a page to menu/sitemap | `src/pages.json` + `src/i18n.json` (`nav`) |

`sitemap.xml` `<lastmod>` is automatic: `src/lastmod.json` remembers a hash of each page and only
bumps the date for pages whose generated output changed.

## Content Editing

- Page content: `src/pages/*.html` (then run `python build.py`)
- `assets/img/` for clinic images and branding assets
- `assets/css/site.css` for custom styling
- `assets/js/` for interactive and booking behavior
- `sitemap.xml` for search-engine page URLs

## Contact / Clinic Info

The website currently uses the clinic details for:

- Phone: `+201113144573`
- WhatsApp: `https://wa.me/201113144573`
- Address: Abbas El Akkad Street, First District, Nasr City, Cairo

## Notes

- The project is static and does not require a backend for basic site display.
- The appointment form sends the request through WhatsApp. The contact form still posts to `/enquiries` (no backend in this project), so it needs a real endpoint or a WhatsApp handler.
- Arabic and English pages are generated from `src/` (see Build).
- Language: visitors are never auto-redirected; if they previously chose the other language a small dismissible suggestion bar is shown.

## Recommended Next Improvements

- Connect the form submissions to a real email, CRM, or API endpoint
- Add analytics and conversion tracking
- Expand accessibility testing and mobile QA
- Add a CMS or dynamic content source for easier maintenance

## License

This project is intended for the website of Dr. Seham Salem's clinic. Add a license only if you have the legal rights to do so.
