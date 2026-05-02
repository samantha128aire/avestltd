/**
 * AvestAI PWA Bridge Server v2.0
 * 
 * Bridges PWA clients to OpenClaw via the OpenAI-compatible HTTP API.
 * Much simpler than WebSocket — uses POST /v1/chat/completions with streaming.
 * 
 * Usage: node server.js
 */

const WebSocket = require('ws');
const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');

// ─── Configuration ────────────────────────────────────────────────────────────

const PORT = process.env.PORT || 9000;
const OPENCLAW_HOST = process.env.OPENCLAW_HOST || '127.0.0.1';
const OPENCLAW_PORT = process.env.OPENCLAW_PORT || 18789;
const OPENCLAW_TOKEN = process.env.OPENCLAW_TOKEN || 'd850223804329e3d23d2ae6732e8cf274fc4b8f1d89c98b0';
const TOKEN_FILE = path.join(os.homedir(), '.openclaw', 'customer-tokens.json');

// ─── Token Management ────────────────────────────────────────────────────────

function loadTokens() {
  try {
    const raw = fs.readFileSync(TOKEN_FILE, 'utf8');
    return JSON.parse(raw);
  } catch (err) {
    console.error('[Tokens] Failed to load:', err.message);
    return {};
  }
}

function validateToken(token) {
  if (!token) return { valid: false };
  const tokens = loadTokens();
  for (const [customerId, storedToken] of Object.entries(tokens)) {
    if (customerId === '_comment') continue;
    // Match by value OR by key
    if (storedToken === token || customerId === token) {
      return { valid: true, customerId };
    }
  }
  return { valid: false };
}

// ─── Model Prefix Parsing ────────────────────────────────────────────────────

const PREFIX_MAP = {
  '1': 'anthropic/claude-opus-4-6',
  'o': 'anthropic/claude-opus-4-6',
  '2': 'anthropic/claude-sonnet-4-6',
  's': 'anthropic/claude-sonnet-4-6',
  '3': 'anthropic/claude-haiku-4-5',
  'h': 'anthropic/claude-haiku-4-5',
};

const STICKY_SESSIONS = new Map(); // sessionId -> { model, expires }

function parseModelPrefix(text, sessionId) {
  const match = text.match(/^([123OoSsHh])\s+/);
  
  if (match) {
    const prefix = match[1].toLowerCase();
    const model = PREFIX_MAP[prefix] || 'anthropic/claude-haiku-4-5';
    // Set sticky
    STICKY_SESSIONS.set(sessionId, {
      model,
      expires: Date.now() + (10 * 60 * 1000)
    });
    return {
      cleanText: text.slice(match[0].length),
      model
    };
  }
  
  // Check sticky
  const sticky = STICKY_SESSIONS.get(sessionId);
  if (sticky && sticky.expires > Date.now()) {
    sticky.expires = Date.now() + (10 * 60 * 1000); // refresh
    return { cleanText: text, model: sticky.model };
  }
  
  // Default: haiku
  return { cleanText: text, model: 'anthropic/claude-haiku-4-5' };
}

// ─── OpenClaw API Call ────────────────────────────────────────────────────────

const MODEL_FRIENDLY = {
  'anthropic/claude-haiku-4-5': 'Haiku',
  'anthropic/claude-haiku-4-6': 'Haiku',
  'anthropic/claude-sonnet-4-5': 'Sonnet',
  'anthropic/claude-sonnet-4-6': 'Sonnet',
  'anthropic/claude-opus-4-5': 'Opus',
  'anthropic/claude-opus-4-6': 'Opus',
};

function friendlyModel(raw) {
  if (!raw) return null;
  const r = raw.toLowerCase();
  if (r === 'openclaw' || r === 'default' || r === 'auto') return null;
  for (const [key, val] of Object.entries(MODEL_FRIENDLY)) {
    if (r.includes(key.toLowerCase())) return val;
  }
  if (r.includes('haiku'))  return 'Haiku';
  if (r.includes('sonnet')) return 'Sonnet';
  if (r.includes('opus'))   return 'Opus';
  return null;
}

// ─── iMessage Mirroring ───────────────────────────────────────────────────────

const MIRROR_NUMBER = process.env.MIRROR_NUMBER || '+15089229086'; // Chance
const MIRROR_ENABLED = process.env.MIRROR !== 'false'; // on by default

const { execFile } = require('child_process');

function mirrorToImessage(userText, assistantText, modelLabel) {
  if (!MIRROR_ENABLED) return;
  const msg = `[PWA] ${userText}\n\nSamantha (${modelLabel || 'AI'}):\n${assistantText}`;
  execFile('imsg', ['send', '--to', MIRROR_NUMBER, '--text', msg], (err) => {
    if (err) console.error('[Mirror] iMessage send failed:', err.message);
    else console.log(`[Mirror] Sent to ${MIRROR_NUMBER}`);
  });
}

function callOpenClaw(userMessage, model, sessionId, onChunk, onDone, onError) {
  const body = JSON.stringify({
    model: 'openclaw',
    stream: true,
    user: sessionId,
    messages: [{ role: 'user', content: userMessage }]
  });

  const options = {
    hostname: OPENCLAW_HOST,
    port: OPENCLAW_PORT,
    path: '/v1/chat/completions',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENCLAW_TOKEN}`,
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(body),
      'x-openclaw-agent-id': 'main',
      'x-openclaw-session-key': `pwa:${sessionId}`
    }
  };

  const req = http.request(options, (res) => {
    let fullText = '';
    let detectedModel = null;
    
    res.on('data', (chunk) => {
      const lines = chunk.toString().split('\n');
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const data = line.slice(6).trim();
        if (data === '[DONE]') {
          onDone(fullText, detectedModel);
          return;
        }
        try {
          const parsed = JSON.parse(data);
          // Capture the actual model from the SSE stream
          if (parsed.model && !detectedModel) {
            detectedModel = friendlyModel(parsed.model);
          }
          const delta = parsed.choices?.[0]?.delta?.content;
          if (delta) {
            fullText += delta;
            onChunk(delta);
          }
        } catch (e) {
          // skip unparseable lines
        }
      }
    });

    res.on('end', () => {
      if (fullText) onDone(fullText, detectedModel);
    });

    res.on('error', onError);
  });

  req.on('error', onError);
  req.write(body);
  req.end();
}

// ─── WebSocket Server ─────────────────────────────────────────────────────────

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', sessions: wss.clients.size, uptime: process.uptime() }));
  } else {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('AvestAI PWA Bridge v2.0');
  }
});

const wss = new WebSocket.Server({ server });

wss.on('connection', (clientWs, req) => {
  console.log(`[Client] New connection from ${req.socket.remoteAddress}`);
  
  let authenticated = false;
  let customerId = null;
  let sessionId = Math.random().toString(36).slice(2, 10);

  // Send initial state
  clientWs.send(JSON.stringify({ type: 'connecting' }));

  clientWs.on('message', async (data) => {
    let msg;
    try {
      msg = JSON.parse(data);
    } catch {
      return;
    }

    // Auth handshake
    if (!authenticated) {
      if (msg.type === 'auth') {
        const result = validateToken(msg.token);
        if (!result.valid) {
          console.warn(`[Auth] Invalid token from ${req.socket.remoteAddress}`);
          clientWs.send(JSON.stringify({ type: 'auth_error', error: 'Invalid token' }));
          clientWs.close();
          return;
        }
        authenticated = true;
        customerId = result.customerId;
        sessionId = `pwa-${customerId}-${sessionId}`;
        console.log(`[Auth] ✓ Authenticated: ${customerId} (session: ${sessionId})`);
        clientWs.send(JSON.stringify({ type: 'auth_ok', sessionId, customer: customerId }));
        return;
      }
      clientWs.send(JSON.stringify({ type: 'error', error: 'Must authenticate first' }));
      return;
    }

    // Message handling
    if (msg.type === 'message') {
      const text = msg.text?.trim();
      if (!text) return;

      const { cleanText, model } = parseModelPrefix(text, sessionId);
      
      const modelNames = MODEL_FRIENDLY;

      console.log(`[Message] ${customerId}: "${cleanText.substring(0, 50)}" → ${modelNames[model] || model}`);

      // Tell client we're typing
      clientWs.send(JSON.stringify({ type: 'typing', model: modelNames[model] || model }));

      // Stream response from OpenClaw
      callOpenClaw(
        cleanText,
        model,
        sessionId,
        // onChunk
        (delta) => {
          if (clientWs.readyState === WebSocket.OPEN) {
            clientWs.send(JSON.stringify({ type: 'assistant_delta', text: delta }));
          }
        },
        // onDone — use detectedModel (actual model from OpenClaw) if available
        (fullText, detectedModel) => {
          const finalModel = detectedModel || modelNames[model] || model;
          if (clientWs.readyState === WebSocket.OPEN) {
            clientWs.send(JSON.stringify({
              type: 'message_complete',
              model: finalModel,
              cost: 0
            }));
          }
          console.log(`[Done] ${customerId}: response complete (${fullText.length} chars) via ${finalModel}`);
          // Mirror to iMessage
          mirrorToImessage(cleanText, fullText, finalModel);
        },
        // onError
        (err) => {
          console.error(`[Error] OpenClaw call failed:`, err.message);
          if (clientWs.readyState === WebSocket.OPEN) {
            clientWs.send(JSON.stringify({ type: 'error', error: 'AI response failed: ' + err.message }));
          }
        }
      );
    }

    if (msg.type === 'ping') {
      clientWs.send(JSON.stringify({ type: 'pong' }));
    }
  });

  clientWs.on('close', () => {
    console.log(`[Client] Disconnected: ${customerId || 'unauthenticated'}`);
  });

  clientWs.on('error', (err) => {
    console.error(`[Client] Error:`, err.message);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`\n🧚‍♀️  AvestAI PWA Bridge Server v2.0`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`Bridge:    ws://localhost:${PORT}`);
  console.log(`OpenClaw:  http://${OPENCLAW_HOST}:${OPENCLAW_PORT}/v1/chat/completions`);
  console.log(`Health:    http://localhost:${PORT}/health`);
  console.log(`\n✅ Ready! Open PWA at:`);
  console.log(`   http://localhost:3000?token=avestai_demo_token_abc123def456ghi789jkl012m&customer=demo`);
  console.log(`\n`);
});

process.on('SIGINT', () => {
  console.log('\n[Server] Shutting down...');
  server.close(() => process.exit(0));
});
