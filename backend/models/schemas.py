# models/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class UploadedFile(BaseModel):
    id: str
    name: str
    type: str
    size: int
    content: str
    uploadedAt: str

class AgentMessage(BaseModel):
    type: str  # "agent_response", "collaboration_update", "status", "user_message"
    agent: str
    message: str
    timestamp: str
    uploadedFiles: List[UploadedFile] = []

class ProjectContext(BaseModel):
    projectName: str = ""
    technology: str = ""
    phase: str = "planning"

class UserRequest(BaseModel):
    request: str
    context: ProjectContext = ProjectContext()
    requested_agents: List[str] = []
    history: List[AgentMessage] = []
    uploaded_files: List[UploadedFile] = []

class SDLCState(BaseModel):
    user_request: str
    current_phase: str = "initial"
    agent_outputs: Dict[str, Any] = {}
    conversation_history: List[AgentMessage] = []
    project_context: Dict[str, Any] = {}
    uploaded_files: List[UploadedFile] = []
    next_agent: str = ""
    final_response: str = ""

class AgentInfo(BaseModel):
    id: str
    name: str
    role: str
    expertise: List[str]
    avatar: Optional[str] = None