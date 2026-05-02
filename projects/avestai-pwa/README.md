# AvestAI PWA

A Progressive Web App for AvestAI — your personal AI running locally on your Mac Mini.

## Features

- 💬 **Chat interface** — iMessage-like design with your branding
- 🎛️ **Model selector** — Switch between Opus, Sonnet, Haiku with one tap
- 🧠 **Smart routing** — Start with `O`, `S`, or `H` to select model; sticky for 10 minutes
- 🎨 **Customizable** — Dark/light mode, color schemes, font sizes
- 📊 **Cost tracking** — See exactly what each message costs
- 💾 **Export** — Download conversations as text
- 🔒 **Token auth** — Secure access with URL-based tokens
- 📱 **Installable** — Works on iPhone, Android, desktop

## Development

### Local Setup

1. Files are in: `/Users/sam/.openclaw/workspace/projects/avestai-pwa/`

2. Start a simple local server:
   ```bash
   cd /Users/sam/.openclaw/workspace/projects/avestai-pwa
   python3 -m http.server 3000
   ```

3. Open in browser: `http://localhost:3000?token=demo`

### Gateway Configuration

The PWA connects to your OpenClaw gateway at:
- **Host**: `192.168.42.161`
- **Port**: `18789`
- **Protocol**: WebSocket (`ws://`)

Update `CONFIG.gatewayHost` in `app.js` to change this.

### Authentication

Tokens are stored in: `~/.openclaw/customer-tokens.json`

Generate a new token:
```bash
node -e "console.log(require('crypto').randomBytes(24).toString('hex'))"
```

URLs:
```
http://localhost:3000?token=YOUR_TOKEN&customer=customer_name
https://avestltd.com/sam?token=YOUR_TOKEN&customer=your_name
```

## Deployment

### Option 1: GitHub Pages

Deploy to `avestltd.com/sam`:

```bash
# Build & deploy
cd /Users/sam/avestltd
cp -r ~/.openclaw/workspace/projects/avestai-pwa/* docs/sam/
git add docs/sam/
git commit -m "PWA: update"
git push
```

### Option 2: Mac Mini Static Server

Serve from your Mac Mini directly using Node.js or Python.

## Files

- `index.html` — Main HTML structure
- `app.js` — Client-side logic (messaging, state, UI)
- `styles.css` — Responsive design with theming
- `manifest.json` — PWA metadata (installable)
- `sw.js` — Service worker (offline support, caching)
- `README.md` — This file

## Gateway Integration

The PWA expects your OpenClaw gateway to handle these WebSocket messages:

**Client → Gateway:**
```json
{
  "type": "message",
  "text": "user message here",
  "model": "opus|sonnet|haiku",
  "sessionId": "session_id",
  "token": "auth_token"
}
```

**Gateway → Client:**
```json
{
  "type": "reply",
  "text": "AI response",
  "model": "sonnet",
  "cost": 0.0123
}
```

or

```json
{
  "type": "error",
  "error": "Error message"
}
```

## TODO (Tier 2)

- [ ] Voice input (speech-to-text)
- [ ] Voice output (text-to-speech)
- [ ] Conversation search/history
- [ ] Export as PDF
- [ ] Custom system prompts
- [ ] Saved replies/templates
- [ ] Usage stats over time

## Notes

- Styling uses CSS custom properties for theming
- Responsive design works on mobile (375px+) and desktop
- Dark mode follows system preference by default
- Service worker enables offline caching of static assets
- WebSocket is required for messaging (not a fallback)
