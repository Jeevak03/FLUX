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
  const [activeAgents, setActiveAgents] = useState<string[]>([]);
  const [thinkingAgents, setThinkingAgents] = useState<string[]>([]);
  const [lastError, setLastError] = useState<string | undefined>();
  const ws = useRef<WebSocket | null>(null);
  const retryRef = useRef(0);
  const manualCloseRef = useRef(false);

  const buildUrl = () => {
    if (typeof window !== 'undefined' && (window as any).NEXT_PUBLIC_WS_URL) {
      return `${(window as any).NEXT_PUBLIC_WS_URL}/ws/${sessionId}`;
    }
    return process.env.NODE_ENV === 'production'
      ? `wss://your-backend.vercel.app/ws/${sessionId}`
      : `ws://localhost:8000/ws/${sessionId}`;
  };

  const healthCheck = async () => {
    try {
      const res = await fetch('http://localhost:8000/health', { method: 'GET' });
      return res.ok;
    } catch {
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
    };

    ws.current.onmessage = (event) => {
      try {
        const data: any = JSON.parse(event.data);
        if (data.type === 'agent_response') {
          setMessages(prev => [...prev, data]);
          // Automatically add responding agents to activeAgents list
          if (data.agent && data.agent !== 'system') {
            setActiveAgents(prev => {
              if (!prev.includes(data.agent)) {
                return [...prev, data.agent];
              }
              return prev;
            });
          }
        } else if (data.type === 'collaboration_update') {
          setActiveAgents(data.agents || []);
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

  const sendMessage = useCallback((request: string, context: any = {}, agents: string[] = []) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
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
      
      // Then send to WebSocket
      ws.current.send(JSON.stringify({
        request,
        context,
        requested_agents: agents,
        uploaded_files: uploadedFiles,
        history: messages.slice(-10)
      }));
    } else {
      setLastError('Cannot send message: socket not open');
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