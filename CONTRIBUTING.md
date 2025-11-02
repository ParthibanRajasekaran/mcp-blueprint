# Contributing to MCP DevOps Blueprint

First off, thank you for considering contributing to MCP DevOps Blueprint! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your Python version, OS, and any other relevant details**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guide (Black + Ruff)
* Include thoughtfully-worded, well-structured tests
* Document new code
* End all files with a newline

## Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/mcp-blueprint.git
cd mcp-blueprint

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Development Process

1. **Create a branch** from `main` for your changes
2. **Make your changes** and add tests
3. **Run the test suite** and ensure all tests pass
4. **Run the linters** and fix any issues
5. **Commit your changes** with clear commit messages
6. **Push to your fork** and submit a pull request

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific tests
pytest tests/test_server.py -v
```

## Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/
```

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Adding New Tools

To add a new tool to the MCP server:

```python
@mcp.tool
def your_tool_name(param1: str, param2: int = 10) -> dict:
    """
    Brief description of what the tool does.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
        
    Returns:
        Description of return value
        
    Example:
        your_tool_name("value", 20)
    """
    # Implementation
    return {"result": "success"}
```

## Documentation

* Use docstrings for all public modules, functions, classes, and methods
* Follow Google-style docstrings
* Update the README.md if you change functionality
* Comment your code where necessary

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉
