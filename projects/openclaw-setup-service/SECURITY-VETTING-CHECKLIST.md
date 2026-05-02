# Security Vetting Checklist - Internal Use Only

**Purpose:** Ensure every OpenClaw setup is secure and free of malware  
**Use:** Follow this checklist for EVERY customer setup, no exceptions  
**Updated:** February 21, 2026

---

## Our Security Promise

**We guarantee customers:**
- ✅ No malicious skills from ClawHub
- ✅ Only vetted, trusted integrations
- ✅ Security hardening by default
- ✅ Ongoing guidance on safe practices

**This checklist is how we deliver on that promise.**

---

## Pre-Setup: Customer Intake

### ☐ Identify Required Integrations

During discovery call, document what customer needs:
- Email access? (Gmail, Outlook, etc.)
- Calendar? (Google Calendar, Apple Calendar)
- Messaging? (iMessage, Slack, WhatsApp)
- Industry-specific? (Aviation weather, commodity prices, etc.)
- Home automation? (HomeKit, smart devices)
- Other? (Document specifically)

### ☐ Plan Safe Implementation

For each need, choose ONLY from approved sources:
- ✅ Built-in OpenClaw tools
- ✅ Vetted CLIs (see Tier 2 list below)
- ✅ Custom SKILL.md we write
- ❌ NEVER: Random ClawHub skills

---

## During Setup: Installation Checklist

### ☐ **Step 1: Base OpenClaw Installation**

**Safe sources only:**
```bash
# Official OpenClaw install
curl -fsSL https://openclaw.ai/install.sh | sh
```

**Verify:**
- Installation script comes from openclaw.ai (official domain)
- Check release notes for security updates
- Current version: [check latest stable]

---

### ☐ **Step 2: Security Hardening**

**Firewall configuration:**
- Mac Mini: Enable macOS Firewall (System Preferences → Security & Privacy → Firewall)
- Block incoming connections by default
- Allow only necessary ports

**SSH Security (if remote access needed):**
- Use SSH keys (never passwords)
- Disable root login
- Change default SSH port (optional but recommended)
- Fail2ban or equivalent (optional for cloud setups)

**File Permissions:**
- OpenClaw config files: 600 (owner read/write only)
- API keys/tokens: Store in secure config, never in code
- No world-readable sensitive files

**Network Security:**
- If running on Mac Mini at home: Behind home router NAT (safe by default)
- If cloud VPS: Firewall rules restricting access
- Never expose OpenClaw UI to public internet without authentication

---

### ☐ **Step 3: Install Only Vetted Tools**

**Tier 1: Built-in OpenClaw Tools (Always Safe)**

These ship with OpenClaw, no additional installation:
- ✅ exec (run shell commands)
- ✅ read, write, edit (file operations)
- ✅ web_search (Brave Search API)
- ✅ web_fetch (fetch URLs, extract content)
- ✅ browser (Chrome/Edge automation)
- ✅ cron (scheduled tasks)
- ✅ message (send messages via configured channels)
- ✅ memory_search, memory_get (memory management)
- ✅ tts (text-to-speech)
- ✅ image (vision analysis)

**No additional installation needed. Use freely.**

---

**Tier 2: Vetted CLIs (Install via Homebrew/npm)**

These are established, auditable tools with good reputations:

**Email & Communication:**
- ✅ `gog` - Google Workspace CLI (from OpenClaw ecosystem)
  ```bash
  npm install -g @openclaw/gog
  ```
- ✅ `himalaya` - IMAP/SMTP email client (Rust, open source)
  ```bash
  brew install himalaya
  ```
- ✅ `imsg` - iMessage CLI (from OpenClaw ecosystem)
  ```bash
  npm install -g @openclaw/imsg
  ```

**Apple Integration:**
- ✅ `memo` - Apple Notes CLI
  ```bash
  npm install -g @openclaw/memo
  ```
- ✅ AppleScript (built into macOS)
- ✅ `shortcuts` command (macOS Shortcuts automation)

**Utilities:**
- ✅ `ffmpeg` - Video/audio processing (if needed)
  ```bash
  brew install ffmpeg
  ```
- ✅ Standard Unix tools: curl, grep, sed, awk, jq (built-in or brew)

**Before installing ANY tool:**
1. Check GitHub stars and activity (legitimate project?)
2. Read source code (any red flags?)
3. Verify Homebrew formula or npm package is official
4. Test in isolated environment first (optional but recommended)

---

**Tier 3: Custom Integrations (We Write Them)**

For industry-specific needs, write custom SKILL.md files that use:
- APIs directly (weather, aviation data, commodity prices)
- Native macOS tools (AppleScript, Shortcuts)
- Simple scripts you write and audit

**Example: Aviation Weather Skill**
```markdown
# Aviation Weather Skill

Use the built-in `web_fetch` tool to get aviation weather:

- METAR: https://aviationweather.gov/metar/data?ids=[ICAO]
- TAF: https://aviationweather.gov/taf/data?ids=[ICAO]
- NOTAMs: https://notams.aim.faa.gov/notamSearch/...

No external dependencies. No risk.
```

---

### ☐ **Step 4: API Keys & Credentials**

**Safe credential management:**

**Store API keys securely:**
- OpenClaw config files (not in code)
- File permissions: 600 (owner only)
- Never commit to version control
- Use environment variables when possible

**Minimize permissions:**
- OAuth scopes: Request only what's needed
- API keys: Use read-only when possible
- Service accounts: Least privilege principle

**Document all credentials:**
- Where stored
- What permissions granted
- How to rotate if compromised

---

### ☐ **Step 5: Test Everything**

**Before delivering to customer:**

**Functional Testing:**
- All integrations work as expected
- No errors in logs
- Scheduled tasks (cron) running correctly
- Message channels connected properly

**Security Testing:**
- No exposed ports (scan with nmap)
- File permissions correct (ls -la ~/.openclaw)
- No secrets in logs or files
- API keys working but not leaked

**Sanity Checks:**
- Can customer trigger AI accidentally? (acceptable)
- Can AI delete critical files? (should require confirmation)
- Can AI send messages without review? (depends on customer preference)

---

## Post-Setup: Customer Education

### ☐ **Teach Safe Practices**

**What to tell every customer:**

1. **"Never install skills from ClawHub without asking us first"**
   - 20% contain malware
   - We'll vet anything you want to add

2. **"If OpenClaw asks to run a command you don't understand, say no"**
   - curl | bash = danger
   - Downloading executables = danger
   - Changing system files = danger

3. **"Text us if you see anything suspicious"**
   - Unexpected prompts for credentials
   - AI suggesting to disable security
   - Strange network activity

4. **"Keep your Mac Mini updated"**
   - macOS security updates (monthly)
   - OpenClaw updates (we'll handle during support period)

---

## Ongoing: Security Monitoring

### ☐ **Monthly Security Review (During Support Period)**

**Check with customer:**
- Any new integrations requested?
- Any unusual behavior noticed?
- Any security updates needed?

**Check system:**
- OpenClaw logs for errors or suspicious activity
- macOS security updates applied?
- Credentials still working (not expired)?

---

## Red Flags: Never Do These

### ❌ **NEVER Install These:**

**From ClawHub (community marketplace):**
- ❌ Crypto/trading skills (highest malware concentration)
- ❌ Twitter/X integration skills (many are malicious)
- ❌ Skills from unknown authors
- ❌ Skills with obfuscated code
- ❌ Skills requesting excessive permissions

**Installation methods:**
- ❌ curl | bash commands (from unknown sources)
- ❌ "Just run this script" (without reading it)
- ❌ Downloading pre-compiled binaries from random sites

**Dangerous patterns:**
- ❌ Skills accessing ~/.ssh, ~/.aws, ~/.env
- ❌ Skills sending data to external servers (without disclosure)
- ❌ Skills that modify system files
- ❌ Skills using eval() or exec() carelessly

---

## If Something Goes Wrong

### ☐ **Incident Response**

**If customer reports suspicious activity:**

1. **Stop OpenClaw immediately**
   ```bash
   openclaw gateway stop
   ```

2. **Assess damage:**
   - Check recent AI actions (logs, memory files)
   - Look for unauthorized access (SSH logs, network connections)
   - Check for data exfiltration (unusual network traffic)

3. **Contain:**
   - Disconnect from network if needed
   - Rotate all API keys and credentials
   - Change passwords for connected services

4. **Investigate:**
   - What skill/integration was involved?
   - How did malware get installed?
   - What data was accessed?

5. **Remediate:**
   - Remove malicious skill/tool
   - Reinstall OpenClaw if necessary
   - Restore from backup if available

6. **Report:**
   - Notify customer honestly
   - Document lessons learned
   - Update this checklist

---

## Vetted Tools Reference

### **Current Approved List:**

**Communication:**
- gog (Google Workspace)
- imsg (iMessage)
- himalaya (email)

**Apple Ecosystem:**
- memo (Apple Notes)
- AppleScript
- Shortcuts

**Utilities:**
- ffmpeg (media)
- Standard Unix tools

**APIs (Direct, No CLI):**
- OpenWeatherMap API
- Aviation Weather (aviationweather.gov)
- Brave Search API (built-in)

### **Request for Addition:**

If customer needs something not on this list:
1. Document the need
2. Research the tool (source code, reputation)
3. Test in isolated environment
4. Add to this list if safe
5. Update customer setups as needed

---

## Version History

- **v1.0** (Feb 21, 2026): Initial checklist
- Future: Update as new threats/tools emerge

---

## Summary: Our Security Layers

**Layer 1: Prevention**
- Only use vetted tools (Tier 1, 2, or custom)
- Never install random ClawHub skills
- Security hardening by default

**Layer 2: Detection**
- Monthly security reviews during support period
- Customer education (report suspicious activity)
- Log monitoring

**Layer 3: Response**
- Incident response plan (stop, assess, contain, remediate)
- Customer communication (honest, transparent)
- Lessons learned (update checklist)

---

**This checklist is our competitive advantage.** Follow it religiously. When customers ask "How do you protect against malware?" — this is your answer.

**Never compromise security for convenience.** Our reputation depends on it.
