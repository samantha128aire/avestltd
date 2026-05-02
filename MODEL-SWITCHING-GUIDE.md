# Model Switching Guide

## Current Default
**Claude Sonnet 4.6** (Anthropic) — balanced performance, best reasoning, 1M context window (beta)

---

## How to Switch Models from Terminal

### ⚠️ Important: Two-Step Process
The one-liner with `&&` doesn't always restart properly. Use **two separate commands**:

```bash
# Step 1: Set the model
openclaw config set agents.defaults.model.primary "MODEL_ID_HERE"

# Step 2: Restart the gateway
openclaw gateway restart
```

---

## Available Models

### **Claude Models (Anthropic)** — Direct, no OpenRouter needed

**Haiku (Fast/Cheap — $1/$5 per 1M tokens)**
```bash
openclaw config set agents.defaults.model.primary "anthropic/claude-haiku-4-5"
openclaw gateway restart
```

**Sonnet 4.5 (Legacy — $3/$15 per 1M tokens)**
```bash
openclaw config set agents.defaults.model.primary "anthropic/claude-sonnet-4-5"
openclaw gateway restart
```

**Sonnet 4.6 (Latest — $3/$15 per 1M tokens)** ⭐ Current Default
```bash
openclaw config set agents.defaults.model.primary "anthropic/claude-sonnet-4-6"
openclaw gateway restart
```

**Opus (Premium — $5/$25 per 1M tokens)**
```bash
openclaw config set agents.defaults.model.primary "anthropic/claude-opus-4-5"
openclaw gateway restart
```

---

### **OpenRouter Models** — Requires OpenRouter API key (already configured)

**GPT-4o (OpenAI — $5/? per 1M tokens)**
```bash
openclaw config set agents.defaults.model.primary "openrouter/openai/gpt-4o"
openclaw gateway restart
```

**GPT-4o Mini (OpenAI — $0.15/$0.60 per 1M tokens)** — Cheapest OpenAI
```bash
openclaw config set agents.defaults.model.primary "openrouter/openai/gpt-4o-mini"
openclaw gateway restart
```

**Gemini 2.0 Flash (Google — $0.50/$3 per 1M tokens)**
```bash
openclaw config set agents.defaults.model.primary "openrouter/google/gemini-2.0-flash-exp"
openclaw gateway restart
```

**Gemini 1.5 Pro (Google — $2/$12 per 1M tokens)**
```bash
openclaw config set agents.defaults.model.primary "openrouter/google/gemini-pro-1.5"
openclaw gateway restart
```

**Grok 2 (xAI — $0.20/$0.50 per 1M tokens)** — Cheapest major model
```bash
openclaw config set agents.defaults.model.primary "openrouter/x-ai/grok-2-1212"
openclaw gateway restart
```

---

## Check Current Model

```bash
openclaw config get agents.defaults.model.primary
```

---

## Notes

- **OpenRouter** lets you access multiple AI providers with one API key
- **Pricing** is per 1M tokens (input/output)
- **Haiku** is best for routine tasks, heartbeats, quick replies
- **Sonnet** is the sweet spot for most work
- **Opus** is for complex reasoning, heavy analysis
- **GPT-4o** is what most customers recognize ("ChatGPT")
- **Gemini** is a solid Google alternative
- **Grok** is the cheapest but politically polarizing (Elon's xAI)

---

## If Something Breaks

**Quick reset to default:**
```bash
openclaw config set agents.defaults.model.primary "anthropic/claude-sonnet-4-6"
openclaw gateway restart
```

**Check if the gateway is running:**
```bash
openclaw gateway status
```

**View the full config:**
```bash
openclaw config get
```

---

## Model Switching Philosophy for AvestAI Customers

- **Default:** Sonnet (balanced, trusted)
- **Budget-conscious:** Haiku or Gemini Flash
- **"I want ChatGPT":** GPT-4o
- **Google Workspace users:** Gemini
- **Maximum reasoning:** Opus
- **Experimental/cheap:** Grok

Let customers pick their preferred provider during setup — brand loyalty matters.
