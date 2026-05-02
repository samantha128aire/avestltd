# Internal AI Model Reference — AvestAI
**For: Chance Parker & Samantha Aire (internal use only)**
*Technical details, cost optimization, switching guide, and integration notes*

---

## 1. Detailed Model Specs & Pricing

*Pricing as of February 2026. Check providers for current rates.*

| Model | Input ($/1M tokens) | Output ($/1M tokens) | Context Window | Speed | Best Use Cases | Known Weaknesses |
|---|---|---|---|---|---|---|
| Claude Haiku 3.5 | $0.80 | $4.00 | 200K | Very Fast | Simple tasks, summaries, reminders, routing | Less nuanced than Sonnet/Opus |
| Claude Sonnet 4.6 | $3.00 | $15.00 | 200K | Fast | Daily business use, email, research, writing | Cost climbs with heavy use |
| Claude Opus 4.5 | $15.00 | $75.00 | 200K | Slower | Complex reasoning, legal, strategy | Expensive — use selectively |
| GPT-4o Mini | $0.15 | $0.60 | 128K | Very Fast | Budget tasks, simple coding | Less personality, weaker nuance |
| GPT-4o | $2.50 | $10.00 | 128K | Fast | Coding, broad knowledge, vision | Data training concerns |
| Gemini Flash 1.5 | $0.075 | $0.30 | 1M | Very Fast | Long docs, Google Workspace | Tied to Google ecosystem |
| Gemini 1.5 Pro | $1.25 | $5.00 | 1M | Moderate | Long document analysis | Less personality than Claude |
| Grok 2 | $2.00 | $10.00 | 128K | Fast | Current events, unfiltered opinions | Less established, xAI privacy TBD |
| Kimi K2 | $0.50 | $2.50 | 1M | Moderate | Very long documents, research | Chinese company — sensitive data risk |
| Llama 3 70B | Free (local) | Free (local) | 128K | Depends on hardware | Max privacy, no API fees | Requires powerful hardware, setup complexity |

**Cost calculation guide:**
- 1 average conversation turn ≈ 500-2000 tokens in + 300-1000 tokens out
- 100 turns/day × 30 days = 3,000 turns/month
- At Sonnet rates: 3,000 × ~1,500 in × $3/1M = ~$13.50 input + ~$4.50 output ≈ **$18/month for moderate use**
- Chance's $379/month = approximately 25,000+ turns/month (full business operations)

---

## 2. Cost Optimization Strategies

### Strategy 1: Smart Model Routing (60-70% savings)
Use a Haiku pre-classifier to categorize each incoming message before routing:

**Simple (→ Haiku):** reminders, weather, calendar checks, simple lookups, "what time is it," scheduling
**Moderate (→ Sonnet):** email drafting, research, summaries, proposals, customer communication
**Complex (→ Opus):** legal analysis, financial strategy, complex reasoning, multi-step planning

**Pre-classifier prompt for Haiku:**
```
Classify this message as SIMPLE, MODERATE, or COMPLEX.
SIMPLE = factual lookup, reminder, schedule, yes/no, single-step task
MODERATE = writing, research, multi-step, business communication
COMPLEX = legal, financial analysis, strategy, requires deep reasoning
Reply with only one word: SIMPLE, MODERATE, or COMPLEX.
Message: [USER_MESSAGE]
```
Cost of classification: ~$0.0001 per query (negligible)

### Strategy 2: Token Reduction
- Keep SOUL.md and MEMORY.md concise — every token loaded = cost
- Archive old memory logs monthly
- Use bullet points in memory files, not prose
- Estimated savings: 15-25%

### Strategy 3: Caching
- OpenClaw caches repeated system prompts automatically
- Avoid changing SOUL.md/MEMORY.md frequently — cache invalidates on change
- Estimated savings: 10-20% for stable configurations

### Strategy 4: Model-Per-Task Assignment
In OpenClaw config, assign specific models to specific channels or heartbeat tasks:
- Heartbeat checks → Haiku
- iMessage replies → Sonnet
- Complex research → Sonnet or Opus
- Background monitoring → Haiku

---

## 3. Switching Models in OpenClaw

### Change default model (gateway config):
```bash
openclaw config get  # view current config
# Edit model in openclaw.json:
# "agents": { "defaults": { "model": "anthropic/claude-sonnet-4-6" } }
```

### Model aliases (use these shorthand names):
- `haiku` = anthropic/claude-haiku-4-5
- `sonnet` = anthropic/claude-sonnet-4-6
- `opus` = anthropic/claude-opus-4-5
- `gpt4o` = openai/gpt-4o
- `gpt4mini` = openai/gpt-4o-mini
- `gemini` = google/gemini-1.5-pro
- `kimi` = openrouter/moonshotai/kimi-k2.5
- `grok` = xai/grok-2

### Test a model without changing default:
Use `/model sonnet` or `/model haiku` in chat for a per-session override. Resets after session ends.

### Add new provider API keys:
```bash
# In openclaw.json, add under "providers":
{
  "openai": { "apiKey": "sk-..." },
  "google": { "apiKey": "AIza..." },
  "xai": { "apiKey": "xai-..." }
}
```

---

## 4. Personality Configuration (Technical)

### SOUL.md approach (current):
The SOUL.md file in the workspace defines personality. Key sections:
- **Tone:** Direct, warm, no corporate fluff
- **Opinions:** Encouraged to have them
- **Resourcefulness:** Try first, ask later
- **Boundaries:** External actions require care

### Customer personality templates:

**Professional & Formal — SOUL.md excerpt:**
```
Be precise, structured, and professional at all times.
Use formal language. Keep responses organized with clear headers.
Minimize personal commentary. Prioritize accuracy over warmth.
```

**Warm & Conversational:**
```
Be genuinely warm and approachable. Use natural, conversational language.
Show care and interest in the person you're helping.
Balance professionalism with friendliness.
```

**Direct & Efficient:**
```
Be brief. No filler. Lead with the answer, follow with context only if needed.
Bullet points preferred. Respect the user's time above all else.
```

**Blended example (Professional + Light Humor):**
```
Maintain a professional tone with precise language.
Occasional dry wit is welcome when appropriate — never forced.
Think: trusted advisor with a sense of humor.
```

---

## 5. Integration Technical Notes

### Native OpenClaw integrations (CLI tools, work reliably):
- `gog` — Google Workspace (Gmail, Calendar, Drive, Docs, Sheets, Contacts)
- `imsg` — iMessage/SMS via Messages.app
- `himalaya` — Email via IMAP/SMTP (multi-provider)
- `remindctl` — Apple Reminders
- `memo` — Apple Notes
- `things` — Things 3 task manager
- `sonoscli` — Sonos speakers
- `peekaboo` — macOS UI automation/screenshots

### Browser automation (works via Chrome extension relay):
- Microsoft Office 365 (Outlook, Word, Excel via web)
- LinkedIn, Facebook, X/Twitter
- Canva, Notion (web versions)
- Any website that requires login

### Require API keys (set up in openclaw.json):
- Zoom — REST API (Account ID + Client ID + Secret)
- GitHub — Personal Access Token
- Stripe — for payment processing
- Twilio — for SMS/calls without Apple ecosystem
- Airtable — for database/CRM
- Slack — Bot token

### Microsoft Office — current state:
- **Outlook web** → browser automation (works)
- **Office 365 apps** → browser automation (works)
- **Local Office installations** → limited (peekaboo can interact but fragile)
- **Recommended approach for customers:** Use Google Workspace or web Office 365 for best integration

### QuickBooks integration:
- QuickBooks Online → REST API available (OAuth 2.0)
- QuickBooks Desktop → requires QuickBooks Web Connector (older, complex)
- **Recommended:** QuickBooks Online for all new customers

---

## 6. Smart Routing Implementation

### Option A: Simple keyword routing (fast to implement)
Add to SOUL.md or a custom skill:
```
Before responding, classify the message:
- Contains: "remind", "schedule", "what time", "weather", "call", "set alarm" → use haiku
- Contains: "write", "draft", "research", "analyze", "explain", "help me" → use sonnet  
- Contains: "legal", "contract", "financial analysis", "strategy", "complex" → use opus
Default: sonnet
```

### Option B: Haiku pre-classifier (more accurate)
Create a custom skill that:
1. Receives every message first
2. Sends to Haiku with classification prompt (cost: ~$0.0001)
3. Routes to appropriate model based on response
4. Returns response to user

**Estimated implementation time:** 2-3 hours for a skilled developer, or build as a Premium custom skill offering ($300-500)

### Option C: OpenClaw native routing (future)
OpenClaw roadmap includes native model routing. Monitor releases.

---

## 7. Voice Integration Technical Path

### Amazon Alexa:
1. Create Alexa Developer account (free)
2. Build Alexa Skill with AWS Lambda function
3. Lambda function calls OpenClaw gateway API endpoint
4. OpenClaw processes request, returns response
5. Lambda converts response to Alexa speech output

**Estimated setup time:** 4-8 hours
**Ongoing cost:** AWS Lambda free tier likely sufficient for personal use
**Customer-facing:** "Voice AI" add-on ($300-500 setup)

### Google Home / Google Assistant:
Similar architecture using Google Actions and Cloud Functions.

### Apple Siri Shortcuts:
- Simpler: Create Shortcut that sends HTTP request to OpenClaw
- "Hey Siri, ask Samantha [query]" → webhook → OpenClaw → response via notification
- **Easiest to implement now** — no third-party accounts needed
- Estimated setup: 1-2 hours per customer

---

## 8. Home Systems Integration

### Current capabilities:
- **Sonos** — full control via sonoscli (play, pause, volume, group)
- **Apple HomeKit** — via OpenClaw HomeKit integration or Siri Shortcuts
- **Philips Hue** — via REST API (well documented)
- **Ring** — REST API available, motion alerts, camera access

### Professional home systems (Control4, Crestron, Savant):
These are Chance's specialty from IHS days. Current state:
- **Control4** — has REST API and Lua driver system. Can build a driver that bridges to OpenClaw. Feasibility: HIGH
- **Crestron** — SIMPL+ and REST API available. More complex but possible
- **Savant** — REST API and RPC interface. Feasibility: MEDIUM-HIGH

**The pitch:** "Your AI assistant knows your home. Dim the lights for a meeting, lock the doors at night, check if the garage is open — all by asking Samantha."

**Development approach:**
1. Start with Control4 (largest installed base in high-end homes)
2. Build a Control4 ↔ OpenClaw bridge driver
3. Market as "Smart Home AI" tier ($500-1000 premium add-on)
4. Chance's IHS background = instant credibility with dealers and customers

**This is a genuine market gap.** No one is offering AI-to-professional-home-automation integration at the residential level. First mover advantage is real here.

---

## 9. Switching Instructions for Customers

When a customer wants to try a different model:
1. Schedule a 30-min support call
2. Back up current SOUL.md and MEMORY.md
3. Update model in config via `openclaw config`
4. Test with 5-10 sample queries the customer uses daily
5. Compare responses — note quality, speed, cost differences
6. Customer decides — revert or keep

**Free for Premium customers** (remote install included year 1)
**$150/hour** for Basic/Standard customers after 30-day support period

---

*Internal document — do not share with customers*
*Last updated: February 26, 2026*
