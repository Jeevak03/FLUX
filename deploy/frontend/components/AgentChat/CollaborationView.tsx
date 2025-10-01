// components/AgentChat/CollaborationView.tsx
import React from 'react';
import { AgentInfo } from '../../types/agents';
import { AgentAvatar } from './AgentAvatar';
import { LoadingSpinner } from '../UI/LoadingSpinner';

interface CollaborationViewProps {
  activeAgents: AgentInfo[];
}

export const CollaborationView: React.FC<CollaborationViewProps> = ({ activeAgents }) => {
  if (activeAgents.length === 0) return null;

  return (
    <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-4 mb-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="flex -space-x-2">
            {activeAgents.slice(0, 3).map((agent) => (
              <AgentAvatar key={agent.id} agent={agent} size="sm" />
            ))}
            {activeAgents.length > 3 && (
              <div className="w-8 h-8 rounded-full bg-gray-400 flex items-center justify-center text-white text-xs font-medium">
                +{activeAgents.length - 3}
              </div>
            )}
          </div>
          <div>
            <h4 className="font-medium text-gray-900">Agent Collaboration</h4>
            <p className="text-sm text-gray-600">
              {activeAgents.length} agent{activeAgents.length > 1 ? 's are' : ' is'} working together
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <LoadingSpinner size="sm" />
          <span className="text-sm text-blue-600">Processing...</span>
        </div>
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        {activeAgents.map((agent) => (
          <div key={agent.id} className="flex items-center space-x-2 bg-white rounded-full px-3 py-1 shadow-sm">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-sm text-gray-700">{agent.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
};