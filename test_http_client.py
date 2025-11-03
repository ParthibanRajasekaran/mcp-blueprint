#!/usr/bin/env python3
"""
Quick test script for the HTTP MCP client.
Make sure to:
1. Start the server: python -m mcp_devops.server_http
2. Set OPENAI_API_KEY: export OPENAI_API_KEY='your-key'
3. Run this: python test_http_client.py
"""

import asyncio
import os
from mcp_client_http import PRAssistantHTTP


async def test_simple_query():
    """Test connecting and listing tools via HTTP (no OpenAI key required)."""
    print("🧪 Testing HTTP MCP connection...")

    server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse")
    assistant = PRAssistantHTTP(server_url=server_url)
    
    try:
        # Just test connection and list tools
        await assistant.connect()
        
        if assistant.session:
            response = await assistant.session.list_tools()
            print(f"\n✅ Successfully connected! Found {len(response.tools)} tools:")
            for tool in response.tools:
                print(f"   - {tool.name}: {tool.description}")
        
        print("\n✅ HTTP transport is working!\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("Make sure the server is running (and URL matches):")
        print("   python -m mcp_devops.server_http --host 127.0.0.1 --port 8000")
        print("Or set MCP_SERVER_URL if using a custom port, e.g.:")
        print("   export MCP_SERVER_URL=http://localhost:8001/sse\n")
    finally:
        await assistant.disconnect()


if __name__ == "__main__":
    asyncio.run(test_simple_query())
