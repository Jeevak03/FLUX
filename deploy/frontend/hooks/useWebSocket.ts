// hooks/useWebSocket.ts
import { useState, useEffect, useRef, useCallback } from 'react';
import { AgentMessage } from '../types/agents';

interface UseWebSocketReturn {
  messages: AgentMessage[];
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'error';
  activeAgents: string[];
  lastError?: string;
  sendMessage: (request: string, context: any, agents: string[]) => void;
  reconnect: () => void;
}

const MAX_RETRIES = 5;
const BASE_DELAY = 500; // ms

export const useWebSocket = (sessionId: string): UseWebSocketReturn => {
  const [messages, setMessages] = useState<AgentMessage[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');
  const [activeAgents, setActiveAgents] = useState<string[]>([
    'requirements_analyst',
    'software_architect', 
    'developer',
    'qa_tester',
    'devops_engineer',
    'project_manager',
    'security_expert'
  ]);
  const [thinkingAgents, setThinkingAgents] = useState<string[]>([]);
  const [lastError, setLastError] = useState<string | undefined>();
  const ws = useRef<WebSocket | null>(null);
  const retryRef = useRef(0);
  const manualCloseRef = useRef(false);

  const buildUrl = () => {
    if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_WS_URL) {
      return `${process.env.NEXT_PUBLIC_WS_URL}/ws/${sessionId}`;
    }
    return process.env.NODE_ENV === 'production'
      ? `wss://${window.location.host}/api/ws/${sessionId}`
      : `ws://localhost:8000/ws/${sessionId}`;
  };

  const getApiUrl = () => {
    if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_API_URL) {
      return process.env.NEXT_PUBLIC_API_URL;
    }
    return process.env.NODE_ENV === 'production'
      ? `/api`
      : `http://localhost:8000`;
  };

  const healthCheck = async () => {
    try {
      const apiUrl = getApiUrl();
      const res = await fetch(`${apiUrl}/health`, { method: 'GET' });
      return res.ok;
    } catch {
      return false;
    }
  };

  // REST API fallback for serverless environments
  const sendMessageViaRest = async (message: string) => {
    try {
      const apiUrl = getApiUrl();
      const response = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      
      // Process responses
      if (data.responses && Array.isArray(data.responses)) {
        data.responses.forEach((resp: any) => {
          const agentMessage: AgentMessage = {
            type: 'agent_response',
            agent: resp.agent,
            message: resp.message,
            timestamp: resp.timestamp || new Date().toISOString()
          };
          setMessages(prev => [...prev, agentMessage]);
        });
      }
      
      return true;
    } catch (error) {
      console.error('REST API error:', error);
      setLastError(`API Error: ${error}`);
      return false;
    }
  };

  const scheduleReconnect = () => {
    if (retryRef.current >= MAX_RETRIES) {
      setConnectionStatus('error');
      setLastError(`Maximum reconnect attempts (${MAX_RETRIES}) reached.`);
      return;
    }
    const delay = BASE_DELAY * Math.pow(2, retryRef.current); // exponential backoff
    retryRef.current += 1;
    setTimeout(() => {
      connect(true);
    }, delay);
  };

  const connect = useCallback(async (isRetry = false) => {
    if (ws.current && (ws.current.readyState === WebSocket.OPEN || ws.current.readyState === WebSocket.CONNECTING)) {
      return;
    }

    setConnectionStatus('connecting');
    setLastError(undefined);

    // Ensure backend is up before opening socket (avoid instant close)
    const healthy = await healthCheck();
    if (!healthy) {
      setLastError('Backend health check failed');
      scheduleReconnect();
      return;
    }

    const url = buildUrl();
    try {
      ws.current = new WebSocket(url);
    } catch (e: any) {
      setLastError(`WebSocket init error: ${e.message || e}`);
      scheduleReconnect();
      return;
    }

    ws.current.onopen = () => {
      retryRef.current = 0;
      setConnectionStatus('connected');
      // Ensure all agents show as active/online when connected
      setActiveAgents([
        'requirements_analyst',
        'software_architect', 
        'developer',
        'qa_tester',
        'devops_engineer',
        'project_manager',
        'security_expert'
      ]);
    };

    ws.current.onmessage = (event) => {
      try {
        const data: any = JSON.parse(event.data);
        if (data.type === 'agent_response') {
          setMessages(prev => [...prev, data]);
          
          // Handle agent status based on message content
          if (data.agent && data.agent !== 'system') {
            // Check if agent is leaving/stepping away
            const message = data.message?.toLowerCase() || '';
            const isLeavingMessage = message.includes("i'll step away") || 
                                   message.includes("leaving the chat") || 
                                   message.includes("signing off") ||
                                   message.includes("catch up with you all later") ||
                                   message.includes("i'll be offline");
            
            if (isLeavingMessage) {
              // Remove agent from active list
              setActiveAgents(prev => prev.filter(agent => agent !== data.agent));
            } else {
              // Add responding agents to activeAgents list
              setActiveAgents(prev => {
                if (!prev.includes(data.agent)) {
                  return [...prev, data.agent];
                }
                return prev;
              });
            }
          }
        } else if (data.type === 'collaboration_update') {
          setActiveAgents(data.agents || []);
        } else if (data.type === 'agent_status') {
          // Handle explicit agent status updates
          if (data.agent && data.status) {
            if (data.status === 'offline' || data.status === 'away') {
              setActiveAgents(prev => prev.filter(agent => agent !== data.agent));
            } else if (data.status === 'online') {
              setActiveAgents(prev => {
                if (!prev.includes(data.agent)) {
                  return [...prev, data.agent];
                }
                return prev;
              });
            }
          }
        } else if (data.type === 'status_update') {
          if (data.status === 'connected') {
            setConnectionStatus('connected');
          }
          // optional debug
          // console.debug('Status update:', data);
        } else if (data.type === 'error') {
          setMessages(prev => [...prev, data]);
          setLastError(data.message || 'Unknown WebSocket error');
        }
      } catch (error: any) {
        setLastError(`Parse error: ${error.message || error}`);
      }
    };

    ws.current.onclose = (evt) => {
      const code = evt.code;
      const reason = evt.reason || 'No reason';
      if (!manualCloseRef.current) {
        setConnectionStatus('disconnected');
        setLastError(`Closed (code=${code}): ${reason}`);
        scheduleReconnect();
      }
    };

    ws.current.onerror = (error: any) => {
      setConnectionStatus('error');
      setLastError('WebSocket error event');
      try { ws.current?.close(); } catch {}
    };
  }, [sessionId]);

  const sendMessage = useCallback(async (request: string, context: any = {}, agents: string[] = []) => {
    // Include uploaded files from context if they exist
    const uploadedFiles = context.uploadedFiles || [];
    
    // First add the user message to the messages array
    const userMessage: AgentMessage = {
      agent: 'user',
      message: request,
      timestamp: new Date().toISOString(),
      type: 'user_message',
      context: context,
      uploadedFiles: uploadedFiles
    };
    
    setMessages(prev => [...prev, userMessage]);
    
    // Try WebSocket first, fallback to REST API
    if (ws.current?.readyState === WebSocket.OPEN) {
      try {
        ws.current.send(JSON.stringify({
          type: 'user_message',
          message: request,
          context,
          requested_agents: agents,
          uploaded_files: uploadedFiles,
          history: messages.slice(-10)
        }));
      } catch (error) {
        console.error('WebSocket send error:', error);
        // Fallback to REST API
        await sendMessageViaRest(request);
      }
    } else {
      // WebSocket not available, use REST API
      const success = await sendMessageViaRest(request);
      if (!success) {
        setLastError('Cannot send message: both WebSocket and REST API failed');
      }
    }
  }, [messages]);

  useEffect(() => {
    manualCloseRef.current = false;
    connect();
    return () => {
      manualCloseRef.current = true;
      ws.current?.close(1000, 'Component unmount');
    };
  }, [connect]);

  const reconnect = () => {
    if (connectionStatus === 'connected') return;
    retryRef.current = 0;
    manualCloseRef.current = false;
    connect();
  };

  return {
    messages,
    connectionStatus,
    activeAgents,
    lastError,
    sendMessage,
    reconnect
  };
};