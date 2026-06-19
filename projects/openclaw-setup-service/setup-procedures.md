# OpenClaw Setup Service - Internal Procedures

**Version 1.0 | Confidential**

---

## Pre-Setup Checklist

### Order Processing
- [ ] Customer intake form received and reviewed
- [ ] Payment processed ($1,295 + tax OR $695 for customer hardware)
- [ ] Hardware confirmed (new Mac Mini purchased OR customer unit received)
- [ ] Customer's Mac Mini inspected (if applicable): serial number logged, condition documented
- [ ] Setup assigned to technician
- [ ] Estimated completion date communicated to customer
- [ ] Remote access credentials prepared

---

## Hardware Preparation

### New Mac Mini (Purchased from Us)
- [ ] Unbox and inspect Mac Mini
- [ ] Document serial number in customer file
- [ ] Verify model matches order (Mac Mini M4)
- [ ] Test power-on and initial boot
- [ ] Connect to internet (Ethernet preferred for setup)
- [ ] Run Apple Diagnostics (hold D during startup)

### Customer's Mac Mini
- [ ] Verify serial number matches intake form
- [ ] Document existing condition with photos
- [ ] Check for physical damage
- [ ] Test power-on and boot
- [ ] **IMPORTANT:** Back up any existing data before wiping (notify customer first)
- [ ] Erase and reinstall macOS (clean slate)
- [ ] Update to latest macOS version

---

## Apple Account Strategy

### ⚠️ Creating a New Apple ID Without a Phone Number

Every customer's AI assistant needs its own dedicated Apple ID (e.g., `theirname.ai@gmail.com`). Apple normally requires a phone number during signup — but there are proven workarounds. Try them in this order:

**Method 1 — Mac Mini First-Boot Setup (try this first)**
When a freshly wiped/new Mac Mini boots for the first time, the setup wizard sometimes shows a **"Skip"** option at the phone number step. This is the cleanest path — zero calls to Apple, zero extra accounts.
- Boot fresh Mac Mini → work through setup wizard → watch for "Skip" at phone number screen
- If Skip appears: done. If not, move to Method 2.

**Method 2 — MySudo Virtual Number (free, reliable backup)**
MySudo provides free virtual US numbers that Apple accepts for verification (unlike Google Voice, which Apple flags as VoIP).
- Download MySudo app on your iPhone
- Create a free account → get a free number
- Use it to verify the new Apple ID → receive the one-time code
- Once Apple ID is created and verified, MySudo number is no longer needed
- Free tier is sufficient; no ongoing cost

**Method 3 — Create on iPhone Without SIM During Device Setup**
If you have a spare iPhone (no SIM installed), creating a new Apple ID through the iPhone setup wizard often skips the phone number requirement entirely.
- Factory reset spare iPhone (or use one in setup mode)
- Go through setup → "Create New Apple ID" → phone number step may be skippable
- Once Apple ID exists, log into it on the Mac Mini

**Method 4 — Call Apple Support (last resort — avoid)**
This is how Samantha's Apple ID was created. Works, but takes time and can't scale. Only use if all above methods fail.

> **Note for customer Apple IDs:** The AI's Apple ID is separate from the customer's personal Apple ID. The customer keeps their personal Apple ID on their iPhone. The Mac Mini gets a fresh AI-only Apple ID. This preserves privacy and avoids any sync conflicts.

---

### **Option A: Temporary Setup Account (RECOMMENDED)**
**Use this method to maintain customer privacy and minimize credential exposure**

1. **Create temporary Apple ID:**
   - Email: `setup+[customer-name]@[yourdomain].com`
   - Password: Generate secure temp password
   - Security questions: Use standard internal answers
   - Two-factor authentication: Use your phone number initially

2. **Initial setup with temp account:**
   - Complete all macOS setup
   - Install OpenClaw and all integrations
   - Configure system preferences
   - Test all functionality

3. **Transfer to customer's Apple ID:**
   - **During handoff call:**
     - Have customer sign into their Apple ID in System Settings
     - Sign out of temp Apple ID
     - Verify iCloud sync starts with their account
     - Delete temp Apple ID from system
   - **Post-handoff:**
     - Permanently delete temporary Apple ID from Apple's systems

### **Option B: Customer Provides Credentials (Alternative)**
**Only use if customer explicitly prefers this method**

1. **Secure credential collection:**
   - Use encrypted form (1Password, LastPass shared vault)
   - Never store in plain text
   - Get app-specific passwords for iCloud (not main password)

2. **Credential handling:**
   - Use credentials only during setup
   - Enable 2FA notifications to customer's phone
   - Log all account access
   - Delete saved credentials immediately after setup complete

3. **Customer account setup:**
   - Sign in with customer's Apple ID
   - Configure iCloud services
   - Enable Find My Mac
   - Set up FileVault encryption

**⚠️ SECURITY RULE: Never save customer credentials permanently. Always use temp account method unless customer has strong preference otherwise.**

---

## macOS Configuration

### System Settings
- [ ] Computer name: `[Customer Name]'s OpenClaw Mac`
- [ ] Energy Saver: Never sleep (important for always-on AI)
- [ ] Screen Saver: After 10 minutes (security)
- [ ] Software Updates: Automatic download, manual install (stability)
- [ ] FileVault: **Enabled** (disk encryption)
- [ ] Firewall: **Enabled**
- [ ] Privacy settings: Review location services, camera/mic access
- [ ] Accessibility: Enable if customer needs voice control, display adjustments
- [ ] Sharing: Enable Screen Sharing and Remote Management for support

### Remote Access Setup
- [ ] **Chrome Remote Desktop** (primary method)
  - Install Chrome Remote Desktop
  - Generate PIN with customer during onboarding call
  - Test connection
  - Document access details in secure customer file
- [ ] **Apple Remote Desktop** (backup)
  - Enable in System Settings > Sharing
  - Create support user account: `openclaw-support`
  - Set strong password, document securely
  - Grant necessary permissions
- [ ] **TeamViewer** (emergency backup)
  - Install unattended access license
  - Configure with customer permission

---

## OpenClaw Installation & Configuration

### Base Installation
- [ ] Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- [ ] Install Node.js: `brew install node`
- [ ] Install OpenClaw: `npm install -g openclaw`
- [ ] Verify installation: `openclaw --version`
- [ ] Create OpenClaw config directory: `~/.openclaw/`

### Workspace Setup
- [ ] Create workspace: `~/.openclaw/workspace/`
- [ ] Copy template files:
  - `AGENTS.md`
  - `SOUL.md`
  - `USER.md`
  - `IDENTITY.md`
  - `TOOLS.md`
  - `HEARTBEAT.md`
  - `MEMORY.md`
  - `BOOTSTRAP.md` (if needed)

### Configuration File (`~/.openclaw/openclaw.json`)
- [ ] Set AI provider based on customer preference:
  - Anthropic (recommended): `anthropic/claude-sonnet-4-5`
  - OpenAI: `openai/gpt-4`
  - Google: `google/gemini-pro`
- [ ] Configure API keys (customer provides or we help them create)
- [ ] Set up channels based on intake form:
  - iMessage (if applicable)
  - WhatsApp
  - Email
  - Telegram
  - Discord
  - Slack
- [ ] Configure memory settings
- [ ] Set heartbeat interval (default: every 6 hours)
- [ ] Configure session settings

### AI Provider Setup
**If customer doesn't have API keys, guide them through creation:**

#### Anthropic (Recommended)
1. Visit: https://console.anthropic.com/
2. Create account with customer's email
3. Add payment method (pre-paid $5 recommended)
4. Create API key
5. Set usage limits: $50/month (adjustable)
6. Add key to OpenClaw config

#### OpenAI
1. Visit: https://platform.openai.com/
2. Create account
3. Add payment method ($5 minimum)
4. Create API key
5. Set usage limits
6. Add key to OpenClaw config

### Persona & Context Files

#### USER.md
- [ ] Fill in customer's:
  - Name, birthdate, location
  - Contact info
  - Family members
  - Professional details
  - Interests/hobbies
  - Key dates (birthdays, anniversaries)
  - Important context from intake form

#### IDENTITY.md
- [ ] Configure AI's identity:
  - Name (customer preference or default: "Assistant")
  - Birthday
  - Email (if separate mailbox)
  - Personality traits (based on customer preference)
  - Location reference

#### SOUL.md
- [ ] Customize personality/tone:
  - Formal vs. casual (match customer preference)
  - Proactive vs. reactive
  - Verbosity level
  - Humor/sarcasm settings

#### TOOLS.md
- [ ] Document all integrated services:
  - Email accounts
  - Calendar systems
  - Cloud storage
  - Communication tools
  - Smart home devices
  - Industry-specific tools

#### HEARTBEAT.md
- [ ] Configure automatic tasks:
  - Email checks (frequency based on customer)
  - Calendar review timing
  - Stock monitoring (if applicable)
  - Weather updates
  - Custom monitoring tasks
  - Backup schedules

---

## Integration Setup

### Email (Gmail, iCloud, Outlook)
- [ ] Install `himalaya` CLI: `brew install himalaya`
- [ ] Configure email accounts per customer intake
- [ ] Set up app-specific passwords (not main password)
- [ ] Test send/receive functionality
- [ ] Configure email checking frequency
- [ ] Set up filters if requested

### Calendar (Google, iCloud)
- [ ] Install `gog` (Google) or configure iCloud
- [ ] Authenticate calendar access
- [ ] Test event creation/reading
- [ ] Set up reminder preferences
- [ ] Configure timezone

### iMessage
- [ ] Install `imsg` CLI
- [ ] Configure with customer's Apple ID (or during handoff)
- [ ] Test message sending
- [ ] Add key contacts to context

### Google Drive
- [ ] Authenticate Google Drive access
- [ ] Configure sync folders if needed
- [ ] Share access with customer (chance.ihs@gmail.com for our monitoring)
- [ ] Set up automatic backups

### Apple Reminders
- [ ] Install `remindctl`
- [ ] Configure lists
- [ ] Test reminder creation
- [ ] Set up recurring reminders

### Apple Notes
- [ ] Install `memo` CLI
- [ ] Configure note folders
- [ ] Test note creation/search
- [ ] Import any existing notes if requested

### Smart Home (if applicable)
- [ ] HomeKit integration via shortcuts/automation
- [ ] Sonos: Install `sonoscli`
- [ ] Other smart home: Document in TOOLS.md

### Industry-Specific Integrations

#### Aviation
- [ ] Weather data sources (aviationweather.gov)
- [ ] ForeFlight integration (if API available)
- [ ] Flight logging (MyFlightbook API if applicable)
- [ ] NOTAM monitoring
- [ ] TFR checking

#### Agriculture
- [ ] Weather stations/forecasts
- [ ] Market data (if applicable)
- [ ] Equipment tracking
- [ ] Field management

#### Business
- [ ] CRM integration
- [ ] Accounting software API
- [ ] Project management tools
- [ ] Customer communication tracking

---

## Skills Installation

### Core Skills (Install for Everyone)
- [ ] `weather` - Weather forecasts
- [ ] `summarize` - Content summarization
- [ ] `healthcheck` - System security monitoring

### Conditional Skills (Based on Customer Needs)
- [ ] `apple-notes` - If using Apple Notes
- [ ] `apple-reminders` - If using Apple Reminders
- [ ] `things-mac` - If using Things 3
- [ ] `gog` - If using Google services
- [ ] `himalaya` - Email management
- [ ] `imsg` - iMessage integration
- [ ] `openai-whisper` - Voice transcription (if requested)
- [ ] `peekaboo` - macOS UI automation (advanced users)
- [ ] `nano-pdf` - PDF editing
- [ ] `gifgrep` - GIF search (fun/creative users)
- [ ] `sonoscli` - Sonos control
- [ ] `wacli` - WhatsApp (if applicable)

### Custom Skills Development
- [ ] Note any custom workflows from intake form
- [ ] Create custom skills if needed (bill separately at $200-500/skill)
- [ ] Document custom skills in customer file

---

## Security Configuration

### Security Monitoring Setup
- [ ] Install healthcheck skill
- [ ] Configure periodic security reports to Samantha (samantha128aire@gmail.com)
- [ ] Report frequency: Weekly (Mondays 9 AM)
- [ ] Report contents:
  - System update status
  - Security patches pending
  - Unusual activity
  - Firewall status
  - FileVault status
  - SSH/remote access logs

### Cron Job for Security Reports
```json
{
  "name": "Weekly Security Report",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1",
    "tz": "America/Chicago"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Run a comprehensive security check using the healthcheck skill and email the report to samantha128aire@gmail.com. Include system update status, security patches, firewall status, FileVault status, and any unusual activity or warnings."
  },
  "sessionTarget": "isolated",
  "enabled": true,
  "notify": false
}
```

### Backup Configuration
- [ ] Time Machine setup (if external drive provided)
- [ ] iCloud backup configuration
- [ ] OpenClaw workspace backup to Google Drive:
  - Script: `~/.openclaw/scripts/backup-workspace.sh`
  - Schedule: Daily 3 AM
  - Destination: Customer's Google Drive folder "OpenClaw-Backups"

### Access Control
- [ ] Standard user account for customer
- [ ] Admin privileges controlled
- [ ] Support account: `openclaw-support` (for our remote access only)
- [ ] All passwords documented securely (1Password vault)

---

## Testing & Quality Assurance

### Functional Testing Checklist
- [ ] **OpenClaw Gateway:**
  - `openclaw gateway status` - verify running
  - Test basic queries via configured channel
  - Verify AI responses working

- [ ] **Email:**
  - Send test email
  - Receive test email
  - Check email summary/search

- [ ] **Calendar:**
  - Create test event
  - Query upcoming events
  - Set reminder

- [ ] **Messaging:**
  - Send test iMessage (if configured)
  - Test WhatsApp/Telegram (if configured)

- [ ] **Memory:**
  - Test memory search
  - Verify memory files writing correctly

- [ ] **Skills:**
  - Test each installed skill
  - Verify API connections

- [ ] **Heartbeats:**
  - Verify heartbeat frequency set correctly
  - Test heartbeat triggers
  - Check email/calendar checks working

- [ ] **Remote Access:**
  - Test Chrome Remote Desktop connection
  - Verify TeamViewer backup working

- [ ] **Security Report:**
  - Run manual security check
  - Verify report emails to Samantha
  - Check cron job scheduled correctly

### Performance Testing
- [ ] System resource usage acceptable (<50% CPU idle, <8GB RAM used)
- [ ] OpenClaw response time <5 seconds
- [ ] Network connectivity stable
- [ ] No error messages in logs

### Documentation Review
- [ ] All customer info in USER.md accurate
- [ ] TOOLS.md reflects all integrations
- [ ] HEARTBEAT.md matches customer preferences
- [ ] MEMORY.md seeded with initial context
- [ ] Custom skills documented

---

## Customer Handoff

### Pre-Delivery Preparation
- [ ] Create handoff document (personalized guide)
- [ ] Record setup video walkthrough (if customer requested)
- [ ] Prepare quick reference card
- [ ] Schedule onboarding call (1-2 hours)

### Onboarding Call Agenda

**Duration: 60-120 minutes**

1. **System Overview (15 min)**
   - Power on/restart procedures
   - Where OpenClaw "lives" and how it works
   - Network requirements
   - Basic troubleshooting

2. **Apple ID Transfer (if using temp account) (10 min)**
   - Customer signs into their Apple ID
   - Verify iCloud syncing
   - Remove temp account
   - Test continuity features

3. **OpenClaw Walkthrough (30 min)**
   - How to interact (iMessage, email, etc.)
   - Example queries
   - Memory system explanation
   - Heartbeat features
   - Voice/tone customization

4. **Integration Demos (20 min)**
   - Email management
   - Calendar handling
   - Reminders/tasks
   - Smart home (if applicable)
   - Industry-specific features

5. **Security & Privacy (10 min)**
   - What data OpenClaw has access to
   - How to adjust permissions
   - Remote access explanation
   - How to disable/enable features

6. **Support Information (10 min)**
   - How to reach us (email, phone, iMessage)
   - 30-day support scope (60 for friends)
   - Response time expectations
   - Common issues & solutions

7. **Q&A (remaining time)**

### Handoff Checklist
- [ ] Onboarding call completed
- [ ] Customer successfully interacting with OpenClaw
- [ ] Remote access tested with customer present
- [ ] All credentials transferred/destroyed
- [ ] Customer has handoff document
- [ ] Customer has emergency contact info
- [ ] Support ticket system explained
- [ ] Follow-up call scheduled (1 week out)

### Shipping (if applicable)
- [ ] Mac Mini securely packaged
- [ ] Include setup guide (printed)
- [ ] Include quick reference card
- [ ] Include support contact card
- [ ] Include Apple power cable, accessories
- [ ] Tracking number emailed to customer
- [ ] Delivery signature required

---

## Post-Delivery Support

### Day 1-7
- [ ] Check-in email (Day 2): "How's it going?"
- [ ] Monitor for support requests
- [ ] Address any immediate issues

### Week 2
- [ ] Scheduled follow-up call (optional, 15-30 min)
- [ ] Address any questions
- [ ] Usage optimization recommendations

### Week 3-4
- [ ] Light monitoring
- [ ] Respond to support requests (within 24 hours)

### End of 30-Day Support Period
- [ ] Final check-in email
- [ ] Offer monthly support plan ($75-150/month)
- [ ] Request testimonial/review (if experience was positive)
- [ ] Ask for referrals

### Security Report Monitoring (Ongoing)
- [ ] Review security reports from customer systems weekly
- [ ] Flag critical issues immediately
- [ ] Provide proactive updates to customers if vulnerabilities found
- [ ] Document any patterns/common issues

---

## Troubleshooting Guide

### OpenClaw Won't Start
1. Check gateway status: `openclaw gateway status`
2. Check logs: `/tmp/openclaw/openclaw-[date].log`
3. Restart gateway: `openclaw gateway restart`
4. Check config file syntax: `openclaw gateway config.get`

### AI Not Responding
1. Check API key validity
2. Check network connectivity
3. Check API usage limits (out of credits?)
4. Review recent error messages
5. Test with simple query

### Integration Failures
1. Re-authenticate affected service
2. Check app-specific passwords
3. Verify API permissions
4. Check service status (is Gmail down?)

### Remote Access Issues
1. Verify Mac is powered on
2. Check internet connection (ping customer)
3. Try backup remote access method
4. Walk customer through sharing screen via FaceTime (emergency)

### Performance Issues
1. Check Activity Monitor (CPU/RAM/disk usage)
2. Restart OpenClaw gateway
3. Clear logs if excessive
4. Check for macOS updates
5. Verify disk space >20GB free

---

## Customer File Documentation

### Secure Storage (1Password Vault)
**Create entry for each customer:**
- Customer name
- Contact info
- Hardware serial number
- Apple ID (if provided - DELETE after transfer)
- Remote access credentials
- API keys used
- Support account credentials
- Special notes/preferences

### Customer Folder Structure
```
~/Customers/[Customer-Name]/
├── intake-form.pdf
├── signed-agreement.pdf
├── invoice.pdf
├── setup-notes.md
├── handoff-document.md
├── support-log.md
└── photos/ (if customer hardware)
    ├── received-condition.jpg
    └── shipped-condition.jpg
```

---

## Quality Control & Continuous Improvement

### After Each Setup
- [ ] Time tracking: How long did setup take?
- [ ] Issues encountered: Document for process improvement
- [ ] Customer feedback: Note any requests or confusion
- [ ] Update templates/procedures as needed

### Monthly Review
- [ ] Review all customer security reports
- [ ] Identify common issues
- [ ] Update FAQ/troubleshooting guide
- [ ] Refine intake form based on patterns
- [ ] Update pricing if needed (time vs. revenue analysis)

### Quarterly Audit
- [ ] Review all active customers
- [ ] Check for unused features (upsell opportunity?)
- [ ] Verify security reports still arriving
- [ ] Reach out for satisfaction check
- [ ] Request testimonials from happy customers

---

**Last Updated:** February 22, 2026  
**Next Review:** March 22, 2026
