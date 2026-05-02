#!/bin/bash

# AvestAI PWA - Start both bridge server and HTTP server

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo ""
echo "🧚‍♀️  AvestAI PWA - Starting servers..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start bridge server in background
echo "🌉 Starting WebSocket bridge server on port 9000..."
node server.js &
BRIDGE_PID=$!

# Wait for bridge to start
sleep 2

# Start HTTP server
echo "🌐 Starting HTTP server on port 3000..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ AvestAI PWA is ready!"
echo ""
echo "📱 Access the PWA at:"
echo "   http://localhost:3000?token=demo&customer=demo"
echo ""
echo "🌉 Bridge server: ws://localhost:9000"
echo "📊 Health check: http://localhost:9000/health"
echo ""
echo "ℹ️  To use from another device:"
echo "   http://your-mac-ip:3000?token=YOUR_TOKEN&customer=name"
echo ""
echo "💾 Tokens are stored in: ~/.openclaw/customer-tokens.json"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start HTTP server (blocks)
python3 -m http.server 3000

# Cleanup
kill $BRIDGE_PID 2>/dev/null || true
