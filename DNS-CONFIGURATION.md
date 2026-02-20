# DNS Configuration for avestltd.com

## What You Need to Do at IONOS

You need to add 5 DNS records total to make your website work with GitHub Pages.

---

## Step 1: Add GitHub Pages A Records

**What these do:** Point your domain (avestltd.com) to GitHub's servers.

Add these **4 A records** exactly as shown:

| Type | Host/Name | Points to (IP Address) | TTL |
|------|-----------|------------------------|-----|
| A    | @         | 185.199.108.153       | 3600 |
| A    | @         | 185.199.109.153       | 3600 |
| A    | @         | 185.199.110.153       | 3600 |
| A    | @         | 185.199.111.153       | 3600 |

**Note:** The "@" symbol means "the root domain" (avestltd.com without any www or subdomain).

---

## Step 2: Add CNAME Record for www

**What this does:** Makes www.avestltd.com redirect to avestltd.com.

Add this **1 CNAME record**:

| Type  | Host/Name | Points to          | TTL  |
|-------|-----------|-------------------|------|
| CNAME | www       | avestltd.com      | 3600 |

---

## How to Add These Records in IONOS

1. **Log in to IONOS** (https://my.ionos.com)
2. Go to **Domains & SSL**
3. Click on **avestltd.com**
4. Find the **DNS Settings** or **Manage DNS** section
5. Click **Add Record** for each entry above

### For each A record:
- Select "A" as the record type
- In the "Host" field, enter `@`
- In the "Points to" or "Value" field, enter the IP address
- Set TTL to 3600 (or leave as default)
- Click **Save**

### For the CNAME record:
- Select "CNAME" as the record type
- In the "Host" or "Alias" field, enter `www`
- In the "Points to" or "Target" field, enter `avestltd.com`
- Set TTL to 3600 (or leave as default)
- Click **Save**

---

## Important Notes

### Propagation Time
- **DNS changes can take 4-48 hours to fully propagate** across the internet
- Most changes are visible within 1-4 hours
- Be patient! Your website might not work immediately after adding these records

### What Success Looks Like
After DNS propagates (wait at least 2 hours), you should be able to:
- Visit **http://avestltd.com** and see your website
- Visit **http://www.avestltd.com** and get redirected to avestltd.com
- After GitHub Pages enables HTTPS (24 hours later), both will work with **https://**

### Check DNS Propagation
You can check if your DNS changes have propagated using:
- https://dnschecker.org (enter "avestltd.com" and select "A" record type)
- Look for the 4 GitHub IP addresses (185.199.108-111.153)

---

## Troubleshooting

**Website not loading?**
- Wait longer (DNS can take up to 48 hours)
- Verify all 5 records are entered correctly with no typos
- Make sure there are no conflicting old A or CNAME records for @ or www

**"DNS_PROBE_FINISHED_NXDOMAIN" error?**
- DNS hasn't propagated yet. Wait and try again in 2-4 hours

**Mixed content warnings?**
- This is normal initially. GitHub will enable HTTPS within 24 hours after DNS is set up

---

## Remove Old Records (If Any)

Before adding the new records, **delete any existing A or CNAME records** for:
- @ (root domain)
- www

This prevents conflicts. If you're not sure, it's safe to delete old pointing records for these - you're replacing them with the new ones above.

---

## Quick Reference Card

**Copy these exact values when setting up DNS:**

```
A Records (add all 4):
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153

CNAME Record:
www → avestltd.com
```

---

**After completing DNS configuration, continue with Step 3 in the DEPLOYMENT-GUIDE.md file.**
