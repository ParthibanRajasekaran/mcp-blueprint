#!/usr/bin/env python3
"""
Setup script for MCP DevOps Blueprint.

This script helps you get started with the project.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def check_git():
    """Check if git is installed."""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Git is not installed (optional but recommended)")
        return False


def setup_virtual_environment():
    """Create and activate virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("\n🔧 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created!")
        
        # Determine activation script based on OS
        if sys.platform == "win32":
            activate_script = "venv\\Scripts\\activate.bat"
        else:
            activate_script = "source venv/bin/activate"
        
        print(f"\n💡 To activate the environment, run:")
        print(f"   {activate_script}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def install_dependencies(dev=False):
    """Install project dependencies."""
    if dev:
        return run_command(
            [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
            "Installing development dependencies"
        )
    else:
        return run_command(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            "Installing dependencies"
        )


def setup_pre_commit():
    """Setup pre-commit hooks."""
    if not Path(".pre-commit-config.yaml").exists():
        print("⚠️  No pre-commit config found, skipping")
        return True
    
    return run_command(
        ["pre-commit", "install"],
        "Setting up pre-commit hooks"
    )


def check_api_key():
    """Check if Anthropic API key is set."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        print("✅ ANTHROPIC_API_KEY is set")
        return True
    else:
        print("⚠️  ANTHROPIC_API_KEY is not set")
        print("   The AI client will not work without an API key.")
        print("   Get one from: https://console.anthropic.com/")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key'")
        return False


def run_tests():
    """Run the test suite."""
    return run_command(
        [sys.executable, "-m", "pytest", "-v"],
        "Running tests"
    )


def main():
    """Main setup process."""
    print("=" * 60)
    print("🚀 MCP DevOps Blueprint - Setup Script")
    print("=" * 60)
    
    # Check prerequisites
    print("\n📋 Checking prerequisites...")
    if not check_python_version():
        sys.exit(1)
    check_git()
    
    # Ask user what to setup
    print("\n📦 Setup Options:")
    print("1. Basic setup (install dependencies)")
    print("2. Development setup (with dev tools and pre-commit hooks)")
    print("3. Full setup (development + run tests)")
    
    choice = input("\nSelect option (1-3) [default: 1]: ").strip() or "1"
    
    dev_mode = choice in ["2", "3"]
    run_test = choice == "3"
    
    # Create virtual environment
    if not setup_virtual_environment():
        print("\n⚠️  Continuing without virtual environment...")
    
    # Install dependencies
    if not install_dependencies(dev=dev_mode):
        print("\n❌ Setup failed!")
        sys.exit(1)
    
    # Setup pre-commit if dev mode
    if dev_mode:
        setup_pre_commit()
    
    # Check API key
    check_api_key()
    
    # Run tests if requested
    if run_test:
        run_tests()
    
    # Success message
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\n📚 Next steps:")
    print("   1. Activate virtual environment (if created)")
    print("   2. Set ANTHROPIC_API_KEY environment variable")
    print("   3. Run the server: python mcp_server.py")
    print("   4. Run the client: python mcp_client.py")
    print("   5. Check examples: ls examples/")
    print("\n📖 Read the README.md for more information!")
    print("\n⭐ If you find this useful, please star the repo on GitHub!")


if __name__ == "__main__":
    main()
