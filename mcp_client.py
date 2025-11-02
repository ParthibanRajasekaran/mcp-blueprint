"""
MCP Client for the "From Pull Request to Production" blueprint.

This client connects to the local MCP server via the stdio transport,
lists available tools and leverages the OpenAI API for tool selection.

See README.md for setup and usage instructions.
"""

import asyncio
import json
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

class PRAssistant:
    """An assistant that orchestrates pull-request workflows via an MCP server."""

    def __init__(self, server_script: str):
        self.server_script = server_script
        self.session: ClientSession | None = None
        self.stdio_context = None
        # Check if API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set it with: export OPENAI_API_KEY='your-api-key'"
            )
        self.openai = OpenAI(api_key=api_key)

    async def connect(self) -> None:
        """Spawn the MCP server and initialise an MCP client session."""
        params = StdioServerParameters(command="python", args=[self.server_script])
        self.stdio_context = stdio_client(params)
        stdio, write = await self.stdio_context.__aenter__()
        self.session = ClientSession(stdio, write)
        await self.session.initialize()
    
    async def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        if self.stdio_context:
            try:
                await self.stdio_context.__aexit__(None, None, None)
            except Exception:
                pass  # Ignore cleanup errors

    async def assist(self, query: str) -> str:
        """Handle a natural-language request and orchestrate tool calls accordingly."""
        if not self.session:
            raise RuntimeError("connect() must be called before assist().")
        # Discover tools
        response = await self.session.list_tools()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                }
            }
            for t in response.tools
        ]
        # Build the conversation for OpenAI
        messages = [
            {"role": "user", "content": query},
        ]
        model_response = self.openai.chat.completions.create(
            model="gpt-4o", max_tokens=800, messages=messages, tools=tools
        )
        final_text: list[str] = []
        choice = model_response.choices[0]
        message = choice.message
        
        # Add assistant's text response if present
        if message.content:
            final_text.append(message.content)
        
        # Execute any tool calls
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                result = await self.session.call_tool(tool_name, arguments)
                # Extract the content from the result
                result_content = result.content[0].text if result.content else str(result)
                final_text.append(f"\n[Tool {tool_name} result]\n{result_content}\n")
        return "".join(final_text)

async def main() -> None:
    # Use the modular server implementation
    assistant = PRAssistant("src/mcp_devops/server.py")
    try:
        print("🔌 Connecting to MCP server...")
        await assistant.connect()
        print("✓ Connected!\n")
        
        result = await assistant.assist(
            "Search for files containing 'MCP', run the tests, and generate release notes from the last 5 commits."
        )
        print("📝 Result:")
        print(result)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await assistant.disconnect()
        print("\n✓ Disconnected")

if __name__ == "__main__":
    asyncio.run(main())
