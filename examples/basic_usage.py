"""
Basic Example: Using MCP Server Tools Directly

This example demonstrates how to interact with the MCP server
without using the AI client.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def basic_example():
    """Demonstrate basic MCP server tool usage."""
    print("🚀 MCP DevOps Blueprint - Basic Example\n")
    print("=" * 50)
    
    # Connect to server
    print("\n1️⃣  Connecting to MCP server...")
    params = StdioServerParameters(command="python", args=["mcp_server.py"])
    
    async with stdio_client(params) as (stdio, write):
        session = ClientSession(stdio, write)
        await session.initialize()
        print("✅ Connected!\n")
        
        # List available tools
        print("2️⃣  Discovering available tools...")
        response = await session.list_tools()
        print(f"✅ Found {len(response.tools)} tools:\n")
        for tool in response.tools:
            print(f"   📦 {tool.name}")
            print(f"      {tool.description}\n")
        
        # Example 1: Search repository
        print("3️⃣  Example 1: Searching for 'MCP' in repository...")
        result = await session.call_tool("search_repo", {
            "keyword": "MCP",
            "root": "."
        })
        content = result.content[0].text if result.content else "No results"
        print(f"✅ Found files: {content}\n")
        
        # Example 2: Generate release notes
        print("4️⃣  Example 2: Generating release notes...")
        result = await session.call_tool("generate_release_notes", {
            "max_commits": 5
        })
        content = result.content[0].text if result.content else "No commits"
        print(f"✅ Release notes:\n{content}\n")
        
        # Example 3: Run tests
        print("5️⃣  Example 3: Running tests...")
        result = await session.call_tool("run_tests", {
            "test_path": "tests"
        })
        content = result.content[0].text if result.content else "No test results"
        print(f"✅ Test results: {content}\n")
        
    print("=" * 50)
    print("✅ Example completed successfully!\n")


if __name__ == "__main__":
    asyncio.run(basic_example())
