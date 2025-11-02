# 🚀 MCP DevOps Blueprint# From Pull Request to Production: MCP Blueprint



[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)This repository contains a minimal implementation of the **Model Context Protocol (MCP)** server and client described in the accompanying blog post. It demonstrates how to connect AI models to developer tooling to orchestrate common workflows such as searching code, running tests, generating release notes and coordinating PRs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)## Overview

[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io/)

- **mcp_server.py** defines an MCP server using [FastMCP](https://gofastmcp.com) that exposes three tools:

> **A production-ready implementation of the Model Context Protocol (MCP) for AI-powered DevOps automation**  - `search_repo`: search repository files for a keyword (case‑insensitive).

  - `run_tests`: execute unit tests via `pytest` and summarise failures.

Transform your development workflow by connecting AI models directly to your DevOps tools. This blueprint demonstrates how to build robust MCP servers and clients that orchestrate complex workflows through natural language.  - `generate_release_notes`: build release notes from recent commits.

- **mcp_client.py** defines a simple client that spawns the server via the stdio transport, lists available tools and uses the Anthropics API to decide which tools to call based on a natural-language request.

![MCP DevOps Architecture](https://via.placeholder.com/800x200/4A90E2/FFFFFF?text=AI-Powered+DevOps+Automation)

## Requirements

## ✨ Features

- Python 3.10+

- 🔍 **Smart Repository Search** - Find files across your codebase with AI-powered semantic search- [FastMCP](https://gofastmcp.com)

- 🧪 **Automated Testing** - Run tests and intelligently analyze failures- [GitPython](https://github.com/gitpython-developers/GitPython)

- 📝 **Release Note Generation** - Auto-generate release notes from git history- [pytest](https://docs.pytest.org/)

- 🤖 **AI Orchestration** - Let Claude decide which tools to use based on natural language requests- [anthropic](https://pypi.org/project/anthropic/)

- 🏗️ **Production-Ready** - Complete with error handling, logging, type hints, and comprehensive tests

- 📦 **Easy Integration** - Extensible architecture for adding your own toolsInstall dependencies with pip:



## 🎯 Quick Start```bash

pip install fastmcp gitpython pytest anthropic

### Prerequisites```



- Python 3.10 or higher## Usage

- Git repository (for full functionality)

- [Anthropic API key](https://console.anthropic.com/) (for AI client)1. **Run the server**



### Installation   Start the MCP server in one terminal:



```bash   ```bash

# Clone the repository   python mcp_server.py

git clone https://github.com/yourusername/mcp-blueprint.git   ```

cd mcp-blueprint

   The server uses the stdio transport by default and listens for JSON‑RPC messages via stdin/stdout.

# Create a virtual environment

python -m venv venv2. **Run the client**

source venv/bin/activate  # On Windows: venv\\Scripts\\activate

   In another terminal, run the client. It will spawn the server internally if not already running and then handle a natural-language query:

# Install dependencies

pip install -r requirements.txt   ```bash

   python mcp_client.py

# Or install as a package   ```

pip install -e .

```   The assistant will connect to the server, discover the available tools, send the query to the Anthropic API and execute the resulting tool calls. You should see a summary of test results and release notes printed to the console.



### Basic Usage## Security Considerations



#### Running the ServerThis sample implementation is for demonstration purposes. When building production servers and clients, follow the [MCP security best practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices) including:



```bash- Avoid logging to stdout when using the stdio transport.

# Using the new modular version- Verify all inbound requests and use secure session IDs.

python -m mcp_devops.server- Require explicit user consent before executing commands.

- Apply least‑privilege scopes to tokens.

# Or using the standalone script

python mcp_server.py## License

```

This project is provided for educational purposes under the MIT License.

The server exposes three tools via MCP:
- `search_repo` - Search repository files for keywords
- `run_tests` - Execute pytest and summarize results
- `generate_release_notes` - Create release notes from git commits

#### Using the AI Client

```bash
# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Run the client
python mcp_client.py
```

The client uses Claude to intelligently orchestrate workflows.

## 📖 Documentation

### Architecture

```
┌─────────────────┐
│   Claude API    │  Natural language understanding
└────────┬────────┘
         │
    ┌────▼─────┐
    │  Client  │  MCP Client (Anthropic SDK)
    └────┬─────┘
         │ JSON-RPC over stdio
    ┌────▼─────┐
    │  Server  │  MCP Server (FastMCP)
    └────┬─────┘
         │
    ┌────▼─────────────────┐
    │  DevOps Tools        │
    │  • Git               │
    │  • pytest            │
    │  • Custom scripts    │
    └──────────────────────┘
```

### Adding Custom Tools

```python
from mcp_devops import create_server

mcp = create_server()

@mcp.tool
def deploy_to_staging(branch: str) -> dict:
    """Deploy a branch to staging environment."""
    return {"status": "deployed", "url": "https://staging.example.com"}

mcp.run()
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Test the server without AI
python test_server.py
```

## 📦 Project Structure

```
mcp-blueprint/
├── src/
│   └── mcp_devops/          # Modern package structure
│       ├── __init__.py
│       ├── server.py        # MCP server implementation
│       └── client.py        # AI-powered client
├── tests/
├── examples/
├── mcp_server.py            # Standalone server
├── mcp_client.py            # Standalone client
├── pyproject.toml           # Modern Python packaging
└── README.md
```

## 🔒 Security

This implementation follows [MCP security best practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices):

- ✅ No stdout logging (when using stdio transport)
- ✅ Input validation on all tool parameters
- ✅ Timeout protection on long-running operations
- ✅ Error handling and sanitization

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Anthropic](https://www.anthropic.com/) - Claude API
- [FastMCP](https://gofastmcp.com/)

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io/docs)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Anthropic Claude API](https://docs.anthropic.com/)

## 💡 Use Cases

- **CI/CD Automation** - Intelligent build workflows
- **Code Review** - Automated PR analysis
- **Documentation** - Auto-generate docs
- **Monitoring** - Intelligent incident response

---

**Made with ❤️ for the developer community** | [Report Bug](https://github.com/yourusername/mcp-blueprint/issues) | [Request Feature](https://github.com/yourusername/mcp-blueprint/issues)
