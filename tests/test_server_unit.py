"""
Unit tests for MCP DevOps Server.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from mcp_devops.server import create_server


def test_create_server():
    """Test that server can be created."""
    server = create_server("test-server")
    assert server is not None
    assert hasattr(server, 'run')


def test_server_has_tools():
    """Test that server has the expected tools."""
    server = create_server()
    # The server should have tools registered
    assert hasattr(server, 'tool')


# Note: More comprehensive integration tests would require
# actually running the server and testing tool execution.
# These are simplified unit tests for CI/CD demonstration.


@pytest.mark.asyncio
async def test_server_initialization():
    """Test server can be initialized."""
    server = create_server("test-init-server")
    assert server is not None
