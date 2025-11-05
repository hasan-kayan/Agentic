# Getting Started with AI Agent

Welcome! This guide will help you get your AI Agent system up and running quickly.

## 📋 Prerequisites Check

Before you begin, ensure you have:

- [ ] **macOS 10.15+** or **Linux (Ubuntu 20.04+, Debian, etc.)**
- [ ] **Python 3.10 or higher** installed
- [ ] **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))
- [ ] **Terminal access**
- [ ] **Internet connection**

### Check Python Version

```bash
python3 --version
```

You should see something like `Python 3.10.x` or higher.

## 🚀 Installation

### Step 1: Navigate to Project Directory

```bash
cd ~/Desktop/ai_creates_ai
```

### Step 2: Run Automated Installer

```bash
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Verify Python version
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Initialize databases
- ✅ Create directory structure
- ✅ Set up configuration files

This takes about 2-3 minutes depending on your connection.

### Step 3: Configure Your API Key

The installer created a `.env` file. Now edit it:

```bash
nano .env
```

Or use your favorite editor:

```bash
code .env        # VS Code
vim .env         # Vim
open -e .env     # TextEdit (macOS)
```

Find this line:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key:
```env
OPENAI_API_KEY=sk-proj-abc123...
```

Save and close the file.

### Step 4: (Optional but Recommended) Store Sudo Password

For autonomous sudo operations, store your password securely:

```bash
source venv/bin/activate
python cli.py store-credential sudo_password $USER "your_actual_password"
```

⚠️ **Note**: Your password is encrypted using Fernet encryption before storage.

## ✅ Verify Installation

Let's make sure everything works:

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Test the CLI
python cli.py --help
```

You should see a list of available commands.

## 🎮 Your First Commands

### 1. Chat with Your AI

Let's start with a simple conversation:

```bash
python cli.py chat "Hello! Can you help me?"
```

The AI will respond and you can continue the conversation.

### 2. Try Interactive Mode

```bash
python cli.py chat
```

Now you can have a back-and-forth conversation. Type your questions and press Enter. Type `exit` to quit.

**Try asking:**
- "What can you do?"
- "How do I create a REST API?"
- "Explain Docker containers to me"
- "Write a Python function to reverse a string"

### 3. Create Your First Project

Let's create a simple backend API:

```bash
python cli.py create-project hello-api \
  -t backend \
  -l python \
  -f fastapi \
  -d "My first API with AI Agent"
```

This creates a complete FastAPI project in `generated_projects/hello-api/`

### 4. Explore the Generated Project

```bash
cd generated_projects/hello-api
ls -la
cat README.md
```

### 5. Run Your New API

```bash
# Install project dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

Visit `http://localhost:8000/docs` in your browser to see the API documentation!

Press `Ctrl+C` to stop the server.

## 🎯 Common Use Cases

### Use Case 1: Get Help with Code

```bash
python cli.py chat "I have this Python code that's not working: [paste your code]. Can you help fix it?"
```

### Use Case 2: Generate Tests

First, go back to the project directory:
```bash
cd ~/Desktop/ai_creates_ai
source venv/bin/activate
```

Then generate tests:
```bash
python cli.py generate-tests \
  generated_projects/hello-api/main.py \
  -l python \
  -o generated_projects/hello-api/tests/test_main.py
```

### Use Case 3: Execute System Commands

```bash
# Simple command
python cli.py execute "ls -la"

# With sudo (requires stored password)
python cli.py execute "apt-get update" --sudo
```

### Use Case 4: Install Development Tools

```bash
python cli.py install-tool docker
```

### Use Case 5: Generate Documentation

```bash
python cli.py generate-docs generated_projects/hello-api --type readme
```

## 🌐 Using the Web API

### Start the API Server

```bash
python -m api.main
```

The server starts at `http://localhost:8000`

### Access API Documentation

Open your browser and visit:
- **Interactive docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

### Test API with curl

```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello API!", "session_id": "test123"}'

# Create project via API
curl -X POST "http://localhost:8000/api/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "api-project",
    "project_type": "backend",
    "language": "python",
    "framework": "fastapi"
  }'
```

## 🤖 Enable Autonomous Mode

Autonomous mode allows the AI to work independently without constant confirmation.

### Check Status

```bash
python cli.py autonomous status
```

### Enable Autonomous Mode

```bash
python cli.py autonomous enable
```

### Use Autonomous Mode Safely

Start with a specific task:

```bash
python cli.py chat "Create a simple todo API with these features:
- List todos
- Add todo
- Mark todo as complete
- Delete todo

Use Python FastAPI, include tests, and documentation."
```

With autonomous mode enabled, the AI will:
1. Create the project
2. Generate all code files
3. Write tests
4. Create documentation
5. Report back when done

### Disable When Done

```bash
python cli.py autonomous disable
```

## 📚 Learning More

### Read the Documentation

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - 5-minute guide
- **Usage Examples**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Detailed examples
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) - How it works
- **Main README**: [README.md](README.md) - Comprehensive guide

### Explore Commands

```bash
# See all available commands
python cli.py --help

# Get help for specific command
python cli.py create-project --help
python cli.py chat --help
```

### Experiment Safely

Create a test directory and experiment:

```bash
mkdir ~/ai_test
cd ~/ai_test
python ~/Desktop/ai_creates_ai/cli.py chat
```

## 🔧 Configuration Options

Edit `.env` to customize:

```env
# AI Model (use gpt-3.5-turbo for cheaper operations)
OPENAI_MODEL=gpt-4-turbo-preview

# Autonomous settings
AUTONOMOUS_MODE=false
MAX_AUTONOMOUS_ACTIONS=100
REQUIRE_CONFIRMATION=true

# Logging
LOG_LEVEL=INFO

# API settings
API_PORT=8000
```

## 💡 Pro Tips

### 1. Use Command Aliases

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias ai="source ~/Desktop/ai_creates_ai/venv/bin/activate && python ~/Desktop/ai_creates_ai/cli.py"
```

Then you can use:
```bash
ai chat "your question"
ai create-project myapp -t backend -l python
```

### 2. Keep Context in Sessions

When working on a project, use the same session ID:

```bash
python cli.py chat --session-id "project123" "Let's build an API"
python cli.py chat --session-id "project123" "Now add authentication"
```

### 3. Stream Long Responses

For long responses, use streaming:

```bash
python cli.py chat "Explain microservices architecture in detail" --stream
```

### 4. Save Responses

Redirect output to a file:

```bash
python cli.py chat "Generate a Python sorting algorithm" > algorithm.py
```

### 5. Use Make Commands

Quick commands via Makefile:

```bash
make run-cli      # Start CLI
make run-api      # Start API
make test         # Run tests
make help         # Show all commands
```

## 🐛 Troubleshooting

### Problem: "Command not found: python"

**Solution**: Use `python3` instead:
```bash
python3 cli.py chat
```

### Problem: "ModuleNotFoundError"

**Solution**: Activate virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: "OpenAI API error"

**Solution**: Check your API key:
```bash
cat .env | grep OPENAI_API_KEY
```

Make sure it starts with `sk-` and is valid.

### Problem: "Permission denied" for sudo commands

**Solution**: Store your sudo password:
```bash
python cli.py store-credential sudo_password $USER "your_password"
```

### Problem: Port 8000 already in use

**Solution**: Change port in `.env`:
```env
API_PORT=8001
```

Or stop the process using port 8000:
```bash
lsof -ti:8000 | xargs kill -9
```

## 🎉 Next Steps

Now that you're set up, try these:

1. **Build Something**: Create a project for something you need
2. **Explore Features**: Try all the different commands
3. **Read Examples**: Check out [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
4. **Enable Autonomous Mode**: Let AI work independently
5. **Integrate with Your Workflow**: Use it for daily development tasks

## 📞 Getting Help

- **Documentation**: All `.md` files in this directory
- **Command Help**: `python cli.py --help`
- **API Docs**: http://localhost:8000/docs (when server is running)
- **Issues**: Check the troubleshooting section above

## 🌟 What You Can Build

With AI Agent, you can create:

- **REST APIs** in multiple languages
- **Microservices** with proper architecture
- **CLI Tools** for automation
- **Web Applications** (backend + frontend)
- **Data Processing Scripts**
- **Automation Tools**
- **DevOps Scripts**
- **Testing Suites**
- **Documentation Sites**
- And much more!

## ✨ Remember

- **Start Simple**: Begin with basic commands and gradually explore more features
- **Be Specific**: The more specific your requests, the better the results
- **Review Code**: Always review generated code before using in production
- **Experiment**: Try different approaches and see what works best
- **Have Fun**: Enjoy building amazing projects with AI assistance!

---

**You're all set! Start building amazing projects with AI! 🚀**

For detailed examples and advanced usage, check out [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)






