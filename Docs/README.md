# AI Agent - Autonomous System Control & Project Generator

A powerful autonomous AI agent that can control your macOS/Linux system, generate complete projects, write tests, fix errors automatically, and much more. Built with OpenAI GPT-4, FastAPI, and advanced system integration.

## 🚀 Features

### Core Capabilities

- **🤖 Autonomous AI Agent**: GPT-4 powered agent with advanced reasoning
- **💻 Full System Control**: Execute terminal commands with or without sudo
- **🏗️ Project Generation**: Create complete backend/frontend/fullstack projects
- **🧪 Test Generation**: Automatically write unit and integration tests
- **🔧 Auto Error Fixing**: Detect and fix errors automatically
- **🔍 Web Search Integration**: Research code examples and documentation
- **📦 Tool Installation**: Automatically install required development tools
- **📚 Documentation Generation**: Create comprehensive project documentation
- **🔐 Secure Credential Storage**: Encrypted storage for passwords and API keys
- **🎯 Autonomous Mode**: Work independently with permission controls

### Supported Project Types

- **Backend**: Python (FastAPI, Django, Flask), Node.js (Express), Go, Rust
- **Frontend**: React, Vue, Angular (coming soon)
- **Fullstack**: MERN, MEAN, Python+React
- **CLI**: Python (Typer, Click), Go

### Supported Languages

Python, JavaScript, TypeScript, Go, Rust, Java, PHP, Ruby, and more

## 📋 Requirements

- **OS**: macOS 10.15+ or Linux (Ubuntu 20.04+, Debian, etc.)
- **Python**: 3.10 or higher
- **OpenAI API Key**: For AI capabilities
- **Tools** (optional, will be installed automatically):
  - Git
  - Docker (for containerized projects)
  - Node.js/npm (for JavaScript projects)
  - Go, Rust, etc. (for respective project types)

## 🛠️ Installation

### 1. Clone the Repository

```bash
cd ~/Desktop/ai_creates_ai
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your-secret-key-change-this-in-production
ENCRYPTION_KEY=your-encryption-key-change-this
```

### 5. Initialize the System

```bash
python cli.py init
```

### 6. Store Sudo Password (Optional)

For autonomous sudo operations:

```bash
python cli.py store-credential sudo_password $USER "your_password"
```

## 🎮 Usage

### CLI Interface

#### Chat with AI

```bash
# Interactive mode
python cli.py chat

# Single message
python cli.py chat "Create a REST API in Python"
```

#### Create Projects

```bash
# Python FastAPI backend
python cli.py create-project my-api -t backend -l python -f fastapi

# Node.js Express backend
python cli.py create-project my-server -t backend -l javascript -f express

# React frontend
python cli.py create-project my-app -t frontend -l javascript -f react
```

#### Execute Commands

```bash
# Regular command
python cli.py execute "ls -la"

# With sudo
python cli.py execute "apt-get update" --sudo
```

#### Generate Tests

```bash
python cli.py generate-tests ./app/models.py -l python -o ./tests/test_models.py
```

#### Generate Documentation

```bash
python cli.py generate-docs ./my-project --type readme
```

#### Install Tools

```bash
python cli.py install-tool docker
python cli.py install-tool kubectl
```

#### Autonomous Mode

```bash
# Enable autonomous mode
python cli.py autonomous enable

# Check status
python cli.py autonomous status

# Disable
python cli.py autonomous disable
```

### Web API

Start the API server:

```bash
python -m api.main
# Or
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

#### API Endpoints

- `POST /api/chat` - Chat with AI
- `POST /api/projects/` - Create project
- `GET /api/projects/` - List projects
- `POST /api/terminal/execute` - Execute command
- `POST /api/credentials/` - Store credential
- `POST /api/autonomous/enable` - Enable autonomous mode
- `POST /api/documentation/readme` - Generate README
- And many more...

API documentation: `http://localhost:8000/docs`

### Python API

```python
import asyncio
from core.ai_agent import AIAgent
from core.project_generator import ProjectGenerator
from core.terminal_executor import TerminalExecutor
from database import init_db, get_db, get_personalization_db

async def main():
    await init_db()
    
    # Chat with AI
    agent = AIAgent(session_id="my_session")
    async for db in get_db():
        response = await agent.chat("How do I optimize this code?", db)
        print(response)
    
    # Create a project
    terminal = TerminalExecutor()
    generator = ProjectGenerator(agent, terminal)
    
    async for db in get_db():
        async for p_db in get_personalization_db():
            project = await generator.create_project(
                db=db,
                personalization_db=p_db,
                name="my-api",
                project_type="backend",
                language="python",
                framework="fastapi"
            )
            print(f"Project created: {project.path}")

asyncio.run(main())
```

## 🔐 Security

### Credential Management

All sensitive data is encrypted using Fernet symmetric encryption:

- Sudo passwords
- API keys
- SSH keys
- Database credentials

### Permission System

The autonomous mode includes a granular permission system:

- `terminal` - Execute terminal commands
- `file_system` - Read/write files
- `network` - Network access
- `sudo` - Sudo operations

Grant permissions:

```python
await autonomous_manager.grant_permission(
    db=db,
    permission_type="terminal",
    scope="/home/user/projects/*",
    grant_level="moderate",
    duration_hours=24
)
```

## 📁 Project Structure

```
ai_creates_ai/
├── api/                    # FastAPI web API
│   ├── main.py            # API entry point
│   └── routes/            # API endpoints
├── core/                  # Core functionality
│   ├── ai_agent.py        # AI agent with OpenAI
│   ├── terminal_executor.py  # Command execution
│   ├── project_generator.py  # Project creation
│   ├── error_handler.py   # Error detection & fixing
│   ├── test_generator.py  # Test generation
│   ├── documentation_generator.py  # Doc generation
│   ├── web_search.py      # Web search
│   ├── autonomous_manager.py  # Autonomous control
│   ├── tool_installer.py  # Tool installation
│   ├── credential_manager.py  # Credential storage
│   └── security.py        # Encryption utilities
├── database/              # Database models
│   ├── models.py          # Main database models
│   ├── personalization_models.py  # User data models
│   └── database.py        # DB connection
├── cli.py                 # Command-line interface
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## 🧪 Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=. --cov-report=html
```

## 📖 Examples

### Example 1: Create a Complete REST API

```bash
python cli.py chat "Create a REST API for a blog with posts and comments in Python FastAPI"
```

The AI will:
1. Create the project structure
2. Generate models and schemas
3. Create API endpoints
4. Write unit tests
5. Generate documentation
6. Set up database migrations

### Example 2: Debug and Fix Code

```bash
python cli.py chat "There's an error in my code: TypeError: 'NoneType' object is not iterable in file app.py line 42"
```

The AI will:
1. Analyze the error
2. Identify the root cause
3. Provide a fix
4. Optionally apply it automatically

### Example 3: Install and Configure Tools

```bash
python cli.py chat "Install Docker and PostgreSQL, then create a database for my project"
```

The AI will:
1. Check if tools are installed
2. Install missing tools
3. Configure them
4. Create the database
5. Provide connection details

## 🚧 Autonomous Mode

When autonomous mode is enabled, the AI can:

- Execute commands without asking
- Install required tools
- Fix errors automatically
- Make architectural decisions
- Manage the entire development workflow

**Safety Features:**

- Action count limits
- Permission scopes
- Time-based expiration
- Confirmation requirements
- Full audit log

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | GPT model to use | gpt-4-turbo-preview |
| `DATABASE_URL` | Main database URL | sqlite+aiosqlite:///./ai_agent.db |
| `PERSONALIZATION_DB_URL` | Personalization DB URL | sqlite+aiosqlite:///./personalization.db |
| `AUTONOMOUS_MODE` | Enable autonomous mode | false |
| `MAX_AUTONOMOUS_ACTIONS` | Max actions in autonomous mode | 100 |
| `REQUIRE_CONFIRMATION` | Require user confirmation | true |
| `LOG_LEVEL` | Logging level | INFO |
| `API_PORT` | API server port | 8000 |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This AI agent has significant system access. Use with caution:

- Review actions before granting autonomous permissions
- Keep credentials secure
- Use in isolated/test environments first
- Monitor system resources
- Set appropriate permission scopes

## 🐛 Troubleshooting

### "ModuleNotFoundError"

Ensure virtual environment is activated and dependencies installed:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Permission Denied" for sudo commands

Store your sudo password:

```bash
python cli.py store-credential sudo_password $USER "your_password"
```

### API key errors

Check your `.env` file has the correct `OPENAI_API_KEY`

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

## 🎯 Roadmap

- [ ] Frontend project generation (React, Vue, Angular)
- [ ] Docker container management
- [ ] Kubernetes deployment automation
- [ ] CI/CD pipeline generation
- [ ] Cloud provider integration (AWS, GCP, Azure)
- [ ] Multi-language support
- [ ] Voice control interface
- [ ] Visual project designer
- [ ] Team collaboration features
- [ ] Plugin system

---

**Built with ❤️ using OpenAI GPT-4, FastAPI, and Python**






