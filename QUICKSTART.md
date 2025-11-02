# Quick Start Guide

Get up and running with MCP DevOps Blueprint in 5 minutes!

### Option 1: Interactive Setup (Recommended)

```bash
python setup_interactive.py
```

## Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key (for AI client)
export OPENAI_API_KEY='your-api-key-here'

# 4. Test the server
python test_server.py

# 5. Run the client
python mcp_client.py
```

## Option 3: Docker Setup

```bash
# Build and run with Docker
docker-compose up --build

# Or build manually
docker build -t mcp-devops .
docker run -e OPENAI_API_KEY='your-key' mcp-devops
```

## Verify Installation

### Test the Server (No API Key Required)

```bash
python test_server.py
```

Expected output:
```
Starting MCP server...
✓ Server connected successfully!
✓ Found 3 tools:
  - search_repo
  - run_tests
  - generate_release_notes
...
```

### Test the Client (Requires API Key)

```bash
export OPENAI_API_KEY='your-key'
python mcp_client.py
```

## Common Issues

### Issue: Import errors
**Solution:** Make sure you're in the virtual environment and dependencies are installed

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "OPENAI_API_KEY not set"
**Solution:** Get an API key and set it

```bash
# Get key from: https://platform.openai.com/api-keys
export OPENAI_API_KEY='sk-proj-...'
```

### Issue: Tests fail
**Solution:** Make sure you're in a git repository

```bash
git init
git add .
git commit -m "Initial commit"
```

## What's Next?

1. **Explore examples:** `ls examples/` and run them
2. **Read the docs:** Check `README.md` for detailed info
3. **Customize:** Add your own tools to `mcp_server.py`
4. **Contribute:** See `CONTRIBUTING.md`

## Need Help?

- 📖 Read the [main README](README.md)
- 🐛 [Report issues](https://github.com/yourusername/mcp-blueprint/issues)
- 💬 [Start a discussion](https://github.com/yourusername/mcp-blueprint/discussions)

Happy coding! 🚀
