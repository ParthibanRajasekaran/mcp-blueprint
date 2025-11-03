#!/usr/bin/env python3
"""
Quick test to verify HTTP transport works.
Requires server running: python -m mcp_devops.server_http
"""

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def test_http_transport():
    """Test that HTTP transport works correctly."""
    print("Testing HTTP/SSE transport...")
    print("(Assumes server is running at http://localhost:8000/sse)\n")
    
    try:
        async with sse_client("http://localhost:8000/sse") as (read, write):
            print("✅ Connected to server")
            
            session = ClientSession(read, write)
            await session.initialize()
            print("✅ Session initialized")
            
            # List tools
            tools_response = await session.list_tools()
            print(f"✅ Found {len(tools_response.tools)} tools:")
            for tool in tools_response.tools:
                print(f"   - {tool.name}")
            
            # Call a tool
            print("\n Testing search_repo tool...")
            result = await session.call_tool("search_repo", {"keyword": "test", "root": "."})
            print(f"✅ Tool executed successfully")
            
            if result.content:
                content = result.content[0]
                if hasattr(content, 'text'):
                    files = eval(content.text) if content.text.startswith('[') else []
                    print(f"   Found {len(files)} files containing 'test'")
            
            print("\n🎉 HTTP transport is WORKING!")
            return True
            
    except ConnectionRefusedError:
        print("❌ Connection refused - is the server running?")
        print("\n   Start it with: python -m mcp_devops.server_http")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_http_transport())
    exit(0 if success else 1)
