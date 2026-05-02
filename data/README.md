# AvestAI Data Directory

## avestai.db — SQLite CRM Database

**Location:** `~/.openclaw/workspace/data/avestai.db`
**Created:** 2026-03-02

### Tables
- **leads** — prospects in the sales pipeline
- **contacts** — log of every contact attempt with a lead
- **customers** — won deals / active customers
- **support** — support tickets and billing
- **revenue** — all revenue transactions

### Views
- **pipeline** — leads sorted by deal stage
- **revenue_summary** — monthly revenue by type

### Quick Queries (via exec/shell)
```bash
# Pipeline overview
~/.openclaw/workspace/scripts/crm.sh pipeline

# All leads
~/.openclaw/workspace/scripts/crm.sh leads

# Active customers
~/.openclaw/workspace/scripts/crm.sh customers

# Revenue
~/.openclaw/workspace/scripts/crm.sh revenue

# Custom SQL
~/.openclaw/workspace/scripts/crm.sh sql "SELECT * FROM leads WHERE status='discovery';"
```

### Lead Status Values
- new → contacted → discovery → proposal → won / lost / cold

### Tier Values
- basic ($695) / standard ($1,295) / premium ($1,795)

### Support Types
- none / monthly ($100/mo) / hourly ($150/hr)

### Revenue Types
- setup / support_monthly / support_hourly / upgrade
