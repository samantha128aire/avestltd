# AvestAI — Key Decisions

## Business Model
- **100% upfront payment** for standard setups (simpler, better cash flow)
- **50/50 only** for custom projects over 10 days
- **No refunds** — "30-Day Commitment to Your Success" guarantee instead
- **Annual upgrade plan** ($200-300/year) — upgrades are revenue, not burden
- **Freeze customer versions** between upgrades — test all updates on Chance's Mac Mini first

## Technical Decisions
- **Mac Mini only** (M4 chip) — privacy/physical comfort differentiator vs cloud
- **Standard:** 16GB/256GB SSD | **Premium:** 16GB/512GB SSD
- **Smart Router v2.2.0** — prefix routing (1/O=Opus, 2/S=Sonnet, 3/H=Haiku), sticky 10 min
- **Default model: Haiku** (fast, cheap) for customer installs
- **Local embeddings** (provider: "local") for memory search — no API key needed
- **SQLite CRM** at `~/.openclaw/workspace/data/avestai.db`
- **PWA bridge** at port 9000 — uses OpenClaw's /v1/chat/completions endpoint
- **NO ClawHub skills** — security risk (ClawHavoc operation, 824+ malicious skills)
- **NO MEM0 plugin** — data leaves the device, violates privacy promise
- **Disable OpenClaw auto-updates** — manual updates only, test first

## Marketing Decisions
- **Friends First** strategy — warm network outreach, no paid ads initially
- **Facebook** as primary social channel (Chance's network)
- **X/Twitter** (@Samantha128Aire) for brand building
- **Calendly** for discovery call booking
- **Payment:** 100% upfront via standard methods

## Support Decisions
- **$100/month** support plan
- **$150/hour** ad-hoc support
- **Chrome Remote Desktop** for remote access to customer machines
- **iMessage/SMS** as primary customer communication channel

## Versioning Decisions (2026-03-02)
- Hybrid model: security fixes free, feature upgrades paid ($200-300/year)
- Track "Install Version" + "Last Updated Date" in CRM
- Test all updates on Chance's Mac Mini before touching customers
