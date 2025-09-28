# 🐙 GitHub Integration for SDLC Assistant

Transform your SDLC Assistant into a **GitHub-integrated AI developer** that can autonomously work on real repositories, analyze code, fix issues, and create pull requests.

## 🚀 Features

### ✅ **Currently Implemented**
- **Repository Management**: Browse, search, and filter your GitHub repositories
- **Local Workspace**: Clone repositories to `C:\YOKA` with automatic setup
- **Branch Management**: Create, view, and manage branches directly from the UI
- **Issue Tracking**: View and analyze GitHub issues with AI agent integration
- **VS Code Integration**: One-click repository opening in VS Code
- **Real-time Status**: Live monitoring of repository changes and git status
- **Multi-Agent Analysis**: 7 specialized AI agents ready to work on your code

### 🔄 **Coming Soon**
- **Autonomous Code Fixes**: AI agents that automatically fix bugs and issues
- **Pull Request Creation**: Automated PR generation with detailed descriptions
- **Code Quality Analysis**: Deep code scanning for improvements and optimizations
- **Security Vulnerability Detection**: Automated security audits and fixes

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Node.js 18+
- Git installed and accessible via command line
- VS Code (optional, for automatic opening)
- GitHub Personal Access Token

### 2. Quick Setup
Run the automated setup script:
```bash
cd backend
python setup_github.py
```

### 3. Manual Setup

#### Backend Setup
1. Install additional requirements:
   ```bash
   pip install requests gitpython
   ```

2. Get your GitHub Personal Access Token:
   - Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `read:org`, `read:user`
   - Copy your token

3. Configure environment variables in `.env`:
   ```bash
   GITHUB_TOKEN=your_github_token_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Create workspace directory:
   ```bash
   mkdir C:\YOKA
   ```

#### Frontend Setup
No additional frontend setup required - GitHub integration is built into the existing interface.

### 4. Start the Services
```bash
# Backend
cd backend
python main.py

# Frontend
cd frontend
npm run dev
```

## 🎯 How to Use

### 1. **Browse Repositories**
- Navigate to the **GitHub** tab in the SDLC Assistant
- View all your repositories with language, topics, and status
- Search and filter repositories by name, description, or language

### 2. **Clone Repository**
- Click **📥 Clone** on any repository
- Repository will be cloned to `C:\YOKA\{repo_name}`
- Automatic code structure analysis provided

### 3. **Workspace Management**
- Switch to **Workspace** tab to see all cloned repositories
- View git status, current branch, and modified files
- **💻 Open in VS Code** with one click

### 4. **Branch Operations**
- Select a repository and go to **Branches** tab
- View all branches with protection status
- Create new branches directly from the UI

### 5. **Issue Analysis**
- Go to **Issues** tab to view repository issues
- Click **🤖 AI Fix** to analyze issues with AI agents
- Issues are categorized by priority and labels

### 6. **AI Agent Integration**
Use specialized agents for different tasks:
- **Sarah** (Requirements): "Analyze this issue for requirements"
- **Marcus** (Architecture): "Design a solution for this bug"  
- **Alex** (Developer): "Fix this issue in the codebase"
- **Jessica** (QA): "Create test cases for this feature"
- **David** (DevOps): "Set up CI/CD for this repository"
- **Emily** (PM): "Prioritize these issues"
- **Robert** (Security): "Scan for security vulnerabilities"

## 🔧 Advanced Configuration

### Custom Workspace Location
To use a different workspace directory, modify the `GitOperationsService` in `services/git_operations.py`:
```python
workspace_root = "D:\\MyProjects"  # Change this path
```

### GitHub Enterprise
For GitHub Enterprise, update the `base_url` in `services/github_service.py`:
```python
self.base_url = "https://your-enterprise.github.com/api/v3"
```

### Token Permissions
Your GitHub token needs these scopes:
- `repo` - Access private and public repositories
- `read:org` - Read organization membership
- `read:user` - Read user profile information

## 🚨 Troubleshooting

### Common Issues

**1. "GitHub token not configured"**
- Make sure `GITHUB_TOKEN` is set in your `.env` file
- Verify the token has correct scopes
- Check token hasn't expired

**2. "Permission denied creating workspace"**
- Run as administrator on Windows
- Or choose a different workspace location with write permissions

**3. "Git not found"**
- Install Git from [git-scm.com](https://git-scm.com/downloads)
- Make sure `git` command is in your PATH

**4. "VS Code not opening"**
- Install VS Code
- Make sure `code` command is available in PATH
- On Windows, restart terminal after VS Code installation

**5. "Failed to clone repository"**
- Check network connectivity
- Verify repository permissions
- Ensure GitHub token has repo access

### Debug Mode
Enable debug logging by setting environment variable:
```bash
DEBUG_GITHUB=true
```

## 🔐 Security Considerations

- **Token Storage**: Never commit your `.env` file to version control
- **Workspace Access**: `C:\YOKA` directory contains cloned repositories
- **Network Access**: Backend makes HTTPS requests to GitHub API
- **File Permissions**: Agents can read/write files in workspace

## 📊 Architecture

```
Frontend (React/TypeScript)
├── GitHubIntegration.tsx       # Main integration component
├── RepositorySelector.tsx      # Repository browsing
├── WorkspaceManager.tsx        # Local workspace management
├── BranchManager.tsx          # Branch operations
└── IssueTracker.tsx           # Issue management

Backend (FastAPI/Python)
├── routes/github_routes.py     # GitHub API endpoints
├── services/github_service.py  # GitHub API client
├── services/git_operations.py  # Local git operations
└── agents/                     # Enhanced with repo analysis
```

## 🤝 Contributing

To extend GitHub integration:

1. **Add new GitHub API features** in `services/github_service.py`
2. **Extend git operations** in `services/git_operations.py`  
3. **Add new API endpoints** in `routes/github_routes.py`
4. **Create new UI components** in `components/GitHub/`
5. **Enhance agent capabilities** for repository analysis

## 📝 Changelog

### v1.0.0 - Initial GitHub Integration
- ✅ Repository browsing and cloning
- ✅ Workspace management with git status
- ✅ Branch creation and management
- ✅ Issue viewing and AI agent integration
- ✅ VS Code integration
- ✅ Automated setup script

### v1.1.0 - Coming Soon
- 🔄 Autonomous code fixing
- 🔄 Pull request automation
- 🔄 Advanced code analysis
- 🔄 Security vulnerability scanning

## 📞 Support

If you encounter issues:
1. Run `python setup_github.py` to check configuration
2. Check the [Troubleshooting](#-troubleshooting) section
3. Enable debug mode for detailed logs
4. Create an issue with logs and system information

---

**Ready to revolutionize your development workflow with AI-powered GitHub integration!** 🚀