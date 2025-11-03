"""
Deprecated stdio client (removed).

This script used the MCP stdio transport which has known issues in MCP SDK 1.20.x.
Use the HTTP/SSE client instead:

  python mcp_client_http.py

Make sure the server is running in another terminal:

  python -m mcp_devops.server_http
"""

import sys

print("This script is deprecated. Use 'python mcp_client_http.py' instead.")
sys.exit(1)
