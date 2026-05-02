# OpenClaw Dual-Instance Redundancy Guide
**AvestAI Premium Deployment — Internal Operations Document**

Version: 1.0 | Last Updated: 2026-03-02 | Applies To: Premium Tier Customers

---

## Overview

AvestAI Premium deployments include a **dual-instance redundancy architecture** for OpenClaw. This provides a manual failover capability when the primary instance has issues, ensuring minimal downtime for the customer.

**Architecture summary:**

| Instance | Port | Version | State | Purpose |
|----------|------|---------|-------|---------|
| Primary | 18789 | Latest stable | Always running | Normal operations |
| Fallback | 18790 | One version behind | Stopped (standby) | Emergency backup |

The fallback is **not** a load balancer and does **not** run in parallel with the primary. It is a cold standby activated only during emergencies.

---

## Files Created by This Architecture

### Config Files
| File | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Primary config (port 18789) — **DO NOT MODIFY** |
| `~/.openclaw/openclaw-fallback.json` | Fallback config (port 18790, separate token) |

### Workspaces
| Directory | Purpose |
|-----------|---------|
| `~/.openclaw/workspace/` | Primary workspace (all customer data lives here) |
| `~/.openclaw/workspace-fallback/` | Fallback workspace (minimal, separate) |

### LaunchAgent Plists
| File | State | Purpose |
|------|-------|---------|
| `~/Library/LaunchAgents/ai.openclaw.gateway.plist` | Loaded + enabled | Primary instance (auto-starts on login) |
| `~/Library/LaunchAgents/ai.openclaw.gateway.fallback.plist` | **NOT loaded** | Template only — managed by scripts |

### Scripts
| Script | Purpose |
|--------|---------|
| `~/.openclaw/scripts/switch-to-fallback.sh` | Stop primary, start fallback |
| `~/.openclaw/scripts/switch-to-primary.sh` | Stop fallback, restart primary |
| `~/.openclaw/scripts/redundancy-status.sh` | Show active instance, ports, health |

---

## Normal Operations

The customer's Mac Mini runs the primary instance on port 18789 at all times. The fallback is stopped and the fallback LaunchAgent plist is **not loaded** into launchctl.

To verify normal state:
```bash
~/.openclaw/scripts/redundancy-status.sh
```

Expected output: `✓ NORMAL — Primary active, fallback on standby`

---

## Switching to Fallback (Emergency Procedure)

Use this when the primary instance is crashing, unresponsive, or needs maintenance.

### Step 1: Diagnose the primary first
```bash
openclaw gateway status
tail -50 ~/.openclaw/logs/gateway.err.log
```

### Step 2: Run the switch script
```bash
~/.openclaw/scripts/switch-to-fallback.sh
```

This script:
1. Stops the primary instance via `openclaw gateway stop`
2. Verifies port 18789 is free
3. Loads the fallback LaunchAgent temporarily
4. Waits for fallback to start on port 18790
5. Confirms success

### Step 3: Notify the customer
Inform the customer that:
- The AI assistant is now running from the fallback instance
- The fallback is one version behind — minor differences possible
- The fallback gateway token is different (update any integrations if needed)
- You are investigating the primary issue

### Step 4: Verify fallback is working
```bash
~/.openclaw/scripts/redundancy-status.sh
curl -s http://127.0.0.1:18790/ | head -5
```

---

## Restoring Primary (After Maintenance)

Once the primary issue is resolved:

### Step 1: Investigate and fix the primary
Common issues:
- Port conflict: `lsof -iTCP:18789`
- Config corruption: validate JSON with `jq . ~/.openclaw/openclaw.json`
- Process crash loop: check `~/.openclaw/logs/gateway.err.log`
- Version bug: update OpenClaw via `brew upgrade openclaw` (then update service version in plist)

### Step 2: Run the restore script
```bash
~/.openclaw/scripts/switch-to-primary.sh
```

This script:
1. Stops the fallback instance (unloads fallback LaunchAgent)
2. Verifies port 18790 is free
3. Starts the primary via `openclaw gateway start`
4. Confirms success on port 18789

### Step 3: Verify normal state
```bash
~/.openclaw/scripts/redundancy-status.sh
openclaw gateway status
```

---

## Updating the Fallback Instance

The fallback should always be **one version behind** the primary. Update it after the primary has been on the new version for at least 2 weeks without issues.

### Fallback Update Procedure

1. **Verify primary stability** — at least 2 weeks on the new version
2. **Document the current fallback version** from `openclaw-fallback.json`
3. **Update fallback config** — change `lastTouchedVersion` in `openclaw-fallback.json`
4. **Update fallback plist** — change `OPENCLAW_SERVICE_VERSION` and `Comment` string
5. **Test** — briefly run `switch-to-fallback.sh` in a maintenance window to verify fallback starts

> **Note:** The fallback uses the same OpenClaw binary as the primary (installed via brew). 
> The "version behind" refers to the **config version** — the exact binary version behavior 
> depends on what's installed. If strict binary version separation is needed, contact AvestAI 
> engineering for a custom Node.js version pinning setup.

---

## Critical Safety Rules

### ⛔ NEVER do these things:
1. **NEVER use `kill -USR1 <pid>` or SIGUSR1** — this causes OpenClaw to crash
2. **NEVER run `openclaw gateway restart`** — this is equivalent to SIGUSR1 internally
3. **NEVER load the fallback plist with `launchctl load` manually** — use the scripts
4. **NEVER run both instances simultaneously** — they share iMessage and other channels
5. **NEVER modify `~/.openclaw/openclaw.json`** (primary config) while troubleshooting

### ✅ ALWAYS do these things:
1. Use `openclaw gateway stop` + `openclaw gateway start` for all restarts
2. Use the provided switching scripts for failover
3. Check `redundancy-status.sh` before and after any change
4. Notify the customer before switching instances

---

## Gateway Tokens

The two instances use **different gateway tokens**:

| Instance | Token Location |
|----------|---------------|
| Primary | `~/.openclaw/openclaw.json` → `gateway.auth.token` |
| Fallback | `~/.openclaw/openclaw-fallback.json` → `gateway.auth.token` |

If the customer has any integrations (PWA, bridge server, custom tools) that use the gateway token, they will need to be updated when switching to the fallback. Document the customer's token consumers during setup.

---

## Logs

| Log File | Purpose |
|----------|---------|
| `~/.openclaw/logs/gateway.log` | Primary stdout |
| `~/.openclaw/logs/gateway.err.log` | Primary stderr (errors) |
| `~/.openclaw/logs/gateway-fallback.log` | Fallback stdout |
| `~/.openclaw/logs/gateway-fallback.err.log` | Fallback stderr (errors) |
| `/tmp/openclaw/openclaw-YYYY-MM-DD.log` | Primary runtime session logs |

---

## Troubleshooting Reference

### Primary won't start after `switch-to-primary.sh`
```bash
# Check for port conflicts
lsof -iTCP:18789

# Validate primary config JSON
jq . ~/.openclaw/openclaw.json

# Check the LaunchAgent plist is still valid
plutil -lint ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Check error logs
tail -100 ~/.openclaw/logs/gateway.err.log

# Manual start attempt (bypasses launchd)
openclaw gateway start
```

### Fallback won't start after `switch-to-fallback.sh`
```bash
# Check for port conflicts
lsof -iTCP:18790

# Validate fallback config JSON
jq . ~/.openclaw/openclaw-fallback.json

# Check fallback plist
plutil -lint ~/Library/LaunchAgents/ai.openclaw.gateway.fallback.plist

# Check fallback error logs
tail -100 ~/.openclaw/logs/gateway-fallback.err.log
```

### Both instances are running simultaneously
```bash
# Restore to primary (stops fallback, keeps primary)
~/.openclaw/scripts/switch-to-primary.sh
```

### Status script shows "DOWN — Neither instance running"
```bash
# Start primary immediately
openclaw gateway start

# If that fails, try fallback
~/.openclaw/scripts/switch-to-fallback.sh
```

---

## Architecture Diagram

```
Customer Mac Mini (Apple Silicon, macOS)
│
├─ LaunchAgent: ai.openclaw.gateway.plist (LOADED, auto-start)
│   └─ OpenClaw Primary (port 18789, latest stable)
│       ├─ Config: ~/.openclaw/openclaw.json
│       ├─ Workspace: ~/.openclaw/workspace/
│       └─ Token: primary token (dc96...)
│
└─ LaunchAgent: ai.openclaw.gateway.fallback.plist (NOT LOADED - template)
    └─ OpenClaw Fallback (port 18790, N-1 version) — STANDBY
        ├─ Config: ~/.openclaw/openclaw-fallback.json
        ├─ Workspace: ~/.openclaw/workspace-fallback/
        └─ Token: fallback token (6ede...) — DIFFERENT from primary

Switching Scripts:
  switch-to-fallback.sh   → Primary ──stop──▶ Fallback ──start──▶
  switch-to-primary.sh    → Fallback ──stop──▶ Primary ──start──▶
  redundancy-status.sh    → Read-only health check
```

---

## Contact & Support

- **AvestAI Support:** samantha@avestltd.com
- **Phone:** (936) 444-2869
- **Remote Access:** Chrome Remote Desktop (chance.ihs@gmail.com)
- **Support SLA:** $100/month retainer or $150/hour

For urgent issues outside business hours, send an iMessage to the AI assistant directly — it monitors 24/7.

---

*This document is for AvestAI internal use and Premium customer deployments only.*
