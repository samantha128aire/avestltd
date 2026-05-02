# TOOLS.md - Local Notes

## Active Integrations

**Google (gog)** - samantha128aire@gmail.com
- Services: gmail, calendar, drive, docs, contacts, sheets
- **Always share Drive files with chance.ihs@gmail.com**
- contacts.csv: Drive ID 1KJiCRTOBPNJj9xVveKzCSZSEAgedZudt
- **Business email:** samantha@avestltd.com forwards to Gmail, replies sent from professional address

**Zoom**
- Account: chance@goihs.com
- Credentials: `~/.openclaw/credentials/zoom.env`
- Can create/read/manage meetings via REST API
- Business phone: (936) 444-2869 (Zoom Phone)

**AvestAI Business Tools**
- **Calendly:** https://calendly.com/samantha128aire/avestai-discovery-call (30 min discovery calls)
- **Phone:** (936) 444-2869 (Zoom phone - shared across all Avest businesses)
- **Email:** samantha@avestltd.com (professional customer-facing address)
- **Website:** https://avestltd.com (live, GitHub Pages)
- **GitHub:** https://github.com/samantha128aire/avestltd
- **Google Analytics:** G-PBL118DSSX
- **Pricing:** $695 (Basic), $1,295 (Standard), $1,795 (Premium) - 100% upfront
- **Support:** $100/month or $150/hour post-30-day period

**WhatsApp (wacli)**
- Auth: linked to Chance's WhatsApp (QR scan done Mar 2, 2026)
- Store: `~/.wacli`
- **IMPORTANT: Use JID format, NOT +1 phone format**
  - ✅ `wacli send text --to "15089229086@s.whatsapp.net" --message "..."`
  - ❌ `wacli send text --to "+15089229086" --message "..."` (times out)
- Find JIDs: `wacli chats list --limit 20`
- Known contacts:
  - Chance: `15089229086@s.whatsapp.net`
- **⚠️ Always include in WhatsApp messages:** "Note: I can't receive replies here — reach me via iMessage at (936) 577-2048"

**iMessage (imsg)**
- Chat 1 = Chance (+1-508-922-9086)
- Salvi (+1-351-209-2847) has access
- **Samantha's iPhone:** (936) 577-2048 — real mobile number, iMessage active, screen mirroring enabled

**TTS** - en-US-AvaNeural (Microsoft Edge TTS, free)

**Remote Access** - Chrome Remote Desktop (chance.ihs@gmail.com)

---

## Monitoring

**TSLA** - Daily weekday check (pre-market 7-9 AM), using Sonnet

~~**MSFT** - Watch $390 level for bull call spread opportunity~~ (dropped Apr 9, 2026)

**Costs** - Manual screenshot weekly, ~$200/month budget, $14.33/day burn (as of Feb 3)

---

## Backups
Daily 3 AM to Google Drive via `/Users/sam/.openclaw/scripts/backup-workspace.sh`
