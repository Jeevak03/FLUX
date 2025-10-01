// components/AgentChat/WorkflowVisualization.tsx
import React, { useState, useEffect } from 'react';
import { AgentMessage } from '../../types/agents';

interface WorkflowPhase {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  agents: string[];
  deliverables: string[];
  status: 'pending' | 'active' | 'completed' | 'blocked';
  progress: number;
  estimatedDuration: string;
  dependencies: string[];
}

interface WorkflowVisualizationProps {
  messages: AgentMessage[];
  activeAgents: string[];
  currentPhase?: string;
  onPhaseSelect?: (phaseId: string) => void;
  className?: string;
}

export const WorkflowVisualization: React.FC<WorkflowVisualizationProps> = ({
  messages,
  activeAgents,
  currentPhase = 'requirements',
  onPhaseSelect,
  className = ''
}) => {
  const [selectedPhase, setSelectedPhase] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'timeline' | 'kanban' | 'circle'>('timeline');
  const [showDetails, setShowDetails] = useState(false);

  // SDLC Workflow Phases
  const workflowPhases: WorkflowPhase[] = [
    {
      id: 'requirements',
      name: 'Requirements Analysis',
      description: 'Gather and analyze project requirements',
      icon: '📋',
      color: 'bg-purple-500',
      agents: ['requirements_analyst', 'project_manager'],
      deliverables: ['Requirements Document', 'User Stories', 'Acceptance Criteria'],
      status: currentPhase === 'requirements' ? 'active' : 'completed',
      progress: currentPhase === 'requirements' ? 75 : 100,
      estimatedDuration: '1-2 weeks',
      dependencies: []
    },
    {
      id: 'design',
      name: 'System Design',
      description: 'Design system architecture and components',
      icon: '🏗️',
      color: 'bg-blue-500',
      agents: ['software_architect', 'developer'],
      deliverables: ['System Architecture', 'API Design', 'Database Schema'],
      status: currentPhase === 'design' ? 'active' : 
              ['requirements'].includes(currentPhase) ? 'pending' : 'completed',
      progress: currentPhase === 'design' ? 45 : 
                ['requirements'].includes(currentPhase) ? 0 : 100,
      estimatedDuration: '2-3 weeks',
      dependencies: ['requirements']
    },
    {
      id: 'development',
      name: 'Development',
      description: 'Implement features and functionality',
      icon: '💻',
      color: 'bg-green-500',
      agents: ['developer', 'software_architect'],
      deliverables: ['Source Code', 'Unit Tests', 'Documentation'],
      status: currentPhase === 'development' ? 'active' :
              ['requirements', 'design'].includes(currentPhase) ? 'pending' : 'completed',
      progress: currentPhase === 'development' ? 60 :
                ['requirements', 'design'].includes(currentPhase) ? 0 : 100,
      estimatedDuration: '4-6 weeks',
      dependencies: ['design']
    },
    {
      id: 'testing',
      name: 'Testing & QA',
      description: 'Test functionality and ensure quality',
      icon: '🧪',
      color: 'bg-yellow-500',
      agents: ['qa_tester', 'developer'],
      deliverables: ['Test Plans', 'Test Cases', 'Bug Reports'],
      status: currentPhase === 'testing' ? 'active' :
              ['requirements', 'design', 'development'].includes(currentPhase) ? 'pending' : 'completed',
      progress: currentPhase === 'testing' ? 30 :
                ['requirements', 'design', 'development'].includes(currentPhase) ? 0 : 100,
      estimatedDuration: '2-3 weeks',
      dependencies: ['development']
    },
    {
      id: 'security',
      name: 'Security Review',
      description: 'Security assessment and vulnerability testing',
      icon: '🛡️',
      color: 'bg-red-500',
      agents: ['security_expert', 'developer'],
      deliverables: ['Security Assessment', 'Vulnerability Report', 'Security Fixes'],
      status: currentPhase === 'security' ? 'active' :
              ['requirements', 'design', 'development', 'testing'].includes(currentPhase) ? 'pending' : 'completed',
      progress: currentPhase === 'security' ? 20 :
                ['requirements', 'design', 'development', 'testing'].includes(currentPhase) ? 0 : 100,
      estimatedDuration: '1 week',
      dependencies: ['testing']
    },
    {
      id: 'deployment',
      name: 'Deployment',
      description: 'Deploy to production environment',
      icon: '🚀',
      color: 'bg-indigo-500',
      agents: ['devops_engineer', 'developer'],
      deliverables: ['Deployment Plan', 'Infrastructure Setup', 'Monitoring'],
      status: currentPhase === 'deployment' ? 'active' : 'pending',
      progress: currentPhase === 'deployment' ? 10 : 0,
      estimatedDuration: '1-2 weeks',
      dependencies: ['security']
    },
    {
      id: 'maintenance',
      name: 'Maintenance',
      description: 'Ongoing maintenance and support',
      icon: '🔧',
      color: 'bg-gray-500',
      agents: ['devops_engineer', 'project_manager'],
      deliverables: ['Support Documentation', 'Monitoring Setup', 'Update Plans'],
      status: 'pending',
      progress: 0,
      estimatedDuration: 'Ongoing',
      dependencies: ['deployment']
    }
  ];

  const getPhaseStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'border-green-500 bg-green-50';
      case 'active': return 'border-blue-500 bg-blue-50 ring-2 ring-blue-200';
      case 'blocked': return 'border-red-500 bg-red-50';
      default: return 'border-gray-300 bg-gray-50';
    }
  };

  const getAgentAvatar = (agentId: string) => {
    const avatars: { [key: string]: string } = {
      'requirements_analyst': '👩‍💼',
      'software_architect': '👨‍💻',
      'developer': '👩‍💻',
      'qa_tester': '👩‍🔬',
      'devops_engineer': '👨‍🔧',
      'project_manager': '👩‍💼',
      'security_expert': '👨‍🛡️'
    };
    return avatars[agentId] || '👤';
  };

  const calculateOverallProgress = () => {
    const totalPhases = workflowPhases.length;
    const totalProgress = workflowPhases.reduce((sum, phase) => sum + phase.progress, 0);
    return Math.round(totalProgress / totalPhases);
  };

  const renderTimelineView = () => (
    <div className="relative">
      {/* Progress line */}
      <div className="absolute left-8 top-12 bottom-12 w-0.5 bg-gray-300"></div>
      <div 
        className="absolute left-8 top-12 w-0.5 bg-blue-500 transition-all duration-1000"
        style={{ height: `${calculateOverallProgress() * 0.8}%` }}
      ></div>

      {/* Phase cards */}
      <div className="space-y-6">
        {workflowPhases.map((phase, index) => (
          <div
            key={phase.id}
            className={`relative flex items-start space-x-6 cursor-pointer transition-all duration-200 ${
              selectedPhase === phase.id ? 'transform scale-102' : ''
            }`}
            onClick={() => {
              setSelectedPhase(selectedPhase === phase.id ? null : phase.id);
              onPhaseSelect?.(phase.id);
            }}
          >
            {/* Phase indicator */}
            <div className={`relative z-10 w-16 h-16 rounded-full border-4 ${getPhaseStatusColor(phase.status)} 
              flex items-center justify-center text-2xl shadow-lg transition-all duration-200 hover:scale-110`}>
              {phase.icon}
              {phase.status === 'active' && (
                <div className="absolute inset-0 rounded-full border-2 border-blue-400 animate-pulse"></div>
              )}
            </div>

            {/* Phase content */}
            <div className={`flex-1 border-2 rounded-xl p-4 transition-all duration-200 ${getPhaseStatusColor(phase.status)}`}>
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-lg text-gray-900">{phase.name}</h3>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 text-xs rounded-full font-medium ${
                    phase.status === 'completed' ? 'bg-green-100 text-green-800' :
                    phase.status === 'active' ? 'bg-blue-100 text-blue-800' :
                    phase.status === 'blocked' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-600'
                  }`}>
                    {phase.status.toUpperCase()}
                  </span>
                  <span className="text-sm text-gray-600">{phase.estimatedDuration}</span>
                </div>
              </div>

              <p className="text-gray-600 text-sm mb-3">{phase.description}</p>

              {/* Progress bar */}
              <div className="mb-3">
                <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                  <span>Progress</span>
                  <span>{phase.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-1000 ${phase.color.replace('bg-', 'bg-')}`}
                    style={{ width: `${phase.progress}%` }}
                  ></div>
                </div>
              </div>

              {/* Assigned agents */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">Team:</span>
                  <div className="flex -space-x-2">
                    {phase.agents.map((agentId) => (
                      <div
                        key={agentId}
                        className={`w-8 h-8 rounded-full border-2 border-white flex items-center justify-center text-sm ${
                          activeAgents.includes(agentId) ? 'ring-2 ring-green-400' : ''
                        }`}
                        style={{ backgroundColor: '#f3f4f6' }}
                        title={agentId.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      >
                        {getAgentAvatar(agentId)}
                      </div>
                    ))}
                  </div>
                </div>

                {selectedPhase === phase.id && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowDetails(!showDetails);
                    }}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    {showDetails ? 'Hide Details' : 'Show Details'}
                  </button>
                )}
              </div>

              {/* Expanded details */}
              {selectedPhase === phase.id && showDetails && (
                <div className="mt-4 pt-4 border-t border-gray-200 space-y-3 animate-in slide-in-from-top duration-300">
                  <div>
                    <h4 className="font-medium text-gray-800 mb-2">📦 Deliverables</h4>
                    <div className="flex flex-wrap gap-2">
                      {phase.deliverables.map((deliverable) => (
                        <span
                          key={deliverable}
                          className="px-3 py-1 bg-white border border-gray-200 rounded-full text-sm"
                        >
                          {deliverable}
                        </span>
                      ))}
                    </div>
                  </div>

                  {phase.dependencies.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-800 mb-2">🔗 Dependencies</h4>
                      <div className="flex flex-wrap gap-2">
                        {phase.dependencies.map((depId) => {
                          const depPhase = workflowPhases.find(p => p.id === depId);
                          return depPhase ? (
                            <span
                              key={depId}
                              className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm"
                            >
                              {depPhase.icon} {depPhase.name}
                            </span>
                          ) : null;
                        })}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderKanbanView = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {['pending', 'active', 'completed', 'blocked'].map((status) => (
        <div key={status} className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-semibold text-gray-800 mb-4 text-center">
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </h3>
          <div className="space-y-3">
            {workflowPhases.filter(phase => phase.status === status).map((phase) => (
              <div
                key={phase.id}
                className="bg-white rounded-lg p-3 shadow-sm border border-gray-200 cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => onPhaseSelect?.(phase.id)}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-lg">{phase.icon}</span>
                  <span className="text-xs text-gray-500">{phase.progress}%</span>
                </div>
                <h4 className="font-medium text-sm text-gray-900 mb-1">{phase.name}</h4>
                <p className="text-xs text-gray-600 mb-2">{phase.description}</p>
                <div className="flex -space-x-1">
                  {phase.agents.slice(0, 3).map((agentId) => (
                    <div
                      key={agentId}
                      className="w-6 h-6 rounded-full border border-white bg-gray-100 flex items-center justify-center text-xs"
                      title={agentId}
                    >
                      {getAgentAvatar(agentId)}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  const renderCircleView = () => {
    const centerX = 200;
    const centerY = 200;
    const radius = 150;
    
    return (
      <div className="flex justify-center">
        <svg width="400" height="400" className="overflow-visible">
          {/* Background circle */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="8"
          />
          
          {/* Progress circle */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            fill="none"
            stroke="#3b82f6"
            strokeWidth="8"
            strokeDasharray={`${2 * Math.PI * radius}`}
            strokeDashoffset={`${2 * Math.PI * radius * (1 - calculateOverallProgress() / 100)}`}
            transform={`rotate(-90 ${centerX} ${centerY})`}
            className="transition-all duration-1000"
          />
          
          {/* Phase indicators */}
          {workflowPhases.map((phase, index) => {
            const angle = (index / workflowPhases.length) * 2 * Math.PI - Math.PI / 2;
            const x = centerX + (radius + 40) * Math.cos(angle);
            const y = centerY + (radius + 40) * Math.sin(angle);
            
            return (
              <g key={phase.id}>
                <circle
                  cx={x}
                  cy={y}
                  r="20"
                  className={`cursor-pointer transition-all hover:r-24 ${getPhaseStatusColor(phase.status).replace('border-', 'fill-').replace('bg-', 'fill-')}`}
                  onClick={() => onPhaseSelect?.(phase.id)}
                />
                <text
                  x={x}
                  y={y + 5}
                  textAnchor="middle"
                  className="text-lg cursor-pointer"
                  onClick={() => onPhaseSelect?.(phase.id)}
                >
                  {phase.icon}
                </text>
              </g>
            );
          })}
          
          {/* Center progress text */}
          <text
            x={centerX}
            y={centerY - 10}
            textAnchor="middle"
            className="text-2xl font-bold fill-gray-800"
          >
            {calculateOverallProgress()}%
          </text>
          <text
            x={centerX}
            y={centerY + 15}
            textAnchor="middle"
            className="text-sm fill-gray-600"
          >
            Complete
          </text>
        </svg>
      </div>
    );
  };

  return (
    <div className={`bg-white rounded-xl shadow-lg border border-gray-100 ${className}`}>
      {/* Header */}
      <div className="bg-gradient-to-r from-green-500 to-teal-600 p-4 rounded-t-xl">
        <div className="flex items-center justify-between text-white">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
              📊
            </div>
            <div>
              <h3 className="font-semibold text-lg">SDLC Workflow</h3>
              <p className="text-sm text-white/80">
                {calculateOverallProgress()}% Complete • {workflowPhases.filter(p => p.status === 'active').length} Active Phases
              </p>
            </div>
          </div>
          
          {/* View mode selector */}
          <div className="flex items-center space-x-2">
            {[
              { mode: 'timeline', icon: '📅', label: 'Timeline' },
              { mode: 'kanban', icon: '📋', label: 'Kanban' },
              { mode: 'circle', icon: '⭕', label: 'Circle' }
            ].map(({ mode, icon, label }) => (
              <button
                key={mode}
                onClick={() => setViewMode(mode as any)}
                className={`p-2 rounded-lg transition-colors ${
                  viewMode === mode 
                    ? 'bg-white/30 text-white' 
                    : 'bg-white/10 text-white/70 hover:bg-white/20'
                }`}
                title={label}
              >
                {icon}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Workflow content */}
      <div className="p-6">
        {viewMode === 'timeline' && renderTimelineView()}
        {viewMode === 'kanban' && renderKanbanView()}
        {viewMode === 'circle' && renderCircleView()}
      </div>
    </div>
  );
};