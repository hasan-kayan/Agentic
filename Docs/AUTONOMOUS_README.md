# 🤖 Autonomous AI Coding Agent

## Like Cursor AI, but fully autonomous in your terminal!

This AI agent can:
- ✅ Execute terminal commands (with sudo if needed)
- ✅ Create files and directories
- ✅ Write complete, production-ready code
- ✅ Run tests and fix errors automatically
- ✅ Build entire projects from a single prompt

---

## 🚀 Quick Start

### 1. Make sure you have your OpenAI API key in `.env`:

```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

### 2. Run the Autonomous CLI:

```bash
python3 autonomous_cli.py
```

### 3. Give it ANY task!

---

## 💡 Example Tasks

### Simple Tasks (Does exactly what you ask):
```
• "Create a Python script that calculates fibonacci numbers"
• "Write a quick test for my code"
• "Make a function to parse CSV files"
```

### End-to-End Projects (Full production-ready code):
```
• "Create a REST API for a todo app with FastAPI"
  - Creates project structure
  - Writes all code files
  - Adds requirements.txt
  - Creates tests
  - Runs tests
  - Creates README

• "Build a web scraper for Amazon product prices"
  - Sets up project
  - Installs dependencies
  - Writes scraper code
  - Adds error handling
  - Tests it
  - Documents usage

• "Create a Discord bot that responds to !hello"
  - Full Discord bot setup
  - Bot token configuration
  - Command handlers
  - Deployment instructions
```

### Complex Projects:
```
• "Create a microservices architecture with user and order services"
• "Build a data pipeline that processes CSV and generates reports"
• "Make a full-stack app with React frontend and FastAPI backend"
• "Create a CLI tool for managing Docker containers"
```

---

## 🎯 How It Works

1. **You give a task** → The AI understands what you want
2. **AI plans** → Creates architecture and file structure
3. **AI builds** → Uses tools to create files, run commands
4. **AI tests** → Runs the code to verify it works
5. **AI fixes** → If errors occur, fixes them automatically
6. **AI reports** → Tells you it's done with summary

---

## 🛠️ Available Tools

The AI has access to these tools:

| Tool | Description |
|------|-------------|
| `execute_command` | Run any terminal command (with sudo if needed) |
| `create_file` | Create or overwrite files |
| `read_file` | Read file contents |
| `create_directory` | Create directories |
| `list_directory` | List directory contents |
| `task_complete` | Signal when task is finished |

---

## 📝 Example Session

```bash
$ python3 autonomous_cli.py

╔═══════════════════════════════════════════════════════════════╗
║   🤖 AUTONOMOUS AI CODING AGENT 🤖                            ║
╚═══════════════════════════════════════════════════════════════╝

What do you want me to build? 
> Create a FastAPI todo app with CRUD operations

🤖 Starting autonomous execution...

AI: Creating project structure...
AI: Writing main.py with FastAPI routes...
AI: Creating models.py for database...
AI: Adding requirements.txt...
AI: Creating tests...
AI: Running tests...
AI: All tests pass! ✓
AI: Creating README.md...

✅ TASK COMPLETED SUCCESSFULLY!

Summary: Created a complete FastAPI todo application with:
  - RESTful API endpoints (GET, POST, PUT, DELETE)
  - SQLite database integration
  - Pydantic models for validation
  - Full test suite (all passing)
  - Documentation in README.md

Project Path: /path/to/generated_projects/todo-api

Iterations: 12
```

---

## ⚙️ Configuration

Edit `.env` to configure:

```env
# Required
OPENAI_API_KEY=your-key-here

# Optional
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-4, gpt-3.5-turbo
MAX_AUTONOMOUS_ACTIONS=50          # Safety limit
```

---

## 🔒 Safety Features

- **Max iterations limit**: Prevents infinite loops (default: 50)
- **Sandboxed by default**: Won't delete system files
- **Sudo confirmation**: Can use sudo when needed for installs
- **Full logging**: See everything the AI does

---

## 🎓 Tips for Best Results

### ✅ DO:
- Be specific about what you want
- Mention the tech stack if you have preferences
- Ask for tests and documentation
- Request specific features

### ❌ DON'T:
- Give vague requirements like "make an app"
- Mix multiple unrelated tasks
- Ask it to modify external systems without permission

### 🌟 GOOD Prompts:
```
"Create a Python Flask API for user authentication with JWT tokens, 
bcrypt password hashing, SQLite database, and unit tests"

"Build a CLI tool in Python that converts Markdown to HTML,
supports custom CSS, and has a --watch mode for live preview"
```

### 😕 VAGUE Prompts:
```
"Make a website"  (What kind? What features?)
"Create an app"   (Too vague - specify the purpose)
```

---

## 🐛 Troubleshooting

### API Key Error
```bash
# Make sure .env exists with your key
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### Module Not Found
```bash
# Reinstall requirements
pip install -r requirements.txt
```

### Permission Denied
```bash
# The AI will use sudo when needed
# Or manually: sudo chown -R $USER /path/to/project
```

---

## 🎬 Ready to Go!

```bash
python3 autonomous_cli.py
```

**Let the AI do the coding!** 🚀

---

## 📚 More Examples

Check out `USAGE_EXAMPLES.md` for more detailed examples and use cases.

---

Built with ❤️ using OpenAI GPT-4

