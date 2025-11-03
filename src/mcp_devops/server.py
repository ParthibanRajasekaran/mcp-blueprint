"""
MCP Server for DevOps automation.

This server exposes tools for repository operations, test execution,
and release note generation via the Model Context Protocol (MCP).
"""

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

import git
from git import GitCommandError, InvalidGitRepositoryError
from git.objects import Blob
from mcp.server.fastmcp import FastMCP

# Ensure stdout is unbuffered for proper stdio communication
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)


def create_server(name: str = "devops-helper") -> FastMCP:
    """Create and configure the MCP server with all tools."""
    mcp = FastMCP(name)

    @mcp.tool()
    def search_repo(keyword: str, root: str = ".") -> List[str]:
        """
        Search for files containing a keyword (case-insensitive).

        Args:
            keyword: The search term to look for
            root: Root directory to search (default: current directory)

        Returns:
            List of file paths containing the keyword

        Example:
            search_repo("TODO", ".")
        """
        try:
            repo = git.Repo(root)
            matches: List[str] = []
            for item in repo.tree().traverse():
                # Type guard: check if it's a Blob
                if isinstance(item, Blob) and item.type == "blob":
                    try:
                        content = item.data_stream.read().decode("utf-8", errors="ignore")
                        if keyword.lower() in content.lower():
                            matches.append(str(item.path))
                    except Exception:
                        # Skip files that can't be read (e.g., binary files)
                        continue
            return matches
        except InvalidGitRepositoryError:
            return [f"Error: {root} is not a valid git repository"]
        except Exception as e:
            return [f"Error: {str(e)}"]

    @mcp.tool()
    def run_tests(test_path: str = "tests") -> Dict[str, Any]:
        """
        Run pytest on the given path and return a summary.

        Args:
            test_path: Path to tests directory or file (default: "tests")

        Returns:
            Dictionary containing returncode, failures, and raw output

        Example:
            run_tests("tests/unit")
        """
        try:
            result = subprocess.run(
                ["pytest", test_path, "-q", "--disable-warnings"],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            output = result.stdout + result.stderr
            failures: List[str] = []
            for line in output.split("\n"):
                if line.startswith("E   ") or "FAILED" in line:
                    failures.append(line.strip())
            
            return {
                "returncode": result.returncode,
                "failures": failures,
                "raw": output[-1000:],  # Last 1000 chars
                "success": result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "failures": ["Test execution timed out after 5 minutes"],
                "raw": "",
                "success": False,
            }
        except FileNotFoundError:
            return {
                "returncode": -1,
                "failures": ["pytest not found. Please install pytest."],
                "raw": "",
                "success": False,
            }
        except Exception as e:
            return {
                "returncode": -1,
                "failures": [f"Error running tests: {str(e)}"],
                "raw": "",
                "success": False,
            }

    @mcp.tool()
    def generate_release_notes(since_tag: str = "", max_commits: int = 10) -> str:
        """
        Generate release notes from commit messages.

        Args:
            since_tag: Git tag to start from (default: last N commits)
            max_commits: Maximum number of commits if no tag specified (default: 10)

        Returns:
            Formatted release notes with commit messages and SHAs

        Example:
            generate_release_notes("v1.0.0")
            generate_release_notes(max_commits=20)
        """
        try:
            repo = git.Repo(".")
            
            if since_tag:
                try:
                    commits = list(repo.iter_commits(f"{since_tag}..HEAD"))
                except GitCommandError:
                    return f"Error: Tag '{since_tag}' not found"
            else:
                commits = list(repo.iter_commits("HEAD", max_count=max_commits))
            
            if not commits:
                return "No commits found for release notes"
            
            notes: List[str] = ["# Release Notes\n"]
            notes.append(f"Generated from {len(commits)} commit(s)\n")
            
            for commit in reversed(commits):
                message_str = str(commit.message).strip()
                message = message_str.split("\n")[0]  # First line only
                notes.append(f"- {message} ([{commit.hexsha[:7]}])")
            
            return "\n".join(notes)
        except InvalidGitRepositoryError:
            return "Error: Not a git repository"
        except Exception as e:
            return f"Error generating release notes: {str(e)}"

    return mcp


def main() -> None:
    """Entry point for running the server."""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
