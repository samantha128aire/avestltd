# AvestAI Smart Model Router
### Automatic AI Cost Optimization — Premium Feature

---

## What It Does

Every message your AI receives is automatically routed to the right model before it responds. Simple questions go to a fast, cheap model. Complex analysis goes to the most capable model. Everything in between lands in the middle.

You never think about it. It just works.

---

## The Three Tiers

| Tier | Model | Cost | Best For |
|------|-------|------|----------|
| ⚡ **Fast** | Claude Haiku | ~$0.001/message | Simple questions, reminders, scheduling, translations, short replies |
| 🧠 **Smart** | Claude Sonnet | ~$0.01/message | Writing, summaries, explanations, emails, research |
| 🔬 **Deep** | Claude Opus | ~$0.075/message | Analysis, legal review, complex strategy, code, detailed reports |

---

## How It Decides

**Fast tier triggers on:**
- Short messages (4 words or fewer)
- Keywords: "what is", "define", "translate", "schedule", "remind me", "weather", "thanks", "ok", "cancel", "search for", "find", "open"...

**Deep tier triggers on:**
- Keywords: "analyze", "evaluate", "strategy", "legal", "contract", "debug", "refactor", "architecture", "financial model", "research paper", "write a report", "detailed plan"...
- Very long prompts (150+ words)

**Smart tier** handles everything in between — the majority of day-to-day work.

---

## Real Savings Example

Without routing (all Sonnet):
- 100 messages/day × $0.01 = **$1.00/day → ~$30/month**

With Smart Routing (estimated mix: 40% Fast, 50% Smart, 10% Deep):
- 40 × $0.001 = $0.04
- 50 × $0.010 = $0.50
- 10 × $0.075 = $0.75
- **Total: $1.29/day → ~$18/month** ← 40% savings

For heavier users the savings compound significantly.

---

## Installation

The plugin lives at:
```
~/.openclaw/extensions/smart-router.ts
~/.openclaw/extensions/openclaw.plugin.json
```

It loads automatically when OpenClaw starts. No configuration needed out of the box.

### Optional Configuration (`openclaw.json`)

```json
"plugins": {
  "entries": {
    "smart-router": {
      "enabled": true,
      "config": {
        "fastModel": "anthropic/claude-haiku-4-5",
        "smartModel": "anthropic/claude-sonnet-4-6",
        "deepModel": "anthropic/claude-opus-4-6",
        "explainRouting": false
      }
    }
  }
}
```

Set `explainRouting: true` to see which model was chosen for each message (logged to gateway console — useful for tuning).

---

## Pricing (AvestAI Offering)

| Package | Price |
|---------|-------|
| **Included with Premium** ($1,795 setup) | ✅ Free |
| **Add-on for Standard** ($1,295 setup) | +$200 one-time |
| **Standalone install** (existing customer) | $200 one-time |

---

## Verify It's Running

```bash
openclaw plugins info smart-router
```

Should show `Status: loaded` with all three model tiers listed.

---

*AvestAI Smart Model Router v1.0.0 — Built February 26, 2026*
