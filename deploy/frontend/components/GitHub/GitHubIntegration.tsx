// components/GitHub/GitHubIntegration.tsx
import React, { useState, useEffect } from 'react';
import { RepositorySelector } from './RepositorySelector';
import { WorkspaceManager } from './WorkspaceManager';
import { BranchManager } from './BranchManager';
import { IssueTracker } from './IssueTracker';

interface GitHubRepository {
  id: number;
  name: string;
  full_name: string;
  description: string | null;
  private: boolean;
  html_url: string;
  clone_url: string;
  default_branch: string;
  language: string | null;
  topics: string[];
}

interface WorkspaceRepo {
  name: string;
  path: string;
  remote_url: string;
  current_branch: string;
  has_changes: boolean;
  modified_files: Array<{file: string, status: string}>;
}

interface GitHubIntegrationProps {
  onRepositorySelect?: (repo: GitHubRepository) => void;
}

export const GitHubIntegration: React.FC<GitHubIntegrationProps> = ({ onRepositorySelect }) => {
  const [activeTab, setActiveTab] = useState<'browse' | 'workspace' | 'branches' | 'issues'>('browse');
  const [repositories, setRepositories] = useState<GitHubRepository[]>([]);
  const [workspaceRepos, setWorkspaceRepos] = useState<WorkspaceRepo[]>([]);
  const [selectedRepo, setSelectedRepo] = useState<GitHubRepository | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadRepositories();
    loadWorkspaceRepositories();
  }, []);

  const loadRepositories = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/github/repositories');
      if (response.ok) {
        const repos = await response.json();
        setRepositories(repos);
      } else {
        setError('Failed to load repositories. Please check your GitHub token.');
      }
    } catch (err) {
      setError('Error connecting to GitHub API');
    } finally {
      setLoading(false);
    }
  };

  const loadWorkspaceRepositories = async () => {
    try {
      const response = await fetch('/api/github/workspace/repositories');
      if (response.ok) {
        const workspaceRepos = await response.json();
        setWorkspaceRepos(workspaceRepos);
      }
    } catch (err) {
      console.error('Error loading workspace repositories:', err);
    }
  };

  const handleCloneRepository = async (repo: GitHubRepository) => {
    setLoading(true);
    try {
      const response = await fetch('/api/github/clone', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          repo_full_name: repo.full_name,
          clone_url: repo.clone_url
        })
      });

      if (response.ok) {
        const result = await response.json();
        await loadWorkspaceRepositories();
        setActiveTab('workspace');
        alert(`Repository cloned successfully to ${result.local_path}`);
      } else {
        const error = await response.json();
        alert(`Failed to clone repository: ${error.detail}`);
      }
    } catch (err) {
      alert('Error cloning repository');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenVSCode = async (repoPath: string) => {
    try {
      const response = await fetch('/api/github/workspace/open-vscode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_path: repoPath })
      });

      if (response.ok) {
        alert('Opening repository in VS Code...');
      } else {
        alert('Failed to open VS Code. Make sure VS Code is installed and accessible.');
      }
    } catch (err) {
      alert('Error opening VS Code');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-gray-900 to-gray-700 rounded-lg flex items-center justify-center">
            <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z" clipRule="evenodd" />
            </svg>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">GitHub Integration</h2>
            <p className="text-sm text-gray-600">Connect, clone, and manage your repositories</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            repositories.length > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            {repositories.length > 0 ? '🟢 Connected' : '🔴 Not Connected'}
          </span>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center">
            <div className="text-red-400 mr-3">⚠️</div>
            <div>
              <p className="text-red-800 font-medium">Connection Error</p>
              <p className="text-red-700 text-sm mt-1">{error}</p>
              <p className="text-red-600 text-xs mt-2">
                Make sure to set your GITHUB_TOKEN in the backend .env file
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex space-x-1 mb-6 bg-gray-100 p-1 rounded-lg">
        {[
          { id: 'browse', label: 'Browse Repos', icon: '🔍' },
          { id: 'workspace', label: 'Workspace', icon: '💻' },
          { id: 'branches', label: 'Branches', icon: '🌿' },
          { id: 'issues', label: 'Issues', icon: '🐛' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex-1 flex items-center justify-center space-x-2 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === tab.id
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            }`}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="min-h-[400px]">
        {activeTab === 'browse' && (
          <RepositorySelector
            repositories={repositories}
            loading={loading}
            onCloneRepository={handleCloneRepository}
            onRepositorySelect={setSelectedRepo}
          />
        )}

        {activeTab === 'workspace' && (
          <WorkspaceManager
            workspaceRepos={workspaceRepos}
            onOpenVSCode={handleOpenVSCode}
            onRefresh={loadWorkspaceRepositories}
          />
        )}

        {activeTab === 'branches' && selectedRepo && (
          <BranchManager
            repository={selectedRepo}
            onBranchCreated={() => {
              // Refresh data
            }}
          />
        )}

        {activeTab === 'issues' && selectedRepo && (
          <IssueTracker
            repository={selectedRepo}
            onIssueSelect={(issue) => {
              // Handle issue selection
              console.log('Selected issue:', issue);
            }}
          />
        )}

        {activeTab === 'issues' && !selectedRepo && (
          <div className="flex flex-col items-center justify-center py-12 text-gray-500">
            <div className="text-4xl mb-4">🔍</div>
            <p className="text-lg font-medium">Select a Repository</p>
            <p className="text-sm">Browse and select a repository to view its issues</p>
          </div>
        )}

        {activeTab === 'branches' && !selectedRepo && (
          <div className="flex flex-col items-center justify-center py-12 text-gray-500">
            <div className="text-4xl mb-4">🌿</div>
            <p className="text-lg font-medium">Select a Repository</p>
            <p className="text-sm">Browse and select a repository to manage its branches</p>
          </div>
        )}
      </div>
    </div>
  );
};