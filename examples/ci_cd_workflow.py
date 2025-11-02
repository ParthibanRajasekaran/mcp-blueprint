"""
Integration Example: Complete CI/CD Workflow

This example demonstrates a complete CI/CD workflow using the
MCP client with AI orchestration.
"""

import asyncio
import os
from mcp_devops import PRAssistant


async def ci_cd_workflow():
    """Run a complete CI/CD workflow with AI assistance."""
    print("🚀 MCP DevOps - Complete CI/CD Workflow Example\n")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set!")
        print("\n📝 To run this example:")
        print("   1. Get API key from: https://console.anthropic.com/")
        print("   2. Set it: export ANTHROPIC_API_KEY='your-key'")
        print("   3. Run this script again")
        return
    
    assistant = PRAssistant("mcp_server.py")
    
    try:
        print("\n🔌 Connecting to MCP server...")
        await assistant.connect()
        print("✅ Connected!\n")
        
        # Scenario 1: Pre-deployment checks
        print("📋 Scenario 1: Pre-deployment checks")
        print("-" * 60)
        result = await assistant.assist(
            "Run all tests and tell me if they pass. "
            "If they fail, summarize the failures."
        )
        print(result)
        print()
        
        # Scenario 2: Code quality check
        print("\n📋 Scenario 2: Code quality check")
        print("-" * 60)
        result = await assistant.assist(
            "Search the repository for TODO and FIXME comments. "
            "List the files that contain them."
        )
        print(result)
        print()
        
        # Scenario 3: Release preparation
        print("\n📋 Scenario 3: Release preparation")
        print("-" * 60)
        result = await assistant.assist(
            "Generate release notes for the last 10 commits. "
            "Format them nicely for a GitHub release."
        )
        print(result)
        print()
        
        # Scenario 4: Full workflow
        print("\n📋 Scenario 4: Complete workflow")
        print("-" * 60)
        result = await assistant.assist(
            "I'm preparing for a production deployment. "
            "Please: 1) Search for any debug or console.log statements, "
            "2) Run the test suite, and 3) Generate release notes. "
            "Summarize everything at the end."
        )
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        await assistant.disconnect()
        print("\n" + "=" * 60)
        print("✅ Workflow completed!")


if __name__ == "__main__":
    asyncio.run(ci_cd_workflow())
