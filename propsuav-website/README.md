# PropsUAV Website

**Professional static website for PropsUAV — Precision drone crop spraying for Central Texas agriculture.**

## Quick Start

This is a fully self-contained, production-ready static website with no dependencies.

### Files & Structure

```
propsuav-website/
├── index.html           — Landing page (hero, features, services preview)
├── services.html        — Service offerings & equipment details
├── about.html           — Team credentials & certifications
├── contact.html         — Contact form, FAQ, service area
├── css/
│   └── style.css        — Responsive stylesheet (12 KB)
├── js/
│   └── main.js          — Mobile menu, form validation (3.1 KB)
├── images/
│   └── PropsUAV-Logo.png — Brand logo (provided)
└── README.md            — This file
```

## Deployment

**Option 1: GitHub Pages (Recommended)**
1. Create a GitHub repo: `propsuav.com`
2. Upload all files
3. Enable GitHub Pages in repo settings
4. Point domain to GitHub Pages nameservers

**Option 2: Netlify**
1. Drag & drop folder into Netlify
2. Connect domain
3. Done

**Option 3: Traditional Web Host**
1. Upload all files (preserving folder structure)
2. Set `index.html` as default document
3. Ensure HTTPS is enabled

## Features

✅ **Responsive** — Mobile-first design, works on all devices
✅ **Fast** — Lightweight CSS/JS, no frameworks
✅ **SEO Ready** — Meta tags, Open Graph, semantic HTML
✅ **Contact Forms** — Integrated with Formspree (same account as AvestAI)
✅ **Professional** — Modern typography, polished UI
✅ **No Dependencies** — Pure HTML/CSS/JavaScript (Google Fonts only)

## Customization

### Change Text
Edit the HTML files directly. Search for the content you want to change.

### Change Colors
Edit `css/style.css` lines 3-11 (CSS variables):
```css
:root {
  --dark-navy: #1a2744;
  --green: #3d8b37;
  --orange: #f57c00;
  /* ... etc */
}
```

### Change Logo
Replace `images/PropsUAV-Logo.png` with your logo (keep the same filename and size).

### Change Contact Details
Update in:
- Navigation header (all HTML files)
- Footer (all HTML files)
- Contact page content

### Add New Pages
1. Copy an existing `.html` file
2. Update header/footer nav
3. Replace content
4. Link from navigation menu

## Form Handling (Contact Form)

The contact form uses **Formspree** (no backend server needed).

**Current Endpoint:** `https://formspree.io/f/xpwzgeyq`

To change where form submissions go:
1. Log in to Formspree (https://formspree.io)
2. Find the `xpwzgeyq` form
3. Update email address or redirect URL

## Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- HTML: 7.3 KB + 12 KB + 13 KB + 15 KB = 47 KB
- CSS: 12 KB
- JavaScript: 3.1 KB
- **Total (excl. logo): 62 KB**
- Logo: 526 KB

Page load time: < 1 second on typical connection.

## SEO

- Meta descriptions included
- Open Graph tags for social sharing
- Proper heading hierarchy (h1 → h2 → h3)
- Semantic HTML5
- Mobile-friendly (responsive)
- Fast load times

## SSL/HTTPS

Always use HTTPS in production. Most hosting providers offer free SSL certificates (Let's Encrypt).

## Analytics

To add Google Analytics:
1. Get your tracking ID from Google Analytics
2. Add this to the `<head>` of each HTML file:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_ID');
</script>
```

## Support

For questions about the build:
- Check `BUILD_SUMMARY.txt` for detailed specs
- Review inline comments in CSS and JavaScript
- HTML is self-documenting

## License

This website is proprietary to PropsUAV / Avest Ltd. All rights reserved.

---

**Built:** May 11, 2026  
**Status:** Production Ready ✓
