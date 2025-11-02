"""
Advanced Example: Custom MCP Tools

This example shows how to extend the MCP server with custom tools
for your specific DevOps workflows.
"""

from typing import Dict, List
from mcp.server.fastmcp import FastMCP
import subprocess
import json

# Create a custom server
mcp = FastMCP("custom-devops-helper")


@mcp.tool()
def check_docker_status() -> Dict[str, str]:
    """
    Check if Docker is running and return version info.
    
    Returns:
        Dictionary with Docker status and version
    """
    try:
        result = subprocess.run(
            ["docker", "version", "--format", "{{.Server.Version}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return {
                "status": "running",
                "version": result.stdout.strip(),
                "message": "Docker is running properly"
            }
        else:
            return {
                "status": "error",
                "version": "unknown",
                "message": "Docker command failed"
            }
    except FileNotFoundError:
        return {
            "status": "not_found",
            "version": "N/A",
            "message": "Docker is not installed"
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "version": "unknown",
            "message": "Docker command timed out"
        }


@mcp.tool()
def list_git_branches(repository_path: str = ".") -> List[str]:
    """
    List all git branches in a repository.
    
    Args:
        repository_path: Path to git repository (default: current directory)
    
    Returns:
        List of branch names
    """
    try:
        result = subprocess.run(
            ["git", "branch", "-a"],
            cwd=repository_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            branches = []
            for line in result.stdout.split("\n"):
                line = line.strip()
                if line and not line.startswith("*"):
                    # Remove "remotes/origin/" prefix if present
                    branch = line.replace("remotes/origin/", "")
                    if branch and branch != "HEAD":
                        branches.append(branch)
            return branches
        else:
            return [f"Error: {result.stderr}"]
    except Exception as e:
        return [f"Error: {str(e)}"]


@mcp.tool()
def analyze_code_metrics(directory: str = "src") -> Dict[str, int]:
    """
    Analyze basic code metrics for Python files.
    
    Args:
        directory: Directory to analyze (default: "src")
    
    Returns:
        Dictionary with code metrics
    """
    import os
    from pathlib import Path
    
    metrics = {
        "total_files": 0,
        "total_lines": 0,
        "total_functions": 0,
        "total_classes": 0,
    }
    
    try:
        for path in Path(directory).rglob("*.py"):
            if path.is_file():
                metrics["total_files"] += 1
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")
                    metrics["total_lines"] += len(lines)
                    metrics["total_functions"] += content.count("def ")
                    metrics["total_classes"] += content.count("class ")
        
        return metrics
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def create_deployment_checklist(environment: str = "production") -> List[str]:
    """
    Generate a deployment checklist for the specified environment.
    
    Args:
        environment: Target environment (e.g., "production", "staging")
    
    Returns:
        List of checklist items
    """
    base_checklist = [
        "✓ All tests passing",
        "✓ Code review completed",
        "✓ Documentation updated",
        "✓ Changelog updated",
        "✓ Database migrations prepared",
    ]
    
    if environment == "production":
        base_checklist.extend([
            "✓ Staging deployment verified",
            "✓ Rollback plan prepared",
            "✓ Monitoring alerts configured",
            "✓ Stakeholders notified",
            "✓ Maintenance window scheduled",
        ])
    
    return base_checklist


if __name__ == "__main__":
    print("Custom MCP DevOps Server")
    print("=" * 50)
    print("\nAvailable custom tools:")
    print("  - check_docker_status")
    print("  - list_git_branches")
    print("  - analyze_code_metrics")
    print("  - create_deployment_checklist")
    print("\nStarting server...")
    mcp.run()
