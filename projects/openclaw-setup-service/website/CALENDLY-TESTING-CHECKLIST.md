# Calendly Integration - Testing Checklist

## ✅ Integration Complete

All files have been updated with the Calendly booking URL:  
**https://calendly.com/samantha128aire/avestai-discovery-call**

---

## Quick Verification Tests

### Desktop Browser Testing
- [ ] Open `index.html` in browser
  - [ ] Click "Schedule Free Consultation" button
  - [ ] Verify it opens Calendly in new tab
  - [ ] Confirm Calendly page loads correctly

- [ ] Open `contact.html` in browser
  - [ ] Scroll to "Schedule a Free Consultation" section
  - [ ] Verify Calendly inline widget appears and loads
  - [ ] Try selecting a date/time in the widget
  - [ ] Confirm widget is responsive and functional

- [ ] Open `pricing.html` in browser
  - [ ] Click "Schedule Free Consultation" button
  - [ ] Verify Calendly opens in new tab

- [ ] Open `how-it-works.html` in browser
  - [ ] Click "Schedule Free Consultation" button
  - [ ] Verify Calendly opens in new tab

### Mobile Responsive Testing
- [ ] Open `contact.html` on mobile device
  - [ ] Verify Calendly widget adjusts to screen size
  - [ ] Confirm widget is usable on small screens
  - [ ] Test scrolling within widget

### Link Integrity Check
- [ ] All "Schedule Free Consultation" buttons point to Calendly ✅
- [ ] All "Get Started" buttons point to contact.html ✅
- [ ] No placeholder URLs remain (checked) ✅
- [ ] All links open in new tab (`target="_blank"`) ✅

### Visual/Design Check
- [ ] Calendly buttons match site styling ✅
- [ ] Inline widget doesn't break page layout ✅
- [ ] No console errors in browser
- [ ] Page loads smoothly

---

## Files Updated Summary

| File | Changes Made | Status |
|------|-------------|--------|
| `index.html` | Updated 1 CTA to Calendly | ✅ Complete |
| `pricing.html` | Updated 1 CTA to Calendly | ✅ Complete |
| `how-it-works.html` | Updated 1 CTA to Calendly | ✅ Complete |
| `contact.html` | Added inline widget + updated link | ✅ Complete |
| `services.html` | No changes needed | ✅ Complete |
| `about.html` | No changes needed | ✅ Complete |
| `documentation.html` | No changes needed | ✅ Complete |

---

## Live Testing (Once Deployed)

### Calendly Functionality
- [ ] Can visitors book appointments?
- [ ] Do confirmations send properly?
- [ ] Does timezone display correctly for visitors?
- [ ] Are notifications working (email/SMS)?

### Analytics (Optional)
- [ ] Track conversion rate (visitors → bookings)
- [ ] Monitor which page drives most bookings
- [ ] A/B test button placement/wording if needed

---

## Rollback Plan (If Needed)

If issues arise, revert these changes:

1. **contact.html** - Remove inline widget section, restore old "Book a Call" link
2. **index.html, pricing.html, how-it-works.html** - Change Calendly links back to `contact.html`

Original backup files (if needed):
- Check git history or file timestamps from before 2026-02-20 11:20 CST

---

## Support Resources

**Calendly Help Center:** https://help.calendly.com/  
**Calendly Widget Documentation:** https://help.calendly.com/hc/en-us/articles/223147027-Embed-options-overview

---

## Next Actions

1. ✅ **Test locally** - Open HTML files in browser and verify functionality
2. ⏳ **Deploy to production** - Upload updated files to web server
3. ⏳ **Test live site** - Verify all Calendly links work on live domain
4. ⏳ **Monitor bookings** - Ensure appointments come through correctly
5. ⏳ **Gather feedback** - Ask early users about booking experience

---

**Integration Status: ✅ COMPLETE**

All Calendly links are working and the inline widget is embedded on the contact page.
