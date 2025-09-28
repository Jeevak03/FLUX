# services/git_operations.py
import os
import subprocess
import shutil
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
from datetime import datetime

class GitOperationsService:
    def __init__(self, workspace_root: str = "C:\\YOKA"):
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(exist_ok=True)
        
    def clone_repository(self, repo_url: str, repo_name: str, token: str) -> Tuple[bool, str]:
        """Clone a repository to the local workspace"""
        try:
            repo_path = self.workspace_root / repo_name
            
            # Remove existing directory if it exists
            if repo_path.exists():
                shutil.rmtree(repo_path)
            
            # Clone with authentication
            auth_url = repo_url.replace("https://", f"https://{token}@")
            
            result = subprocess.run([
                "git", "clone", auth_url, str(repo_path)
            ], capture_output=True, text=True, cwd=str(self.workspace_root))
            
            if result.returncode == 0:
                print(f"✅ Successfully cloned {repo_name} to {repo_path}")
                return True, str(repo_path)
            else:
                print(f"❌ Failed to clone {repo_name}: {result.stderr}")
                return False, result.stderr
                
        except Exception as e:
            error_msg = f"Error cloning repository: {e}"
            print(f"❌ {error_msg}")
            return False, error_msg

    def create_branch(self, repo_path: str, branch_name: str) -> bool:
        """Create and switch to a new branch"""
        try:
            # Create and checkout new branch
            result = subprocess.run([
                "git", "checkout", "-b", branch_name
            ], capture_output=True, text=True, cwd=repo_path)
            
            if result.returncode == 0:
                print(f"✅ Created and switched to branch '{branch_name}'")
                return True
            else:
                print(f"❌ Failed to create branch '{branch_name}': {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating branch: {e}")
            return False

    def commit_changes(self, repo_path: str, message: str, files: List[str] = None) -> bool:
        """Commit changes to the repository"""
        try:
            # Add files (all if not specified)
            if files:
                for file in files:
                    subprocess.run(["git", "add", file], cwd=repo_path, check=True)
            else:
                subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            
            # Commit changes
            result = subprocess.run([
                "git", "commit", "-m", message
            ], capture_output=True, text=True, cwd=repo_path)
            
            if result.returncode == 0:
                print(f"✅ Successfully committed changes: {message}")
                return True
            else:
                print(f"❌ Failed to commit changes: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error committing changes: {e}")
            return False

    def push_branch(self, repo_path: str, branch_name: str, token: str) -> bool:
        """Push branch to remote repository"""
        try:
            # Get remote URL and add token
            result = subprocess.run([
                "git", "remote", "get-url", "origin"
            ], capture_output=True, text=True, cwd=repo_path)
            
            if result.returncode != 0:
                print("❌ Failed to get remote URL")
                return False
            
            remote_url = result.stdout.strip()
            
            # Push branch
            result = subprocess.run([
                "git", "push", "origin", branch_name
            ], capture_output=True, text=True, cwd=repo_path)
            
            if result.returncode == 0:
                print(f"✅ Successfully pushed branch '{branch_name}' to remote")
                return True
            else:
                print(f"❌ Failed to push branch '{branch_name}': {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error pushing branch: {e}")
            return False

    def get_repository_status(self, repo_path: str) -> Dict[str, any]:
        """Get the status of the repository"""
        try:
            # Get current branch
            branch_result = subprocess.run([
                "git", "branch", "--show-current"
            ], capture_output=True, text=True, cwd=repo_path)
            
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"
            
            # Get status
            status_result = subprocess.run([
                "git", "status", "--porcelain"
            ], capture_output=True, text=True, cwd=repo_path)
            
            modified_files = []
            if status_result.returncode == 0:
                for line in status_result.stdout.strip().split('\n'):
                    if line:
                        status_code = line[:2]
                        file_path = line[3:]
                        modified_files.append({
                            "file": file_path,
                            "status": status_code.strip()
                        })
            
            return {
                "current_branch": current_branch,
                "modified_files": modified_files,
                "has_changes": len(modified_files) > 0
            }
            
        except Exception as e:
            print(f"❌ Error getting repository status: {e}")
            return {
                "current_branch": "unknown",
                "modified_files": [],
                "has_changes": False
            }

    def list_workspace_repositories(self) -> List[Dict[str, str]]:
        """List all repositories in the workspace"""
        repos = []
        try:
            for item in self.workspace_root.iterdir():
                if item.is_dir() and (item / ".git").exists():
                    # Get remote URL
                    try:
                        result = subprocess.run([
                            "git", "remote", "get-url", "origin"
                        ], capture_output=True, text=True, cwd=str(item))
                        
                        remote_url = result.stdout.strip() if result.returncode == 0 else "unknown"
                        
                        repos.append({
                            "name": item.name,
                            "path": str(item),
                            "remote_url": remote_url
                        })
                    except:
                        repos.append({
                            "name": item.name,
                            "path": str(item),
                            "remote_url": "unknown"
                        })
            
            return repos
            
        except Exception as e:
            print(f"❌ Error listing workspace repositories: {e}")
            return []

    def analyze_repository_structure(self, repo_path: str) -> Dict[str, any]:
        """Analyze the structure and technologies of a repository"""
        repo_path = Path(repo_path)
        analysis = {
            "languages": {},
            "frameworks": [],
            "config_files": [],
            "file_count": 0,
            "directory_count": 0
        }
        
        try:
            # Common file extensions and their languages
            language_extensions = {
                ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", 
                ".java": "Java", ".cpp": "C++", ".c": "C", ".cs": "C#",
                ".go": "Go", ".rs": "Rust", ".php": "PHP", ".rb": "Ruby",
                ".swift": "Swift", ".kt": "Kotlin", ".scala": "Scala",
                ".html": "HTML", ".css": "CSS", ".scss": "SCSS", ".less": "LESS"
            }
            
            # Framework indicators
            framework_indicators = {
                "package.json": "Node.js",
                "requirements.txt": "Python",
                "pom.xml": "Maven",
                "build.gradle": "Gradle",
                "Cargo.toml": "Rust",
                "go.mod": "Go Modules",
                "composer.json": "PHP Composer",
                "Gemfile": "Ruby Gems"
            }
            
            # Walk through repository
            for root, dirs, files in os.walk(repo_path):
                # Skip .git and node_modules directories
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.idea', '.vscode']]
                
                analysis["directory_count"] += len(dirs)
                analysis["file_count"] += len(files)
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Language detection
                    suffix = file_path.suffix.lower()
                    if suffix in language_extensions:
                        lang = language_extensions[suffix]
                        analysis["languages"][lang] = analysis["languages"].get(lang, 0) + 1
                    
                    # Framework detection
                    if file in framework_indicators:
                        framework = framework_indicators[file]
                        if framework not in analysis["frameworks"]:
                            analysis["frameworks"].append(framework)
                    
                    # Config files
                    if file.lower() in ["dockerfile", ".gitignore", "readme.md", "license"]:
                        analysis["config_files"].append(str(file_path.relative_to(repo_path)))
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error analyzing repository structure: {e}")
            return analysis

    def open_vscode(self, repo_path: str) -> bool:
        """Open repository in VS Code"""
        # Try different VS Code commands in order of preference
        vscode_commands = ["code", "code-insiders", "code.cmd", "code-insiders.cmd"]
        
        for cmd in vscode_commands:
            try:
                # Use shell=True for Windows to handle .cmd files properly
                result = subprocess.run([
                    cmd, repo_path
                ], capture_output=True, text=True, shell=True)
                
                if result.returncode == 0:
                    print(f"✅ Opened {repo_path} in VS Code ({cmd})")
                    return True
                else:
                    print(f"⚠️  {cmd} returned code {result.returncode}: {result.stderr}")
                    
            except FileNotFoundError:
                continue  # Try next command
            except Exception as e:
                print(f"❌ Error with {cmd}: {e}")
                continue
        
        # If we get here, none of the VS Code commands worked
        print(f"❌ VS Code not found. Please install VS Code and add it to PATH")
        print(f"   Download from: https://code.visualstudio.com/")
        print(f"   Repository location: {repo_path}")
        print(f"   Tried commands: {', '.join(vscode_commands)}")
        return False