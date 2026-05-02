# HEARTBEAT.md

## 📈 Stock Monitoring (Weekdays 7-9 AM CST ONLY)
**Skip weekends and after-hours. Market: 8:30 AM - 3:00 PM CST**

**TSLA** - Search "TSLA Tesla stock news" (last 24h)
- Check for: Major moves (>5%), earnings, launches, regulatory issues
- **Only alert if significant** — routine trading = no notification

**MSFT** - Check if trading near $390
- Alert if within $5 of target ($385-$395)
- Context: Bull call spread opportunity

---

## 📧 Email (8-10 AM, 2-4 PM, 7-9 PM)
```bash
gog gmail search 'is:unread newer_than:4h' --max 5
```
Alert only if: urgent/important/time-sensitive

---

## 📅 Calendar (Morning only, 8-9 AM)
```bash
gog calendar events primary --from $(date -Iseconds) --to $(date -v+2d -Iseconds)
```
Alert if: event <2h away, new event, important meeting

---

## 🎂 Birthdays (7 AM daily)
Check `memory/contacts.csv`, send iMessage birthday wishes

---

## 💾 Backup (3 AM daily)
```bash
/Users/sam/.openclaw/scripts/backup-workspace.sh
```
Only alert if fails

---

## 📋 Weekly Check (Monday 8 AM)
Check `SOPHIA-PROJECT-TRACKER.md` for progress
- 7+ days no progress: Gentle reminder
- 14+ days: Ask if pause needed
- 30+ days: Suggest priority review

---

## State Tracking
Track all checks in `memory/heartbeat-state.json`

## Quiet Mode
Late night (11 PM - 7 AM) or >12h since last message: Only urgent alerts
