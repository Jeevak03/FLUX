// components/AgentChat/ProjectContextPanel.tsx
import React, { useState } from 'react';
import { AgentMessage } from '../../types/agents';

interface ProjectInfo {
  name: string;
  technology: string;
  phase: string;
  description?: string;
  startDate?: string;
}

interface ProjectContextPanelProps {
  projectInfo: ProjectInfo;
  messages: AgentMessage[];
  activeAgents: string[];
  onUpdateProject?: (updates: Partial<ProjectInfo>) => void;
}

export const ProjectContextPanel: React.FC<ProjectContextPanelProps> = ({
  projectInfo,
  messages,
  activeAgents,
  onUpdateProject
}) => {
  const [isExpanded, setIsExpanded] = useState(true);

  const getPhaseColor = (phase: string) => {
    const colors: { [key: string]: string } = {
      'requirements': 'bg-purple-100 text-purple-800 border-purple-200',
      'planning': 'bg-blue-100 text-blue-800 border-blue-200',
      'design': 'bg-indigo-100 text-indigo-800 border-indigo-200',
      'development': 'bg-green-100 text-green-800 border-green-200',
      'testing': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'deployment': 'bg-red-100 text-red-800 border-red-200',
      'maintenance': 'bg-gray-100 text-gray-800 border-gray-200'
    };
    return colors[phase.toLowerCase()] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getPhaseIcon = (phase: string) => {
    const icons: { [key: string]: string } = {
      'requirements': '📋',
      'planning': '🗓️',
      'design': '🎨',
      'development': '⚡',
      'testing': '🧪',
      'deployment': '🚀',
      'maintenance': '🔧'
    };
    return icons[phase.toLowerCase()] || '📊';
  };

  const getPhaseProgress = (phase: string): number => {
    const progressMap: { [key: string]: number } = {
      'requirements': 10,
      'planning': 25,
      'design': 40,
      'development': 60,
      'testing': 80,
      'deployment': 95,
      'maintenance': 100
    };
    return progressMap[phase.toLowerCase()] || 0;
  };

  const getRecentActivity = () => {
    return messages.slice(-3).reverse().map(msg => ({
      agent: msg.agent,
      preview: msg.message.substring(0, 80) + (msg.message.length > 80 ? '...' : ''),
      timestamp: new Date().toLocaleTimeString()
    }));
  };

  const recentActivity = getRecentActivity();
  const progress = getPhaseProgress(projectInfo.phase);

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
      {/* Header */}
      <div 
        className="bg-gradient-to-r from-indigo-500 to-purple-600 p-4 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between text-white">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
              📁
            </div>
            <div>
              <h3 className="font-semibold text-lg">{projectInfo.name}</h3>
              <p className="text-sm text-white/80">{projectInfo.technology}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`px-3 py-1 rounded-full border text-sm font-medium ${getPhaseColor(projectInfo.phase)} bg-white/90`}>
              {getPhaseIcon(projectInfo.phase)} {projectInfo.phase}
            </div>
            <button className="text-white/80 hover:text-white">
              {isExpanded ? '⬆️' : '⬇️'}
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      {isExpanded && (
        <div className="p-4 space-y-4">
          {/* Progress Bar */}
          <div>
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Project Progress</span>
              <span>{progress}% Complete</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-indigo-500 to-purple-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          {/* Team Status */}
          <div className="bg-gray-50 rounded-lg p-3">
            <h4 className="font-medium text-gray-900 mb-2 flex items-center">
              👥 Team Status
            </h4>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-gray-600">{activeAgents.length} agents online</span>
              </div>
              <div className="text-xs text-gray-500">
                {messages.length} messages exchanged
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          {recentActivity.length > 0 && (
            <div>
              <h4 className="font-medium text-gray-900 mb-3 flex items-center">
                ⚡ Recent Activity
              </h4>
              <div className="space-y-2">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-start space-x-3 p-2 bg-gray-50 rounded-lg">
                    <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-xs text-white font-bold">
                      {activity.agent.charAt(0).toUpperCase()}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900 truncate">{activity.preview}</p>
                      <p className="text-xs text-gray-500">{activity.timestamp}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Quick Stats */}
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-blue-50 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-blue-600">{messages.length}</div>
              <div className="text-xs text-blue-600">Messages</div>
            </div>
            <div className="bg-green-50 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-green-600">{activeAgents.length}</div>
              <div className="text-xs text-green-600">Active Agents</div>
            </div>
          </div>

          {/* Phase Navigation */}
          <div className="border-t pt-3">
            <h4 className="font-medium text-gray-900 mb-2 text-sm">SDLC Phases</h4>
            <div className="flex flex-wrap gap-1">
              {['requirements', 'design', 'development', 'testing', 'deployment'].map((phase) => {
                const isCurrent = phase === projectInfo.phase.toLowerCase();
                const isCompleted = getPhaseProgress(phase) < progress;
                
                return (
                  <button
                    key={phase}
                    className={`px-2 py-1 text-xs rounded-full border transition-all ${
                      isCurrent 
                        ? 'bg-indigo-100 text-indigo-800 border-indigo-300 font-medium' 
                        : isCompleted
                        ? 'bg-green-50 text-green-700 border-green-200'
                        : 'bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100'
                    }`}
                    onClick={() => onUpdateProject?.({ phase })}
                  >
                    {getPhaseIcon(phase)} {phase}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};