// components/AgentChat/AgentSelector.tsx
import React from 'react';
import { AgentInfo } from '../../types/agents';
import { AgentAvatar } from './AgentAvatar';

interface AgentSelectorProps {
  agents: AgentInfo[];
  selectedAgents: string[];
  onAgentToggle: (agentId: string) => void;
  activeAgents: string[];
  thinkingAgents?: string[];
}

export const AgentSelector: React.FC<AgentSelectorProps> = ({
  agents,
  selectedAgents,
  onAgentToggle,
  activeAgents,
  thinkingAgents = []
}) => {
  const getAgentStatus = (agentId: string) => {
    if (thinkingAgents.includes(agentId)) return 'thinking';
    if (activeAgents.includes(agentId)) return 'active';
    return 'idle';
  };

  const getStatusIndicator = (status: string) => {
    switch (status) {
      case 'thinking':
        return (
          <div className="flex space-x-1 items-center">
            <div className="flex space-x-1">
              <div className="w-1.5 h-1.5 bg-yellow-500 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
              <div className="w-1.5 h-1.5 bg-yellow-500 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
              <div className="w-1.5 h-1.5 bg-yellow-500 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
            </div>
            <span className="text-xs text-yellow-600 font-medium ml-1">Thinking...</span>
          </div>
        );
      case 'active':
        return (
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-lg shadow-green-500/50"></div>
            <span className="text-xs text-green-600 font-medium">Available online</span>
          </div>
        );
      default:
        return (
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
            <span className="text-xs text-gray-500">Ready</span>
          </div>
        );
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-100">
      <div className="flex items-center justify-between mb-5">
        <h3 className="text-xl font-semibold text-gray-900 flex items-center">
          SDLC Team
        </h3>
        <div className="text-sm text-gray-500">
          {activeAgents.length} online • {selectedAgents.length} selected
        </div>
      </div>
      
      <div className="space-y-4">
        {agents.map((agent) => {
          const isSelected = selectedAgents.includes(agent.id);
          const status = getAgentStatus(agent.id);

          return (
            <div
              key={agent.id}
              onClick={() => onAgentToggle(agent.id)}
              className={`relative p-4 rounded-xl border-2 cursor-pointer transition-all duration-300 hover:shadow-md group ${
                isSelected
                  ? 'border-blue-500 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-md'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              } ${
                status === 'thinking' ? 'ring-2 ring-yellow-400/50 animate-pulse' : ''
              } ${
                status === 'active' ? 'ring-2 ring-green-400/30' : ''
              }`}
            >
              {/* Selection Indicator */}
              {isSelected && (
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center shadow-lg z-10">
                  <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              )}

              <div className="flex items-center space-x-4">
                <div className="relative">
                  <AgentAvatar agent={agent} size="lg" />
                  {/* Status dot overlay */}
                  <div className="absolute -bottom-1 -right-1">
                    {status === 'active' && <div className="w-4 h-4 bg-green-500 rounded-full border-2 border-white animate-pulse"></div>}
                    {status === 'thinking' && <div className="w-4 h-4 bg-yellow-500 rounded-full border-2 border-white animate-bounce"></div>}
                    {status === 'idle' && <div className="w-4 h-4 bg-gray-400 rounded-full border-2 border-white"></div>}
                  </div>
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <h4 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {agent.name}
                    </h4>
                  </div>
                  
                  <p className="text-sm text-gray-600 mb-2 capitalize">
                    {agent.role.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </p>
                  
                  {/* Status Indicator */}
                  <div className="mb-2">
                    {getStatusIndicator(status)}
                  </div>
                  
                  {/* Expertise Tags */}
                  <div className="flex flex-wrap gap-1">
                    {agent.expertise.slice(0, 3).map((skill) => (
                      <span
                        key={skill}
                        className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full border group-hover:bg-blue-100 group-hover:text-blue-700 transition-colors"
                      >
                        {skill}
                      </span>
                    ))}
                    {agent.expertise.length > 3 && (
                      <span className="px-2 py-1 text-xs bg-gray-100 text-gray-500 rounded-full">
                        +{agent.expertise.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Hover Effect */}
              <div className={`absolute inset-0 rounded-xl bg-gradient-to-r from-blue-400/5 to-indigo-400/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none ${isSelected ? 'opacity-100' : ''}`}></div>
            </div>
          );
        })}
      </div>
      
      {/* Team Summary */}
      {selectedAgents.length > 0 && (
        <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200">
          <div className="flex items-center justify-between">
            <div className="text-sm text-blue-800">
              <strong className="text-lg">{selectedAgents.length}</strong> agent{selectedAgents.length > 1 ? 's' : ''} selected for collaboration
            </div>
            <div className="text-xs text-blue-600 bg-blue-100 px-3 py-1 rounded-full">
              Ready to collaborate
            </div>
          </div>
        </div>
      )}
    </div>
  );
};