# TOOLS.md - Local Notes

## Google Integration (gog)

**Account**: samantha128aire@gmail.com  
**Services**: calendar, contacts, docs, drive, gmail, sheets  
**Setup**: OAuth configured, credentials active

### Key Files
- **contacts.csv** (Drive ID: 1KJiCRTOBPNJj9xVveKzCSZSEAgedZudt)
  - Full contact list with names, phones, emails, birthdays
  - Downloaded to: `memory/contacts.csv`
  - Used for iMessage allowlist configuration

- **Samantha's Tax Recommendation** (Drive ID: 1UVX3WoZYkRCu0WXWb0YfVabjUkWPdJvde6AfKlIv-r0)
  - Tax-related document

### Common Gmail Operations
```bash
# Check inbox
gog gmail search 'is:unread' --max 10

# Send email
gog gmail send --to someone@example.com --subject "Subject" --body "Message"

# Check calendar (next 7 days)
gog calendar events primary --from $(date -Iseconds) --to $(date -v+7d -Iseconds)
```

---

## iMessage (imsg)

**CLI**: `imsg` (Homebrew installed)  
**Primary Chat**: Chat ID 1 = Chance (+1-508-922-9086)

### Allowlist
- Configured with contact list phone numbers
- Salvi (+1-351-209-2847) has access
- Only approved contacts can message

### Common Operations
```bash
# List chats
imsg chats --limit 10

# View history
imsg history --chat-id 1 --limit 50

# Send message (use OpenClaw message tool instead)
```

---

## TTS (Text-to-Speech)

**Status**: Configured  
**Provider**: *(needs verification - likely ElevenLabs or OpenAI)*

Use the `tts` tool in OpenClaw for voice messages.

---

## Stock Monitoring

### TSLA
- **Frequency**: Daily (weekdays via heartbeat)
- **Purpose**: Check for significant news/price movements
- **Method**: Web search + news analysis
- **Model**: Currently Sonnet (considering Haiku for cost reduction)

### MSFT
- **Watch Level**: $390
- **Strategy**: Bull call spread when price reaches target
- **Status**: Trade NOT executed as of Feb 2
- **Context**: Thin structure from April down to ~$390 level

---

## Remote Access

**Chrome Remote Desktop**: Configured  
**URL**: https://remotedesktop.google.com/access  
**Account**: chance.ihs@gmail.com (likely)

Allows remote Mac Mini access from any device.

---

## Cost Monitoring

**Method**: Manual screenshot from Anthropic dashboard  
**Frequency**: Weekly (Monday mornings)  
**Budget**: ~$200/month  
**Current Burn**: $14.33/day (as of Feb 3)

No public Anthropic billing API available — must use dashboard.

---

## Notes

- Contact list in Drive is the source of truth for phone numbers and birthdays
- Birthday automation relies on contacts.csv
- Keep tokens/costs documented in `memory/usage-tracking.md` (if it exists)
