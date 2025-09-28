// components/GitHub/WorkspaceManager.tsx
import React, { useState } from 'react';

interface WorkspaceRepo {
  name: string;
  path: string;
  remote_url: string;
  current_branch: string;
  has_changes: boolean;
  modified_files: Array<{file: string, status: string}>;
}

interface WorkspaceManagerProps {
  workspaceRepos: WorkspaceRepo[];
  onOpenVSCode: (repoPath: string) => void;
  onRefresh: () => void;
}

export const WorkspaceManager: React.FC<WorkspaceManagerProps> = ({
  workspaceRepos,
  onOpenVSCode,
  onRefresh
}) => {
  const [selectedRepo, setSelectedRepo] = useState<WorkspaceRepo | null>(null);

  const getStatusColor = (hasChanges: boolean) => {
    return hasChanges ? 'text-yellow-600' : 'text-green-600';
  };

  const getStatusIcon = (hasChanges: boolean) => {
    return hasChanges ? '📝' : '✅';
  };

  const getFileStatusIcon = (status: string) => {
    switch (status.trim()) {
      case 'M': return '📝'; // Modified
      case 'A': return '➕'; // Added
      case 'D': return '🗑️'; // Deleted
      case '??': return '❓'; // Untracked
      default: return '📄';
    }
  };

  const getFileStatusText = (status: string) => {
    switch (status.trim()) {
      case 'M': return 'Modified';
      case 'A': return 'Added';
      case 'D': return 'Deleted';
      case '??': return 'Untracked';
      default: return 'Changed';
    }
  };

  if (workspaceRepos.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-gray-500">
        <div className="text-4xl mb-4">💻</div>
        <p className="text-lg font-medium">No repositories in workspace</p>
        <p className="text-sm mb-4">Clone a repository to get started</p>
        <button
          onClick={onRefresh}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          🔄 Refresh Workspace
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Workspace Info */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-gray-900">Workspace Location</h3>
            <p className="text-sm text-gray-600 font-mono">C:\YOKA</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-500">
              {workspaceRepos.length} repositories
            </span>
            <button
              onClick={onRefresh}
              className="p-2 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-100"
              title="Refresh workspace"
            >
              🔄
            </button>
          </div>
        </div>
      </div>

      {/* Repository List */}
      <div className="space-y-4">
        {workspaceRepos.map((repo, index) => (
          <div key={index} className="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors">
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">{repo.name}</h3>
                  <span className={`inline-flex items-center space-x-1 text-sm ${getStatusColor(repo.has_changes)}`}>
                    <span>{getStatusIcon(repo.has_changes)}</span>
                    <span>{repo.has_changes ? 'Has Changes' : 'Clean'}</span>
                  </span>
                </div>
                
                <div className="space-y-1 text-sm text-gray-600">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium">Path:</span>
                    <span className="font-mono bg-gray-100 px-2 py-1 rounded">{repo.path}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="font-medium">Branch:</span>
                    <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                      🌿 {repo.current_branch}
                    </span>
                  </div>
                  {repo.remote_url !== 'unknown' && (
                    <div className="flex items-center space-x-2">
                      <span className="font-medium">Remote:</span>
                      <span className="font-mono text-xs">{repo.remote_url}</span>
                    </div>
                  )}
                </div>
              </div>
              
              <div className="flex flex-col space-y-2 ml-4">
                <button
                  onClick={() => onOpenVSCode(repo.path)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium flex items-center space-x-2"
                >
                  <span>💻</span>
                  <span>Open in VS Code</span>
                </button>
                <button
                  onClick={() => setSelectedRepo(selectedRepo?.name === repo.name ? null : repo)}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
                >
                  {selectedRepo?.name === repo.name ? '🔼 Hide Details' : '🔽 Show Details'}
                </button>
              </div>
            </div>

            {/* Modified Files (if any) */}
            {repo.has_changes && (
              <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                <h4 className="text-sm font-medium text-yellow-800 mb-2">
                  📝 Modified Files ({repo.modified_files.length})
                </h4>
                <div className="space-y-1 max-h-24 overflow-y-auto">
                  {repo.modified_files.slice(0, 5).map((file, fileIndex) => (
                    <div key={fileIndex} className="flex items-center space-x-2 text-sm">
                      <span>{getFileStatusIcon(file.status)}</span>
                      <span className="font-mono text-yellow-700">{file.file}</span>
                      <span className="text-yellow-600 text-xs">
                        ({getFileStatusText(file.status)})
                      </span>
                    </div>
                  ))}
                  {repo.modified_files.length > 5 && (
                    <p className="text-xs text-yellow-600">
                      +{repo.modified_files.length - 5} more files...
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* Expanded Details */}
            {selectedRepo?.name === repo.name && (
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-3">Repository Details</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Full Path:</span>
                    <p className="font-mono text-gray-600 break-all">{repo.path}</p>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Current Branch:</span>
                    <p className="text-gray-600">{repo.current_branch}</p>
                  </div>
                  <div className="md:col-span-2">
                    <span className="font-medium text-gray-700">Remote URL:</span>
                    <p className="font-mono text-gray-600 break-all">{repo.remote_url}</p>
                  </div>
                </div>
                
                {/* Quick Actions */}
                <div className="mt-4 pt-3 border-t border-gray-200">
                  <p className="text-sm font-medium text-gray-700 mb-2">Quick Actions:</p>
                  <div className="flex flex-wrap gap-2">
                    <button className="px-3 py-1 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm">
                      🔍 Analyze Code
                    </button>
                    <button className="px-3 py-1 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm">
                      🐛 Find Issues
                    </button>
                    <button className="px-3 py-1 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors text-sm">
                      🔧 Auto Fix
                    </button>
                    <button className="px-3 py-1 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 transition-colors text-sm">
                      📊 Generate Report
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};