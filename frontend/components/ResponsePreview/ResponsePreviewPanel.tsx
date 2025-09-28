// components/ResponsePreview/ResponsePreviewPanel.tsx
import React, { useState, useRef, useEffect } from 'react';
import { AgentMessage, UploadedFile } from '../../types/agents';

interface ResponsePreviewPanelProps {
  messages: AgentMessage[];
  className?: string;
  showToolbar?: boolean;
  onCopyResponse?: (content: string) => void;
  onRegenerateResponse?: (messageId: string) => void;
}

export const ResponsePreviewPanel: React.FC<ResponsePreviewPanelProps> = ({
  messages,
  className = '',
  showToolbar = true,
  onCopyResponse,
  onRegenerateResponse
}) => {
  const [selectedMessage, setSelectedMessage] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearch, setShowSearch] = useState(false);
  const [copySuccess, setCopySuccess] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (showSearch && searchInputRef.current) {
      searchInputRef.current.focus();
    }
  }, [showSearch]);

  const formatTimestamp = (timestamp: string): string => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getAgentInfo = (agent: string) => {
    const agentData: { [key: string]: { name: string; avatar: string; color: string } } = {
      'user': { name: 'You', avatar: '👤', color: 'bg-gray-100 text-gray-800' },
      'requirements_analyst': { name: 'Sara', avatar: '👩‍💼', color: 'bg-purple-100 text-purple-800' },
      'software_architect': { name: 'Marc', avatar: '👨‍💻', color: 'bg-blue-100 text-blue-800' },
      'developer': { name: 'Alex', avatar: '👩‍💻', color: 'bg-green-100 text-green-800' },
      'qa_tester': { name: 'Jess', avatar: '👩‍🔬', color: 'bg-yellow-100 text-yellow-800' },
      'devops_engineer': { name: 'Dave', avatar: '👨‍🔧', color: 'bg-red-100 text-red-800' },
      'project_manager': { name: 'Emma', avatar: '👩‍💼', color: 'bg-indigo-100 text-indigo-800' },
      'security_expert': { name: 'Robt', avatar: '👨‍🛡️', color: 'bg-gray-100 text-gray-800' }
    };
    
    return agentData[agent] || { name: agent, avatar: '🤖', color: 'bg-gray-100 text-gray-800' };
  };

  const handleCopy = async (content: string, messageId: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopySuccess(messageId);
      onCopyResponse?.(content);
      setTimeout(() => setCopySuccess(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const highlightSearchTerm = (text: string, query: string): string => {
    if (!query) return text;
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark class="bg-yellow-200 px-1 rounded">$1</mark>');
  };

  const formatMessage = (message: string): string => {
    // Convert markdown-style formatting to HTML
    let formatted = message
      // Bold text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Italic text  
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      // Code blocks
      .replace(/```([\s\S]*?)```/g, '<pre class="bg-gray-100 p-3 rounded-lg overflow-x-auto text-sm"><code>$1</code></pre>')
      // Inline code
      .replace(/`([^`]+)`/g, '<code class="bg-gray-100 px-2 py-1 rounded text-sm">$1</code>')
      // Line breaks
      .replace(/\n/g, '<br/>');

    return formatted;
  };

  const renderUploadedFiles = (files: UploadedFile[]) => {
    if (!files || files.length === 0) return null;

    return (
      <div className="mt-3 pt-3 border-t border-gray-100">
        <div className="flex items-center space-x-2 mb-2">
          <span className="text-sm font-medium text-gray-600">📎 Attached Files:</span>
        </div>
        <div className="space-y-2">
          {files.map((file) => (
            <div key={file.id} className="flex items-center space-x-3 p-2 bg-gray-50 rounded-lg">
              <span className="text-lg">📄</span>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">{file.name}</p>
                <p className="text-xs text-gray-500">
                  {(file.size / 1024).toFixed(1)}KB • {file.type}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const filteredMessages = messages.filter(message => {
    if (!searchQuery) return true;
    return message.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
           getAgentInfo(message.agent).name.toLowerCase().includes(searchQuery.toLowerCase());
  });

  return (
    <div className={`bg-white rounded-xl shadow-lg border border-gray-100 flex flex-col ${className}`}>
      {/* Header with Toolbar */}
      {showToolbar && (
        <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-4 rounded-t-xl">
          <div className="flex items-center justify-between text-white">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                💬
              </div>
              <div>
                <h3 className="font-semibold text-lg">Conversation Preview</h3>
                <p className="text-sm text-white/80">{filteredMessages.length} messages</p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              {/* Search Toggle */}
              <button
                onClick={() => {
                  setShowSearch(!showSearch);
                  if (!showSearch) setSearchQuery('');
                }}
                className={`p-2 rounded-lg transition-colors ${
                  showSearch ? 'bg-white/30' : 'bg-white/10 hover:bg-white/20'
                }`}
                title="Search messages"
              >
                🔍
              </button>

              {/* Clear Chat */}
              <button
                onClick={() => window.location.reload()}
                className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
                title="Clear conversation"
              >
                🗑️
              </button>

              {/* Scroll to bottom */}
              <button
                onClick={scrollToBottom}
                className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
                title="Scroll to bottom"
              >
                ⬇️
              </button>
            </div>
          </div>

          {/* Search Bar */}
          {showSearch && (
            <div className="mt-4">
              <input
                ref={searchInputRef}
                type="text"
                placeholder="Search messages..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-4 py-2 bg-white/20 border border-white/30 rounded-lg text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-white/50"
              />
            </div>
          )}
        </div>
      )}

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-96">
        {filteredMessages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <div className="text-6xl mb-4">💬</div>
            <p className="text-lg font-medium">No messages yet</p>
            <p className="text-sm">Start a conversation with the SDLC team!</p>
          </div>
        ) : (
          <>
            {filteredMessages.map((message, index) => {
              const agentInfo = getAgentInfo(message.agent);
              const isSelected = selectedMessage === `${message.timestamp}-${index}`;
              const isUser = message.agent === 'user';
              
              return (
                <div
                  key={`${message.timestamp}-${index}`}
                  className={`group relative ${
                    isUser 
                      ? 'ml-12' 
                      : 'mr-12'
                  }`}
                >
                  {/* Message Container */}
                  <div
                    className={`relative p-4 rounded-xl transition-all duration-200 cursor-pointer ${
                      isUser
                        ? 'bg-blue-500 text-white ml-auto'
                        : 'bg-gray-50 border border-gray-200 hover:shadow-md'
                    } ${isSelected ? 'ring-2 ring-blue-300' : ''}`}
                    onClick={() => setSelectedMessage(isSelected ? null : `${message.timestamp}-${index}`)}
                  >
                    {/* Agent Header */}
                    {!isUser && (
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          <div className="flex items-center space-x-2">
                            <span className="text-lg">{agentInfo.avatar}</span>
                            <span className={`px-2 py-1 text-xs rounded-full font-medium ${agentInfo.color}`}>
                              {agentInfo.name}
                            </span>
                          </div>
                        </div>
                        <span className="text-xs text-gray-500">
                          {formatTimestamp(message.timestamp)}
                        </span>
                      </div>
                    )}

                    {/* User Message Header */}
                    {isUser && (
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs text-white/70">
                          {formatTimestamp(message.timestamp)}
                        </span>
                        <span className="text-lg">{agentInfo.avatar}</span>
                      </div>
                    )}

                    {/* Message Content */}
                    <div className={`prose max-w-none ${isUser ? 'text-white' : 'text-gray-900'}`}>
                      <div 
                        dangerouslySetInnerHTML={{ 
                          __html: highlightSearchTerm(formatMessage(message.message), searchQuery)
                        }} 
                      />
                    </div>

                    {/* Uploaded Files */}
                    {message.uploadedFiles && renderUploadedFiles(message.uploadedFiles)}

                    {/* Message Actions */}
                    <div className={`absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity ${
                      isUser ? 'right-2' : 'right-2'
                    }`}>
                      <div className="flex items-center space-x-1">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleCopy(message.message, `${message.timestamp}-${index}`);
                          }}
                          className={`p-1 rounded hover:bg-white/20 transition-colors ${
                            copySuccess === `${message.timestamp}-${index}` ? 'text-green-500' : 
                            isUser ? 'text-white/70 hover:text-white' : 'text-gray-500 hover:text-gray-700'
                          }`}
                          title="Copy message"
                        >
                          {copySuccess === `${message.timestamp}-${index}` ? '✅' : '📋'}
                        </button>
                        
                        {!isUser && onRegenerateResponse && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              onRegenerateResponse(`${message.timestamp}-${index}`);
                            }}
                            className="p-1 rounded text-gray-500 hover:text-gray-700 hover:bg-white/20 transition-colors"
                            title="Regenerate response"
                          >
                            🔄
                          </button>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Timestamp for mobile */}
                  {isSelected && (
                    <div className="mt-2 text-xs text-gray-400 text-center animate-in fade-in duration-200">
                      {new Date(message.timestamp).toLocaleString()}
                    </div>
                  )}
                </div>
              );
            })}
            
            {/* Scroll anchor */}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Footer with stats */}
      <div className="border-t border-gray-200 px-4 py-3 bg-gray-50 rounded-b-xl">
        <div className="flex items-center justify-between text-sm text-gray-600">
          <div className="flex items-center space-x-4">
            <span>
              {filteredMessages.filter(m => m.agent !== 'user').length} agent responses
            </span>
            <span>
              {filteredMessages.filter(m => m.agent === 'user').length} user messages
            </span>
            {searchQuery && (
              <span className="text-blue-600">
                {filteredMessages.length} results for "{searchQuery}"
              </span>
            )}
          </div>
          
          {copySuccess && (
            <div className="flex items-center space-x-2 text-green-600">
              <span>✅</span>
              <span>Copied to clipboard!</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};