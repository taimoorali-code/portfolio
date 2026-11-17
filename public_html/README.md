# Taimoor Ali — Shopify Operations & Automation (static site)

Pure HTML, CSS, and vanilla JavaScript. No framework and no build step required to run. The generated HTML files are ready for static hosting.

## Structure
```
index.html
services/index.html
services/<slug>/index.html
results/index.html
results/<slug>/index.html
about/index.html
book/index.html
assets/styles.css
assets/main.js
assets/images/avatar.png
sitemap.xml
robots.txt
build.py
```

## Production domain
The generated canonicals, schema URLs, robots.txt, and sitemap.xml are set to:

```
https://taimoorproject.site
```

## Preview locally
Run from this folder:

```bash
python3 -m http.server 8000
```

Open:

```
http://localhost:8000
```

## Deploy on Hostinger
Upload the contents of this folder into `public_html` so `index.html`, `assets`, `services`, `results`, `about`, `book`, `sitemap.xml`, and `robots.txt` are directly inside `public_html`.

## Booking form
The Book a Call form currently uses a lightweight mail fallback to `bookings@taimoorproject.site`. Before launch, create that inbox in Hostinger or change `data-mailto` in `book/index.html` to your preferred email. Later, you can replace it with Calendly/SavvyCal or a Formspree/Netlify endpoint.

## Notes
- The site uses a premium black/white/grey palette.
- The avatar is included locally at `assets/images/avatar.png`.
- No visible draft/testimonial filler or unverified metric notes remain in generated pages.
- Positioning stays focused on Shopify operations, integrations, inventory sync, ERP, subscription operations, fulfillment automation, and business outcomes.
