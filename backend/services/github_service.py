# services/github_service.py
import os
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import base64
import json

load_dotenv()

@dataclass
class GitHubRepo:
    id: int
    name: str
    full_name: str
    description: Optional[str]
    private: bool
    html_url: str
    clone_url: str
    default_branch: str
    language: Optional[str]
    topics: List[str]

@dataclass
class GitHubBranch:
    name: str
    sha: str
    protected: bool

@dataclass
class GitHubIssue:
    id: int
    number: int
    title: str
    body: str
    state: str
    labels: List[str]
    html_url: str

class GitHubService:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.base_url = "https://api.github.com"

    def get_user_repositories(self, per_page: int = 50) -> List[GitHubRepo]:
        """Get all repositories for the authenticated user"""
        try:
            repos = []
            page = 1
            
            while True:
                url = f"{self.base_url}/user/repos"
                params = {
                    "per_page": per_page,
                    "page": page,
                    "sort": "updated",
                    "direction": "desc"
                }
                
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                
                page_repos = response.json()
                if not page_repos:
                    break
                
                for repo_data in page_repos:
                    repo = GitHubRepo(
                        id=repo_data["id"],
                        name=repo_data["name"],
                        full_name=repo_data["full_name"],
                        description=repo_data.get("description"),
                        private=repo_data["private"],
                        html_url=repo_data["html_url"],
                        clone_url=repo_data["clone_url"],
                        default_branch=repo_data["default_branch"],
                        language=repo_data.get("language"),
                        topics=repo_data.get("topics", [])
                    )
                    repos.append(repo)
                
                page += 1
                if len(page_repos) < per_page:  # Last page
                    break
            
            return repos
            
        except Exception as e:
            print(f"Error fetching repositories: {e}")
            return []

    def get_repository_branches(self, repo_full_name: str) -> List[GitHubBranch]:
        """Get all branches for a repository"""
        try:
            url = f"{self.base_url}/repos/{repo_full_name}/branches"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            branches = []
            for branch_data in response.json():
                branch = GitHubBranch(
                    name=branch_data["name"],
                    sha=branch_data["commit"]["sha"],
                    protected=branch_data.get("protected", False)
                )
                branches.append(branch)
            
            return branches
            
        except Exception as e:
            print(f"Error fetching branches for {repo_full_name}: {e}")
            return []

    def get_repository_issues(self, repo_full_name: str, state: str = "open") -> List[GitHubIssue]:
        """Get issues for a repository"""
        try:
            url = f"{self.base_url}/repos/{repo_full_name}/issues"
            params = {"state": state, "per_page": 50}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            issues = []
            for issue_data in response.json():
                # Skip pull requests (they appear as issues in GitHub API)
                if "pull_request" in issue_data:
                    continue
                    
                issue = GitHubIssue(
                    id=issue_data["id"],
                    number=issue_data["number"],
                    title=issue_data["title"],
                    body=issue_data.get("body", ""),
                    state=issue_data["state"],
                    labels=[label["name"] for label in issue_data.get("labels", [])],
                    html_url=issue_data["html_url"]
                )
                issues.append(issue)
            
            return issues
            
        except Exception as e:
            print(f"Error fetching issues for {repo_full_name}: {e}")
            return []

    def create_branch(self, repo_full_name: str, branch_name: str, from_branch: str = "main") -> bool:
        """Create a new branch from an existing branch"""
        try:
            # Get the SHA of the source branch
            url = f"{self.base_url}/repos/{repo_full_name}/git/refs/heads/{from_branch}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            source_sha = response.json()["object"]["sha"]
            
            # Create new branch
            url = f"{self.base_url}/repos/{repo_full_name}/git/refs"
            data = {
                "ref": f"refs/heads/{branch_name}",
                "sha": source_sha
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            print(f"✅ Created branch '{branch_name}' in {repo_full_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating branch '{branch_name}' in {repo_full_name}: {e}")
            return False

    def get_file_content(self, repo_full_name: str, file_path: str, branch: str = "main") -> Optional[str]:
        """Get the content of a file from repository"""
        try:
            url = f"{self.base_url}/repos/{repo_full_name}/contents/{file_path}"
            params = {"ref": branch}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            file_data = response.json()
            if file_data["encoding"] == "base64":
                content = base64.b64decode(file_data["content"]).decode('utf-8')
                return content
            
            return file_data["content"]
            
        except Exception as e:
            print(f"Error fetching file {file_path} from {repo_full_name}: {e}")
            return None

    def update_file(self, repo_full_name: str, file_path: str, content: str, 
                   commit_message: str, branch: str = "main") -> bool:
        """Update or create a file in repository"""
        try:
            # Get current file info (if exists) to get SHA
            current_file = None
            try:
                url = f"{self.base_url}/repos/{repo_full_name}/contents/{file_path}"
                params = {"ref": branch}
                response = requests.get(url, headers=self.headers, params=params)
                if response.status_code == 200:
                    current_file = response.json()
            except:
                pass  # File doesn't exist, we'll create it
            
            # Prepare update data
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            data = {
                "message": commit_message,
                "content": encoded_content,
                "branch": branch
            }
            
            if current_file:
                data["sha"] = current_file["sha"]
            
            # Update/create file
            url = f"{self.base_url}/repos/{repo_full_name}/contents/{file_path}"
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            print(f"✅ Updated file '{file_path}' in {repo_full_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating file '{file_path}' in {repo_full_name}: {e}")
            return False

    def create_pull_request(self, repo_full_name: str, title: str, body: str, 
                           head_branch: str, base_branch: str = "main") -> Optional[str]:
        """Create a pull request"""
        try:
            url = f"{self.base_url}/repos/{repo_full_name}/pulls"
            data = {
                "title": title,
                "body": body,
                "head": head_branch,
                "base": base_branch
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            pr_data = response.json()
            print(f"✅ Created pull request: {pr_data['html_url']}")
            return pr_data["html_url"]
            
        except Exception as e:
            print(f"❌ Error creating pull request: {e}")
            return None

    def get_repository_structure(self, repo_full_name: str, branch: str = "main") -> Dict[str, Any]:
        """Get the file structure of a repository"""
        try:
            url = f"{self.base_url}/repos/{repo_full_name}/git/trees/{branch}"
            params = {"recursive": "1"}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            tree_data = response.json()
            structure = {
                "files": [],
                "directories": []
            }
            
            for item in tree_data["tree"]:
                if item["type"] == "blob":  # File
                    structure["files"].append({
                        "path": item["path"],
                        "size": item.get("size", 0),
                        "sha": item["sha"]
                    })
                elif item["type"] == "tree":  # Directory
                    structure["directories"].append(item["path"])
            
            return structure
            
        except Exception as e:
            print(f"Error fetching repository structure for {repo_full_name}: {e}")
            return {"files": [], "directories": []}