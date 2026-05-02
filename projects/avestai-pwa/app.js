/**
 * AvestAI PWA - Client-side chat application
 * Communicates with OpenClaw gateway via WebSocket
 */

// ─── Configuration ───────────────────────────────────────────────────────────

const CONFIG = {
    // For local development: ws://localhost:9000
    // For production: ws://your-mac-mini-ip:9000 (or through reverse proxy)
    bridgeHost: window.location.hostname === 'localhost' ? 'localhost' : window.location.hostname,
    bridgePort: 9000,
    getBridgeUrl() {
        return `ws://${this.bridgeHost}:${this.bridgePort}`;
    }
};

// Get token from URL parameters
const urlParams = new URLSearchParams(window.location.search);
const TOKEN = urlParams.get('token') || '';
const CUSTOMER_ID = urlParams.get('customer') || 'unknown';

// ─── State ───────────────────────────────────────────────────────────────────

const STATE = {
    ws: null,
    isConnected: false,
    stickyModel: null,
    stickyModelExpires: null,
    messages: [],
    sessionId: null,
    streamingEl: null,
    streamingModelEl: null,
    isDarkMode: window.matchMedia('(prefers-color-scheme: dark)').matches,
    theme: 'auto',
    colorScheme: 'avestai',
    fontSize: 'normal'
};

// ─── DOM Elements ───────────────────────────────────────────────────────────

const DOM = {
    messagesContainer: document.getElementById('messages'),
    messageInput: document.getElementById('messageInput'),
    sendBtn: document.getElementById('sendBtn'),
    voiceBtn: document.getElementById('voiceBtn'),
    settingsBtn: document.getElementById('settingsBtn'),
    typingIndicator: document.getElementById('typingIndicator'),
    settingsModal: document.getElementById('settingsModal'),
    modalOverlay: document.getElementById('modalOverlay'),
    closeSettings: document.getElementById('closeSettings'),
    themeSelect: document.getElementById('themeSelect'),
    colorSelect: document.getElementById('colorSelect'),
    fontSizeSelect: document.getElementById('fontSizeSelect'),
    exportBtn: document.getElementById('exportBtn')
};

// ─── Initialization ──────────────────────────────────────────────────────────

function init() {
    console.log('[AvestAI PWA] Initializing...');
    
    // Load persisted settings
    loadSettings();
    
    // ALWAYS enable input (don't wait for connection)
    DOM.messageInput.disabled = false;
    DOM.messageInput.style.cursor = 'text';
    DOM.messageInput.style.pointerEvents = 'auto';
    DOM.sendBtn.disabled = false;
    
    console.log('[Init] Input enabled:', !DOM.messageInput.disabled);
    
    // Setup event listeners
    setupEventListeners();
    
    // Connect to gateway
    connectWebSocket();
    
    // Register service worker for PWA (disabled during development)
    // if ('serviceWorker' in navigator) {
    //     navigator.serviceWorker.register('sw.js').catch(err => {
    //         console.warn('[PWA] Service worker registration failed:', err);
    //     });
    // }
    
    console.log('[AvestAI PWA] Ready!');
}

// ─── WebSocket Connection ────────────────────────────────────────────────────

function connectWebSocket() {
    if (!TOKEN) {
        showError('No authentication token provided. Check your URL.');
        return;
    }
    
    const wsUrl = CONFIG.getBridgeUrl();
    console.log('[WS] Connecting to bridge at', wsUrl);
    
    try {
        STATE.ws = new WebSocket(wsUrl);
        
        STATE.ws.onopen = () => {
            console.log('[WS] Connected to bridge');
            STATE.isConnected = true;
            // Send auth token to bridge
            STATE.ws.send(JSON.stringify({
                type: 'auth',
                token: TOKEN,
                customer: CUSTOMER_ID
            }));
            DOM.messageInput.disabled = false;
            DOM.sendBtn.disabled = false;
        };
        
        STATE.ws.onmessage = (event) => {
            handleMessage(JSON.parse(event.data));
        };
        
        STATE.ws.onerror = (error) => {
            console.error('[WS] Error:', error);
            showError('Connection error. Check your gateway URL.');
        };
        
        STATE.ws.onclose = () => {
            console.log('[WS] Disconnected');
            STATE.isConnected = false;
            DOM.messageInput.disabled = true;
            DOM.sendBtn.disabled = true;
            showError('Disconnected from gateway. Attempting to reconnect...');
            setTimeout(connectWebSocket, 3000);
        };
    } catch (err) {
        console.error('[WS] Connection failed:', err);
        showError('Failed to connect to gateway.');
    }
}

function handleMessage(msg) {
    console.log('[Bridge] Received:', msg.type);
    
    if (msg.type === 'auth_ok') {
        STATE.sessionId = msg.sessionId;
        STATE.isConnected = true;
        console.log('[Bridge] Authenticated, session:', STATE.sessionId);
    } else if (msg.type === 'auth_error') {
        showError('Authentication failed: ' + msg.error);
    } else if (msg.type === 'connecting') {
        console.log('[Bridge] Connecting...');
    } else if (msg.type === 'typing') {
        hideTypingIndicator();
        // Start a new streaming message bubble
        const { textEl, modelEl } = createStreamingBubble(msg.model);
        STATE.streamingEl = textEl;
        STATE.streamingModelEl = modelEl;
    } else if (msg.type === 'assistant_delta') {
        // Append delta to streaming bubble
        if (STATE.streamingEl) {
            STATE.streamingEl.textContent += msg.text;
            scrollToBottom();
        }
    } else if (msg.type === 'message_complete') {
        // Finalize streaming bubble — remove streaming class (stops cursor), update model label
        if (STATE.streamingEl) {
            const bubble = STATE.streamingEl.closest('.message-bubble');
            if (bubble) bubble.classList.remove('streaming');
        }
        if (STATE.streamingModelEl) {
            const model = msg.model || 'auto';
            STATE.streamingModelEl.textContent = getModelLabel(model);
            STATE.streamingEl = null;
            STATE.streamingModelEl = null;
        }
        DOM.messageInput.disabled = false;
        DOM.sendBtn.disabled = false;
    } else if (msg.type === 'error') {
        STATE.streamingEl = null;
        showErrorToast(msg.error);
        DOM.messageInput.disabled = false;
        DOM.sendBtn.disabled = false;
    }
}

function createStreamingBubble(model) {
    // Remove welcome message on first message
    if (STATE.messages.length === 0) {
        const welcome = DOM.messagesContainer.querySelector('.welcome-message');
        if (welcome) welcome.remove();
    }

    const messageEl = document.createElement('div');
    messageEl.className = 'message assistant';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble streaming';

    const textNode = document.createElement('span');
    textNode.className = 'bubble-text';
    bubble.appendChild(textNode);
    
    // Model label shown below the bubble
    const modelLabel = document.createElement('div');
    modelLabel.className = 'message-model-label';
    modelLabel.textContent = '···';
    
    messageEl.appendChild(bubble);
    messageEl.appendChild(modelLabel);
    DOM.messagesContainer.appendChild(messageEl);
    scrollToBottom();
    
    return { textEl: textNode, modelEl: modelLabel };
}

function showErrorToast(message) {
    console.error('[Error]', message);
    const toast = document.createElement('div');
    toast.className = 'error-toast';
    toast.textContent = '⚠️ ' + message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

function sendMessage(text) {
    if (!STATE.isConnected) {
        showError('Not connected to bridge');
        return;
    }
    
    if (!text.trim()) return;
    
    // Add user message to UI (force scroll so it's always visible)
    addMessage('user', text, null, true);
    
    // Clear input & reset height
    DOM.messageInput.value = '';
    DOM.messageInput.style.height = 'auto';
    
    // Disable input while waiting for response
    DOM.messageInput.disabled = true;
    DOM.sendBtn.disabled = true;

    // Send to bridge (it handles model detection + streaming)
    STATE.ws.send(JSON.stringify({
        type: 'message',
        text: text,
        sessionId: STATE.sessionId
    }));
}

function parseModelPrefix(text) {
    const match = text.match(/^([123OoSsHh])\s+/);
    
    if (match) {
        const prefix = match[1].toLowerCase();
        const modelMap = {
            '1': 'opus', 'o': 'opus',
            '2': 'sonnet', 's': 'sonnet',
            '3': 'haiku', 'h': 'haiku'
        };
        
        const newModel = modelMap[prefix] || 'sonnet';
        STATE.stickyModel = newModel;
        STATE.stickyModelExpires = Date.now() + (10 * 60 * 1000); // 10 minutes
        
        const cleanText = text.slice(match[0].length);
        return { model: newModel, cleanText };
    }
    
    // Check if sticky model is still valid
    if (STATE.stickyModel && STATE.stickyModelExpires > Date.now()) {
        STATE.stickyModelExpires = Date.now() + (10 * 60 * 1000); // Refresh timer
        return { model: STATE.stickyModel, cleanText: text };
    }
    
    // Reset to default (Sonnet)
    STATE.stickyModel = null;
    STATE.stickyModelExpires = null;
    return { model: 'sonnet', cleanText: text };
}

// ─── UI Helpers ──────────────────────────────────────────────────────────────

function addMessage(role, text, model = null, forceScroll = false) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;
    
    messageEl.appendChild(bubble);
    
    if (role === 'assistant' && model) {
        const label = document.createElement('div');
        label.className = 'message-model-label';
        label.textContent = getModelLabel(model);
        messageEl.appendChild(label);
    }
    
    // Remove welcome message on first real message
    if (STATE.messages.length === 0) {
        const welcome = DOM.messagesContainer.querySelector('.welcome-message');
        if (welcome) welcome.remove();
    }
    
    DOM.messagesContainer.appendChild(messageEl);
    STATE.messages.push({ role, text, model, timestamp: new Date() });
    
    scrollToBottom(forceScroll);
}

function showTypingIndicator() {
    DOM.typingIndicator.style.display = 'flex';
    scrollToBottom();
}

function hideTypingIndicator() {
    DOM.typingIndicator.style.display = 'none';
}

function showError(message) {
    console.error('[Error]', message);
    // Could show in toast, for now just log
}

function getModelLabel(model) {
    const m = (model || '').toLowerCase();
    if (m.includes('opus'))   return 'Opus';
    if (m.includes('sonnet')) return 'Sonnet';
    if (m.includes('haiku'))  return 'Haiku';
    return model || 'AI';
}

function scrollToBottom(force = false) {
    const el = DOM.messagesContainer;
    const distFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    // Auto-scroll if user is within 120px of the bottom, or forced (new message sent)
    if (force || distFromBottom < 120) {
        el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
    }
}

// ─── Settings ────────────────────────────────────────────────────────────────

function loadSettings() {
    const saved = localStorage.getItem('avestai-settings');
    if (saved) {
        const settings = JSON.parse(saved);
        STATE.theme = settings.theme || 'auto';
        STATE.colorScheme = settings.colorScheme || 'avestai';
        STATE.fontSize = settings.fontSize || 'normal';
    }
    
    applySettings();
}

function saveSettings() {
    localStorage.setItem('avestai-settings', JSON.stringify({
        theme: STATE.theme,
        colorScheme: STATE.colorScheme,
        fontSize: STATE.fontSize
    }));
}

function applySettings() {
    document.body.className = `theme-${STATE.theme === 'auto' ? (STATE.isDarkMode ? 'dark' : 'light') : STATE.theme} scheme-${STATE.colorScheme} font-${STATE.fontSize}`;
    DOM.themeSelect.value = STATE.theme;
    DOM.colorSelect.value = STATE.colorScheme;
    DOM.fontSizeSelect.value = STATE.fontSize;
}

function exportConversation() {
    const pdf = document.createElement('a');
    let content = `AvestAI Conversation Export\nGenerated: ${new Date().toLocaleString()}\n\n`;
    
    STATE.messages.forEach(msg => {
        const modelStr = msg.model ? ` — ${getModelLabel(msg.model)}` : '';
        content += `[${msg.role.toUpperCase()}${modelStr}]\n${msg.text}\n\n`;
    });
    
    const blob = new Blob([content], { type: 'text/plain' });
    pdf.href = URL.createObjectURL(blob);
    pdf.download = `avestai-export-${Date.now()}.txt`;
    pdf.click();
}

// ─── Event Listeners ──────────────────────────────────────────────────────────

function setupEventListeners() {
    // Message sending
    DOM.sendBtn.addEventListener('click', () => {
        sendMessage(DOM.messageInput.value);
    });
    
    DOM.messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage(DOM.messageInput.value);
        }
    });
    
    // Auto-expand textarea
    DOM.messageInput.addEventListener('input', () => {
        DOM.messageInput.style.height = 'auto';
        DOM.messageInput.style.height = Math.min(DOM.messageInput.scrollHeight, 120) + 'px';
    });
    
    // Voice input (placeholder)
    DOM.voiceBtn.addEventListener('click', () => {
        alert('Voice input coming soon!');
    });
    
    // Settings
    DOM.settingsBtn.addEventListener('click', () => {
        DOM.settingsModal.style.display = 'block';
        DOM.modalOverlay.style.display = 'block';
    });
    
    DOM.closeSettings.addEventListener('click', () => {
        DOM.settingsModal.style.display = 'none';
        DOM.modalOverlay.style.display = 'none';
    });
    
    DOM.modalOverlay.addEventListener('click', () => {
        DOM.settingsModal.style.display = 'none';
        DOM.modalOverlay.style.display = 'none';
    });
    
    DOM.themeSelect.addEventListener('change', (e) => {
        STATE.theme = e.target.value;
        applySettings();
        saveSettings();
    });
    
    DOM.colorSelect.addEventListener('change', (e) => {
        STATE.colorScheme = e.target.value;
        applySettings();
        saveSettings();
    });
    
    DOM.fontSizeSelect.addEventListener('change', (e) => {
        STATE.fontSize = e.target.value;
        applySettings();
        saveSettings();
    });
    
    DOM.exportBtn.addEventListener('click', exportConversation);
}

// ─── Start ───────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', init);
