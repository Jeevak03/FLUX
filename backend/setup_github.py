#!/usr/bin/env python3
"""
GitHub Integration Setup Script for SDLC Assistant
This script helps set up the GitHub integration features.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'requests', 'gitpython', 'fastapi', 'uvicorn', 
        'websockets', 'python-dotenv', 'pydantic', 'groq'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_environment():
    """Check environment variables"""
    print("\n🔧 Checking environment configuration...")
    
    env_file = Path('.env')
    example_env = Path('.env.example')
    
    if not env_file.exists():
        if example_env.exists():
            print("📄 Creating .env file from .env.example...")
            env_file.write_text(example_env.read_text())
        else:
            print("❌ No .env file found. Creating one...")
            env_content = """# SDLC Assistant Environment Variables

# GitHub Personal Access Token
# Get your token from: https://github.com/settings/tokens
# Required scopes: repo, read:org, read:user
GITHUB_TOKEN=your_github_token_here

# Groq API Key
# Get your key from: https://groq.com
GROQ_API_KEY=your_groq_api_key_here
"""
            env_file.write_text(env_content)
    
    # Check if tokens are configured
    from dotenv import load_dotenv
    load_dotenv()
    
    github_token = os.getenv('GITHUB_TOKEN')
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not github_token or github_token == 'your_github_token_here':
        print("⚠️  GitHub token not configured")
        print("   1. Go to https://github.com/settings/tokens")
        print("   2. Create a new token with 'repo', 'read:org', 'read:user' scopes")
        print("   3. Add it to your .env file: GITHUB_TOKEN=your_token")
        return False
    else:
        print("✅ GitHub token configured")
    
    if not groq_key or groq_key == 'your_groq_api_key_here':
        print("⚠️  Groq API key not configured")
        print("   1. Go to https://groq.com")
        print("   2. Get your API key")
        print("   3. Add it to your .env file: GROQ_API_KEY=your_key")
        return False
    else:
        print("✅ Groq API key configured")
    
    return True

def check_git():
    """Check if Git is installed"""
    print("\n🔧 Checking Git installation...")
    
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git not found")
            return False
    except FileNotFoundError:
        print("❌ Git not installed")
        print("   Please install Git from: https://git-scm.com/downloads")
        return False

def check_vscode():
    """Check if VS Code is installed"""
    print("\n💻 Checking VS Code installation...")
    
    try:
        result = subprocess.run(['code', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ VS Code installed and accessible via 'code' command")
            return True
        else:
            print("⚠️  VS Code not accessible via 'code' command")
            return False
    except FileNotFoundError:
        print("⚠️  VS Code not found or 'code' command not in PATH")
        print("   Make sure VS Code is installed and 'code' command is available")
        return False

def create_workspace():
    """Create the C:\\YOKA workspace directory"""
    print("\n📁 Setting up workspace...")
    
    workspace_path = Path("C:\\YOKA")
    try:
        workspace_path.mkdir(exist_ok=True)
        print(f"✅ Workspace created at: {workspace_path}")
        
        # Test write permissions
        test_file = workspace_path / "test_write.tmp"
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Workspace has write permissions")
        
        return True
    except PermissionError:
        print(f"❌ Permission denied creating workspace at {workspace_path}")
        print("   Try running as administrator or choose a different location")
        return False
    except Exception as e:
        print(f"❌ Error creating workspace: {e}")
        return False

def main():
    print("🚀 SDLC Assistant GitHub Integration Setup")
    print("=" * 50)
    
    success = True
    success &= check_requirements()
    success &= check_environment()
    success &= check_git()
    check_vscode()  # Optional, don't fail setup
    success &= create_workspace()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Make sure your GitHub token and Groq API key are set in .env")
        print("2. Start the backend: python main.py")
        print("3. Start the frontend: npm run dev")
        print("4. Go to the GitHub tab to connect your repositories!")
    else:
        print("⚠️  Setup completed with warnings")
        print("Please resolve the issues above before using GitHub integration")

if __name__ == "__main__":
    main()