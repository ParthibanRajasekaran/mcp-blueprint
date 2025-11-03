"""
Basic Example: Using MCP Server Tools via HTTP/SSE

This example demonstrates how to interact with the MCP server
without using the AI client. Requires the server running:

  python -m mcp_devops.server_http
"""

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def basic_example():
    """Demonstrate basic MCP server tool usage over HTTP/SSE."""
    print("🚀 MCP DevOps Blueprint - Basic Example (HTTP/SSE)\n")
    print("=" * 50)

    print("\n1️⃣  Connecting to MCP server over HTTP/SSE...")
    async with sse_client("http://localhost:8000/sse") as (read, write):
        session = ClientSession(read, write)
        await session.initialize()
        print("✅ Connected!\n")

        # List available tools
        print("2️⃣  Discovering available tools...")
        response = await session.list_tools()
        print(f"✅ Found {len(response.tools)} tools:\n")
        for tool in response.tools:
            print(f"   📦 {tool.name}")
            print(f"      {tool.description}\n")

        # Small helper to extract readable text from a tool result
        def _as_text(res) -> str:
            try:
                if not res or not getattr(res, "content", None):
                    return ""
                parts = []
                for item in res.content:
                    # Prefer items that expose textual content
                    text = getattr(item, "text", None)
                    if isinstance(text, str):
                        parts.append(text)
                    else:
                        parts.append(str(item))
                return "\n".join(parts)
            except Exception:
                return str(res)

        # Example 1: Search repository
        print("3️⃣  Example 1: Searching for 'MCP' in repository...")
        result = await session.call_tool("search_repo", {
            "keyword": "MCP",
            "root": "."
        })
        content = _as_text(result) or "No results"
        print(f"✅ Found files: {content}\n")

        # Example 2: Generate release notes
        print("4️⃣  Example 2: Generating release notes...")
        result = await session.call_tool("generate_release_notes", {
            "max_commits": 5
        })
        content = _as_text(result) or "No commits"
        print(f"✅ Release notes:\n{content}\n")

        # Example 3: Run tests
        print("5️⃣  Example 3: Running tests...")
        result = await session.call_tool("run_tests", {
            "test_path": "tests"
        })
        content = _as_text(result) or "No test results"
        print(f"✅ Test results: {content}\n")

    print("=" * 50)
    print("✅ Example completed successfully!\n")


if __name__ == "__main__":
    asyncio.run(basic_example())
