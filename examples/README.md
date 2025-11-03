"""Example README for the examples directory."""

# MCP DevOps Blueprint - Examples

This directory contains example scripts demonstrating various use cases of the MCP DevOps Blueprint.

## Examples

### 1. Basic Usage (`basic_usage.py`)
Demonstrates direct interaction with MCP server tools without AI orchestration.

```bash
python examples/basic_usage.py
```

**What it does:**
- Connects to the MCP server
- Lists available tools
- Executes each tool with example parameters
- Displays results

### 2. Custom Tools (`custom_tools.py`)
Shows how to extend the MCP server with your own custom tools.

```bash
python examples/custom_tools.py
```

**What it includes:**
- `check_docker_status` - Check Docker installation and status
- `list_git_branches` - List all branches in a repository
- `analyze_code_metrics` - Basic code metrics for Python files
- `create_deployment_checklist` - Generate deployment checklists

### 3. HTTP Client with OpenAI (root `mcp_client_http.py`)
AI-orchestrated workflow using OpenAI and the HTTP/SSE transport.

```bash
export OPENAI_API_KEY='your-openai-key'
python mcp_client_http.py
```

## Running the Examples

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **For AI-powered examples, set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY='sk-proj-...'
   ```

3. **Run any example:**
   ```bash
   python examples/[example_name].py
   ```

## Creating Your Own Examples

Feel free to create your own examples! Follow this pattern:

```python
import asyncio
from mcp_devops import PRAssistant

async def my_workflow():
    assistant = PRAssistant("mcp_server.py")
    await assistant.connect()
    
    result = await assistant.assist("Your natural language request here")
    print(result)
    
    await assistant.disconnect()

if __name__ == "__main__":
    asyncio.run(my_workflow())
```

## Need Help?

- Check the main [README.md](../README.md)
- Review the [CONTRIBUTING.md](../CONTRIBUTING.md) guide
- Open an issue on GitHub
