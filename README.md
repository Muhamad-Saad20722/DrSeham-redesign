# Dr. Seham Salem Clinic Website

A modern static website for Dr. Seham Salem's chest, allergy, and tuberculosis clinic in Nasr City, Cairo. The project includes Arabic and English versions, appointment booking UI, contact information, patient testimonials, service listings, and WhatsApp/phone call CTAs.

## Overview

This website is built as a lightweight static HTML/CSS/JS project with a generated structure for Arabic and English pages. It is designed for medical marketing and patient booking, with a polished responsive layout and strong conversion-focused calls to action.

## Features

- Arabic landing page and clinic content
- English translation pages under `en/`
- Services overview and specialty sections
- Patient testimonials and FAQ sections
- Contact page with clinic details and directions
- Appointment form UI for booking requests
- WhatsApp and phone direct contact buttons
- Bootstrap-based responsive design
- SEO metadata and social sharing tags

## Project Structure

```text
DrSeham-redesign/
├── index.html                  # Arabic homepage
├── services.html               # Arabic services page
├── testimonials.html           # Arabic testimonials page
├── contact.html                # Arabic contact page
├── appointment.html            # Arabic appointment page
├── en/                         # English versions of pages
│   ├── index.html
│   ├── services.html
│   ├── testimonials.html
│   ├── contact.html
│   └── appointment.html
├── assets/
│   ├── css/
│   ├── fonts/
│   ├── img/
│   └── js/
├── _source/
│   ├── build.py                # Generates Arabic pages from source data
│   ├── build_en.py             # Generates English pages from Arabic output
│   ├── en_dict.py              # English translation dictionary
│   └── testimonials.json       # Review data source
├── README.md
└── .gitignore (if present)
```

## Technologies

- HTML5
- CSS3
- Bootstrap
- JavaScript
- Python build scripts for page generation

## Local Development

Because this is a static website, you can run it locally without a framework.

### Option 1: Open directly

Open any of the HTML files directly in a browser, for example:

- `index.html`
- `services.html`
- `contact.html`

### Option 2: Run a local server

From the project root, run:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

## Regenerating Pages

The project includes Python generators that produce the site content and translation pages.

### Arabic site source

```bash
python _source/build.py
```

### English site translation

```bash
python _source/build_en.py
```

These scripts read content data from `_source/` and generate the HTML pages in the main project directory and the `en/` folder.

## Content Editing

Common content updates can be made in:

- `_source/build.py` for text, services, FAQs, metadata, and site content
- `_source/testimonials.json` for patient reviews
- `assets/img/` for clinic images and branding assets
- `assets/css/site.css` for custom styling

## Contact / Clinic Info

The website currently uses the clinic details for:

- Phone: `01113144573`
- WhatsApp: `https://wa.me/201113144573`
- Address: Abbas El Akkad Street, First District, Nasr City, Cairo

## Notes

- The project is static and does not require a backend for basic site display.
- The appointment and contact forms are front-end UI placeholders and may need integration with a backend or third-party service.
- The generated site is already committed as HTML, so changes to source scripts should be followed by regeneration if you want the output updated.

## Recommended Next Improvements

- Connect the form submissions to a real email, CRM, or API endpoint
- Add analytics and conversion tracking
- Expand accessibility testing and mobile QA
- Add a CMS or dynamic content source for easier maintenance

## License

This project is intended for the website of Dr. Seham Salem's clinic. Add a license only if you have the legal rights to do so.
