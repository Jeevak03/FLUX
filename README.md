# 🚀 FLUX - Multi-Agent Collaboration System

**FLUX** is an advanced, real-time multi-agent collaboration platform powered by AI. It enables seamless interaction between specialized AI agents for comprehensive software development lifecycle (SDLC) management, project planning, and team collaboration.

## ✨ Features

### 🤖 **7 Specialized AI Agents**
- **Sara** (Requirements Analyst) - Analyzes and documents project requirements
- **Marc** (Software Architect) - Designs system architecture and technical specifications  
- **Alex** (Developer) - Implements features and writes code
- **Jess** (QA Tester) - Ensures quality through comprehensive testing
- **Dave** (DevOps Engineer) - Handles deployment and infrastructure
- **Emma** (Project Manager) - Coordinates team and manages timelines
- **Robt** (Security Expert) - Assesses security risks and implements protective measures

### 🔥 **Core Capabilities**
- **Direct Agent Routing** - Call specific agents with natural language ("Hi Marc", "Hello Jess")
- **Multi-Agent Collaboration** - Engage all agents with "Hi Everyone" or collaboration keywords
- **Real-time Communication** - WebSocket-powered instant messaging
- **Agent Status Tracking** - Dynamic online/offline status with intelligent detection
- **GitHub Integration** - Repository management, cloning, and VS Code integration
- **Document Upload** - File analysis and processing capabilities
- **Project Context Management** - Track project phases and progress
- **Workflow Visualization** - Visual representation of team collaboration

### 🌟 **Advanced Features**
- **Agent-to-Agent Communication** - Autonomous team coordination
- **Intelligent Keyword Detection** - Context-aware agent selection
- **Dynamic Status Management** - Agents can go offline/online during conversations
- **Clean UI Design** - Consolidated status management and intuitive interface
- **Hot Reload Support** - Development-friendly with instant updates

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **WebSockets** - Real-time bidirectional communication
- **Groq AI** - Advanced language model integration
- **Python 3.8+** - Modern Python features and async support

### Frontend
- **Next.js 14** - React framework with server-side rendering
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **React Hooks** - Modern state management

### Infrastructure
- **CORS Support** - Cross-origin resource sharing
- **Environment Configuration** - Secure API key management
- **Git Integration** - Version control and repository management

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- Git (for repository management)
- Groq API key ([Get one here](https://console.groq.com/))

### 1. Clone Repository
```bash
git clone <your-repository-url>
cd FLUX
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Add your Groq API key to .env
GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_token_here  # Optional, for GitHub integration
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Development server will run on port 3002
npm run dev
```

### 4. Start Backend
```bash
cd backend
python main_minimal.py
```

### 5. Access Application
- **Frontend**: [http://localhost:3002](http://localhost:3002)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🎯 Usage Examples

### Direct Agent Communication
```
"Hi Marc, can you review this system architecture?"
"Hello Jess, please create test cases for this feature"
"Hey Dave, what's the deployment status?"
```

### Multi-Agent Collaboration
```
"Hi Everyone, let's discuss the new project requirements"
"Team, we need to brainstorm solutions for this issue"
"All agents, collaborate on this security assessment"
```

### Project Management
```
"Emma, can you update the project timeline?"
"Sara, analyze these user requirements"
"Robt, perform a security audit on this code"
```

## 📁 Project Structure

```
FLUX/
├── 📁 backend/                 # Python FastAPI backend
│   ├── 🐍 main_minimal.py     # Main server with enhanced collaboration
│   ├── 📁 agents/             # AI agent definitions and personalities
│   ├── 📁 models/             # Data models and schemas
│   ├── 📁 routes/             # API route handlers
│   ├── 📁 services/           # Business logic and external services
│   ├── 📁 utils/              # Utility functions and helpers
│   ├── 📁 workflows/          # SDLC workflow management
│   └── 📄 requirements.txt    # Python dependencies
│
├── 📁 frontend/               # Next.js React frontend
│   ├── 📁 components/         # Reusable UI components
│   │   ├── 📁 AgentChat/      # Chat interface components
│   │   ├── 📁 EnhancedChat/   # Main chat interface
│   │   ├── 📁 GitHub/         # GitHub integration UI
│   │   └── 📁 UI/             # Base UI components
│   ├── 📁 hooks/              # React custom hooks
│   ├── 📁 pages/              # Next.js pages
│   ├── 📁 types/              # TypeScript type definitions
│   └── 📄 package.json       # Node.js dependencies
│
├── 📄 README.md               # This file
├── 📄 GITHUB_INTEGRATION.md   # GitHub integration guide
└── 📄 .env.example           # Environment variables template
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional - For GitHub Integration
GITHUB_TOKEN=your_github_token_here

# Optional - Custom Configuration
DEBUG=false
WORKSPACE_ROOT=C:\YOKA
```

### Agent Customization
Modify agent personalities in `backend/main_minimal.py`:

```python
AGENTS = {
    "sara": {
        "name": "Sara (Requirements Analyst)",
        "role": "requirements_analyst",
        "personality": "Your custom personality here..."
    },
    # ... other agents
}
```

## 🔌 API Reference

### WebSocket Endpoints
- **Connect**: `ws://localhost:8000/ws/{session_id}`
- **Message Types**: 
  - `user_message` - Send message to agents
  - `agent_response` - Receive agent responses
  - `agent_status` - Agent online/offline status updates
  - `collaboration_request` - Multi-agent collaboration

### REST Endpoints
- **Health Check**: `GET /health`
- **GitHub Routes**: `GET /github/*` (when GitHub integration enabled)

## 🧪 Testing

### Test Agent Routing
1. Open [http://localhost:3002](http://localhost:3002)
2. Try these test scenarios:
   - **Single Agent**: "Hi Marc" → Only Marc responds
   - **Collaboration**: "Hi Everyone" → All agents respond
   - **Context Aware**: "Sara, analyze these requirements"

### Test Status Tracking
1. Ask an agent to leave: "Jess, can you step away?"
2. Watch the online count decrease
3. Agent status should change to offline (gray dot)

### Test GitHub Integration
1. Configure `GITHUB_TOKEN` in `.env`
2. Navigate to GitHub tab
3. Clone a repository to test workspace management

## 🚀 Deployment

### Production Backend
```bash
cd backend
pip install gunicorn
gunicorn main_minimal:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Production Frontend
```bash
cd frontend
npm run build
npm start
```

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example for backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main_minimal.py"]
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines
- Follow existing code style and patterns
- Add TypeScript types for new frontend features
- Include docstrings for new Python functions
- Test agent interactions thoroughly
- Update documentation for new features

## 🐛 Troubleshooting

### Common Issues

**Backend won't start**
- Check if port 8000 is available: `netstat -an | find "8000"`
- Verify Groq API key is set in `.env`
- Install all requirements: `pip install -r requirements.txt`

**Frontend connection errors**
- Ensure backend is running on port 8000
- Check CORS configuration in `main_minimal.py`
- Try hard refresh: `Ctrl+Shift+R`

**Agents not responding**
- Check WebSocket connection status in browser console
- Verify agent names are spelled correctly
- Ensure Groq API key is valid and has credits

**Status tracking issues**
- Refresh browser to reset agent status
- Check for JavaScript errors in browser console
- Verify WebSocket messages in Network tab

### Debug Mode
Enable detailed logging by setting environment variables:
```bash
DEBUG=true
VERBOSE_LOGS=true
```

## 📊 Performance

### System Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB for application, additional for repositories
- **Network**: Stable internet for Groq API calls

### Optimization Tips
- Use production builds for better performance
- Configure proper WebSocket timeouts
- Monitor Groq API usage and limits
- Implement connection pooling for high traffic

## 🔐 Security

### Best Practices
- Never commit `.env` files to repository
- Use environment variables for all secrets
- Implement proper input validation
- Monitor API usage for unusual patterns
- Keep dependencies updated

### Data Privacy
- Messages are processed by Groq AI
- No conversation data is stored permanently
- GitHub tokens are used only for API access
- Local repositories remain on your machine

## 📝 Changelog

### v2.0.0 - Enhanced Collaboration System
- ✅ Multi-agent collaboration with "Hi Everyone"
- ✅ Agent-to-agent communication
- ✅ Dynamic status tracking with offline detection
- ✅ Clean UI with consolidated status management
- ✅ Improved agent routing with keyword detection

### v1.5.0 - Agent Status Tracking
- ✅ Real-time online/offline status
- ✅ Intelligent leaving message detection
- ✅ Dynamic agent count updates
- ✅ UI improvements and cleanup

### v1.0.0 - Initial Release
- ✅ 7 specialized AI agents
- ✅ Direct agent routing system
- ✅ WebSocket real-time communication
- ✅ GitHub integration
- ✅ Project context management

## 🙏 Acknowledgments

- **Groq** for providing powerful AI capabilities
- **FastAPI** for the excellent web framework
- **Next.js** for the robust React framework
- **Tailwind CSS** for beautiful UI components
- **Open Source Community** for inspiration and tools

## 📞 Support

Need help? Here are your options:

1. **Check the documentation** in this README
2. **Review troubleshooting** section above
3. **Enable debug mode** for detailed logs
4. **Check browser console** for frontend errors
5. **Verify environment configuration**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to revolutionize your team collaboration with AI-powered agents!** 🚀

*Built with ❤️ using FastAPI, Next.js, and Groq AI*