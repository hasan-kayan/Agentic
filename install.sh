#!/bin/bash
# Installation script for AI Agent

set -e

echo "================================"
echo "AI Agent Installation Script"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_CMD=""
if command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
elif command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    if [[ "$PYTHON_VERSION" > "3.10" ]]; then
        PYTHON_CMD="python3"
    fi
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python 3.10 or higher is required"
    echo "Please install Python 3.10+ and try again"
    exit 1
fi

echo "✓ Found Python: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ Pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your OpenAI API key"
    echo ""
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p data
mkdir -p generated_projects
echo "✓ Directories created"
echo ""

# Initialize database
echo "Initializing database..."
$PYTHON_CMD -c "
import asyncio
from database import init_db

async def init():
    await init_db()
    print('✓ Database initialized')

asyncio.run(init())
"
echo ""

# Create alias helper script
cat > setup_alias.sh << 'EOF'
#!/bin/bash
# Add this to your ~/.bashrc or ~/.zshrc

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

alias ai-agent="source $SCRIPT_DIR/venv/bin/activate && python $SCRIPT_DIR/cli.py"

echo "Alias 'ai-agent' has been set up for this session"
echo "To make it permanent, add this to your ~/.bashrc or ~/.zshrc:"
echo ""
echo "alias ai-agent=\"source $SCRIPT_DIR/venv/bin/activate && python $SCRIPT_DIR/cli.py\""
EOF

chmod +x setup_alias.sh

echo "================================"
echo "✓ Installation Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file and add your OpenAI API key:"
echo "   nano .env"
echo ""
echo "2. (Optional) Store your sudo password for autonomous operations:"
echo "   python cli.py store-credential sudo_password \$USER \"your_password\""
echo ""
echo "3. Set up command alias (optional):"
echo "   source setup_alias.sh"
echo ""
echo "4. Start using AI Agent:"
echo "   python cli.py chat"
echo "   python cli.py create-project my-app -t backend -l python"
echo ""
echo "5. Or start the API server:"
echo "   python -m api.main"
echo ""
echo "For more information, see README.md"
echo ""



