"""
Unit tests for MCP DevOps Client.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import os
from unittest.mock import Mock, patch


def test_client_import():
    """Test that client module can be imported."""
    from mcp_devops.client import PRAssistant
    assert PRAssistant is not None


def test_client_requires_api_key():
    """Test that client requires API key."""
    from mcp_devops.client import PRAssistant
    
    # Remove API key if present
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
            PRAssistant("test_server.py")


def test_client_accepts_api_key_parameter():
    """Test that client accepts API key as parameter."""
    from mcp_devops.client import PRAssistant
    
    # Should not raise with explicit API key
    with patch.dict(os.environ, {}, clear=True):
        assistant = PRAssistant("test_server.py", api_key="test-key")
        assert assistant is not None


def test_client_uses_env_api_key():
    """Test that client uses environment API key."""
    from mcp_devops.client import PRAssistant
    
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "env-test-key"}):
        assistant = PRAssistant("test_server.py")
        assert assistant is not None


def test_client_server_script_attribute():
    """Test that client stores server script path."""
    from mcp_devops.client import PRAssistant
    
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
        assistant = PRAssistant("my_server.py")
        assert assistant.server_script == "my_server.py"
