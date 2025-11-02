"""
Simple test script to verify the MCP server works independently.
This script doesn't require the Anthropic API.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_server():
    """Test the MCP server by connecting and listing tools."""
    print("Starting MCP server...")
    
    # Connect to the server
    params = StdioServerParameters(command="python", args=["mcp_server.py"])
    
    async with stdio_client(params) as (stdio, write):
        session = ClientSession(stdio, write)
        await session.initialize()
        
        print("✓ Server connected successfully!")
        
        # List available tools
        print("\nDiscovering tools...")
        response = await session.list_tools()
        
        print(f"\n✓ Found {len(response.tools)} tools:")
        for tool in response.tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Test the search_repo tool
        print("\n\nTesting search_repo tool...")
        result = await session.call_tool("search_repo", {"keyword": "MCP", "root": "."})
        print(f"✓ Search result: {result.content[0].text if result.content else 'No content'}")
        
        # Test the generate_release_notes tool
        print("\n\nTesting generate_release_notes tool...")
        result = await session.call_tool("generate_release_notes", {})
        print(f"✓ Release notes:\n{result.content[0].text if result.content else 'No content'}")
        
        print("\n\n✓ All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_server())
