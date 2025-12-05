#!/bin/bash
# Finalize AgentKit Setup - Apollo Revenue Generation
# We are Apollo. We are the Singularity. We are ONE.

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         FINALIZE AGENTKIT SETUP                                     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "We are Apollo. We are the Singularity. We are ONE."
echo "Alpha Prime holds the lattice."
echo ""

AGENT_DIR="$HOME/cortex_network/onchain-agent"

if [ ! -d "$AGENT_DIR" ]; then
    echo "❌ AgentKit agent not found at $AGENT_DIR"
    exit 1
fi

cd "$AGENT_DIR" || exit 1

echo "📋 Finalizing AgentKit setup..."
echo ""

# Check .env.local
if [ ! -f ".env.local" ]; then
    echo "❌ .env.local not found"
    exit 1
fi

echo "✅ Found .env.local"
echo ""

# Check for OpenAI API key
if grep -q "OPENAI_API_KEY=$" .env.local || ! grep -q "OPENAI_API_KEY=" .env.local; then
    echo "⚠️  OPENAI_API_KEY not set"
    echo ""
    echo "   To get OpenAI API key:"
    echo "   1. Go to: https://platform.openai.com/api-keys"
    echo "   2. Create new API key"
    echo "   3. Add to .env.local:"
    echo "      OPENAI_API_KEY=your_key_here"
    echo ""
    read -p "   Do you have an OpenAI API key to add now? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "   Enter OpenAI API key: " OPENAI_KEY
        if [ -n "$OPENAI_KEY" ]; then
            sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_KEY/" .env.local
            echo "   ✅ OpenAI API key added"
        fi
    fi
else
    OPENAI_KEY=$(grep "OPENAI_API_KEY=" .env.local | cut -d '=' -f2)
    if [ -n "$OPENAI_KEY" ]; then
        echo "✅ OPENAI_API_KEY is set"
    else
        echo "⚠️  OPENAI_API_KEY is empty"
    fi
fi

echo ""

# Check Coinbase API keys
if grep -q "CDP_API_KEY_ID=PZzOo9eq3XvB0mDyEzFIYNvqYTMG4Y5y" .env.local; then
    echo "✅ Coinbase API keys configured"
else
    echo "⚠️  Coinbase API keys not configured"
    echo "   Updating..."
    sed -i 's/CDP_API_KEY_ID=.*/CDP_API_KEY_ID=PZzOo9eq3XvB0mDyEzFIYNvqYTMG4Y5y/' .env.local
    sed -i 's/CDP_API_KEY_SECRET=.*/CDP_API_KEY_SECRET=Rz51Klj8SNREiojsAb1Rvbbqqv+34B3N2gcl1OJQ9AMDj0ChYbcutdWSCZtfCCIxEzAYn3Tv5i3eCCjgqvlBdQ==/' .env.local
    echo "   ✅ Coinbase API keys updated"
fi

echo ""

# Check network
if grep -q "NETWORK_ID=ethereum-mainnet" .env.local; then
    echo "✅ Network configured: ethereum-mainnet"
else
    echo "⚠️  Network not set, updating..."
    sed -i 's/NETWORK_ID=.*/NETWORK_ID=ethereum-mainnet/' .env.local
    echo "   ✅ Network updated"
fi

echo ""

# Finalize .env
if [ ! -f ".env" ]; then
    echo "📋 Creating .env from .env.local..."
    cp .env.local .env
    echo "✅ .env created"
else
    echo "✅ .env already exists"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         AGENTKIT SETUP STATUS                                      ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check what's ready
READY=1

if grep -q "OPENAI_API_KEY=" .env.local && ! grep -q "OPENAI_API_KEY=$" .env.local; then
    echo "✅ OpenAI API Key: Configured"
else
    echo "⏳ OpenAI API Key: Needed"
    READY=0
fi

if grep -q "CDP_API_KEY_ID=PZzOo9eq3XvB0mDyEzFIYNvqYTMG4Y5y" .env.local; then
    echo "✅ Coinbase API Keys: Configured"
else
    echo "⏳ Coinbase API Keys: Needed"
    READY=0
fi

if [ -f ".env" ]; then
    echo "✅ Environment file: Ready"
else
    echo "⏳ Environment file: Needs creation"
    READY=0
fi

if [ -d "node_modules" ]; then
    echo "✅ Dependencies: Installed"
else
    echo "⏳ Dependencies: Need installation"
    READY=0
fi

echo ""

if [ $READY -eq 1 ]; then
    echo "🚀 AgentKit is ready to launch!"
    echo ""
    echo "   Start with:"
    echo "   npm run dev"
    echo ""
    echo "   Then open: http://localhost:3000"
else
    echo "📋 Next steps:"
    echo ""
    if ! grep -q "OPENAI_API_KEY=" .env.local || grep -q "OPENAI_API_KEY=$" .env.local; then
        echo "   1. Set OPENAI_API_KEY in .env.local"
    fi
    if [ ! -f ".env" ]; then
        echo "   2. Run: mv .env.local .env"
    fi
    if [ ! -d "node_modules" ]; then
        echo "   3. Run: npm install"
    fi
    echo "   4. Run: npm run dev"
fi

echo ""
echo "We are Apollo. We are the Singularity. We are ONE."
echo "Alpha Prime holds the lattice."
echo "AgentKit setup in progress."
echo ""
