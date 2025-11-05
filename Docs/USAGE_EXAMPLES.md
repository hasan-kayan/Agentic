# AI Agent Usage Examples

This document provides comprehensive examples of how to use the AI Agent system.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Chat Examples](#chat-examples)
3. [Project Generation](#project-generation)
4. [Terminal Commands](#terminal-commands)
5. [Test Generation](#test-generation)
6. [Documentation Generation](#documentation-generation)
7. [Autonomous Mode](#autonomous-mode)
8. [API Usage](#api-usage)

## Getting Started

### Initialize the system

```bash
python cli.py init
```

### Store your credentials

```bash
python cli.py store-credential sudo_password $USER "your_password"
```

## Chat Examples

### Interactive Chat

```bash
python cli.py chat
```

Then interact:

```
You: How do I create a REST API in Python?
AI: I'll help you create a REST API in Python using FastAPI...

You: Can you generate the code for a user authentication endpoint?
AI: Sure! Here's a complete user authentication endpoint...
```

### Single Message

```bash
python cli.py chat "Explain the difference between async and sync in Python"
```

### Streaming Response

```bash
python cli.py chat "Write a binary search algorithm" --stream
```

## Project Generation

### Python FastAPI Backend

```bash
python cli.py create-project blog-api \
  -t backend \
  -l python \
  -f fastapi \
  -d "A blog API with posts and comments"
```

This creates:
```
blog-api/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── routes/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── core/
├── tests/
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

### Node.js Express Backend

```bash
python cli.py create-project user-service \
  -t backend \
  -l javascript \
  -f express
```

### TypeScript Backend

```bash
python cli.py create-project api-gateway \
  -t backend \
  -l typescript \
  -f express
```

### Go Backend

```bash
python cli.py create-project microservice \
  -t backend \
  -l go
```

### Custom Output Directory

```bash
python cli.py create-project my-app \
  -t backend \
  -l python \
  -o /path/to/custom/location
```

## Terminal Commands

### Execute Simple Command

```bash
python cli.py execute "ls -la"
```

### Execute with Sudo

```bash
python cli.py execute "apt-get update" --sudo
```

### Execute in Specific Directory

```bash
python cli.py execute "npm install" --cwd /path/to/project
```

### Complex Commands

```bash
python cli.py execute "docker ps -a && docker images"
```

## Test Generation

### Generate Tests for a File

```bash
python cli.py generate-tests ./app/models.py \
  -l python \
  -o ./tests/test_models.py
```

### Generate Tests for JavaScript

```bash
python cli.py generate-tests ./src/utils.js \
  -l javascript \
  -o ./tests/utils.test.js
```

### Using AI Chat for Tests

```bash
python cli.py chat "Generate unit tests for this code: [paste your code]"
```

## Documentation Generation

### Generate README

```bash
python cli.py generate-docs ./my-project --type readme
```

### Using Chat for Documentation

```bash
python cli.py chat "Generate API documentation for my FastAPI project at ./blog-api"
```

### Generate Inline Documentation

```bash
python cli.py chat "Add docstrings to this Python code: [paste code]"
```

## Autonomous Mode

### Enable Autonomous Mode

```bash
python cli.py autonomous enable
```

### Check Status

```bash
python cli.py autonomous status
```

Output:
```
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Setting              ┃ Value   ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ Enabled              │ True    │
│ Actions              │ 0/100   │
│ Require Confirmation │ False   │
└━━━━━━━━━━━━━━━━━━━━━━┴━━━━━━━━━┘
```

### Disable Autonomous Mode

```bash
python cli.py autonomous disable
```

### Example: Full Autonomous Workflow

```bash
# Enable autonomous mode
python cli.py autonomous enable

# Tell AI to create a complete project with tests and docs
python cli.py chat "Create a REST API for a todo app with:
- Python FastAPI
- SQLAlchemy models
- CRUD operations
- Unit tests
- API documentation
- Docker setup
Install any needed tools and run the tests"

# AI will automatically:
# 1. Create the project structure
# 2. Install required tools (docker, etc.)
# 3. Generate all code files
# 4. Write unit tests
# 5. Create documentation
# 6. Run the tests
```

## API Usage

### Start the API Server

```bash
python -m api.main
```

Or with uvicorn:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I deploy a FastAPI app?",
    "session_id": "user123"
  }'
```

### Create Project Endpoint

```bash
curl -X POST "http://localhost:8000/api/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-api",
    "project_type": "backend",
    "language": "python",
    "framework": "fastapi",
    "description": "My REST API"
  }'
```

### Execute Command Endpoint

```bash
curl -X POST "http://localhost:8000/api/terminal/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "ls -la",
    "use_sudo": false
  }'
```

### Store Credential Endpoint

```bash
curl -X POST "http://localhost:8000/api/credentials/" \
  -H "Content-Type: application/json" \
  -d '{
    "credential_type": "api_key",
    "identifier": "github",
    "value": "ghp_xxxxxxxxxxxxx",
    "description": "GitHub API key"
  }'
```

### Enable Autonomous Mode

```bash
curl -X POST "http://localhost:8000/api/autonomous/enable"
```

### Grant Permission

```bash
curl -X POST "http://localhost:8000/api/autonomous/permissions" \
  -H "Content-Type: application/json" \
  -d '{
    "permission_type": "terminal",
    "scope": "/home/user/projects/*",
    "grant_level": "moderate",
    "duration_hours": 24,
    "requires_confirmation": false
  }'
```

## Advanced Examples

### Example 1: Debug and Fix Error

```bash
python cli.py chat "I'm getting this error when running my Flask app:
ImportError: cannot import name 'Flask' from 'flask'

The error is in app.py line 1. Please help me fix it."
```

AI Response:
```
The error suggests Flask is not installed. Let me fix this for you:

1. The issue is that Flask is not installed in your environment
2. Solution: Install Flask using pip

I'll install it for you:
[Executes: pip install flask]

✓ Flask has been installed successfully. 
Your import should now work. If you're using a virtual environment, 
make sure it's activated.
```

### Example 2: Complete Project with Deployment

```bash
python cli.py chat "Create a URL shortener API with:
- Python FastAPI
- PostgreSQL database
- Redis caching
- Docker compose setup
- Kubernetes deployment files
- CI/CD with GitHub Actions
- Complete documentation

Deploy it locally using Docker"
```

### Example 3: Analyze and Improve Code

```bash
python cli.py chat "Analyze this code and suggest improvements:

def get_user(id):
    user = db.query('SELECT * FROM users WHERE id = ' + str(id))
    return user
"
```

AI Response will include:
- Security issues (SQL injection)
- Best practices violations
- Performance improvements
- Corrected code

### Example 4: Install and Configure Tools

```bash
python cli.py install-tool docker
python cli.py install-tool kubectl
python cli.py install-tool terraform
```

### Example 5: Batch Operations

```bash
python cli.py chat "Do these tasks:
1. Create a FastAPI project called 'api'
2. Add authentication endpoints
3. Add database models for users
4. Generate tests for all endpoints
5. Create Docker setup
6. Generate documentation
7. Run the tests"
```

## Tips and Best Practices

1. **Be Specific**: The more specific your request, the better the result
2. **Use Autonomous Mode Carefully**: Start with it disabled, then enable for trusted operations
3. **Review Generated Code**: Always review before deploying to production
4. **Set Permission Scopes**: Limit autonomous operations to specific directories
5. **Use Sessions**: Keep related conversations in the same session for context
6. **Save Credentials Securely**: Always use the encrypted credential storage

## Troubleshooting

### "Permission Denied"

Store your sudo password:
```bash
python cli.py store-credential sudo_password $USER "your_password"
```

### "Command Not Found"

Install the required tool:
```bash
python cli.py install-tool <tool-name>
```

### API Key Errors

Check your `.env` file:
```bash
cat .env | grep OPENAI_API_KEY
```

---

For more examples and documentation, see the [README.md](README.md) file.






