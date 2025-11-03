#!/usr/bin/env python3
"""
MCP Client using HTTP transport (recommended for production).
This works around the stdio transport issues in MCP SDK 1.20.0.
"""

import asyncio
import json
import os
import argparse
from openai import OpenAI
from mcp import ClientSession
from mcp.client.sse import sse_client

class PRAssistantHTTP:
    """An assistant that connects to MCP server via HTTP/SSE transport."""

    def __init__(self, server_url: str = "http://localhost:8000/sse"):
        self.server_url = server_url
        self.session: ClientSession | None = None
        self.sse_context = None
        # Defer OpenAI initialization until assist() to allow connection/tests without API key
        self.openai: OpenAI | None = None

    async def _execute_tool_calls(self, message, messages: list[dict]) -> list[dict]:
        """Execute tool calls from an OpenAI response and append results to messages."""
        if not self.session:
            return messages
        for tool_call in getattr(message, "tool_calls", []) or []:
            if hasattr(tool_call, "function"):
                tool_name = tool_call.function.name  # type: ignore[attr-defined]
                arguments = json.loads(tool_call.function.arguments)  # type: ignore[attr-defined]
                result = await self.session.call_tool(tool_name, arguments)
                result_content = result.content[0].text if result.content else str(result)  # type: ignore[union-attr]
                messages.append({
                    "role": "assistant",
                    "content": f"Called {tool_name}({arguments})",
                })
                messages.append({"role": "user", "content": result_content})
        return messages

    async def connect(self) -> None:
        """Connect to the MCP server via HTTP/SSE."""
        print(f"🔌 Connecting to {self.server_url}...")
        self.sse_context = sse_client(self.server_url)
        stdio, write = await self.sse_context.__aenter__()
        self.session = ClientSession(stdio, write)
        await self.session.initialize()
        print("✓ Connected!")
    
    async def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        if self.sse_context:
            try:
                await self.sse_context.__aexit__(None, None, None)
            except Exception:
                pass  # Ignore cleanup errors

    async def assist(self, query: str) -> str:
        """Handle a natural-language request and orchestrate tool calls accordingly."""
        if not self.session:
            raise RuntimeError("connect() must be called before assist().")
        # Lazy init OpenAI client here so connect/list can work without a key
        if self.openai is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is not set. "
                    "Please set it with: export OPENAI_API_KEY='your-api-key'"
                )
            self.openai = OpenAI(api_key=api_key)
        
        # Discover tools
        response = await self.session.list_tools()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                },
            }
            for t in response.tools
        ]

        messages = [{"role": "user", "content": query}]
        
        # Ask GPT to decide which tools to call
        completion = self.openai.chat.completions.create(
            model="gpt-4o", max_tokens=800, messages=messages, tools=tools  # type: ignore[arg-type]
        )
        message = completion.choices[0].message
        
        # Execute tool calls if any
        if message.tool_calls:
            messages = await self._execute_tool_calls(message, messages)
            # Final response
            final_completion = self.openai.chat.completions.create(
                model="gpt-4o", max_tokens=800, messages=messages  # type: ignore[arg-type]
            )
            return final_completion.choices[0].message.content or "No response"
        
        return message.content or "No response"


async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="MCP HTTP/SSE client")
    parser.add_argument(
        "--url",
        default=os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse"),
        help="MCP server SSE URL (default: http://localhost:8000/sse)",
    )
    args = parser.parse_args()

    assistant = PRAssistantHTTP(server_url=args.url)
    
    try:
        await assistant.connect()
        result = await assistant.assist(
            "Search for files containing 'MCP', run tests, and generate release notes from last 5 commits"
        )
        print("\n📝 Assistant response:")
        print(result)
    finally:
        await assistant.disconnect()


if __name__ == "__main__":
    print("\n⚠️  Note: This requires the server to be running separately:")
    print("   Start the server in another terminal, e.g.:")
    print("   python -m mcp_devops.server_http --host 127.0.0.1 --port 8000\n")
    asyncio.run(main())
