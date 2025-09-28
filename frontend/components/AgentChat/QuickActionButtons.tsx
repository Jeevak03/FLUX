// components/AgentChat/QuickActionButtons.tsx
import React from 'react';

interface QuickAction {
  id: string;
  label: string;
  icon: string;
  description: string;
  color: string;
  suggestedAgents: string[];
  template: string;
}

interface QuickActionButtonsProps {
  onActionClick: (action: QuickAction) => void;
  currentPhase: string;
}

export const QuickActionButtons: React.FC<QuickActionButtonsProps> = ({
  onActionClick,
  currentPhase
}) => {
  const allActions: QuickAction[] = [
    {
      id: 'new-feature',
      label: 'New Feature',
      icon: '✨',
      description: 'Start planning a new feature',
      color: 'bg-purple-500 hover:bg-purple-600',
      suggestedAgents: ['requirements_analyst', 'software_architect'],
      template: 'I need to add a new feature to our application. Can Sara help gather the requirements and Marc design the architecture?'
    },
    {
      id: 'review-architecture',
      label: 'Review Architecture',
      icon: '🏗️',
      description: 'Get architecture review and feedback',
      color: 'bg-blue-500 hover:bg-blue-600',
      suggestedAgents: ['software_architect', 'security_expert'],
      template: 'Can Marc review our current architecture and Robt assess any security considerations?'
    },
    {
      id: 'code-review',
      label: 'Code Review',
      icon: '👁️',
      description: 'Request code review and feedback',
      color: 'bg-green-500 hover:bg-green-600',
      suggestedAgents: ['developer', 'security_expert'],
      template: 'I need Alex to review my code implementation and Robt to check for security issues.'
    },
    {
      id: 'run-tests',
      label: 'Run Tests',
      icon: '🧪',
      description: 'Execute testing and QA procedures',
      color: 'bg-yellow-500 hover:bg-yellow-600',
      suggestedAgents: ['qa_tester'],
      template: 'Jess, can you run comprehensive tests on our latest changes and report any issues?'
    },
    {
      id: 'deploy-setup',
      label: 'Deployment',
      icon: '🚀',
      description: 'Plan and execute deployment',
      color: 'bg-red-500 hover:bg-red-600',
      suggestedAgents: ['devops_engineer', 'security_expert'],
      template: 'Dave, I need help setting up deployment pipeline. Robt, please review security configurations.'
    },
    {
      id: 'project-status',
      label: 'Project Status',
      icon: '📊',
      description: 'Get project status and updates',
      color: 'bg-indigo-500 hover:bg-indigo-600',
      suggestedAgents: ['project_manager'],
      template: 'Emma, can you provide a comprehensive project status update and timeline review?'
    },
    {
      id: 'bug-fix',
      label: 'Bug Investigation',
      icon: '🐛',
      description: 'Investigate and fix bugs',
      color: 'bg-orange-500 hover:bg-orange-600',
      suggestedAgents: ['developer', 'qa_tester'],
      template: 'We have a critical bug that needs investigation. Alex, can you look into it? Jess, please help with reproduction steps.'
    },
    {
      id: 'performance',
      label: 'Performance Review',
      icon: '⚡',
      description: 'Analyze and improve performance',
      color: 'bg-cyan-500 hover:bg-cyan-600',
      suggestedAgents: ['software_architect', 'developer'],
      template: 'Marc and Alex, I need help analyzing application performance and identifying optimization opportunities.'
    }
  ];

  const getPhaseActions = (phase: string): QuickAction[] => {
    const phaseMap: { [key: string]: string[] } = {
      'requirements': ['new-feature', 'project-status'],
      'planning': ['new-feature', 'review-architecture', 'project-status'],
      'design': ['review-architecture', 'project-status'],
      'development': ['code-review', 'bug-fix', 'performance', 'project-status'],
      'testing': ['run-tests', 'bug-fix', 'code-review', 'project-status'],
      'deployment': ['deploy-setup', 'run-tests', 'project-status'],
      'maintenance': ['bug-fix', 'performance', 'project-status']
    };

    const phaseActionIds = phaseMap[phase.toLowerCase()] || Object.keys(phaseMap).flatMap(k => phaseMap[k]);
    return allActions.filter(action => phaseActionIds.includes(action.id));
  };

  const recommendedActions = getPhaseActions(currentPhase);
  const otherActions = allActions.filter(action => !recommendedActions.includes(action));

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 to-red-600 p-4">
        <div className="flex items-center justify-between text-white">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
              ⚡
            </div>
            <div>
              <h3 className="font-semibold text-lg">Quick Actions</h3>
              <p className="text-sm text-white/80">Context-aware SDLC shortcuts</p>
            </div>
          </div>
          <span className="text-xs bg-white/20 px-3 py-1 rounded-full font-medium">
            {currentPhase}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">

      {/* Recommended Actions */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
          🎯 Recommended for {currentPhase} Phase
        </h4>
        <div className="space-y-3">
          {recommendedActions.map((action) => (
            <button
              key={action.id}
              onClick={() => onActionClick(action)}
              className={`${action.color} text-white p-4 rounded-lg shadow-md transition-all duration-200 hover:shadow-lg hover:scale-[1.02] group w-full text-left`}
            >
              <div className="flex items-start space-x-3">
                <div className="text-2xl flex-shrink-0 mt-0.5">{action.icon}</div>
                <div className="flex-1 min-w-0">
                  <div className="font-semibold text-sm mb-1 truncate">{action.label}</div>
                  <div className="text-xs text-white/90 mb-2 leading-relaxed">
                    {action.description}
                  </div>
                  <div className="text-xs text-white/70 flex items-center">
                    <span className="mr-2">👥</span>
                    <span>
                      {action.suggestedAgents.length} agent{action.suggestedAgents.length > 1 ? 's' : ''} involved
                    </span>
                  </div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Other Actions */}
      {otherActions.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">
            🛠️ Other Actions
          </h4>
          <div className="grid grid-cols-2 gap-3">
            {otherActions.map((action) => (
              <button
                key={action.id}
                onClick={() => onActionClick(action)}
                className="p-3 border-2 border-gray-200 rounded-lg hover:border-gray-300 hover:bg-gray-50 transition-all duration-200 group text-center min-h-[4rem] flex flex-col items-center justify-center"
                title={action.description}
              >
                <div className="text-lg mb-1 flex-shrink-0">{action.icon}</div>
                <div className="text-xs font-medium text-gray-700 group-hover:text-gray-900 leading-tight text-center break-words">
                  {action.label}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

        {/* Help Text */}
        <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-xs text-blue-700 leading-relaxed">
            <span className="font-semibold">💡 Tip:</span> Quick actions automatically suggest the right team members and provide context-aware prompts for your current project phase.
          </p>
        </div>
      </div>
    </div>
  );
};