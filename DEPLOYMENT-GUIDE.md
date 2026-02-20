# Complete Deployment Guide for AvestAI Website
## Deploy avestltd.com to GitHub Pages

**Time Required:** 30-60 minutes (most of it is waiting for DNS)  
**Technical Level:** Beginner-friendly - no coding required!

This guide will walk you through every step to get your AvestAI website live at **avestltd.com**.

---

## What You'll Need

- [ ] GitHub account (we'll help you create one if needed)
- [ ] Access to IONOS DNS settings for avestltd.com
- [ ] The website files (already in this folder!)
- [ ] 30 minutes of focused time

---

## Overview: What We're Doing

1. **Create a GitHub account** (if you don't have one)
2. **Create a new repository** on GitHub to store your website
3. **Upload your website files** to the repository
4. **Enable GitHub Pages** to make the site live
5. **Configure DNS** at IONOS to point your domain to GitHub
6. **Enable HTTPS** for secure connections
7. **Test everything** to make sure it works

Let's get started! 🚀

---

## Step 1: Create a GitHub Account

**If you already have a GitHub account, skip to Step 2.**

1. Go to **https://github.com**
2. Click **Sign up** in the top-right corner
3. Enter your email address (use samantha@avestltd.com or personal email)
4. Create a strong password
5. Choose a username (e.g., "avestai" or "avestltd")
6. Complete the verification puzzle
7. Check your email and verify your account

**What success looks like:** You're logged into GitHub and see your dashboard.

---

## Step 2: Create a New Repository

A "repository" is like a folder on GitHub where your website files will live.

1. **Log in to GitHub**
2. Click the **+** button in the top-right corner
3. Select **New repository**
4. Fill out the form:
   - **Repository name:** `avestltd-website` (or any name you like)
   - **Description:** "AvestAI official website - avestltd.com"
   - **Public** (select this - required for free GitHub Pages)
   - **DO NOT** check "Add a README file" (we already have files to upload)
5. Click **Create repository**

**What success looks like:** You see a page with instructions for uploading files. Keep this page open - we'll use it in the next step.

---

## Step 3: Upload Your Website Files

Now we'll put all your website files into the repository.

### Option A: Upload via Web Browser (Easiest)

1. On the repository page you just created, you'll see quick setup instructions
2. Click the link that says **"uploading an existing file"** (in the gray box)
3. You'll see a page that says "Drag files here to add them to your repository"
4. **Open a new Finder window** and navigate to:
   ```
   /Users/sam/.openclaw/workspace/projects/openclaw-setup-service/website/
   ```
5. **Select ALL files and folders:**
   - All 7 HTML files (index.html, about.html, etc.)
   - CNAME file
   - assets folder (with all its contents)
   - README.md
   
   **Tip:** Click on the first file, then hold Command (⌘) and click on the last file to select everything. You can also drag a selection box around all items.

6. **Drag all selected files** into the GitHub upload area
7. Wait for all files to upload (you'll see a progress indicator)
8. Scroll down to the **"Commit changes"** section at the bottom
9. In the commit message box, it will say "Add files via upload" - that's fine
10. Click the green **"Commit changes"** button

**What success looks like:** After clicking commit, you'll see your repository page with all your files listed, including:
- index.html
- about.html, contact.html, documentation.html, how-it-works.html, pricing.html, services.html
- CNAME
- assets folder
- README.md

### Option B: Using GitHub Desktop (Alternative)

If you prefer a desktop app:
1. Download GitHub Desktop from https://desktop.github.com
2. Install and sign in with your GitHub account
3. Clone your repository
4. Copy all website files into the local repository folder
5. Commit and push changes

---

## Step 4: Enable GitHub Pages

Now we'll turn your repository into a live website!

1. In your repository, click **Settings** (top menu, far right)
   - If you don't see Settings, you might need to scroll the menu to the right
2. In the left sidebar, scroll down and click **Pages**
3. Under **Source**, you'll see a dropdown that says "None"
4. Click the dropdown and select **main** (or **master** if that's what you see)
5. Leave the folder as **/ (root)**
6. Click **Save**
7. Wait 30 seconds, then **refresh the page**

**What success looks like:** At the top of the Pages settings, you'll see a blue or green box that says:
> "Your site is ready to be published at https://your-username.github.io/avestltd-website/"

or

> "Your site is published at https://your-username.github.io/avestltd-website/"

**Important:** At this point, your site is live at the GitHub URL, but NOT yet at avestltd.com. We'll fix that next!

### Test Your Site

Click the link in the green/blue box. Your website should load! 

**Troubleshooting:**
- If you see a 404 error, wait 2-3 minutes and refresh
- If you see a list of files instead of your website, make sure index.html is in the root (not in a subfolder)

---

## Step 5: Configure Your Custom Domain (avestltd.com)

Now we'll connect your custom domain to GitHub Pages.

### Part A: Tell GitHub About Your Domain

1. Still in **Settings → Pages** on GitHub
2. Scroll down to **Custom domain**
3. In the text box, type: `avestltd.com`
4. Click **Save**
5. You'll see a message: "DNS check in progress" (this is normal)

**Note:** GitHub will check your DNS settings. This will fail initially because we haven't set up DNS yet - that's our next step!

### Part B: Configure DNS at IONOS

**This is the most important step!** Follow the detailed instructions in the **DNS-CONFIGURATION.md** file.

**Quick summary:**
1. Log in to IONOS (https://my.ionos.com)
2. Go to your domain settings for avestltd.com
3. Add 4 A records pointing to GitHub's IP addresses
4. Add 1 CNAME record for www subdomain
5. Save all changes

**Full details:** See **DNS-CONFIGURATION.md** for exact values and step-by-step IONOS instructions.

---

## Step 6: Wait for DNS Propagation

After configuring DNS at IONOS:

1. **Wait at least 2-4 hours** (can take up to 48 hours, but usually faster)
2. During this time, your website might:
   - Not load at all
   - Show a "DNS not found" error
   - Work for some people but not others
   - Load at the GitHub URL but not at avestltd.com

**This is all normal!** DNS propagation takes time.

### Check DNS Propagation Status

You can monitor progress:
1. Go to **https://dnschecker.org**
2. Enter `avestltd.com`
3. Select **A** from the record type dropdown
4. Click **Search**
5. Look for the 4 GitHub IP addresses (185.199.108-111.153)

When you see green checkmarks showing these IPs around the world, your DNS has propagated!

---

## Step 7: Enable HTTPS (Secure Connection)

After DNS has propagated (wait at least 4 hours after Step 5):

1. Go back to **GitHub → Your Repository → Settings → Pages**
2. Scroll down to **Custom domain**
3. You should now see a green checkmark next to "DNS check successful"
4. Below that, find the checkbox: **"Enforce HTTPS"**
5. If it's disabled (grayed out), wait a few more hours - GitHub is provisioning your SSL certificate
6. Once available, **check the "Enforce HTTPS" box**

**What success looks like:** The checkbox is enabled and checked. At the top, you'll see:
> "Your site is published at https://avestltd.com"

**Note:** HTTPS can take up to 24 hours after DNS propagation to become available.

---

## Step 8: Test Everything

Once HTTPS is enabled, test your website thoroughly:

### Testing Checklist

- [ ] **Visit http://avestltd.com** - should redirect to https://avestltd.com
- [ ] **Visit http://www.avestltd.com** - should redirect to https://avestltd.com
- [ ] **Visit https://avestltd.com** - should load your homepage
- [ ] **Visit https://www.avestltd.com** - should redirect to https://avestltd.com
- [ ] **Test all navigation links:**
  - [ ] Home → index.html
  - [ ] About → about.html
  - [ ] Services → services.html
  - [ ] How It Works → how-it-works.html
  - [ ] Pricing → pricing.html
  - [ ] Documentation → documentation.html
  - [ ] Contact → contact.html
- [ ] **Test Calendly integration** on the Contact page
- [ ] **Check on mobile device** (phone or tablet)
- [ ] **Test in different browsers** (Chrome, Safari, Firefox)
- [ ] **Look for HTTPS padlock** in the browser address bar (should be there)

**What success looks like:** Everything loads, all links work, Calendly form appears on contact page, and you see the green padlock icon in your browser.

---

## Troubleshooting Common Issues

### Issue: "Your site is having problems" on GitHub Pages

**Solution:**
- Make sure CNAME file contains only `avestltd.com` (no https://, no www, just the domain)
- Check that DNS records are correct at IONOS
- Wait longer (DNS can take up to 48 hours)

### Issue: Website shows 404 error

**Solution:**
- Make sure `index.html` is in the root of your repository (not in a subfolder)
- Check that GitHub Pages is enabled and set to "main" branch, "/ (root)" folder
- Wait 2-3 minutes after enabling Pages, then refresh

### Issue: "DNS check failed" on GitHub

**Solution:**
- DNS records not set up yet or not propagated
- Verify you added all 4 A records and 1 CNAME record correctly at IONOS
- Wait 2-4 hours after adding DNS records
- Use dnschecker.org to verify propagation

### Issue: "Enforce HTTPS" checkbox is grayed out

**Solution:**
- DNS needs to be fully propagated first
- GitHub is still provisioning your SSL certificate
- Wait 24 hours after DNS propagates
- Make sure DNS check shows successful

### Issue: www.avestltd.com doesn't work

**Solution:**
- Check that CNAME record for "www" is set up correctly at IONOS
- Should point to `avestltd.com` (not to a GitHub URL)
- Wait for DNS propagation

### Issue: Mixed content warnings (not all HTTPS)

**Solution:**
- All your links are relative, so this shouldn't happen
- If it does, GitHub is still setting up HTTPS
- Wait 24 hours after "Enforce HTTPS" is enabled

### Issue: Calendly widget not loading

**Solution:**
- Check that contact.html uploaded correctly
- Make sure JavaScript isn't blocked by browser
- Test in an incognito/private window
- Verify Calendly link is correct (https://calendly.com/samantha128aire/avestai-discovery-call)

---

## Making Updates to Your Website

After your site is live, you can update it anytime:

1. **Edit files locally** on your Mac (in the website folder)
2. **Go to your GitHub repository** in your web browser
3. Click on the file you want to update
4. Click the **pencil icon** (Edit) in the top-right
5. **Delete the old content** and copy-paste your new content
6. Scroll down and click **Commit changes**
7. **Wait 1-2 minutes** for GitHub Pages to rebuild
8. **Refresh your website** (https://avestltd.com) to see changes

**Or use the upload method:**
1. Navigate to your repository
2. Click **Add file → Upload files**
3. Drag your updated files (they'll replace the old versions)
4. Commit changes

**Changes are usually live within 1-2 minutes!**

---

## Monitoring Your Site

### View Site Traffic (Later)

You can add Google Analytics to track visitors:
1. Sign up for Google Analytics
2. Get your tracking code
3. Add it to each HTML file's `<head>` section
4. Upload updated files to GitHub

### Check Site Status

- **Is my site up?** Visit https://avestltd.com
- **GitHub Pages status:** https://www.githubstatus.com (for outages)
- **Check SSL certificate:** Click the padlock icon in your browser when viewing your site

---

## Quick Reference: Key Information

| Item | Value |
|------|-------|
| **Website URL** | https://avestltd.com |
| **Repository** | github.com/[your-username]/avestltd-website |
| **GitHub Pages URL** | [your-username].github.io/avestltd-website |
| **Domain Registrar** | IONOS |
| **DNS Records** | See DNS-CONFIGURATION.md |
| **CNAME** | avestltd.com |
| **Contact Form** | Calendly integration |
| **Hosting Cost** | FREE (GitHub Pages) |

---

## Need Help?

- **GitHub Pages Documentation:** https://docs.github.com/en/pages
- **GitHub Support:** https://support.github.com
- **IONOS Support:** https://www.ionos.com/help
- **DNS Checker:** https://dnschecker.org

---

## Summary: What You've Accomplished

✅ Created a GitHub account and repository  
✅ Uploaded your website files to GitHub  
✅ Enabled GitHub Pages hosting (free!)  
✅ Connected your custom domain (avestltd.com)  
✅ Configured DNS records at IONOS  
✅ Enabled HTTPS for secure connections  
✅ Your website is live to the world at https://avestltd.com  

**Congratulations! Your AvestAI website is now live! 🎉**

---

## Timeline Summary

- **Steps 1-4:** 15-30 minutes (creating account, uploading files, enabling Pages)
- **Step 5:** 10 minutes (DNS configuration)
- **Step 6:** 2-48 hours (waiting for DNS propagation, usually 2-4 hours)
- **Step 7:** Up to 24 hours (HTTPS certificate provisioning)
- **Step 8:** 15 minutes (testing)

**Total active time:** ~1 hour  
**Total elapsed time:** 1-3 days (mostly automated waiting)

**Pro tip:** Do Steps 1-5 before bed, and by morning your DNS will be propagated!

---

*Last updated: February 20, 2026*
