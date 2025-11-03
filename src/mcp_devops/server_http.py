"""
MCP Server configured for HTTP/SSE transport.
Run this in a separate terminal for testing.
"""

import argparse
import os
import uvicorn
from mcp_devops.server import create_server


def main_http() -> None:
    """Entry point for HTTP/SSE server.

    Supports overriding host/port via CLI flags or environment variables:
    - --host / HOST (default: 127.0.0.1)
    - --port / PORT (default: 8000)
    """
    parser = argparse.ArgumentParser(description="Run MCP HTTP/SSE server")
    parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"), help="Host interface to bind")
    parser.add_argument(
        "--port", type=int, default=int(os.getenv("PORT", "8000")), help="Port to listen on"
    )
    args = parser.parse_args()

    server = create_server()
    print(f"🚀 Starting MCP server on http://{args.host}:{args.port}/sse")
    print("   Press Ctrl+C to stop\n")
    # Run the FastMCP SSE ASGI app directly with uvicorn to control host/port
    uvicorn.run(server.sse_app, host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main_http()
