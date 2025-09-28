# FLUX - Where Agents Meet Agile

A comprehensive AI-powered development platform that orchestrates specialized agents for agile software development using LangGraph, FastAPI, and Groq AI.

## Architecture

This application consists of three main components:

- **Backend**: FastAPI server with LangGraph orchestration and Groq AI integration
- **Frontend**: Next.js React application with real-time WebSocket communication
- **Deployment**: Vercel hosting with serverless functions

## Features

- **7 Specialized AI Agents**:
  - Sara - Requirements Analyst
  - Marc - Software Architect
  - Alex - Senior Developer
  - Jess - QA Engineer
  - Dave - DevOps Engineer
  - Emma - Project Manager
  - Robt - Security Expert

- **Real-time Collaboration**: Multiple agents can work together on complex requests
- **WebSocket Communication**: Live updates and streaming responses
- **GitHub Integration**: Direct repository access and VS Code integration
- **Intelligent Routing**: LangGraph workflow automatically routes requests to appropriate agents

## Setup Instructions

### Prerequisites

1. **Python 3.8+** for the backend
2. **Node.js 18+** for the frontend
3. **Groq AI API Key** - Sign up at [groq.com](https://groq.com)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create environment file:
   ```bash
   # Create .env file in backend directory
   echo "GROQ_API_KEY=your-groq-api-key-here" > .env
   ```

4. Start the backend server:
   ```bash
   python run_full_server.py
   ```

   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Fix any security vulnerabilities:
   ```bash
   npm audit fix --force
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Deployment

### Vercel Deployment

1. **Backend Deployment**:
   - Connect your GitHub repository to Vercel
   - Set the root directory to `backend`
   - Add environment variables in Vercel dashboard:
     - `GROQ_API_KEY`
     - `REDIS_URL` (optional)

2. **Frontend Deployment**:
   - Create a new Vercel project for the frontend
   - Set the root directory to `frontend`
   - Add environment variable:
     - `NEXT_PUBLIC_WS_URL` (WebSocket URL for production)

### Environment Variables

#### Backend
- `GROQ_API_KEY`: Your Groq AI API key
- `REDIS_URL`: Redis connection URL (optional)
- `REDIS_HOST`: Redis host (default: localhost)
- `REDIS_PORT`: Redis port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)

#### Frontend
- `NEXT_PUBLIC_WS_URL`: WebSocket URL for the backend API

## Usage

1. **Select Agents**: Choose which SDLC agents you want to involve in the conversation
2. **Set Project Context**: Provide project name, technology stack, and current phase
3. **Start Chatting**: Ask questions or describe requirements to get AI-powered assistance
4. **Real-time Collaboration**: Watch as multiple agents work together on complex requests

### Agent Model Configuration

The application uses diversified Groq models for each SDLC agent role:

- **Requirements Analyst (Sarah)**: `llama-3.3-70b-versatile` - Advanced analysis capabilities for complex requirement gathering
- **Software Architect (Marcus)**: `llama-3.1-8b-instant` - Fast architectural decisions and system design
- **Developer Agent (Alex)**: `openai/gpt-oss-120b` - Code generation and development tasks with high context (131K tokens)
- **QA Tester (Jessica)**: `openai/gpt-oss-20b` - Thorough testing analysis and quality assurance (65K max completion)
- **DevOps Engineer (David)**: `meta-llama/llama-guard-4-12b` - Infrastructure and deployment with safety focus (20MB file support)
- **Project Manager (Emily)**: `llama-3.1-8b-instant` - Quick project decisions and coordination
- **Security Expert (Robert)**: `llama-3.3-70b-versatile` - Security analysis and recommendations

## API Documentation

The FastAPI backend provides automatic API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## WebSocket Communication

The application uses WebSocket connections for real-time communication:

- **Connection**: `ws://localhost:8000/ws/{session_id}`
- **Message Types**:
  - `agent_response`: Individual agent responses
  - `collaboration_update`: Multi-agent collaboration status
  - `status_update`: System status messages
  - `error`: Error messages

## Architecture Details

### Backend Components

- **Agents**: Specialized AI personas with different Groq models
- **LangGraph Workflow**: Orchestrates agent interactions and routing
- **WebSocket Manager**: Handles real-time communication
- **Session Manager**: Manages user sessions and conversation history

### Frontend Components

- **WebSocket Hook**: Manages WebSocket connections and state
- **Agent Components**: UI components for agent selection and display
- **Chat Interface**: Real-time chat with message history
- **Collaboration View**: Shows active multi-agent collaborations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or contact the development team.