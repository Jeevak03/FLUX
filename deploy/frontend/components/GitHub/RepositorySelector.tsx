// components/GitHub/RepositorySelector.tsx
import React, { useState } from 'react';

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

interface RepositorySelectorProps {
  repositories: GitHubRepository[];
  loading: boolean;
  onCloneRepository: (repo: GitHubRepository) => void;
  onRepositorySelect: (repo: GitHubRepository) => void;
}

export const RepositorySelector: React.FC<RepositorySelectorProps> = ({
  repositories,
  loading,
  onCloneRepository,
  onRepositorySelect
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [languageFilter, setLanguageFilter] = useState<string>('');
  const [selectedRepo, setSelectedRepo] = useState<GitHubRepository | null>(null);

  const filteredRepositories = repositories.filter(repo => {
    const matchesSearch = repo.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         repo.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLanguage = !languageFilter || repo.language === languageFilter;
    return matchesSearch && matchesLanguage;
  });

  const uniqueLanguages = Array.from(new Set(
    repositories
      .map(repo => repo.language)
      .filter(lang => lang !== null)
  )).sort();

  const handleRepositoryClick = (repo: GitHubRepository) => {
    setSelectedRepo(repo);
    onRepositorySelect(repo);
  };

  const getLanguageColor = (language: string | null) => {
    const colors: { [key: string]: string } = {
      'JavaScript': 'bg-yellow-100 text-yellow-800',
      'TypeScript': 'bg-blue-100 text-blue-800',
      'Python': 'bg-green-100 text-green-800',
      'Java': 'bg-red-100 text-red-800',
      'C++': 'bg-purple-100 text-purple-800',
      'C#': 'bg-indigo-100 text-indigo-800',
      'Go': 'bg-cyan-100 text-cyan-800',
      'Rust': 'bg-orange-100 text-orange-800',
      'PHP': 'bg-violet-100 text-violet-800'
    };
    return colors[language || ''] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
        <p className="text-gray-600">Loading repositories...</p>
      </div>
    );
  }

  if (repositories.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-gray-500">
        <div className="text-4xl mb-4">📂</div>
        <p className="text-lg font-medium">No Repositories Found</p>
        <p className="text-sm">Make sure your GitHub token has the correct permissions</p>
      </div>
    );
  }

  return (
    <div>
      {/* Search and Filter */}
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Search repositories..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <select
          value={languageFilter}
          onChange={(e) => setLanguageFilter(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">All Languages</option>
          {uniqueLanguages.map(lang => (
            <option key={lang} value={lang}>{lang}</option>
          ))}
        </select>
      </div>

      {/* Repository List */}
      <div className="space-y-4 max-h-[500px] overflow-y-auto">
        {filteredRepositories.map((repo) => (
          <div
            key={repo.id}
            onClick={() => handleRepositoryClick(repo)}
            className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md ${
              selectedRepo?.id === repo.id
                ? 'border-blue-500 bg-blue-50 shadow-md'
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-2">
                  <h3 className="text-lg font-semibold text-gray-900 truncate">
                    {repo.name}
                  </h3>
                  {repo.private && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                      🔒 Private
                    </span>
                  )}
                  {repo.language && (
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getLanguageColor(repo.language)}`}>
                      {repo.language}
                    </span>
                  )}
                </div>
                
                <p className="text-gray-600 text-sm mb-2">{repo.full_name}</p>
                
                {repo.description && (
                  <p className="text-gray-700 text-sm mb-3">{repo.description}</p>
                )}
                
                {repo.topics.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-3">
                    {repo.topics.slice(0, 5).map(topic => (
                      <span
                        key={topic}
                        className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                      >
                        {topic}
                      </span>
                    ))}
                    {repo.topics.length > 5 && (
                      <span className="text-xs text-gray-500">
                        +{repo.topics.length - 5} more
                      </span>
                    )}
                  </div>
                )}
                
                <div className="flex items-center space-x-4 text-sm text-gray-500">
                  <span>Default: {repo.default_branch}</span>
                  <a
                    href={repo.html_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800"
                    onClick={(e) => e.stopPropagation()}
                  >
                    View on GitHub ↗
                  </a>
                </div>
              </div>
              
              <div className="ml-4 flex flex-col space-y-2">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onCloneRepository(repo);
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  📥 Clone
                </button>
                {selectedRepo?.id === repo.id && (
                  <div className="text-xs text-blue-600 font-medium">
                    ✓ Selected
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredRepositories.length === 0 && searchTerm && (
        <div className="flex flex-col items-center justify-center py-12 text-gray-500">
          <div className="text-4xl mb-4">🔍</div>
          <p className="text-lg font-medium">No repositories found</p>
          <p className="text-sm">Try adjusting your search criteria</p>
        </div>
      )}

      {/* Repository Count */}
      <div className="mt-4 text-sm text-gray-500 text-center">
        Showing {filteredRepositories.length} of {repositories.length} repositories
      </div>
    </div>
  );
};