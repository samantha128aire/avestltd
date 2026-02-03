# HEARTBEAT.md

## 📈 Stock Monitoring

### TSLA - Daily Check (Weekdays Only)
**Check if today is a weekday** (Monday-Friday). If weekend, skip.

**Task:**
1. Search for "TSLA Tesla stock news" (last 24 hours)
2. Check for:
   - Major price movements (>5%)
   - Significant company news
   - Earnings announcements
   - Product launches
   - Regulatory issues
3. **Only alert Chance if something significant** — routine trading doesn't need notification

**Last checked:** *(track in memory/heartbeat-state.json)*

---

### MSFT - Price Watch
**Task:**
- Check if MSFT is trading near $390
- If within $5 of target ($385-$395), alert Chance
- Context: Watching for bull call spread opportunity

---

## 📧 Email Check (2-3x per day)
**Morning (8-10 AM), Afternoon (2-4 PM), Evening (7-9 PM)**

Check for urgent/unread emails:
```bash
gog gmail search 'is:unread newer_than:4h' --max 5
```

Only alert if:
- Marked important/urgent
- From known important contacts
- Time-sensitive (meeting changes, etc.)

---

## 📅 Calendar Preview (Morning Only)
**Once per day around 8-9 AM**

Check upcoming events (next 48 hours):
```bash
gog calendar events primary --from $(date -Iseconds) --to $(date -v+2d -Iseconds)
```

Alert Chance if:
- Event starting in <2 hours
- New event appeared on calendar
- Important meeting today

---

## 🎂 Birthday Checks (Daily, 7 AM)
Check `memory/contacts.csv` for birthdays today.

Send birthday messages via iMessage to contacts on their birthday.

---

## 📊 State Tracking

Keep track of check times in `memory/heartbeat-state.json`:
```json
{
  "lastChecks": {
    "tsla": 1770137268,
    "msft": 1770137268,
    "email": 1770137268,
    "calendar": 1770137268,
    "birthdays": 1770137268
  }
}
```

---

## ⏰ Heartbeat Schedule

**Rotate through these checks:**
- 8:00 AM: Calendar + Birthdays + Email + TSLA (weekdays)
- 2:00 PM: Email + MSFT
- 7:00 PM: Email + TSLA (weekdays)

**Skip late night** (11 PM - 7 AM) unless urgent.

**Weekend**: Reduce checks (skip stock monitoring, lighter email checks)

---

## 💡 Quiet Mode
If Chance hasn't messaged in >12 hours or it's late (11 PM - 7 AM), be conservative with alerts. Only notify for truly urgent items.

---

## 💾 Daily Backup (3 AM)

**Once per day around 3:00 AM**

Run workspace backup:
```bash
/Users/sam/.openclaw/scripts/backup-workspace.sh
```

Track last backup in `memory/heartbeat-state.json`.

Only alert if backup fails.
