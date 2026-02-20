# AvestAI Website - Deployment Guide

Complete professional website for AvestAI - Personal AI setup service.

## 🚀 Quick Start

This website is ready to deploy to GitHub Pages. Follow the steps below to get your site live at **avestltd.com**.

---

## 📁 File Structure

```
website/
├── index.html                  # Homepage
├── services.html               # Services page
├── pricing.html                # Pricing page
├── how-it-works.html          # Process timeline
├── documentation.html          # Customer portal/docs
├── about.html                  # About page
├── contact.html                # Contact form
├── assets/
│   ├── css/
│   │   ├── reset.css          # CSS reset
│   │   └── style.css          # Main stylesheet
│   └── images/
│       ├── logo-transparent-256.png
│       ├── favicon-32.png
│       ├── favicon-16.png
│       └── (other logo variations)
└── README.md                   # This file
```

---

## 🌐 Deploying to GitHub Pages

### Step 1: Create a GitHub Account

1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Follow the registration process
4. Verify your email address

### Step 2: Create a New Repository

1. Log in to GitHub
2. Click the **+** icon in the top-right corner
3. Select **"New repository"**
4. Repository settings:
   - **Repository name:** `avestltd.com` (or `avestai-website`)
   - **Description:** "AvestAI - Personal AI Setup Service"
   - **Visibility:** Public (required for free GitHub Pages)
   - **DO NOT** check "Add a README file" (we already have one)
5. Click **"Create repository"**

### Step 3: Upload Your Website Files

#### Option A: Using GitHub Web Interface (Easiest)

1. On your new repository page, click **"uploading an existing file"**
2. Drag and drop ALL files from the `website/` folder:
   - All `.html` files
   - `assets/` folder (with css/ and images/ subfolders)
   - `README.md`
3. Scroll down and click **"Commit changes"**

#### Option B: Using GitHub Desktop (Recommended)

1. Download GitHub Desktop: [desktop.github.com](https://desktop.github.com)
2. Install and sign in with your GitHub account
3. Click **"Clone a repository"** → Select your repository
4. Choose a local folder location
5. Copy all files from `website/` into the cloned repository folder
6. In GitHub Desktop:
   - Write commit message: "Initial website upload"
   - Click **"Commit to main"**
   - Click **"Push origin"**

#### Option C: Using Git Command Line (Advanced)

```bash
# Navigate to the website directory
cd /path/to/website

# Initialize Git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial website upload"

# Add GitHub remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/avestltd.com.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Enable GitHub Pages

1. In your GitHub repository, click **"Settings"** (top menu)
2. In the left sidebar, click **"Pages"**
3. Under **"Source"**, select:
   - **Branch:** main
   - **Folder:** / (root)
4. Click **"Save"**
5. Wait 1-2 minutes
6. Your site will be live at: `https://USERNAME.github.io/avestltd.com/`

---

## 🔗 Configuring Custom Domain (avestltd.com)

### Step 1: Update GitHub Pages Settings

1. In GitHub repository → Settings → Pages
2. Under **"Custom domain"**, enter: `avestltd.com`
3. Click **"Save"**
4. Check **"Enforce HTTPS"** (after DNS propagates)

### Step 2: Configure DNS Settings

You need to configure DNS records with your domain registrar (where you bought avestltd.com).

#### A Records (Required)

Add these **A records** pointing to GitHub Pages:

```
Type: A
Host: @
Value: 185.199.108.153

Type: A
Host: @
Value: 185.199.109.153

Type: A
Host: @
Value: 185.199.110.153

Type: A
Host: @
Value: 185.199.111.153
```

#### CNAME Record (For www subdomain)

```
Type: CNAME
Host: www
Value: USERNAME.github.io
```

Replace `USERNAME` with your GitHub username.

#### Example DNS Configuration (Generic Registrar)

1. Log in to your domain registrar (GoDaddy, Namecheap, etc.)
2. Find "DNS Management" or "DNS Settings"
3. Delete any existing A records for `@` or `avestltd.com`
4. Add the 4 A records listed above
5. Add the CNAME record for `www`
6. Save changes

**DNS propagation takes 24-48 hours.** Your site will be available at avestltd.com once complete.

---

## ✅ Pre-Deployment Checklist

Before deploying, complete these setup tasks:

### 1. Formspree Setup (Contact Form)

**File:** `contact.html`

1. Go to [formspree.io](https://formspree.io)
2. Create a free account
3. Create a new form
4. Copy your form ID (looks like: `mqazwxyz`)
5. In `contact.html`, find this line:
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST" class="contact-form">
   ```
6. Replace `YOUR_FORM_ID` with your actual form ID
7. Save the file

### 2. Calendly Setup (Consultation Booking)

**File:** `contact.html`

1. Go to [calendly.com](https://calendly.com)
2. Create a free account
3. Set up a "15-Minute Consultation" event type
4. Copy your Calendly username
5. In `contact.html`, find this line:
   ```html
   <a href="https://calendly.com/YOUR_CALENDLY_USERNAME/15min" target="_blank" class="btn btn-primary">Book a Call</a>
   ```
6. Replace `YOUR_CALENDLY_USERNAME` with your actual username
7. Save the file

### 3. Create Thank You Page (Optional)

**File:** `thank-you.html` (create this)

Create a simple thank you page for form submissions:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You - AvestAI</title>
    <link rel="stylesheet" href="assets/css/reset.css">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <section class="hero">
        <div class="container" style="text-align: center;">
            <h1>Thank You!</h1>
            <p class="subheading">We've received your message and will get back to you within 24 hours.</p>
            <a href="index.html" class="btn btn-primary" style="margin-top: 30px;">Return to Home</a>
        </div>
    </section>
</body>
</html>
```

---

## 🧪 Testing Before Going Live

### Local Testing

Open `index.html` in your browser to test:

```bash
# macOS
open index.html

# Or just drag index.html into your browser
```

### Test Checklist

- [ ] All navigation links work
- [ ] All images load correctly
- [ ] Logo displays properly
- [ ] Contact form submits (after Formspree setup)
- [ ] Calendly link works (after setup)
- [ ] Mobile responsive (resize browser to 375px, 768px, 1024px)
- [ ] All text is readable
- [ ] No broken links
- [ ] Footer displays on all pages

### Responsive Testing

Test at these viewport widths:

- **375px** - iPhone SE / small phones
- **768px** - iPad / tablets
- **1024px** - iPad Pro / small laptops
- **1440px** - Desktop / large screens

---

## 📱 Mobile Testing

### Test on Real Devices

1. Deploy to GitHub Pages (even with temporary URL)
2. Visit `https://USERNAME.github.io/avestltd.com/` on:
   - iPhone / Android phone
   - iPad / Android tablet
3. Test:
   - Navigation menu (hamburger icon)
   - All links and buttons
   - Form submission
   - Image loading
   - Scrolling performance

---

## 🎨 Customization

### Updating Colors

**File:** `assets/css/style.css`

Find the `:root` section at the top:

```css
:root {
  --primary-blue: #00A8E8;    /* Change this to update brand color */
  --dark-gray: #1d1d1f;
  --medium-gray: #86868b;
  --light-gray: #f5f5f7;
  --white: #ffffff;
}
```

### Updating Logo

Replace these files in `assets/images/`:
- `logo-transparent-256.png` (main logo)
- `favicon-32.png` (browser favicon)
- `favicon-16.png` (browser favicon)

### Updating Content

Edit the respective `.html` files directly. Content is structured with clear HTML comments.

---

## 🔧 Troubleshooting

### Images Not Loading

- Check file paths: `assets/images/logo-transparent-256.png`
- Ensure images were uploaded to GitHub
- Check browser console (F12) for errors

### Custom Domain Not Working

- Wait 24-48 hours for DNS propagation
- Check DNS settings with: [dnschecker.org](https://dnschecker.org)
- Verify A records point to correct GitHub IPs
- Ensure "Enforce HTTPS" is enabled in GitHub Pages settings

### Contact Form Not Submitting

- Verify Formspree form ID is correct
- Check Formspree dashboard for submissions
- Test form in private/incognito window

### Mobile Menu Not Working

- Ensure JavaScript is enabled
- Check browser console (F12) for errors
- Clear browser cache and reload

---

## 📊 Analytics (Optional)

### Adding Google Analytics

1. Create Google Analytics account
2. Get your tracking ID (e.g., `G-XXXXXXXXXX`)
3. Add this code before `</head>` in all HTML files:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🚀 Performance Optimization

### Already Implemented

- ✅ Minimal CSS (no frameworks)
- ✅ Optimized images (PNG, web-safe sizes)
- ✅ Fast loading (no external dependencies except Formspree)
- ✅ Mobile-first responsive design
- ✅ Semantic HTML for accessibility

### Future Improvements

- Convert images to WebP format (smaller file size)
- Add lazy loading for images
- Minify CSS and JavaScript
- Add service worker for offline support

---

## 📝 Maintenance

### Regular Updates

- Update pricing if it changes
- Add customer testimonials (when available)
- Update team bios as you grow
- Add blog posts or case studies

### Backup

GitHub automatically keeps version history. To download a backup:

1. Go to your repository
2. Click **"Code"** → **"Download ZIP"**

---

## 🆘 Support

### Need Help?

- **GitHub Pages Docs:** [docs.github.com/en/pages](https://docs.github.com/en/pages)
- **Formspree Docs:** [help.formspree.io](https://help.formspree.io)
- **Calendly Help:** [help.calendly.com](https://help.calendly.com)

### Common Resources

- [Markdown Guide](https://www.markdownguide.org) - For editing this README
- [HTML Reference](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)

---

## ✅ Launch Checklist

Before announcing your site publicly:

- [ ] Formspree form ID updated and tested
- [ ] Calendly link updated and tested
- [ ] All placeholder text replaced
- [ ] DNS configured (for custom domain)
- [ ] HTTPS enforced
- [ ] Tested on mobile devices
- [ ] Contact email addresses verified
- [ ] Phone numbers correct
- [ ] All links working
- [ ] Spelling/grammar checked
- [ ] Google Analytics added (optional)
- [ ] Favicon displays correctly

---

## 📄 License

This website is proprietary to Avest Ltd / AvestAI.

---

## 🎉 You're Ready!

Your professional website is ready to launch. Good luck with AvestAI!

**Questions?** Email: hello@avestltd.com | Phone: (508) 922-9086
