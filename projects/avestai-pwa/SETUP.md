# AvestAI PWA - Setup Guide

## Quick Start (5 minutes)

### 1. Navigate to the PWA directory

```bash
cd /Users/sam/.openclaw/workspace/projects/avestai-pwa
```

### 2. Start both servers

```bash
./start.sh
```

This will:
- Install npm dependencies (first time only)
- Start the WebSocket bridge server on port 9000
- Start the HTTP server on port 3000
- Display access URLs

### 3. Open the PWA in your browser

```
http://localhost:3000?token=demo&customer=demo
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Your Browser                         │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │     AvestAI PWA (index.html + app.js)              │ │
│  │  - Chat UI (iMessage-like design)                 │ │
│  │  - Model selector (O/S/H prefix)                  │ │
│  │  - Settings (theme, color, font size)            │ │
│  └────────────────────┬─────────────────────────────┘ │
│                       │ WebSocket                      │
│                       └────────────┬────────────────────┘
│
├─────────────────────────────────────────────────────────────┤
│                   Your Mac Mini (192.168.42.161)            │
│                                                             │
│  ┌──────────────────────────┐  ┌──────────────────────────┐│
│  │  Bridge Server (9000)    │  │  HTTP Server (3000)     ││
│  │  - Token validation      │  │  - Serves PWA files     ││
│  │  - Message routing       │  │  - Static assets        ││
│  │  - Model prefix parsing  │  │  - Health checks        ││
│  └────────────┬─────────────┘  └──────────────────────────┘│
│               │                                             │
│               │ ws://localhost:18789                        │
│               ▼                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  OpenClaw Gateway (18789)                           │ │
│  │  - Agent loop & model selection                     │ │
│  │  - Smart Router plugin (model detection)            │ │
│  │  - Message history & tool execution                │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
avestai-pwa/
├── index.html          # Main PWA HTML structure
├── app.js              # Client-side chat logic, WebSocket handling
├── styles.css          # Responsive design, theming
├── manifest.json       # PWA metadata (installable)
├── sw.js               # Service worker (offline support)
├── server.js           # Bridge server (WebSocket → OpenClaw)
├── package.json        # Node.js dependencies
├── start.sh            # Startup script (runs both servers)
├── README.md           # Feature overview
├── SETUP.md            # This file
└── DEPLOYMENT.md       # How to deploy to production
```

## Bridge Server Details

The bridge server (`server.js`) handles:

1. **Authentication**: Validates tokens from `~/.openclaw/customer-tokens.json`
2. **Message Routing**: Sends user messages to OpenClaw via its WebSocket API
3. **Model Detection**: Parses prefixes (O/S/H) and manages sticky models
4. **Session Management**: One WebSocket connection per PWA client → one session per user

### Environment Variables

```bash
# Customize these (defaults shown)
PORT=9000                              # Bridge server port
OPENCLAW_HOST=127.0.0.1               # OpenClaw gateway host
OPENCLAW_PORT=18789                   # OpenClaw gateway port

# Example
OPENCLAW_HOST=192.168.42.161 node server.js
```

### Health Check

```bash
curl http://localhost:9000/health
```

Returns:
```json
{
  "status": "ok",
  "sessions": 2,
  "uptime": 1234.5
}
```

## Token Management

Tokens are stored in: `~/.openclaw/customer-tokens.json`

### Generate a new token

```bash
node -e "console.log(require('crypto').randomBytes(24).toString('hex'))"
```

### Add a customer

```bash
# Edit ~/.openclaw/customer-tokens.json
{
  "demo": "avestai_demo_token_abc123def456ghi789jkl012m",
  "jim-sweeney": "jim_token_xyz789abc456def123ghi012jkl",
  "gerry-masucci": "gerry_token_mno345pqr678stu901vwx234yz"
}
```

## Development

### Local Testing

```bash
# Terminal 1: Start everything
./start.sh

# Terminal 2: Test bridge server
curl http://localhost:9000/health

# Browser: Visit
http://localhost:3000?token=demo&customer=demo
```

### Debugging

**Browser console:**
```javascript
// Check WebSocket state
console.log(STATE.ws.readyState);  // 0=connecting, 1=open, 2=closing, 3=closed

// View current model
console.log(STATE.currentModel);

// View all messages
console.log(STATE.messages);
```

**Bridge server logs:**
```
[Client] New connection from 127.0.0.1
[Auth] Authenticated: demo
[Session] Created abc12345 for customer demo
[OpenClaw] Connecting to ws://127.0.0.1:18789 for session abc12345
[OpenClaw] Connected for session abc12345
```

## Troubleshooting

### "WebSocket connection failed"
- Check that bridge server is running on port 9000
- Check that OpenClaw gateway is running on 127.0.0.1:18789
- Ensure no firewall is blocking the connection

### "Invalid token"
- Verify token is in `~/.openclaw/customer-tokens.json`
- Check token format (should be ~48 hex characters)
- Restart bridge server after editing token file

### "Gateway not connected"
- Ensure OpenClaw is running: `openclaw status`
- Check gateway logs: `openclaw logs --follow`
- Verify gateway is listening on port 18789

### Model not changing with prefix
- Make sure prefix is followed by a space: `O analyze this...` ✅
- Prefixes are case-insensitive: `o`, `O`, `1` all work
- Check browser console for parsing errors

## Next Steps

1. **Test locally** with the demo token
2. **Add real customers** to `customer-tokens.json`
3. **Deploy to production** (see DEPLOYMENT.md)
4. **Add voice input** (Tier 2 feature)
5. **Implement conversation search** (Tier 2 feature)

## Support

For issues or questions:
1. Check the logs in both windows (bridge + HTTP server)
2. Test the health endpoint: `curl http://localhost:9000/health`
3. Verify tokens: `cat ~/.openclaw/customer-tokens.json`
4. Check OpenClaw status: `openclaw status`
