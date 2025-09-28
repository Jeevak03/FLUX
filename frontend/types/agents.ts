// types/agents.ts
export interface UploadedFile {
  id: string;
  name: string;
  type: string;
  size: number;
  content?: string;
  url?: string;
  uploadedAt: string;
}

export interface AgentMessage {
  type: 'agent_response' | 'collaboration_update' | 'status_update' | 'error' | 'user_message';
  agent: string;
  message: string;
  timestamp: string;
  agents?: string[];
  status?: string;
  details?: string;
  context?: any;
  uploadedFiles?: UploadedFile[];
}

export interface ProjectContext {
  projectName: string;
  technology: string;
  phase: 'planning' | 'requirements' | 'design' | 'development' | 'testing' | 'deployment';
}

export interface AgentInfo {
  id: string;
  name: string;
  role: string;
  expertise: string[];
  avatar?: string;
}

export interface UserRequest {
  request: string;
  context: ProjectContext;
  requested_agents: string[];
  history: AgentMessage[];
}