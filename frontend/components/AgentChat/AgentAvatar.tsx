// components/AgentChat/AgentAvatar.tsx
import React from 'react';
import { AgentInfo } from '../../types/agents';

interface AgentAvatarProps {
  agent: AgentInfo;
  size?: 'sm' | 'md' | 'lg';
  showName?: boolean;
}

export const AgentAvatar: React.FC<AgentAvatarProps> = ({
  agent,
  size = 'md',
  showName = false
}) => {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12'
  };

  const textSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  };

  // Generate initials from agent name
  const initials = agent.name.split(' ').map(n => n[0]).join('').toUpperCase();

  return (
    <div className="flex items-center space-x-2">
      <div className={`${sizeClasses[size]} rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-semibold ${textSizeClasses[size]}`}>
        {initials}
      </div>
      {showName && (
        <div>
          <div className="font-medium text-gray-900">{agent.name}</div>
          <div className="text-sm text-gray-500">{agent.role}</div>
        </div>
      )}
    </div>
  );
};