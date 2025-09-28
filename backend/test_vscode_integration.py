#!/usr/bin/env python3
"""
Test VS Code Integration
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.git_operations import GitOperationsService

def test_vscode_integration():
    print("🧪 Testing VS Code Integration")
    print("=" * 40)
    
    git_ops = GitOperationsService()
    
    # Test with the cloned repository path
    test_repo_path = "C:\\YOKA\\IlamSingleBrainCell"
    
    if os.path.exists(test_repo_path):
        print(f"📂 Testing with repository: {test_repo_path}")
        success = git_ops.open_vscode(test_repo_path)
        
        if success:
            print("🎉 VS Code integration is working!")
            return True
        else:
            print("❌ VS Code integration failed")
            return False
    else:
        print(f"❌ Test repository not found: {test_repo_path}")
        print("   Clone a repository first from the GitHub tab")
        return False

if __name__ == "__main__":
    test_vscode_integration()