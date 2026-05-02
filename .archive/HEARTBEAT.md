# HEARTBEAT.md

## 📈 Stock Monitoring

**IMPORTANT:** Only check stocks on **weekdays before market open** (7-9 AM CST). Market hours: 8:30 AM - 3:00 PM CST. Skip weekends and after-hours.

### TSLA - Daily Check (Weekdays, Morning Only)
**Check only Monday-Friday, 7-9 AM CST** before market opens.

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

### MSFT - Price Watch (Weekdays, Morning Only)
**Check only Monday-Friday, 7-9 AM CST** before market opens.

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
- 8:00 AM: Calendar + Birthdays + Email + TSLA + MSFT (weekdays only, pre-market)
- 2:00 PM: Email only (market is open, no stock checks)
- 7:00 PM: Email only (market is closed, no stock checks)

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

---

## 📋 Weekly Project Check-In (Monday 8 AM)

**Every Monday morning:**

1. Check `SOPHIA-PROJECT-TRACKER.md` - has there been progress in the last 7 days?
2. If NO progress for 7+ days: Gently remind Chance about next action
3. If NO progress for 14+ days: Ask if he wants to pause temporarily
4. If NO progress for 30+ days: Suggest reviewing priorities

**Reminder format (if needed):**
"Hey - just checking in on the Sophia project. Last activity was [X days ago]. Want to knock out one quick task this week, or should we pause while you focus on [current priority]?"

**Don't nag - be helpful.** If he's swamped with PropsUAV/CFI renewal/life, it's OK to pause.
