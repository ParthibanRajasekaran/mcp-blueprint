#!/usr/bin/env python3
"""
Simple test to check MCP client-server connection.
"""

import asyncio
import os

async def test_connection():
    """Test basic MCP connection."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    
    print("🔍 Testing MCP Connection...\n")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set (needed for full client)")
        print("   But we can still test server connection...\n")
    else:
        print(f"✅ API key found: {api_key[:20]}...\n")
    
    try:
        print("1️⃣ Creating server parameters...")
        params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )
        print("   ✅ Parameters created\n")
        
        print("2️⃣ Starting server subprocess...")
        async with stdio_client(params) as (stdio, write):
            print("   ✅ Server process started\n")
            
            print("3️⃣ Creating client session...")
            session = ClientSession(stdio, write)
            print("   ✅ Session created\n")
            
            print("4️⃣ Initializing session (this may take a moment)...")
            await asyncio.wait_for(session.initialize(), timeout=10.0)
            print("   ✅ Session initialized!\n")
            
            print("5️⃣ Listing available tools...")
            response = await session.list_tools()
            print(f"   ✅ Found {len(response.tools)} tools:")
            for tool in response.tools:
                print(f"      • {tool.name}: {tool.description[:60]}...")
            print()
            
        print("✅ All connection tests passed!")
        print("\n📝 Server is working correctly!")
        print("   You can now run: python mcp_client.py")
        return True
        
    except asyncio.TimeoutError:
        print("\n❌ Connection timed out!")
        print("   The server may not be responding properly.")
        print("   Try running the server directly: python mcp_server.py")
        return False
    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    exit(0 if success else 1)
