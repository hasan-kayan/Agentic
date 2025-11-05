# Quick Start Guide

Get up and running with AI Agent in 5 minutes!

## Prerequisites

- macOS 10.15+ or Linux (Ubuntu 20.04+)
- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation

### Step 1: Run the installer

```bash
chmod +x install.sh
./install.sh
```

This will:
- ✓ Check Python version
- ✓ Create virtual environment
- ✓ Install dependencies
- ✓ Initialize database
- ✓ Create configuration files

### Step 2: Configure API Key

Edit the `.env` file:

```bash
nano .env
```

Add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

Save and exit (Ctrl+X, Y, Enter).

### Step 3: (Optional) Store Sudo Password

For autonomous sudo operations:

```bash
source venv/bin/activate
python cli.py store-credential sudo_password $USER "your_password"
```

## First Steps

### 1. Chat with AI

```bash
source venv/bin/activate
python cli.py chat
```

Try asking:
- "How do I create a REST API?"
- "Write a Python function to sort a list"
- "Explain Docker to me"

### 2. Create Your First Project

```bash
python cli.py create-project my-first-api \
  -t backend \
  -l python \
  -f fastapi \
  -d "My first API project"
```

Your project will be created in `generated_projects/my-first-api/`

### 3. Explore the Project

```bash
cd generated_projects/my-first-api
cat README.md
```

### 4. Run the Generated API

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

Visit `http://localhost:8000/docs` to see the API documentation!

## Common Commands

```bash
# Chat
python cli.py chat "your message"

# Create projects
python cli.py create-project name -t backend -l python

# Execute commands
python cli.py execute "ls -la"

# Generate tests
python cli.py generate-tests file.py -l python

# Install tools
python cli.py install-tool docker

# Start API server
python -m api.main
```

## What's Next?

1. **Read the full documentation**: [README.md](README.md)
2. **See more examples**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
3. **Try autonomous mode**: `python cli.py autonomous enable`
4. **Create complex projects**: Ask AI to create fullstack apps, microservices, etc.

## Troubleshooting

### Python version error

Make sure you have Python 3.10 or higher:

```bash
python3 --version
```

### API key errors

Check your `.env` file has the correct key:

```bash
cat .env | grep OPENAI_API_KEY
```

### Permission errors

Store your sudo password:

```bash
python cli.py store-credential sudo_password $USER "your_password"
```

### Module not found

Make sure virtual environment is activated:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Need Help?

- Check [README.md](README.md) for detailed documentation
- See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for more examples
- Open an issue on GitHub

---

**You're ready to go! Start creating amazing projects with AI! 🚀**






