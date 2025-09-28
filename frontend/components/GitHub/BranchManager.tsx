// components/GitHub/BranchManager.tsx
import React, { useState, useEffect } from 'react';

interface GitHubRepository {
  id: number;
  name: string;
  full_name: string;
  default_branch: string;
}

interface GitHubBranch {
  name: string;
  sha: string;
  protected: boolean;
}

interface BranchManagerProps {
  repository: GitHubRepository;
  onBranchCreated: () => void;
}

export const BranchManager: React.FC<BranchManagerProps> = ({
  repository,
  onBranchCreated
}) => {
  const [branches, setBranches] = useState<GitHubBranch[]>([]);
  const [loading, setLoading] = useState(false);
  const [newBranchName, setNewBranchName] = useState('');
  const [selectedFromBranch, setSelectedFromBranch] = useState(repository.default_branch);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    loadBranches();
  }, [repository]);

  const loadBranches = async () => {
    setLoading(true);
    try {
      const encodedRepoName = repository.full_name.replace('/', '%2F');
      const response = await fetch(`/api/github/repositories/${encodedRepoName}/branches`);
      if (response.ok) {
        const branchData = await response.json();
        setBranches(branchData);
      }
    } catch (err) {
      console.error('Error loading branches:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBranch = async () => {
    if (!newBranchName.trim()) return;

    setCreating(true);
    try {
      const response = await fetch('/api/github/create-branch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          repo_full_name: repository.full_name,
          branch_name: newBranchName.trim(),
          from_branch: selectedFromBranch
        })
      });

      if (response.ok) {
        setNewBranchName('');
        await loadBranches();
        onBranchCreated();
        alert(`Branch '${newBranchName}' created successfully!`);
      } else {
        const error = await response.json();
        alert(`Failed to create branch: ${error.detail}`);
      }
    } catch (err) {
      alert('Error creating branch');
    } finally {
      setCreating(false);
    }
  };

  const getBranchIcon = (branch: GitHubBranch) => {
    if (branch.name === repository.default_branch) return '🏠';
    if (branch.protected) return '🔒';
    return '🌿';
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <p className="text-gray-600">Loading branches...</p>
      </div>
    );
  }

  return (
    <div>
      {/* Repository Info */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <h3 className="font-semibold text-gray-900 mb-2">{repository.name}</h3>
        <p className="text-sm text-gray-600">{repository.full_name}</p>
      </div>

      {/* Create New Branch */}
      <div className="bg-white border border-gray-200 rounded-lg p-4 mb-6">
        <h4 className="font-semibold text-gray-900 mb-4">🌿 Create New Branch</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Branch Name
            </label>
            <input
              type="text"
              value={newBranchName}
              onChange={(e) => setNewBranchName(e.target.value)}
              placeholder="feature/new-feature"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Create From
            </label>
            <select
              value={selectedFromBranch}
              onChange={(e) => setSelectedFromBranch(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {branches.map((branch) => (
                <option key={branch.name} value={branch.name}>
                  {branch.name} {branch.name === repository.default_branch ? '(default)' : ''}
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={handleCreateBranch}
              disabled={!newBranchName.trim() || creating}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              {creating ? '🔄 Creating...' : '➕ Create Branch'}
            </button>
          </div>
        </div>
      </div>

      {/* Branches List */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h4 className="font-semibold text-gray-900">Branches ({branches.length})</h4>
          <button
            onClick={loadBranches}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            🔄 Refresh
          </button>
        </div>

        <div className="space-y-2">
          {branches.map((branch) => (
            <div
              key={branch.name}
              className={`border rounded-lg p-4 ${
                branch.name === repository.default_branch
                  ? 'border-green-200 bg-green-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-lg">{getBranchIcon(branch)}</span>
                  <div>
                    <p className="font-medium text-gray-900 flex items-center space-x-2">
                      <span>{branch.name}</span>
                      {branch.name === repository.default_branch && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          Default
                        </span>
                      )}
                      {branch.protected && (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                          Protected
                        </span>
                      )}
                    </p>
                    <p className="text-sm text-gray-500 font-mono">SHA: {branch.sha.substring(0, 8)}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <button className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors">
                    🔍 View
                  </button>
                  {branch.name !== repository.default_branch && !branch.protected && (
                    <button className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                      🗑️ Delete
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};