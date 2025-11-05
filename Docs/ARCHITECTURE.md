# AI Agent Architecture

## System Overview

AI Agent is a sophisticated autonomous AI system designed to control macOS/Linux environments, generate complete projects, and assist with all aspects of software development. The system is built with a modular architecture that separates concerns and allows for easy extension.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interfaces                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  CLI (Typer) │  │  Web API     │  │  Python API  │      │
│  │              │  │  (FastAPI)   │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Core AI Agent                           │
│  ┌────────────────────────────────────────────────────┐     │
│  │  AI Agent (OpenAI GPT-4 Integration)               │     │
│  │  - Natural language understanding                  │     │
│  │  - Context management                              │     │
│  │  - Task planning and execution                     │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  Execution Layer │ │ Data Layer   │ │  Security Layer  │
├──────────────────┤ ├──────────────┤ ├──────────────────┤
│ - Terminal       │ │ - Main DB    │ │ - Credential Mgr │
│ - File System    │ │ - Personal DB│ │ - Encryption     │
│ - Web Search     │ │ - ORM        │ │ - Permissions    │
│ - Tool Install   │ │              │ │                  │
└──────────────────┘ └──────────────┘ └──────────────────┘
```

## Core Components

### 1. AI Agent Core (`core/ai_agent.py`)

The central brain of the system powered by OpenAI GPT-4.

**Responsibilities:**
- Process natural language requests
- Maintain conversation context
- Plan and coordinate complex tasks
- Generate code and solutions

**Key Features:**
- Session-based conversation history
- Streaming responses
- Context-aware decision making
- Multi-step task execution

### 2. Terminal Executor (`core/terminal_executor.py`)

Handles all system command execution.

**Responsibilities:**
- Execute shell commands
- Manage sudo operations
- Install system packages
- Monitor command output

**Key Features:**
- Cross-platform support (macOS/Linux)
- Secure sudo password handling
- Timeout management
- Output capture and logging

### 3. Project Generator (`core/project_generator.py`)

Creates complete project structures.

**Responsibilities:**
- Generate project scaffolding
- Create configuration files
- Set up dependencies
- Initialize version control

**Supported Project Types:**
- Backend (Python, Node.js, Go, Rust)
- Frontend (React, Vue - coming soon)
- Fullstack
- CLI applications

### 4. Error Handler (`core/error_handler.py`)

Automatic error detection and fixing.

**Responsibilities:**
- Parse error messages
- Identify error patterns
- Generate fixes
- Apply fixes automatically

**Error Types Handled:**
- Syntax errors
- Import errors
- Type errors
- Runtime errors
- Dependency issues

### 5. Test Generator (`core/test_generator.py`)

Automatic test generation.

**Responsibilities:**
- Analyze code structure
- Generate unit tests
- Create integration tests
- Generate test fixtures

**Supported Frameworks:**
- Python: pytest, unittest
- JavaScript: Jest, Mocha
- Go: testing package
- Others: Auto-detected

### 6. Documentation Generator (`core/documentation_generator.py`)

Automatic documentation generation.

**Responsibilities:**
- Generate README files
- Create API documentation
- Add inline documentation
- Build MkDocs sites

**Documentation Types:**
- README.md
- API reference
- Architecture docs
- Inline docstrings
- Changelog

### 7. Web Searcher (`core/web_search.py`)

Research capability via web search.

**Responsibilities:**
- Search for code examples
- Find documentation
- Research best practices
- Discover solutions to errors

**Features:**
- DuckDuckGo integration
- Result caching
- Relevance filtering

### 8. Autonomous Manager (`core/autonomous_manager.py`)

Permission and autonomous operation control.

**Responsibilities:**
- Manage permissions
- Track action counts
- Enforce safety limits
- Handle confirmations

**Permission Types:**
- Terminal access
- File system operations
- Network access
- Sudo operations

### 9. Tool Installer (`core/tool_installer.py`)

Automatic tool installation.

**Responsibilities:**
- Detect missing tools
- Install packages
- Configure tools
- Verify installations

**Supported Tools:**
- Docker, Kubernetes
- Node.js, npm, yarn
- Python, pip
- Go, Rust, Cargo
- Cloud CLIs (AWS, GCP)
- Databases (PostgreSQL, MySQL, MongoDB)

### 10. Credential Manager (`core/credential_manager.py`)

Secure credential storage.

**Responsibilities:**
- Encrypt sensitive data
- Store credentials securely
- Retrieve when needed
- Manage credential lifecycle

**Credential Types:**
- Sudo passwords
- API keys
- SSH keys
- Database credentials
- Cloud credentials

## Data Layer

### Main Database (`database/models.py`)

Stores operational data:

**Tables:**
- `projects` - Generated projects
- `tasks` - Task tracking
- `actions` - Action history
- `conversations` - Chat history
- `error_logs` - Error tracking
- `search_queries` - Search history
- `documentation` - Generated docs

### Personalization Database (`database/personalization_models.py`)

Stores sensitive user data:

**Tables:**
- `credentials` - Encrypted credentials
- `user_preferences` - User settings
- `system_info` - System configuration
- `learning_data` - AI learning patterns
- `permission_grants` - Permission records

### Database Technology

- **SQLAlchemy**: ORM
- **Alembic**: Migrations
- **SQLite**: Default (development)
- **PostgreSQL**: Production-ready

## Security Architecture

### Encryption

- **Algorithm**: Fernet (symmetric encryption)
- **Key Derivation**: PBKDF2 with SHA256
- **Usage**: All sensitive data encrypted at rest

### Permission System

```
Permission Grant
├── Type (terminal, file_system, network, sudo)
├── Scope (specific paths or patterns)
├── Level (limited, moderate, full)
├── Duration (time-based expiration)
└── Confirmation (require user approval)
```

### Security Principles

1. **Defense in Depth**: Multiple security layers
2. **Least Privilege**: Minimal permissions by default
3. **Encryption at Rest**: All sensitive data encrypted
4. **Audit Logging**: All actions logged
5. **User Control**: User has final say

## API Layer

### FastAPI Application (`api/main.py`)

RESTful API for web access.

**Endpoints:**
- `/api/chat` - Chat interface
- `/api/projects/*` - Project management
- `/api/tasks/*` - Task management
- `/api/terminal/*` - Command execution
- `/api/credentials/*` - Credential management
- `/api/autonomous/*` - Autonomous control
- `/api/documentation/*` - Documentation generation

### CLI Application (`cli.py`)

Command-line interface using Typer.

**Commands:**
- `chat` - Interactive or single-message chat
- `create-project` - Project generation
- `execute` - Command execution
- `generate-tests` - Test generation
- `generate-docs` - Documentation
- `autonomous` - Autonomous mode control
- `install-tool` - Tool installation

## Data Flow

### Example: Create a Project

```
1. User → CLI/API: "Create Python FastAPI project"
   │
   ▼
2. AI Agent: Parse request, plan steps
   │
   ▼
3. Project Generator: Create structure
   │
   ├─→ File System: Write files
   ├─→ Terminal: Install dependencies
   └─→ Database: Store project record
   │
   ▼
4. Response to User: "Project created at /path"
```

### Example: Execute Sudo Command

```
1. User → Terminal Executor: Execute with sudo
   │
   ▼
2. Autonomous Manager: Check permissions
   │
   ├─→ If permitted → Continue
   └─→ If not → Request confirmation
   │
   ▼
3. Credential Manager: Get sudo password
   │
   ▼
4. Terminal: Execute with pexpect
   │
   ▼
5. Database: Log action
   │
   ▼
6. Response to User: Command output
```

## Extension Points

### Adding New Project Types

1. Create generator in `project_generator.py`
2. Add template structures
3. Update routing logic

### Adding New Languages

1. Add error patterns in `error_handler.py`
2. Add test framework mapping in `test_generator.py`
3. Update language detection

### Adding New Tools

1. Add installation commands in `tool_installer.py`
2. Add detection logic
3. Update documentation

## Performance Considerations

### Optimization Strategies

1. **Async I/O**: All I/O operations are async
2. **Connection Pooling**: Database connection pooling
3. **Caching**: Permission and tool detection caching
4. **Streaming**: Streaming responses for better UX
5. **Batch Operations**: Batch database operations

### Scalability

- **Horizontal**: Multiple API instances
- **Database**: PostgreSQL for production
- **Caching**: Redis integration ready
- **Queue**: Background task processing

## Monitoring and Logging

### Logging Strategy

- **Loguru**: Structured logging
- **Levels**: DEBUG, INFO, WARNING, ERROR
- **Rotation**: 10MB rotation
- **Retention**: 1 week

### Audit Trail

All operations logged to database:
- User actions
- AI decisions
- System commands
- Permission checks
- Errors and fixes

## Testing Strategy

### Unit Tests

- Core functionality
- Individual components
- Mocking external services

### Integration Tests

- API endpoints
- Database operations
- Multi-component workflows

### Test Coverage

Target: >80% code coverage

## Deployment

### Development

```bash
python cli.py init
python -m api.main
```

### Production

```bash
# Use production database
DATABASE_URL=postgresql://...

# Use gunicorn/uvicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Enable authentication
# Set up reverse proxy (nginx)
# Configure SSL/TLS
```

### Docker Deployment

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
```

## Future Enhancements

1. **Multi-User Support**: User authentication and isolation
2. **Webhook Integration**: External service integration
3. **Plugin System**: User-developed extensions
4. **Distributed Execution**: Multi-machine coordination
5. **ML Model Fine-tuning**: Custom model training
6. **Visual Interface**: Web-based UI
7. **Voice Control**: Speech interface
8. **Team Collaboration**: Shared projects and history

## Dependencies

### Core
- OpenAI API (GPT-4)
- FastAPI (Web framework)
- SQLAlchemy (ORM)
- Pydantic (Data validation)

### System Integration
- pexpect (Terminal control)
- psutil (System info)

### Search
- duckduckgo-search (Web search)
- beautifulsoup4 (HTML parsing)

### CLI
- typer (CLI framework)
- rich (Terminal formatting)

### Security
- cryptography (Encryption)
- passlib (Password hashing)

## Contributing

See main README.md for contribution guidelines.

## License

MIT License - See LICENSE file.



