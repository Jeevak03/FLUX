# routes/github_routes.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from services.github_service import GitHubService, GitHubRepo, GitHubBranch, GitHubIssue
from services.git_operations import GitOperationsService
import os

router = APIRouter(prefix="/api/github", tags=["github"])

# Pydantic models for requests/responses
class RepositoryResponse(BaseModel):
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

class BranchResponse(BaseModel):
    name: str
    sha: str
    protected: bool

class IssueResponse(BaseModel):
    id: int
    number: int
    title: str
    body: str
    state: str
    labels: List[str]
    html_url: str

class CloneRepositoryRequest(BaseModel):
    repo_full_name: str
    clone_url: str

class CreateBranchRequest(BaseModel):
    repo_full_name: str
    branch_name: str
    from_branch: str = "main"

class WorkspaceRepository(BaseModel):
    name: str
    path: str
    remote_url: str
    current_branch: str
    has_changes: bool
    modified_files: List[Dict[str, str]]

class AnalyzeCodeRequest(BaseModel):
    repo_path: str
    files_to_analyze: List[str] = []

# Initialize services
github_service = GitHubService() if os.getenv("GITHUB_TOKEN") else None
git_ops = GitOperationsService()

@router.get("/repositories", response_model=List[RepositoryResponse])
async def get_repositories():
    """Get all repositories for the authenticated user"""
    if not github_service:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    try:
        repos = github_service.get_user_repositories()
        return [
            RepositoryResponse(
                id=repo.id,
                name=repo.name,
                full_name=repo.full_name,
                description=repo.description,
                private=repo.private,
                html_url=repo.html_url,
                clone_url=repo.clone_url,
                default_branch=repo.default_branch,
                language=repo.language,
                topics=repo.topics
            ) for repo in repos
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repositories: {str(e)}")

@router.get("/repositories/{repo_full_name}/branches", response_model=List[BranchResponse])
async def get_repository_branches(repo_full_name: str):
    """Get all branches for a repository"""
    if not github_service:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    try:
        # Replace %2F with / for proper repo name
        repo_full_name = repo_full_name.replace("%2F", "/")
        branches = github_service.get_repository_branches(repo_full_name)
        return [
            BranchResponse(
                name=branch.name,
                sha=branch.sha,
                protected=branch.protected
            ) for branch in branches
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch branches: {str(e)}")

@router.get("/repositories/{repo_full_name}/issues", response_model=List[IssueResponse])
async def get_repository_issues(repo_full_name: str, state: str = "open"):
    """Get issues for a repository"""
    if not github_service:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    try:
        repo_full_name = repo_full_name.replace("%2F", "/")
        issues = github_service.get_repository_issues(repo_full_name, state)
        return [
            IssueResponse(
                id=issue.id,
                number=issue.number,
                title=issue.title,
                body=issue.body,
                state=issue.state,
                labels=issue.labels,
                html_url=issue.html_url
            ) for issue in issues
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch issues: {str(e)}")

@router.post("/clone")
async def clone_repository(request: CloneRepositoryRequest, background_tasks: BackgroundTasks):
    """Clone a repository to local workspace"""
    if not github_service:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    try:
        repo_name = request.repo_full_name.split('/')[-1]
        token = os.getenv("GITHUB_TOKEN")
        
        # Clone in background
        success, result = git_ops.clone_repository(request.clone_url, repo_name, token)
        
        if success:
            # Analyze repository structure
            analysis = git_ops.analyze_repository_structure(result)
            
            return {
                "success": True,
                "message": f"Repository {repo_name} cloned successfully",
                "local_path": result,
                "analysis": analysis
            }
        else:
            raise HTTPException(status_code=500, detail=result)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clone repository: {str(e)}")

@router.post("/create-branch")
async def create_branch(request: CreateBranchRequest):
    """Create a new branch in repository (both locally and remotely)"""
    if not github_service:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    try:
        # Create branch remotely on GitHub
        remote_success = github_service.create_branch(
            request.repo_full_name, 
            request.branch_name, 
            request.from_branch
        )
        
        if not remote_success:
            raise HTTPException(status_code=500, detail="Failed to create remote branch")
        
        # If repository exists locally, create branch there too
        repo_name = request.repo_full_name.split('/')[-1]
        local_repo_path = f"C:\\YOKA\\{repo_name}"
        
        if os.path.exists(local_repo_path):
            git_ops.create_branch(local_repo_path, request.branch_name)
        
        return {
            "success": True,
            "message": f"Branch '{request.branch_name}' created successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create branch: {str(e)}")

@router.get("/workspace/repositories", response_model=List[WorkspaceRepository])
async def get_workspace_repositories():
    """Get all repositories in the local workspace"""
    try:
        repos = git_ops.list_workspace_repositories()
        workspace_repos = []
        
        for repo in repos:
            status = git_ops.get_repository_status(repo["path"])
            workspace_repo = WorkspaceRepository(
                name=repo["name"],
                path=repo["path"],
                remote_url=repo["remote_url"],
                current_branch=status["current_branch"],
                has_changes=status["has_changes"],
                modified_files=status["modified_files"]
            )
            workspace_repos.append(workspace_repo)
        
        return workspace_repos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get workspace repositories: {str(e)}")

@router.post("/workspace/open-vscode")
async def open_repository_in_vscode(request: dict):
    """Open a repository in VS Code"""
    repo_path = request.get("repo_path")
    if not repo_path:
        raise HTTPException(status_code=400, detail="repo_path is required")
        
    try:
        if not os.path.exists(repo_path):
            raise HTTPException(status_code=404, detail="Repository path not found")
        
        success = git_ops.open_vscode(repo_path)
        
        if success:
            return {"success": True, "message": "Opened repository in VS Code"}
        else:
            return {
                "success": False, 
                "message": "VS Code not found. Please install VS Code and add it to PATH.",
                "instructions": {
                    "download_url": "https://code.visualstudio.com/",
                    "setup_note": "Make sure to check 'Add to PATH' during installation",
                    "repository_path": repo_path
                }
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to open VS Code: {str(e)}")

@router.get("/repositories/{repo_full_name}/structure")
async def get_repository_structure(repo_full_name: str, branch: str = "main"):
    """Get the file structure of a repository"""
    if not github_service:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    try:
        repo_full_name = repo_full_name.replace("%2F", "/")
        structure = github_service.get_repository_structure(repo_full_name, branch)
        return structure
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get repository structure: {str(e)}")

@router.get("/repositories/{repo_full_name}/file-content")
async def get_file_content(repo_full_name: str, file_path: str, branch: str = "main"):
    """Get the content of a specific file"""
    if not github_service:
        raise HTTPException(status_code=400, detail="GitHub token not configured")
    
    try:
        repo_full_name = repo_full_name.replace("%2F", "/")
        content = github_service.get_file_content(repo_full_name, file_path, branch)
        
        if content is None:
            raise HTTPException(status_code=404, detail="File not found")
        
        return {
            "file_path": file_path,
            "content": content,
            "branch": branch
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file content: {str(e)}")

@router.post("/analyze-code")
async def analyze_repository_code(request: AnalyzeCodeRequest):
    """Analyze repository code for issues and improvement opportunities"""
    try:
        if not os.path.exists(request.repo_path):
            raise HTTPException(status_code=404, detail="Repository path not found")
        
        analysis = git_ops.analyze_repository_structure(request.repo_path)
        
        # Add more detailed analysis here
        # This will be enhanced when we integrate with agents
        
        return {
            "success": True,
            "repository_path": request.repo_path,
            "analysis": analysis,
            "recommendations": []  # Will be populated by agents
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze code: {str(e)}")