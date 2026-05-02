# AvestAI Website - Deployment Package

**Website:** https://avestltd.com  
**Status:** Ready for deployment to GitHub Pages  
**Last Updated:** February 20, 2026

---

## What Is This?

This is the complete, production-ready website for **AvestAI**, a professional AI-powered service business. The website showcases AvestAI's services, pricing, and includes a Calendly integration for scheduling discovery calls.

This package is configured and ready to deploy to **GitHub Pages** with your custom domain **avestltd.com**.

---

## Quick Start: Deploy in 3 Steps

1. **Read DEPLOYMENT-GUIDE.md** - Complete step-by-step instructions
2. **Configure DNS** using DNS-CONFIGURATION.md
3. **Upload files to GitHub** and enable GitHub Pages

**Time required:** 1 hour + waiting for DNS (2-24 hours)

---

## What's Included

### 📄 Website Pages (7 HTML files)

| File | Purpose | Key Features |
|------|---------|--------------|
| **index.html** | Homepage | Hero section, overview, CTA buttons |
| **about.html** | About Us | Company story, mission, team |
| **services.html** | Services | Service offerings, benefits |
| **how-it-works.html** | Process | Step-by-step workflow |
| **pricing.html** | Pricing Plans | Basic/Standard/Premium tiers with pricing |
| **documentation.html** | Docs & FAQs | Technical documentation, FAQs |
| **contact.html** | Contact Form | Calendly integration for bookings |

### 🎨 Assets

- **CSS:** `assets/css/`
  - `reset.css` - Browser normalization
  - `style.css` - Main stylesheet (modern, responsive design)
  
- **Images:** `assets/images/`
  - Logo files (multiple sizes: 64px, 128px, 256px, 512px)
  - Transparent logo variants
  - Favicons (16px, 32px)

### 📋 Deployment Files

| File | Purpose |
|------|---------|
| **CNAME** | Tells GitHub Pages to use avestltd.com domain |
| **DEPLOYMENT-GUIDE.md** | Complete deployment walkthrough |
| **DNS-CONFIGURATION.md** | Exact DNS records for IONOS |
| **FILE-INVENTORY.md** | Complete file checklist |

---

## File Structure

```
website/
├── index.html              # Homepage
├── about.html              # About page
├── services.html           # Services page
├── how-it-works.html       # How It Works page
├── pricing.html            # Pricing page
├── documentation.html      # Documentation & FAQs
├── contact.html            # Contact page with Calendly
├── CNAME                   # Domain configuration
├── README-DEPLOYMENT.md    # This file
├── DEPLOYMENT-GUIDE.md     # Step-by-step deployment
├── DNS-CONFIGURATION.md    # DNS setup instructions
├── FILE-INVENTORY.md       # File checklist
└── assets/
    ├── css/
    │   ├── reset.css       # CSS reset
    │   └── style.css       # Main styles
    └── images/
        ├── favicon-16.png
        ├── favicon-32.png
        ├── logo-64.png
        ├── logo-128.png
        ├── logo-256.png
        ├── logo-512.png
        ├── logo-transparent-128.png
        ├── logo-transparent-256.png
        └── logo-transparent-512.png
```

---

## Key Features

### 🎯 Professional Design
- Clean, modern, responsive layout
- Mobile-friendly (works on phones, tablets, desktops)
- Professional color scheme (blue/white/gray)
- Consistent branding across all pages

### 📱 Responsive & Accessible
- Works on all screen sizes
- Fast loading times
- No external dependencies (except Calendly widget)
- SEO-friendly HTML structure

### 🔗 Calendly Integration
- Embedded scheduling on contact page
- Links to: https://calendly.com/samantha128aire/avestai-discovery-call
- Professional intake flow

### 🌐 SEO Ready
- Proper heading hierarchy
- Meta descriptions on all pages
- Semantic HTML
- Fast load times

---

## How to Make Updates

### Updating Content

1. **Edit the HTML file** you want to change
2. Open it in a text editor (VS Code, TextEdit, etc.)
3. Find the section you want to update
4. Make your changes
5. Save the file
6. **Upload to GitHub** (see Deployment Workflow below)

### Updating Styles

1. Edit `assets/css/style.css`
2. CSS uses custom properties (variables) for easy theming:
   ```css
   --primary-blue: #2E86AB
   --secondary-blue: #5AB9EA
   --dark-gray: #2C3E50
   ```
3. Change colors, fonts, spacing as needed
4. Save and upload to GitHub

### Adding Images

1. Add image files to `assets/images/`
2. Use relative paths in HTML: `assets/images/your-image.png`
3. Upload to GitHub (include the new image file)

---

## Deployment Workflow

### Initial Deployment (First Time)

Follow **DEPLOYMENT-GUIDE.md** for complete instructions:
1. Create GitHub repository
2. Upload all files from this directory
3. Enable GitHub Pages
4. Configure custom domain (avestltd.com)
5. Set up DNS at IONOS
6. Enable HTTPS

### Updating After Initial Deployment

**Method 1: GitHub Web Interface (Easiest)**
1. Go to your repository on GitHub
2. Navigate to the file you want to update
3. Click the pencil icon (Edit)
4. Make your changes
5. Scroll down, add a commit message
6. Click "Commit changes"
7. Wait 1-2 minutes for GitHub Pages to rebuild
8. Refresh your website to see changes

**Method 2: Upload Files**
1. Make changes to files locally
2. Go to your GitHub repository
3. Click "Add file" → "Upload files"
4. Drag updated files (they replace old versions)
5. Commit changes
6. Wait 1-2 minutes for changes to go live

**Method 3: GitHub Desktop (Advanced)**
1. Use GitHub Desktop app
2. Make changes locally
3. Commit and push to GitHub
4. Changes go live automatically

---

## Technical Details

### Hosting
- **Platform:** GitHub Pages (free)
- **Domain:** avestltd.com (via IONOS)
- **SSL:** Automatic (via GitHub/Let's Encrypt)
- **CDN:** Included with GitHub Pages

### Browser Compatibility
- Chrome ✅
- Safari ✅
- Firefox ✅
- Edge ✅
- Mobile browsers ✅

### Performance
- All assets hosted locally (fast)
- Minimal external dependencies
- Optimized images
- Clean, efficient CSS

### External Dependencies
- **Calendly Widget:** Loaded on contact.html only
  - Script: https://assets.calendly.com/assets/external/widget.js
  - Link: https://assets.calendly.com/assets/external/widget.css

---

## Maintenance & Updates

### Regular Maintenance (Optional)

**Monthly:**
- Review Calendly integration (make sure booking link works)
- Test all pages on mobile and desktop
- Check for broken links

**As Needed:**
- Update pricing if plans change
- Add new services to services.html
- Update FAQs in documentation.html
- Refresh team information in about.html

### Content Updates

All content is in plain HTML - no database required!

**To update pricing:**
- Edit `pricing.html`
- Find the pricing cards (around line 100-300)
- Update prices, features, descriptions
- Save and upload to GitHub

**To update services:**
- Edit `services.html`
- Update service descriptions, benefits
- Save and upload to GitHub

**To update FAQs:**
- Edit `documentation.html`
- Scroll to FAQ section
- Add/edit/remove questions and answers
- Save and upload to GitHub

---

## Pre-Deployment Checklist

Before deploying to GitHub Pages, verify:

- [✓] All 7 HTML files present
- [✓] All assets (CSS, images) present
- [✓] CNAME file created with `avestltd.com`
- [✓] All internal links use relative paths
- [✓] Calendly integration URL is correct
- [✓] Favicons present
- [✓] No broken links between pages
- [✓] Mobile-responsive design verified

**Status: All items checked ✓ - Ready for deployment!**

---

## Testing Checklist (After Deployment)

After deploying to GitHub Pages:

- [ ] Visit https://avestltd.com - loads homepage
- [ ] Visit https://www.avestltd.com - redirects correctly
- [ ] Test all 7 pages load correctly
- [ ] Test all navigation links work
- [ ] Verify Calendly widget loads on contact page
- [ ] Test on mobile device
- [ ] Verify HTTPS (green padlock) in browser
- [ ] Check page load speed (should be fast)
- [ ] Test form submission on Calendly

---

## Troubleshooting

### Website not loading after deployment?
→ Check DNS-CONFIGURATION.md and verify DNS propagation

### 404 error on GitHub Pages?
→ Make sure index.html is in root directory, not in a subfolder

### Calendly widget not showing?
→ Verify JavaScript isn't blocked, check browser console for errors

### Styles not loading?
→ Check that assets/css/style.css path is correct in HTML files

### Images not showing?
→ Verify image paths are relative: `assets/images/filename.png`

**For detailed troubleshooting, see DEPLOYMENT-GUIDE.md.**

---

## Support & Resources

- **Deployment Help:** See DEPLOYMENT-GUIDE.md
- **DNS Help:** See DNS-CONFIGURATION.md
- **GitHub Pages Docs:** https://docs.github.com/en/pages
- **Calendly Support:** https://help.calendly.com

---

## Important Notes

### Custom Domain Configuration
- Domain: **avestltd.com** (managed at IONOS)
- CNAME file must contain exactly: `avestltd.com`
- DNS configured at IONOS (see DNS-CONFIGURATION.md)

### Contact Information
- **Business Email:** samantha@avestltd.com
- **Phone:** (936) 444-2869
- **Calendly:** https://calendly.com/samantha128aire/avestai-discovery-call

### Calendly Setup
The contact page uses an embedded Calendly widget. The integration is already configured - no setup needed. Bookings go to samantha128aire@gmail.com.

---

## Version History

- **v1.0** - February 20, 2026 - Initial deployment package
  - 7 pages complete
  - Calendly integration
  - Professional design
  - Responsive layout
  - Ready for GitHub Pages deployment

---

## Next Steps

1. **Read DEPLOYMENT-GUIDE.md** from start to finish
2. **Set aside 1 hour** to follow the deployment steps
3. **Configure DNS** at IONOS using DNS-CONFIGURATION.md
4. **Wait for DNS propagation** (2-24 hours)
5. **Test your live site** using the testing checklist
6. **Celebrate!** 🎉 Your website is live!

---

**Questions? Issues? Feedback?**

All documentation is in this directory:
- DEPLOYMENT-GUIDE.md - Full walkthrough
- DNS-CONFIGURATION.md - DNS records
- FILE-INVENTORY.md - Complete file list

**This website is ready to deploy - no additional setup required!**

---

*Package prepared: February 20, 2026*  
*Status: Production-ready*  
*Platform: GitHub Pages*  
*Domain: avestltd.com*
