// components/AgentChat/AgentExpertiseCards.tsx
import React, { useState, useMemo } from 'react';
import { AgentMessage } from '../../types/agents';

interface AgentExpertise {
  id: string;
  name: string;
  role: string;
  avatar: string;
  skills: string[];
  specializations: string[];
  currentWorkload: 'low' | 'medium' | 'high';
  recentContributions: number;
  totalMessages: number;
  responseTime: string;
  collaborationStyle: string;
  keyStrengths: string[];
  preferredTasks: string[];
}

interface AgentExpertiseCardsProps {
  messages: AgentMessage[];
  activeAgents: string[];
  onAgentSelect?: (agentId: string) => void;
  className?: string;
}

export const AgentExpertiseCards: React.FC<AgentExpertiseCardsProps> = ({
  messages,
  activeAgents,
  onAgentSelect,
  className = ''
}) => {
  const [expandedAgent, setExpandedAgent] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Define agent expertise data
  const agentExpertiseData: { [key: string]: AgentExpertise } = {
    'requirements_analyst': {
      id: 'requirements_analyst',
      name: 'Sara',
      role: 'Requirements Analyst',
      avatar: '👩‍💼',
      skills: ['Requirements Gathering', 'Stakeholder Analysis', 'User Stories', 'Process Modeling'],
      specializations: ['Business Analysis', 'User Experience', 'Functional Requirements'],
      currentWorkload: 'medium',
      recentContributions: 0,
      totalMessages: 0,
      responseTime: '2-3 min',
      collaborationStyle: 'Methodical and detail-oriented, asks clarifying questions',
      keyStrengths: ['Clear requirement definition', 'Stakeholder communication', 'Gap analysis'],
      preferredTasks: ['Feature planning', 'User story creation', 'Requirements validation']
    },
    'software_architect': {
      id: 'software_architect',
      name: 'Marc',
      role: 'Software Architect',
      avatar: '👨‍💻',
      skills: ['System Design', 'Architecture Patterns', 'Technology Selection', 'Scalability'],
      specializations: ['Microservices', 'Cloud Architecture', 'API Design'],
      currentWorkload: 'high',
      recentContributions: 0,
      totalMessages: 0,
      responseTime: '3-5 min',
      collaborationStyle: 'Strategic thinker, focuses on long-term sustainability',
      keyStrengths: ['System architecture', 'Technology decisions', 'Performance optimization'],
      preferredTasks: ['Architecture design', 'Tech stack decisions', 'System integration']
    },
    'developer': {
      id: 'developer',
      name: 'Alex',
      role: 'Senior Developer',
      avatar: '👩‍💻',
      skills: ['Full-Stack Development', 'Code Review', 'Testing', 'Debugging'],
      specializations: ['React/Next.js', 'Node.js', 'Python', 'Database Design'],
      currentWorkload: 'high',
      recentContributions: 0,
      totalMessages: 0,
      responseTime: '1-2 min',
      collaborationStyle: 'Hands-on problem solver, provides practical solutions',
      keyStrengths: ['Code implementation', 'Technical problem solving', 'Code quality'],
      preferredTasks: ['Feature development', 'Bug fixes', 'Code optimization']
    },
    'qa_tester': {
      id: 'qa_tester',
      name: 'Jess',
      role: 'QA Engineer',
      avatar: '👩‍🔬',
      skills: ['Test Planning', 'Automation', 'Bug Tracking', 'Quality Assurance'],
      specializations: ['UI Testing', 'API Testing', 'Performance Testing'],
      currentWorkload: 'medium',
      recentContributions: 0,
      totalMessages: 0,
      responseTime: '2-4 min',
      collaborationStyle: 'Thorough and systematic, focuses on edge cases',
      keyStrengths: ['Test case design', 'Quality validation', 'Risk assessment'],
      preferredTasks: ['Test planning', 'Bug investigation', 'Quality reviews']
    },
    'devops_engineer': {
      id: 'devops_engineer',
      name: 'Dave',
      role: 'DevOps Engineer',
      avatar: '👨‍🔧',
      skills: ['CI/CD', 'Infrastructure', 'Monitoring', 'Deployment'],
      specializations: ['AWS/Azure', 'Docker/Kubernetes', 'Infrastructure as Code'],
      currentWorkload: 'medium',
      recentContributions: 0,
      totalMessages: 0,
      responseTime: '3-5 min',
      collaborationStyle: 'Process-oriented, emphasizes automation and reliability',
      keyStrengths: ['Infrastructure setup', 'Deployment automation', 'System monitoring'],
      preferredTasks: ['CI/CD setup', 'Infrastructure planning', 'Performance monitoring']
    },
    'project_manager': {
      id: 'project_manager',
      name: 'Emma',
      role: 'Project Manager',
      avatar: '👩‍💼',
      skills: ['Project Planning', 'Team Coordination', 'Risk Management', 'Communication'],
      specializations: ['Agile/Scrum', 'Resource Management', 'Timeline Planning'],
      currentWorkload: 'low',
      recentContributions: 0,
      totalMessages: 0,
      responseTime: '1-3 min',
      collaborationStyle: 'Collaborative facilitator, keeps team aligned and focused',
      keyStrengths: ['Project coordination', 'Timeline management', 'Team communication'],
      preferredTasks: ['Sprint planning', 'Progress tracking', 'Team coordination']
    },
    'security_expert': {
      id: 'security_expert',
      name: 'Robt',
      role: 'Security Expert',
      avatar: '👨‍🛡️',
      skills: ['Security Analysis', 'Vulnerability Assessment', 'Compliance', 'Risk Analysis'],
      specializations: ['Application Security', 'Data Protection', 'Security Architecture'],
      currentWorkload: 'low',
      recentContributions: 0,
      totalMessages: 0,
      responseTime: '4-6 min',
      collaborationStyle: 'Risk-focused, provides thorough security assessments',
      keyStrengths: ['Security reviews', 'Vulnerability identification', 'Compliance guidance'],
      preferredTasks: ['Security assessments', 'Code security reviews', 'Compliance checks']
    }
  };

  // Calculate real-time metrics based on message history
  const agentMetrics = useMemo(() => {
    const metrics: { [key: string]: AgentExpertise } = { ...agentExpertiseData };
    
    // Calculate message counts and recent activity
    const now = new Date();
    const recentThreshold = 30 * 60 * 1000; // 30 minutes
    
    Object.keys(metrics).forEach(agentId => {
      const agentMessages = messages.filter(m => m.agent === agentId);
      metrics[agentId].totalMessages = agentMessages.length;
      
      const recentMessages = agentMessages.filter(m => 
        new Date(m.timestamp).getTime() > (now.getTime() - recentThreshold)
      );
      metrics[agentId].recentContributions = recentMessages.length;
      
      // Update workload based on recent activity
      if (recentMessages.length > 3) {
        metrics[agentId].currentWorkload = 'high';
      } else if (recentMessages.length > 1) {
        metrics[agentId].currentWorkload = 'medium';
      } else {
        metrics[agentId].currentWorkload = 'low';
      }
    });
    
    return metrics;
  }, [messages]);

  const getWorkloadColor = (workload: string) => {
    switch (workload) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getWorkloadIcon = (workload: string) => {
    switch (workload) {
      case 'high': return '🔴';
      case 'medium': return '🟡';
      case 'low': return '🟢';
      default: return '⚪';
    }
  };

  const isAgentActive = (agentId: string) => activeAgents.includes(agentId);

  const sortedAgents = Object.values(agentMetrics).sort((a, b) => {
    // Active agents first
    if (isAgentActive(a.id) && !isAgentActive(b.id)) return -1;
    if (!isAgentActive(a.id) && isAgentActive(b.id)) return 1;
    
    // Then by recent contributions
    return b.recentContributions - a.recentContributions;
  });

  return (
    <div className={`bg-white rounded-xl shadow-lg border border-gray-100 ${className}`}>
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-500 to-pink-600 p-4 rounded-t-xl">
        <div className="flex items-center justify-between text-white">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
              👥
            </div>
            <div>
              <h3 className="font-semibold text-lg">Team Expertise</h3>
              <p className="text-sm text-white/80">
                {activeAgents.length} active • {Object.keys(agentMetrics).length} total agents
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
              className="p-2 bg-white/20 rounded-lg hover:bg-white/30 transition-colors"
              title={`Switch to ${viewMode === 'grid' ? 'list' : 'grid'} view`}
            >
              {viewMode === 'grid' ? '📋' : '⚏'}
            </button>
          </div>
        </div>
      </div>

      {/* Agent Cards */}
      <div className="p-4">
        <div className={viewMode === 'grid' 
          ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
          : 'space-y-3'
        }>
          {sortedAgents.map((agent) => (
            <div
              key={agent.id}
              className={`border border-gray-200 rounded-lg p-4 transition-all duration-200 cursor-pointer ${
                isAgentActive(agent.id) 
                  ? 'ring-2 ring-blue-500 bg-blue-50' 
                  : 'hover:shadow-md hover:border-gray-300'
              } ${expandedAgent === agent.id ? 'shadow-lg' : ''}`}
              onClick={() => {
                if (expandedAgent === agent.id) {
                  setExpandedAgent(null);
                } else {
                  setExpandedAgent(agent.id);
                  onAgentSelect?.(agent.id);
                }
              }}
            >
              {/* Agent Header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className="relative">
                    <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center text-lg">
                      {agent.avatar}
                    </div>
                    {isAgentActive(agent.id) && (
                      <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white animate-pulse"></div>
                    )}
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900">{agent.name}</h4>
                    <p className="text-sm text-gray-600">{agent.role}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 text-xs rounded-full ${getWorkloadColor(agent.currentWorkload)}`}>
                    {getWorkloadIcon(agent.currentWorkload)} {agent.currentWorkload}
                  </span>
                </div>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-3 gap-2 mb-3">
                <div className="text-center">
                  <div className="text-lg font-semibold text-blue-600">{agent.totalMessages}</div>
                  <div className="text-xs text-gray-500">Messages</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-semibold text-green-600">{agent.recentContributions}</div>
                  <div className="text-xs text-gray-500">Recent</div>
                </div>
                <div className="text-center">
                  <div className="text-sm font-semibold text-purple-600">{agent.responseTime}</div>
                  <div className="text-xs text-gray-500">Avg Time</div>
                </div>
              </div>

              {/* Core Skills Preview */}
              <div className="mb-3">
                <div className="flex flex-wrap gap-1">
                  {agent.skills.slice(0, 3).map((skill) => (
                    <span
                      key={skill}
                      className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                    >
                      {skill}
                    </span>
                  ))}
                  {agent.skills.length > 3 && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                      +{agent.skills.length - 3}
                    </span>
                  )}
                </div>
              </div>

              {/* Expanded Details */}
              {expandedAgent === agent.id && (
                <div className="mt-4 pt-4 border-t border-gray-200 space-y-4 animate-in slide-in-from-top duration-200">
                  {/* Specializations */}
                  <div>
                    <h5 className="text-sm font-semibold text-gray-800 mb-2">🎯 Specializations</h5>
                    <div className="flex flex-wrap gap-1">
                      {agent.specializations.map((spec) => (
                        <span
                          key={spec}
                          className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                        >
                          {spec}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Key Strengths */}
                  <div>
                    <h5 className="text-sm font-semibold text-gray-800 mb-2">💪 Key Strengths</h5>
                    <ul className="text-sm text-gray-600 space-y-1">
                      {agent.keyStrengths.map((strength, index) => (
                        <li key={index} className="flex items-center space-x-2">
                          <span className="w-1 h-1 bg-gray-400 rounded-full"></span>
                          <span>{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Preferred Tasks */}
                  <div>
                    <h5 className="text-sm font-semibold text-gray-800 mb-2">✅ Best For</h5>
                    <div className="flex flex-wrap gap-1">
                      {agent.preferredTasks.map((task) => (
                        <span
                          key={task}
                          className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full"
                        >
                          {task}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Collaboration Style */}
                  <div>
                    <h5 className="text-sm font-semibold text-gray-800 mb-2">🤝 Collaboration Style</h5>
                    <p className="text-sm text-gray-600 italic">{agent.collaborationStyle}</p>
                  </div>
                </div>
              )}

              {/* Expansion Indicator */}
              <div className="flex justify-center mt-2">
                <span className="text-xs text-gray-400">
                  {expandedAgent === agent.id ? 'Click to collapse ▲' : 'Click for details ▼'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};