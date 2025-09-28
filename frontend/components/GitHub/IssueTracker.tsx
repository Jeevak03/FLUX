// components/GitHub/IssueTracker.tsx
import React, { useState, useEffect } from 'react';

interface GitHubRepository {
  id: number;
  name: string;
  full_name: string;
}

interface GitHubIssue {
  id: number;
  number: number;
  title: string;
  body: string;
  state: string;
  labels: string[];
  html_url: string;
}

interface IssueTrackerProps {
  repository: GitHubRepository;
  onIssueSelect: (issue: GitHubIssue) => void;
}

export const IssueTracker: React.FC<IssueTrackerProps> = ({
  repository,
  onIssueSelect
}) => {
  const [issues, setIssues] = useState<GitHubIssue[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedIssue, setSelectedIssue] = useState<GitHubIssue | null>(null);
  const [stateFilter, setStateFilter] = useState<'open' | 'closed' | 'all'>('open');

  useEffect(() => {
    loadIssues();
  }, [repository, stateFilter]);

  const loadIssues = async () => {
    setLoading(true);
    try {
      const encodedRepoName = repository.full_name.replace('/', '%2F');
      const response = await fetch(`/api/github/repositories/${encodedRepoName}/issues?state=${stateFilter}`);
      if (response.ok) {
        const issueData = await response.json();
        setIssues(issueData);
      }
    } catch (err) {
      console.error('Error loading issues:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleIssueClick = (issue: GitHubIssue) => {
    setSelectedIssue(selectedIssue?.id === issue.id ? null : issue);
    onIssueSelect(issue);
  };

  const getLabelColor = (label: string) => {
    const colors = {
      'bug': 'bg-red-100 text-red-800',
      'enhancement': 'bg-blue-100 text-blue-800',
      'feature': 'bg-green-100 text-green-800',
      'documentation': 'bg-purple-100 text-purple-800',
      'help wanted': 'bg-yellow-100 text-yellow-800',
      'good first issue': 'bg-pink-100 text-pink-800'
    };
    return colors[label.toLowerCase() as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  const getStateIcon = (state: string) => {
    return state === 'open' ? '🟢' : '🔴';
  };

  const getPriorityIcon = (labels: string[]) => {
    if (labels.some(label => label.toLowerCase().includes('critical'))) return '🔥';
    if (labels.some(label => label.toLowerCase().includes('high'))) return '🚨';
    if (labels.some(label => label.toLowerCase().includes('medium'))) return '⚡';
    if (labels.some(label => label.toLowerCase().includes('low'))) return '🔵';
    return '📋';
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <p className="text-gray-600">Loading issues...</p>
      </div>
    );
  }

  return (
    <div>
      {/* Repository Info */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">{repository.name}</h3>
            <p className="text-sm text-gray-600">{repository.full_name}</p>
          </div>
          <div className="flex items-center space-x-2">
            <select
              value={stateFilter}
              onChange={(e) => setStateFilter(e.target.value as 'open' | 'closed' | 'all')}
              className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="open">Open Issues</option>
              <option value="closed">Closed Issues</option>
              <option value="all">All Issues</option>
            </select>
            <button
              onClick={loadIssues}
              className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-100"
              title="Refresh issues"
            >
              🔄
            </button>
          </div>
        </div>
      </div>

      {issues.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-gray-500">
          <div className="text-4xl mb-4">🐛</div>
          <p className="text-lg font-medium">No {stateFilter} issues found</p>
          <p className="text-sm">Great job keeping the repository clean!</p>
        </div>
      ) : (
        <div>
          {/* Issues Stats */}
          <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center space-x-4">
                <span className="flex items-center space-x-1">
                  <span>🐛</span>
                  <span>{issues.length} {stateFilter} issues</span>
                </span>
                <span className="flex items-center space-x-1">
                  <span>🏷️</span>
                  <span>{new Set(issues.flatMap(issue => issue.labels)).size} unique labels</span>
                </span>
              </div>
              <button className="px-3 py-1 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm">
                ➕ Create Issue
              </button>
            </div>
          </div>

          {/* Issues List */}
          <div className="space-y-3">
            {issues.map((issue) => (
              <div key={issue.id} className="bg-white border border-gray-200 rounded-lg hover:border-gray-300 transition-colors">
                <div
                  onClick={() => handleIssueClick(issue)}
                  className="p-4 cursor-pointer"
                >
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0 mt-1">
                      <span className="text-lg">{getStateIcon(issue.state)}</span>
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="text-lg">{getPriorityIcon(issue.labels)}</span>
                        <h4 className="text-lg font-semibold text-gray-900 truncate">
                          {issue.title}
                        </h4>
                        <span className="text-sm text-gray-500">#{issue.number}</span>
                      </div>
                      
                      {issue.labels.length > 0 && (
                        <div className="flex flex-wrap gap-2 mb-3">
                          {issue.labels.map(label => (
                            <span
                              key={label}
                              className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getLabelColor(label)}`}
                            >
                              {label}
                            </span>
                          ))}
                        </div>
                      )}
                      
                      {issue.body && (
                        <p className="text-gray-600 text-sm line-clamp-2 mb-2">
                          {issue.body.substring(0, 150)}
                          {issue.body.length > 150 ? '...' : ''}
                        </p>
                      )}
                    </div>
                    
                    <div className="flex-shrink-0 flex flex-col space-y-2">
                      <a
                        href={issue.html_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        className="px-3 py-1 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm"
                      >
                        🔗 GitHub
                      </a>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          // Handle AI analysis
                          alert(`Analyzing issue #${issue.number} with AI agents...`);
                        }}
                        className="px-3 py-1 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm"
                      >
                        🤖 AI Fix
                      </button>
                    </div>
                  </div>
                </div>
                
                {/* Expanded Issue Details */}
                {selectedIssue?.id === issue.id && (
                  <div className="border-t border-gray-200 p-4 bg-gray-50">
                    <div className="space-y-4">
                      <div>
                        <h5 className="font-medium text-gray-900 mb-2">Issue Description</h5>
                        <div className="bg-white p-3 rounded-lg border border-gray-200">
                          <p className="text-gray-700 whitespace-pre-wrap">
                            {issue.body || 'No description provided.'}
                          </p>
                        </div>
                      </div>
                      
                      <div className="flex flex-wrap gap-2">
                        <button className="px-3 py-1 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
                          🔍 Analyze with Sara
                        </button>
                        <button className="px-3 py-1 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm">
                          🏗️ Design with Marc
                        </button>
                        <button className="px-3 py-1 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm">
                          💻 Code with Alex
                        </button>
                        <button className="px-3 py-1 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors text-sm">
                          🧪 Test with Jess
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};