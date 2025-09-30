// components/EnhancedChat/EnhancedChatInterface.tsx
import React, { useState, useRef } from 'react';
import { useWebSocket } from '../../hooks/useWebSocket';
import { DocumentUpload } from '../DocumentUpload';
import { ResponsePreviewPanel } from '../ResponsePreview';
import { AgentSelector, MessageThreading, AgentExpertiseCards, WorkflowVisualization } from '../AgentChat';
import { ProjectContextPanel } from '../AgentChat/ProjectContextPanel';
import { QuickActionButtons } from '../AgentChat/QuickActionButtons';
import { GitHubIntegration } from '../GitHub/GitHubIntegration';
import { UploadedFile } from '../../types/agents';

interface EnhancedChatInterfaceProps {
  sessionId: string;
  className?: string;
}

export const EnhancedChatInterface: React.FC<EnhancedChatInterfaceProps> = ({
  sessionId,
  className = ''
}) => {
  // WebSocket connection
  const { messages, connectionStatus, activeAgents, sendMessage, reconnect } = useWebSocket(sessionId);
  
  // UI State
  const [currentMessage, setCurrentMessage] = useState('');
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [activeTab, setActiveTab] = useState<'chat' | 'documents' | 'expertise' | 'workflow' | 'github' | 'history'>('chat');
  const [currentPhase, setCurrentPhase] = useState<string>('requirements');

  const [projectContext, setProjectContext] = useState({
    name: 'New Project',
    technology: 'Web Application',
    phase: 'requirements',
    progress: 15,
    description: '',
    startDate: new Date().toISOString().split('T')[0]
  });

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Helper function to get agent display names
  const getAgentDisplayName = (agentId: string): string => {
    const names: { [key: string]: string } = {
      'requirements_analyst': 'Sara',
      'software_architect': 'Marc',
      'developer': 'Alex',
      'qa_tester': 'Jess',
      'devops_engineer': 'Dave',
      'project_manager': 'Emma',
      'security_expert': 'Robt'
    };
    return names[agentId] || agentId;
  };

  // Detect if user is making a direct call to an agent
  const detectDirectCall = (message: string): string | null => {
    const lowerMsg = message.toLowerCase().trim();
    const directPatterns = [
      /^(hi|hello|hey|greetings)\s+(sara|marc|alex|jess|dave|emma|robt)/i,
      /^@?(sara|marc|alex|jess|dave|emma|robt)\b/i
    ];
    
    for (const pattern of directPatterns) {
      const match = lowerMsg.match(pattern);
      if (match) {
        const name = match[match.length - 1].toLowerCase();
        const agentMap: { [key: string]: string } = {
          'sara': 'requirements_analyst',
          'marc': 'software_architect',
          'alex': 'developer',
          'jess': 'qa_tester',
          'dave': 'devops_engineer',
          'emma': 'project_manager',
          'robt': 'security_expert'
        };
        return agentMap[name] || null;
      }
    }
    return null;
  };

  // Handle message sending
  const handleSendMessage = async () => {
    if (!currentMessage.trim() && uploadedFiles.length === 0) return;
    if (connectionStatus !== 'connected') {
      alert('Not connected to server. Please check connection.');
      return;
    }

    try {
      await sendMessage(
        currentMessage || 'I have uploaded some documents for analysis.',
        { 
          project: projectContext, 
          phase: currentPhase, 
          uploadedFiles: uploadedFiles 
        },
        selectedAgents
      );
      
      // Clear form
      setCurrentMessage('');
      setUploadedFiles([]);
      
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = '60px';
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  // Handle textarea auto-resize
  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setCurrentMessage(value);
    
    // Auto-resize textarea
    const textarea = e.target;
    textarea.style.height = '60px';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
  };

  // Handle Enter key
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Connection status indicator
  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'connecting': return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'error': return 'bg-red-500/10 text-red-400 border-red-500/30';
      default: return 'bg-slate-700/50 text-slate-400 border-slate-600/50';
    }
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 ${className}`}>
      <div className="max-w-full mx-auto">
        {/* Header */}
        <div className="bg-slate-900/95 backdrop-blur-xl shadow-2xl border-b border-slate-700/50 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between py-4">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-gradient-to-br from-cyan-400/20 to-blue-500/20 rounded-xl flex items-center justify-center border border-cyan-400/30 shadow-lg">
                  <svg className="w-7 h-7 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">FLUX</h1>
                  <p className="text-sm text-slate-400 mt-1 font-medium">Where Agents Meet Agile</p>
                </div>
              </div>
              
              {/* Connection Status */}
              <div className="flex items-center space-x-3">
                <div className={`flex items-center space-x-3 px-4 py-2 rounded-xl border backdrop-blur-sm ${getConnectionStatusColor()}`}>
                  <div className={`w-3 h-3 rounded-full ${
                    connectionStatus === 'connected' ? 'bg-emerald-400 animate-pulse shadow-lg shadow-emerald-400/50' :
                    connectionStatus === 'connecting' ? 'bg-amber-400 animate-spin shadow-lg shadow-amber-400/50' :
                    connectionStatus === 'error' ? 'bg-red-400 shadow-lg shadow-red-400/50' : 'bg-slate-500'
                  }`}></div>
                  <span className="text-sm font-medium capitalize">{connectionStatus}</span>
                </div>
                
                {connectionStatus !== 'connected' && (
                  <button
                    onClick={reconnect}
                    className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 text-white text-sm rounded-xl hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 border border-cyan-500/30"
                  >
                    Reconnect
                  </button>
                )}
              </div>
            </div>

            {/* Navigation Tabs */}
            <div className="border-t border-slate-700/50 pt-4 pb-4">
              <div className="flex space-x-2 bg-slate-800/60 backdrop-blur-sm p-2 rounded-xl max-w-fit shadow-lg border border-slate-700/50">
                <button
                  onClick={() => setActiveTab('chat')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                    activeTab === 'chat'
                      ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30 transform scale-105 border border-cyan-500/30'
                      : 'text-slate-400 hover:text-cyan-400 hover:bg-slate-700/50 border border-transparent hover:border-slate-600/50'
                  }`}
                >
                  💬 Chat
                  {messages.length > 0 && (
                    <span className="ml-2 bg-slate-800/80 text-cyan-400 text-xs rounded-full h-5 w-5 flex items-center justify-center inline-flex font-semibold shadow-sm border border-cyan-500/30">
                      {messages.length}
                    </span>
                  )}
                </button>
                
                <button
                  onClick={() => setActiveTab('documents')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                    activeTab === 'documents'
                      ? 'bg-gradient-to-r from-emerald-500 to-green-600 text-white shadow-lg shadow-emerald-500/30 transform scale-105 border border-emerald-500/30'
                      : 'text-slate-400 hover:text-emerald-400 hover:bg-slate-700/50 border border-transparent hover:border-slate-600/50'
                  }`}
                >
                  📎 Documents
                  {uploadedFiles.length > 0 && (
                    <span className="ml-2 bg-slate-800/80 text-emerald-400 text-xs rounded-full h-5 w-5 flex items-center justify-center inline-flex font-semibold shadow-sm border border-emerald-500/30">
                      {uploadedFiles.length}
                    </span>
                  )}
                </button>
                
                <button
                  onClick={() => setActiveTab('expertise')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                    activeTab === 'expertise'
                      ? 'bg-gradient-to-r from-purple-500 to-indigo-600 text-white shadow-lg shadow-purple-500/30 transform scale-105 border border-purple-500/30'
                      : 'text-slate-400 hover:text-purple-400 hover:bg-slate-700/50 border border-transparent hover:border-slate-600/50'
                  }`}
                >
                  👥 Team
                  {activeAgents.length > 0 && (
                    <span className="ml-2 bg-slate-800/80 text-purple-400 text-xs rounded-full h-5 w-5 flex items-center justify-center inline-flex font-semibold shadow-sm border border-purple-500/30">
                      {activeAgents.length}
                    </span>
                  )}
                </button>
                
                <button
                  onClick={() => setActiveTab('workflow')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                    activeTab === 'workflow'
                      ? 'bg-gradient-to-r from-amber-500 to-orange-600 text-white shadow-lg shadow-amber-500/30 transform scale-105 border border-amber-500/30'
                      : 'text-slate-400 hover:text-amber-400 hover:bg-slate-700/50 border border-transparent hover:border-slate-600/50'
                  }`}
                >
                  📊 Workflow
                </button>

                <button
                  onClick={() => setActiveTab('github')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                    activeTab === 'github'
                      ? 'bg-gradient-to-r from-slate-700 to-slate-800 text-white shadow-lg shadow-slate-700/30 transform scale-105 border border-slate-600/50'
                      : 'text-slate-400 hover:text-slate-300 hover:bg-slate-700/50 border border-transparent hover:border-slate-600/50'
                  }`}
                >
                  🐙 GitHub
                </button>
                
                <button
                  onClick={() => setActiveTab('history')}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                    activeTab === 'history'
                      ? 'bg-gradient-to-r from-rose-500 to-pink-600 text-white shadow-lg shadow-rose-500/30 transform scale-105 border border-rose-500/30'
                      : 'text-slate-400 hover:text-rose-400 hover:bg-slate-700/50 border border-transparent hover:border-slate-600/50'
                  }`}
                >
                  🔍 History
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {/* Chat Tab - GitHub Copilot Style Layout */}
          {activeTab === 'chat' && (
            <div className="max-w-4xl mx-auto">
              {/* Team Selection Panel */}
              <div className="mb-6">
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                      <h3 className="text-sm font-semibold text-gray-800">Select Team Members</h3>
                    </div>
                    <span className="text-sm text-gray-500">{selectedAgents.length} selected</span>
                  </div>
                  
                  <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                    {[
                      { id: 'requirements_analyst', name: 'Sara', role: 'Requirements Analyst', color: 'border-purple-200 bg-purple-50 text-purple-700' },
                      { id: 'software_architect', name: 'Marc', role: 'Software Architect', color: 'border-blue-200 bg-blue-50 text-blue-700' },
                      { id: 'developer', name: 'Alex', role: 'Senior Developer', color: 'border-green-200 bg-green-50 text-green-700' },
                      { id: 'qa_tester', name: 'Jess', role: 'QA Engineer', color: 'border-yellow-200 bg-yellow-50 text-yellow-700' },
                      { id: 'devops_engineer', name: 'Dave', role: 'DevOps Engineer', color: 'border-red-200 bg-red-50 text-red-700' },
                      { id: 'project_manager', name: 'Emma', role: 'Project Manager', color: 'border-indigo-200 bg-indigo-50 text-indigo-700' },
                      { id: 'security_expert', name: 'Robt', role: 'Security Expert', color: 'border-gray-200 bg-gray-50 text-gray-700' }
                    ].map(agent => (
                      <button
                        key={agent.id}
                        onClick={() => {
                          setSelectedAgents(prev =>
                            prev.includes(agent.id)
                              ? prev.filter(id => id !== agent.id)
                              : [...prev, agent.id]
                          );
                        }}
                        className={`p-3 rounded-lg border-2 transition-all duration-200 text-left hover:shadow-sm ${
                          selectedAgents.includes(agent.id)
                            ? `${agent.color} border-opacity-100 shadow-sm`
                            : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
                        }`}
                      >
                        <div className="flex items-center space-x-2 mb-1">
                          <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                            selectedAgents.includes(agent.id) ? 'bg-white/80' : 'bg-gray-100'
                          }`}>
                            {agent.name[0]}
                          </div>
                          <div className={`w-2 h-2 rounded-full ${
                            activeAgents.includes(agent.id) ? 'bg-green-500' : 'bg-gray-300'
                          }`}></div>
                        </div>
                        <div className="text-xs font-medium">{agent.name}</div>
                        <div className="text-xs opacity-70 truncate">{agent.role}</div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Claude-Style Conversation Area */}
              <div className="mb-6">
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 h-96 flex flex-col">
                  {/* Simple Header */}
                  <div className="px-6 py-3 border-b border-gray-100 bg-gray-50/50">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                        </svg>
                        <span className="text-sm font-medium text-gray-700">{messages.length} messages</span>
                        {activeAgents.length > 0 && (
                          <>
                            <span className="text-gray-300">•</span>
                            <div className="flex items-center space-x-1">
                              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                              <span className="text-sm text-green-600">{activeAgents.length} online</span>
                            </div>
                          </>
                        )}
                      </div>
                      <button
                        onClick={() => window.location.reload()}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                        title="Clear conversation"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                  
                  {/* Messages Area - Claude Style */}
                  <div className="flex-1 overflow-y-auto">
                    {messages.length === 0 ? (
                      <div className="flex flex-col items-center justify-center h-full text-gray-500">
                        <svg className="w-12 h-12 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                        </svg>
                        <p className="text-lg font-medium text-gray-400">No messages yet</p>
                        <p className="text-sm text-gray-400">Start a conversation with the SDLC team</p>
                      </div>
                    ) : (
                      <div className="space-y-0">
                        {messages.map((message, index) => {
                          const isUser = message.agent === 'user';
                          const agentNames: { [key: string]: string } = {
                            'requirements_analyst': 'Sara',
                            'software_architect': 'Marc',
                            'developer': 'Alex',
                            'qa_tester': 'Jess',
                            'devops_engineer': 'Dave',
                            'project_manager': 'Emma',
                            'security_expert': 'Robt'
                          };
                          const displayName = agentNames[message.agent] || message.agent;
                          
                          return (
                            <div 
                              key={`${message.timestamp}-${index}`} 
                              className={`px-6 py-4 ${isUser ? 'bg-blue-50/50' : 'bg-white'} ${index > 0 ? 'border-t border-gray-100' : ''} hover:bg-gray-50/50 transition-colors group`}
                            >
                              <div className="flex space-x-3">
                                {/* Avatar */}
                                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                                  isUser 
                                    ? 'bg-blue-500 text-white' 
                                    : 'bg-gradient-to-br from-purple-500 to-indigo-600 text-white'
                                }`}>
                                  {isUser ? 'You' : displayName[0]}
                                </div>
                                
                                {/* Message Content */}
                                <div className="flex-1 min-w-0">
                                  <div className="flex items-center space-x-2 mb-1">
                                    <p className="text-sm font-medium text-gray-900">
                                      {isUser ? 'You' : displayName}
                                    </p>
                                    <p className="text-xs text-gray-500">
                                      {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </p>
                                    {!isUser && (
                                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                                        {message.agent.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                      </span>
                                    )}
                                  </div>
                                  <div className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
                                    {message.message}
                                  </div>
                                  
                                  {/* Copy Button */}
                                  <button
                                    onClick={() => navigator.clipboard.writeText(message.message)}
                                    className="mt-2 opacity-0 group-hover:opacity-100 text-xs text-gray-400 hover:text-gray-600 transition-all duration-200 flex items-center space-x-1"
                                  >
                                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                    </svg>
                                    <span>Copy</span>
                                  </button>
                                </div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Message Input - Claude Style */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200">
                {/* Selected Recipients Bar */}
                {selectedAgents.length > 0 && (
                  <div className="px-4 py-3 border-b border-gray-100 bg-gray-50/50">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-xs text-gray-500 font-medium">Messaging:</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {selectedAgents.map(agentId => (
                        <span
                          key={agentId}
                          className="inline-flex items-center px-2 py-1 bg-blue-100 text-blue-700 text-sm rounded-md font-medium"
                        >
                          {getAgentDisplayName(agentId)}
                          <button
                            onClick={() => setSelectedAgents(prev => prev.filter(id => id !== agentId))}
                            className="ml-1 text-blue-500/60 hover:text-blue-500 transition-colors"
                          >
                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                          </button>
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Main Input Area */}
                <div className="p-4">
                  {/* Upload Status */}
                  {uploadedFiles.length > 0 && (
                    <div className="mb-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                      <div className="flex items-center space-x-2">
                        <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                        </svg>
                        <span className="text-sm text-blue-700 font-medium">{uploadedFiles.length} file{uploadedFiles.length !== 1 ? 's' : ''} attached</span>
                      </div>
                    </div>
                  )}

                  {/* Message Input - Claude Style */}
                  <div className="relative">
                    <textarea
                      ref={textareaRef}
                      value={currentMessage}
                      onChange={handleTextareaChange}
                      onKeyPress={handleKeyPress}
                      placeholder={selectedAgents.length > 0 
                        ? `Message ${selectedAgents.map(getAgentDisplayName).join(', ')}...`
                        : "Ask a question, start a discussion, or request help from the SDLC team..."
                      }
                      className="w-full p-4 pr-16 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none transition-all duration-200 bg-white hover:border-gray-400 placeholder-gray-400 text-gray-900"
                      style={{ minHeight: '60px', maxHeight: '200px' }}
                    />
                    
                    {/* Send Button */}
                    <div className="absolute right-3 bottom-3 flex items-center space-x-2">
                      {currentMessage.length > 0 && (
                        <span className="text-xs text-gray-400">{currentMessage.length}/2000</span>
                      )}
                      <button
                        onClick={handleSendMessage}
                        disabled={!currentMessage.trim() && uploadedFiles.length === 0}
                        className="inline-flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-blue-600 transition-colors"
                        title="Send message"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  {/* Quick Actions Bar */}
                  <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-200">
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => setActiveTab('documents')}
                        className="inline-flex items-center px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-blue-600 bg-gray-100 hover:bg-blue-50 rounded-md border border-gray-200 hover:border-blue-200 transition-all duration-200"
                      >
                        <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                        </svg>
                        Attach
                      </button>
                      <button
                        onClick={() => setActiveTab('workflow')}
                        className="inline-flex items-center px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-blue-600 bg-gray-100 hover:bg-blue-50 rounded-md border border-gray-200 hover:border-blue-200 transition-all duration-200"
                      >
                        <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                        Workflow
                      </button>
                      <button
                        onClick={() => setActiveTab('history')}
                        className="inline-flex items-center px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-blue-600 bg-gray-100 hover:bg-blue-50 rounded-md border border-gray-200 hover:border-blue-200 transition-all duration-200"
                      >
                        <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                        History
                      </button>
                    </div>
                    
                    <div className="flex items-center space-x-3 text-xs text-gray-500">
                      <span>{messages.length} messages</span>
                      <span>•</span>
                      <span>{activeAgents.length} online</span>
                      {currentPhase && (
                        <>
                          <span>•</span>
                          <span className="capitalize">{currentPhase.replace('_', ' ')}</span>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Other Tabs */}
          {activeTab === 'documents' && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-gradient-to-br from-slate-800/95 via-slate-700/90 to-slate-800/95 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700/50 p-6 hover:shadow-2xl transition-all duration-300">
                <DocumentUpload
                  onFilesUploaded={setUploadedFiles}
                  maxFiles={10}
                  maxFileSize={30 * 1024 * 1024}
                />
              </div>
            </div>
          )}

          {activeTab === 'expertise' && (
            <div className="max-w-6xl mx-auto">
              <div className="bg-gradient-to-br from-slate-800/95 via-slate-700/90 to-slate-800/95 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700/50 p-6 hover:shadow-2xl transition-all duration-300">
                <AgentExpertiseCards
                  messages={messages}
                  activeAgents={activeAgents}
                  onAgentSelect={(agentId) => {
                    setSelectedAgents(prev =>
                      prev.includes(agentId) ? prev : [...prev, agentId]
                    );
                    setActiveTab('chat');
                  }}
                />
              </div>
            </div>
          )}

          {activeTab === 'workflow' && (
            <div className="max-w-6xl mx-auto">
              <div className="bg-gradient-to-br from-slate-800/95 via-slate-700/90 to-slate-800/95 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700/50 p-6 hover:shadow-2xl transition-all duration-300">
                <WorkflowVisualization
                  messages={messages}
                  activeAgents={activeAgents}
                  currentPhase={currentPhase}
                  onPhaseSelect={(phase) => {
                    setCurrentPhase(phase);
                    setProjectContext(prev => ({ ...prev, phase }));
                  }}
                />
              </div>
            </div>
          )}

          {activeTab === 'github' && (
            <div className="max-w-7xl mx-auto">
              <GitHubIntegration
                onRepositorySelect={(repo) => {
                  setProjectContext(prev => ({
                    ...prev,
                    name: repo.name,
                    technology: repo.language || 'Unknown'
                  }));
                  console.log('Selected repository:', repo);
                }}
              />
            </div>
          )}

          {activeTab === 'history' && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-gradient-to-br from-slate-800/95 via-slate-700/90 to-slate-800/95 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700/50 p-6 hover:shadow-2xl transition-all duration-300">
                <MessageThreading
                  messages={messages}
                  onThreadSelect={(threadId) => {
                    console.log('Selected thread:', threadId);
                    setActiveTab('chat');
                  }}
                  onMessageSearch={(query) => {
                    console.log('Search query:', query);
                  }}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};