"""
MCP Client for AI-powered DevOps workflows.

This client connects to an MCP server and uses Claude to orchestrate
complex development workflows through natural language.
"""

import asyncio
import os
from contextlib import AbstractAsyncContextManager
from typing import Any, Optional

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class PRAssistant:
    """
    An AI assistant that orchestrates DevOps workflows via an MCP server.

    This client connects to a local MCP server, discovers available tools,
    and uses Claude to intelligently select and execute them based on
    natural language requests.

    Example:
        >>> assistant = PRAssistant("server.py")
        >>> await assistant.connect()
        >>> result = await assistant.assist("Run tests and generate release notes")
        >>> print(result)
    """

    def __init__(self, server_script: str, api_key: Optional[str] = None):
        """
        Initialize the PR Assistant.

        Args:
            server_script: Path to the MCP server script
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)

        Raises:
            ValueError: If API key is not provided and not in environment
        """
        self.server_script = server_script
        self.session: Optional[ClientSession] = None
        self.stdio_context: Optional[AbstractAsyncContextManager[Any]] = None

        # Get API key from parameter or environment
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is required. Set it via environment variable:\n"
                "  export ANTHROPIC_API_KEY='your-api-key'\n"
                "Or pass it to the constructor:\n"
                "  PRAssistant('server.py', api_key='your-api-key')"
            )
        self.anthropic = Anthropic(api_key=api_key)

    async def connect(self) -> None:
        """
        Connect to the MCP server.

        Spawns the server process and establishes a client session.

        Raises:
            RuntimeError: If connection fails
        """
        try:
            params = StdioServerParameters(command="python", args=[self.server_script])
            self.stdio_context = stdio_client(params)
            stdio, write = await self.stdio_context.__aenter__()
            self.session = ClientSession(stdio, write)
            await self.session.initialize()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to MCP server: {e}") from e

    async def disconnect(self) -> None:
        """Disconnect from the MCP server and clean up resources."""
        if self.stdio_context:
            try:
                await self.stdio_context.__aexit__(None, None, None)
            except Exception:
                pass  # Ignore cleanup errors
            finally:
                self.stdio_context = None
                self.session = None

    async def assist(self, query: str, model: str = "claude-3-5-sonnet-20241022") -> str:
        """
        Process a natural language request using AI and available tools.

        Args:
            query: Natural language description of the desired workflow
            model: Claude model to use (default: claude-3-5-sonnet-20241022)

        Returns:
            The assistant's response, including tool execution results

        Raises:
            RuntimeError: If not connected to server

        Example:
            >>> result = await assistant.assist(
            ...     "Search for TODO comments and run the tests"
            ... )
        """
        if not self.session:
            raise RuntimeError(
                "Not connected to server. Call connect() first."
            )

        # Discover available tools
        response = await self.session.list_tools()
        tools = [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.inputSchema,
            }
            for t in response.tools
        ]

        # Build conversation for Claude
        messages: Any = [{"role": "user", "content": query}]

        # Get response from Claude with tool support
        model_response = self.anthropic.messages.create(
            model=model,
            max_tokens=2000,
            messages=messages,
            tools=tools,  # type: ignore[arg-type]
        )

        # Process response and execute tools
        final_text: list[str] = []
        for part in model_response.content:
            if part.type == "text" and hasattr(part, "text"):
                final_text.append(part.text)
            elif part.type == "tool_use":
                # Execute the requested tool
                tool_name = part.name
                arguments = part.input

                try:
                    result = await self.session.call_tool(tool_name, arguments)
                    # Extract content from result
                    result_content = str(result)
                    if result.content:
                        first_content = result.content[0]
                        if hasattr(first_content, "text"):
                            result_content = first_content.text  # type: ignore[attr-defined]
                    final_text.append(f"\n[Tool: {tool_name}]\n{result_content}\n")
                except Exception as e:
                    final_text.append(f"\n[Tool {tool_name} failed: {e}]\n")

        return "".join(final_text)


async def main() -> None:
    """Example usage of the PR Assistant."""
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable not set.")
        print("\nTo use this client:")
        print("1. Get an API key from: https://console.anthropic.com/")
        print("2. Set it: export ANTHROPIC_API_KEY='your-key'")
        print("3. Run this script again")
        return

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
    finally:
        await assistant.disconnect()
        print("\n✓ Disconnected")


if __name__ == "__main__":
    asyncio.run(main())
