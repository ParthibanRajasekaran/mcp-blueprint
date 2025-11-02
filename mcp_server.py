"""
MCP Server for the "From Pull Request to Production" blueprint.

This server exposes three tools via the Model Context Protocol (MCP):

- search_repo: search repository files for a keyword
- run_tests: execute unit tests and summarise failures
- generate_release_notes: generate release notes from recent commits

See README.md for setup and usage instructions.
"""

from typing import List
from mcp.server.fastmcp import FastMCP
import subprocess
import git

mcp = FastMCP("devops-helper")

@mcp.tool()
def search_repo(keyword: str, root: str = ".") -> List[str]:
    """Search for files containing a keyword (case‑insensitive) and return file paths."""
    repo = git.Repo(root)
    matches: List[str] = []
    for blob in repo.tree().traverse():
        if blob.type == 'blob':
            try:
                content = blob.data_stream.read().decode('utf-8', errors='ignore')
                if keyword.lower() in content.lower():
                    matches.append(blob.path)
            except Exception:
                # If we can't read a file (e.g., binary), skip it
                pass
    return matches

@mcp.tool()
def run_tests(test_path: str = "tests") -> dict:
    """Run pytest on the given path and return a summary of results.

    Parameters:
        test_path: Path to the tests directory or file (default: "tests").

    Returns:
        A dict containing the return code, list of failure lines and the tail of the raw output.
    """
    result = subprocess.run(
        ["pytest", test_path, "-q", "--disable-warnings"],
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    failures: List[str] = []
    for line in output.split("\n"):
        if line.startswith("E   "):
            failures.append(line.strip())
    return {
        "returncode": result.returncode,
        "failures": failures,
        "raw": output[-500:],
    }

@mcp.tool()
def generate_release_notes(since_tag: str = "") -> str:
    """Generate release notes from commit messages since a tag or from the last 10 commits.

    Parameters:
        since_tag: Git tag to start from. If empty, use the last 10 commits.

    Returns:
        A formatted string with each commit message and its short SHA.
    """
    repo = git.Repo(".")
    if since_tag:
        commits = list(repo.iter_commits(f"{since_tag}..HEAD"))
    else:
        commits = list(repo.iter_commits('HEAD', max_count=10))
    notes: List[str] = []
    for commit in reversed(commits):
        notes.append(f"- {commit.message.strip()} (#{commit.hexsha[:7]})")
    return "\n".join(notes)

if __name__ == "__main__":
    # Start the server using the default stdio transport
    mcp.run()
