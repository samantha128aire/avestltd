# AvestAI vs. Standard OpenClaw: Complete Comparison
**AvestAI Premium Customer Deployment — Internal Reference**

Version: 1.0 | Last Updated: 2026-03-02 | Operator: Avest Ltd

---

## Purpose

This document comprehensively lists every difference between a **standard out-of-the-box OpenClaw installation** and an **AvestAI Premium-tier customer deployment**. It is intended for:

- AvestAI engineers setting up new customer deployments
- Onboarding documentation for new AvestAI staff
- Troubleshooting reference (know what's been changed from defaults)
- Customer transparency when requested

---

## Summary Table

| Category | Standard OpenClaw | AvestAI Premium |
|----------|------------------|-----------------|
| Hardware | Any machine | Mac Mini M4 (specified) |
| Version management | Auto-update | Frozen, manually approved |
| Default model | User-set | Claude Sonnet (latest stable) |
| Smart Router | Not installed | v2.2.0, prefix routing, Haiku default |
| Memory architecture | Flat workspace | Structured folders, SQLite CRM |
| PWA | Optional, generic | Custom chat UI, Fast/Smart/Smartest |
| Redundancy | None | Dual-instance (Primary/Fallback) |
| Security posture | Open | Locked down (no ClawHub, no auto-update) |
| Skills | Community available | Vetted-only whitelist |
| Branding | Generic "AI assistant" | Samantha Aire persona |
| Channels | Configured by user | iMessage, customer allowlist |
| Support | Community/docs | White-glove, $100/mo retainer |

---

## 1. Hardware

### Standard OpenClaw
- Runs on any macOS, Linux, or Windows machine
- No hardware requirements specified beyond Node.js support
- Customer uses whatever machine they have

### AvestAI Premium
- **Required platform:** Apple Mac Mini (Apple Silicon — M4 or later)
- **Minimum storage:** 512 GB SSD (for workspace, logs, memory, SQLite CRM)
- **OS:** macOS Sequoia (15.x) or later
- **RAM:** 16 GB minimum (24 GB recommended for parallel agent workloads)
- **Network:** Always-on broadband; iMessage requires Apple ID signed in

**Why Mac Mini:** iMessage integration requires macOS + Messages.app. Apple Silicon provides excellent performance-per-watt for a machine running 24/7. The M4 Mac Mini is the reference deployment platform.

---

## 2. OpenClaw Version Management

### Standard OpenClaw
- Installed via `brew install openclaw` (or npm)
- Homebrew automatically updates on `brew upgrade` or `brew upgrade --all`
- Latest version always active
- No version pinning

### AvestAI Premium
- **Version is frozen** at the last vetted stable release
- Homebrew auto-upgrades are **disabled** for the openclaw formula
- New versions are reviewed by AvestAI engineering before deploying
- Update procedure: AvestAI engineer tests new version in staging → approves → deploys via Chrome Remote Desktop session
- **Fallback always stays one version behind primary** (safety net)
- Version documented in `openclaw.json` → `meta.lastTouchedVersion`
- Current deployed version: `2026.3.1`

**Rationale:** Auto-updates can break custom plugins, Smart Router configs, or workspace hooks. AvestAI controls the update cycle to protect customer stability.

---

## 3. Configuration Differences

### 3a. Model Defaults

| Setting | Standard | AvestAI Premium |
|---------|----------|-----------------|
| Primary model | Varies / user-set | `anthropic/claude-sonnet-4-6` (latest Sonnet) |
| Model aliases | None by default | `sonnet`, `opus`, `haiku` configured |
| Thinking mode | Off | Off (explicitly set, not just default) |
| Context pruning | None | `cache-ttl`, 1h TTL |
| Compaction | Default | `safeguard` mode |
| Max concurrent agents | Default | 4 (primary), 8 subagents |

### 3b. Ports and Auth

| Setting | Standard | AvestAI Premium |
|---------|----------|-----------------|
| Gateway port | 18789 | 18789 (primary), 18790 (fallback) |
| Auth mode | Token (default) | Token (explicitly configured, unique per deployment) |
| Gateway bind | `loopback` | `loopback` (hardened — not exposed to network) |
| Tailscale mode | Off | Off (explicitly disabled) |

### 3c. Memory Search

| Setting | Standard | AvestAI Premium |
|---------|----------|-----------------|
| Provider | None configured | `local` (local embedding search) |
| Vector DB | None | Local embeddings in workspace |

### 3d. Heartbeat

| Setting | Standard | AvestAI Premium |
|---------|----------|-----------------|
| Heartbeat | Disabled | Every 1 hour |
| Active hours | N/A | 06:00–22:00 America/Chicago |
| Purpose | N/A | Proactive memory maintenance, stock checks, project updates |

### 3e. Context Pruning & Compaction

| Setting | Standard | AvestAI Premium |
|---------|----------|-----------------|
| Context pruning | None | `cache-ttl` mode, 1h TTL |
| Compaction | Not configured | `safeguard` mode (prevents loss of important context) |

---

## 4. Smart Router Plugin

### Standard OpenClaw
- Not installed by default
- No intelligent model routing

### AvestAI Premium
- **Smart Router v2.2.0** installed as a plugin
- **Default model override:** `anthropic/claude-haiku-4-5` (fast, cheap, for simple queries)
- **Sticky timeout:** 10 minutes (maintains model choice within a session window)
- **Prefix routing:** User can prefix messages with model shortcuts (e.g., `@sonnet`, `@opus`)
- **Explain routing:** Disabled (no routing rationale shown to customer — cleaner UX)
- **Purpose:** Automatically routes simple questions to Haiku (fast, cheap), complex reasoning to Sonnet or Opus

**Cost impact:** Smart Router reduces API costs by 60–80% for typical customer usage vs. always using Sonnet.

---

## 5. Memory Architecture

### Standard OpenClaw
- Single flat workspace directory
- No structured memory system
- No CRM
- Relies on in-context memory only

### AvestAI Premium
- **Structured workspace folders:**
  ```
  workspace/
  ├── SOUL.md         — AI persona definition
  ├── USER.md         — Customer profile (name, family, businesses, etc.)
  ├── IDENTITY.md     — AI identity card (name, birthday, location)
  ├── MEMORY.md       — Long-term curated memories (main session only)
  ├── AGENTS.md       — Agent operating procedures
  ├── TOOLS.md        — Integrations and tool notes
  ├── HEARTBEAT.md    — Heartbeat schedule and tasks
  ├── memory/
  │   ├── YYYY-MM-DD.md     — Daily session logs
  │   └── projects/         — Per-project memory
  │       ├── avestai/      — goals.md, decisions.md, status.md
  │       └── <project>/    — project-specific memory
  └── data/
      └── <customer>.db     — SQLite CRM database
  ```
- **SQLite CRM:** `~/.openclaw/workspace/data/avestai.db`
  - Tables: leads, contacts, customers, revenue tracking
  - Queried by AI during heartbeats and customer interactions
- **Local embeddings:** Memory search provider set to `local` (no third-party memory service)
- **No MEM0:** AvestAI does not use MEM0 or any cloud memory service — all memory is local

---

## 6. PWA (Custom Chat Interface)

### Standard OpenClaw
- Dashboard at `http://127.0.0.1:18789/` (dev/admin UI)
- No customer-facing chat UI
- API via OpenAI-compatible endpoint at `/v1/chat/completions`

### AvestAI Premium
- **Custom PWA** (Progressive Web App) chat interface
  - Branded with customer name / AvestAI branding
  - Mobile-optimized, installable on iPhone home screen
- **Bridge server** running locally (separate port, e.g., 3001)
  - Translates PWA requests to OpenClaw gateway API
  - Handles token authentication for the customer
- **Token auth:** PWA uses its own access token (not the raw gateway token)
- **Model display names** in the PWA UI:
  - `Fast` → Claude Haiku (via Smart Router prefix)
  - `Smart` → Claude Sonnet (via Smart Router prefix)
  - `Smartest` → Claude Opus (via Smart Router prefix)
- **No technical jargon exposed** to customer — they pick Fast/Smart/Smartest, not model names

---

## 7. Redundancy (Premium Only)

### Standard OpenClaw
- Single instance
- No failover capability
- If instance crashes, manual restart required
- No documented recovery procedure

### AvestAI Premium
- **Dual-instance architecture:**
  - **Primary:** port 18789, latest stable, always running, LaunchAgent enabled
  - **Fallback:** port 18790, one version behind, stopped by default, LaunchAgent NOT loaded
- **Separate configs:** Primary and fallback have different gateway tokens, different workspace paths
- **Switching scripts:**
  - `switch-to-fallback.sh` — graceful failover (stops primary, starts fallback)
  - `switch-to-primary.sh` — graceful restore (stops fallback, restarts primary)
  - `redundancy-status.sh` — read-only health check
- **Safety rules enforced:**
  - No SIGUSR1 — always use `openclaw gateway stop` + `start`
  - No `openclaw gateway restart` command
  - Fallback plist never loaded into launchctl by default
- **LaunchAgent behavior:**
  - Primary: `RunAtLoad=true`, `KeepAlive=true` (survives reboots and crashes)
  - Fallback: `RunAtLoad=false`, `KeepAlive=false` (manual only)

---

## 8. Security

### Standard OpenClaw
- ClawHub community skills can be installed freely
- Auto-updates enabled (Homebrew)
- No explicit skill vetting
- Remote gateway restart may be possible via API
- MEM0 integration available
- No defined allowlist for channels

### AvestAI Premium
- **No ClawHub skills:** Community skill marketplace is not used. Only AvestAI-vetted skills are installed.
- **No MEM0:** No cloud-based memory services. All memory is local.
- **No auto-updates:** `brew` auto-upgrade for `openclaw` is disabled. AvestAI controls the update cycle.
- **No remote gateway restarts:** The `restart` API endpoint is intentionally disabled in config. Engineers use Chrome Remote Desktop for hands-on access.
- **iMessage allowlist:** Only explicitly approved phone numbers can message the AI. Unknown numbers are silently dropped.
- **Loopback-only binding:** Gateway is bound to `127.0.0.1` only — not exposed on the local network or internet.
- **Separate fallback token:** Fallback instance uses a different gateway token from primary.

---

## 9. Support Model

### Standard OpenClaw
- Community forum support
- GitHub issues
- Documentation at docs.openclaw.ai
- Self-service only

### AvestAI Premium
- **White-glove setup:** AvestAI engineers set up everything — customer just uses the AI
- **Post-setup support:**
  - $100/month retainer (priority support, response within 4 hours during business hours)
  - $150/hour on-demand (no retainer)
- **Remote access:** Chrome Remote Desktop (chance.ihs@gmail.com) for hands-on troubleshooting
- **Initial 30-day period:** Included in setup price, covers bugs, adjustments, training
- **Pricing tiers:**
  - Basic: $695 (standard setup, iMessage only)
  - Standard: $1,295 (+ PWA, Smart Router, custom persona)
  - Premium: $1,795 (+ redundancy, full memory architecture, CRM)
- **Setup time:** 2–4 hours on-site or via Chrome Remote Desktop

---

## 10. Branding & Persona

### Standard OpenClaw
- Generic AI assistant
- Default name depends on the model being used
- No custom persona
- No customer profile file
- Workspace is empty at install

### AvestAI Premium
- **AI name:** Samantha Aire 🧚‍♀️
- **Birthday:** January 28, 2000 (gives the AI a sense of identity)
- **Persona:** Pleasant, direct, resourceful, proactive — never corporate-drone
- **Custom workspace files:**
  - `SOUL.md` — personality, communication style, core values
  - `USER.md` — customer profile (name, family, businesses, financial goals, aviation certificates, etc.)
  - `IDENTITY.md` — AI's identity card (name, email, location, emoji, mission)
  - `MEMORY.md` — long-term curated memories (read only by main session)
  - `AGENTS.md` — agent operating procedures, memory system instructions
- **Customer-specific customization:** USER.md is fully customized per customer at setup
- **Mission alignment:** The AI is briefed on the customer's income goals and actively suggests and executes income-generating tasks

---

## 11. Skills (Tools)

### Standard OpenClaw
- Any skill can be installed from ClawHub
- No vetting process
- Community skills may have bugs, security issues, or unexpected behavior

### AvestAI Premium
- **Vetted skills only** — AvestAI tests and approves each skill before customer deployment
- **No community skills** from ClawHub
- **Currently approved skills** (as of 2026.3.1):
  - `apple-notes` — Manage Apple Notes via memo CLI
  - `apple-reminders` — Manage Apple Reminders
  - `gog` — Google Workspace (Gmail, Calendar, Drive, Contacts, Sheets, Docs)
  - `himalaya` — Email via IMAP/SMTP
  - `imsg` — iMessage/SMS via Messages.app
  - `things-mac` — Things 3 task manager
  - `weather` — Weather via wttr.in / Open-Meteo
  - `gemini` — Gemini CLI for Q&A and generation
  - `summarize` — Summarize URLs, podcasts, local files
  - `peekaboo` — macOS UI capture and automation
  - `sonoscli` — Sonos speaker control
  - `gifgrep` — GIF search and download
  - `nano-pdf` — Natural-language PDF editing
  - `video-frames` — Video frame/clip extraction via ffmpeg
  - `openai-whisper` — Local speech-to-text
  - `wacli` — WhatsApp messaging
  - `eightctl` — Eight Sleep pod control
- **Skill updates:** Skills are not auto-updated; updates are deployed by AvestAI after vetting

---

## 12. Channels

### Standard OpenClaw
- Channels enabled and configured by user
- No default allowlist
- Any sender can message the AI (if channel is enabled)
- iMessage not configured by default

### AvestAI Premium
- **iMessage:** Primary communication channel, configured at setup
  - Plugin: `imessage` (enabled)
  - `dmPolicy`: `allowlist` (only known numbers can DM the AI)
  - `allowFrom`: Customer-specific list (operator + family + trusted contacts)
  - `groupPolicy`: `allowlist` (configured to avoid accidental group chat exposure)
- **Customer allowlist:** AvestAI configures the list of approved phone numbers during setup
- **Channel security:** Unapproved numbers are silently dropped — no "unauthorized" response leak
- **Samantha's iPhone number:** (936) 577-2048 — a real mobile number with iMessage active, giving the AI a stable identity in contacts
- **TTS:** Configured with Microsoft Edge TTS, `en-US-AvaNeural` voice
  - Format: `audio-24khz-48kbitrate-mono-mp3`
  - Auto-TTS: Off (customer must request voice response)

---

## 13. Integrations (Customer-Specific)

### Standard OpenClaw
- No integrations pre-configured
- User sets up everything manually

### AvestAI Premium (Chance's Deployment Reference)
- **Google Workspace:** `samantha128aire@gmail.com` → all Google services (Gmail, Calendar, Drive, etc.)
- **Zoom:** Business phone (936) 444-2869, meeting creation/management
- **Calendly:** Discovery call scheduling at `/samantha128aire/avestai-discovery-call`
- **Business email:** `samantha@avestltd.com` (forwards to Gmail, replies from professional address)
- **Financial:** TSLA daily monitoring pre-market 7–9 AM on weekdays
- **Backup:** Daily 3 AM backup to Google Drive via `/Users/sam/.openclaw/scripts/backup-workspace.sh`
- **Web search:** Brave Search API (configured with customer API key)

*Note: Integrations are customer-specific and documented in that customer's `TOOLS.md`.*

---

## Quick Reference: Files Changed from Default

| File | Standard State | AvestAI State |
|------|---------------|---------------|
| `~/.openclaw/openclaw.json` | Minimal (wizard-generated) | Fully configured (model, smart router, heartbeat, channels, plugins) |
| `~/.openclaw/openclaw-fallback.json` | Does not exist | Created with port 18790, separate token |
| `~/Library/LaunchAgents/ai.openclaw.gateway.plist` | Basic | Enhanced with env vars, service metadata |
| `~/Library/LaunchAgents/ai.openclaw.gateway.fallback.plist` | Does not exist | Created (NOT loaded) |
| `~/.openclaw/workspace/SOUL.md` | Does not exist | Full persona definition |
| `~/.openclaw/workspace/USER.md` | Does not exist | Full customer profile |
| `~/.openclaw/workspace/IDENTITY.md` | Does not exist | AI identity card |
| `~/.openclaw/workspace/MEMORY.md` | Does not exist | Curated long-term memory |
| `~/.openclaw/workspace/AGENTS.md` | Does not exist | Agent operating procedures |
| `~/.openclaw/workspace/TOOLS.md` | Does not exist | Integration reference |
| `~/.openclaw/workspace/HEARTBEAT.md` | Does not exist | Heartbeat schedule |
| `~/.openclaw/workspace/data/<customer>.db` | Does not exist | SQLite CRM |
| `~/.openclaw/workspace-fallback/` | Does not exist | Fallback workspace with SOUL.md, AGENTS.md |
| `~/.openclaw/scripts/switch-to-fallback.sh` | Does not exist | Failover script (chmod +x) |
| `~/.openclaw/scripts/switch-to-primary.sh` | Does not exist | Restore script (chmod +x) |
| `~/.openclaw/scripts/redundancy-status.sh` | Does not exist | Status check script (chmod +x) |
| `~/.openclaw/scripts/backup-workspace.sh` | Does not exist | Daily backup script |

---

## Deployment Checklist (Premium Tier)

Use this during new customer setup:

- [ ] Mac Mini M4 (Apple Silicon) with 512 GB+ SSD
- [ ] macOS Sequoia, Apple ID signed in, Messages.app configured
- [ ] Node.js via Homebrew, OpenClaw installed at approved version
- [ ] `openclaw.json` — full config (model, smart router, heartbeat, channels, auth token)
- [ ] `openclaw-fallback.json` — fallback config (port 18790, different token)
- [ ] `workspace/SOUL.md` — Samantha Aire persona
- [ ] `workspace/USER.md` — customer profile (fully customized)
- [ ] `workspace/IDENTITY.md` — AI identity card
- [ ] `workspace/MEMORY.md` — initial empty or seeded memory
- [ ] `workspace/AGENTS.md` — agent operating procedures
- [ ] `workspace/TOOLS.md` — integration reference
- [ ] `workspace/HEARTBEAT.md` — heartbeat schedule
- [ ] `data/<customer>.db` — SQLite CRM (create initial schema)
- [ ] `workspace-fallback/SOUL.md` — fallback soul
- [ ] `workspace-fallback/AGENTS.md` — fallback agents
- [ ] LaunchAgent primary plist — loaded and verified
- [ ] LaunchAgent fallback plist — present but NOT loaded
- [ ] Switching scripts — created and `chmod +x`
- [ ] All vetted skills installed and tested
- [ ] iMessage channel configured with customer's allowlist
- [ ] Google Workspace `gog` authenticated
- [ ] Brave Search API key configured
- [ ] PWA bridge server set up and tested
- [ ] Chrome Remote Desktop configured for AvestAI access
- [ ] `redundancy-status.sh` shows `✓ NORMAL`
- [ ] Customer walkthrough completed (how to use iMessage AI, PWA, Fast/Smart/Smartest)
- [ ] 30-day support window documented and communicated

---

*This document is for AvestAI internal use only. © Avest Ltd 2026.*
