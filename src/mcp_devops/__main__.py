"""
MCP DevOps Server - Module entry point.

Default to running the HTTP/SSE transport for reliability.
"""
from .server_http import main_http

if __name__ == "__main__":
    main_http()
