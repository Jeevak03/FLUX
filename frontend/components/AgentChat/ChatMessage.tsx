// components/AgentChat/ChatMessage.tsx
import React from 'react';
import { AgentMessage, AgentInfo } from '../../types/agents';
import { AgentAvatar } from './AgentAvatar';

interface ChatMessageProps {
  message: AgentMessage;
  agent?: AgentInfo;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message, agent }) => {
  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getMessageTypeColor = (type: string) => {
    switch (type) {
      case 'agent_response':
        return 'bg-blue-50 border-blue-200';
      case 'error':
        return 'bg-red-50 border-red-200';
      case 'status_update':
        return 'bg-gray-50 border-gray-200';
      default:
        return 'bg-white border-gray-200';
    }
  };

  return (
    <div className={`p-4 rounded-lg border ${getMessageTypeColor(message.type)}`}>
      <div className="flex items-start space-x-3">
        {agent && <AgentAvatar agent={agent} size="sm" />}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              {agent && (
                <span className="font-medium text-gray-900">{agent.name}</span>
              )}
              <span className="text-xs text-gray-500 uppercase">{message.type.replace('_', ' ')}</span>
            </div>
            <span className="text-xs text-gray-500">{formatTimestamp(message.timestamp)}</span>
          </div>
          <div className="mt-1 text-gray-700 whitespace-pre-wrap">{message.message}</div>
          {message.details && (
            <div className="mt-2 text-sm text-gray-600">{message.details}</div>
          )}
        </div>
      </div>
    </div>
  );
};