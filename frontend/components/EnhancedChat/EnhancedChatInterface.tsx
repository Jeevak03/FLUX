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
      case 'connected': return 'text-green-700 bg-green-50 border-green-200';
      case 'connecting': return 'text-yellow-700 bg-yellow-50 border-yellow-200';
      case 'error': return 'text-red-700 bg-red-50 border-red-200';
      default: return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br from-indigo-50 via-blue-50 to-purple-50 ${className}`}>
      <div className="max-w-full mx-auto">
        {/* Header */}
        <div className="bg-white/80 backdrop-blur-lg shadow-lg border-b border-gray-200/50 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between py-4">
              <div className="flex items-center space-x-3">
                <img src="/flux-logo.svg" alt="FLUX" className="w-10 h-10" />
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">FLUX</h1>
                  <p className="text-sm text-gray-600 mt-1">Where Agents Meet Agile</p>
                </div>
              </div>
              
              {/* Connection Status */}
              <div className="flex items-center space-x-3">
                <div className={`flex items-center space-x-2 px-4 py-2 rounded-full border backdrop-blur-sm ${getConnectionStatusColor()}`}>
                  <div className={`w-2 h-2 rounded-full ${
                    connectionStatus === 'connected' ? 'bg-green-500 animate-pulse shadow-sm shadow-green-400' :
                    connectionStatus === 'connecting' ? 'bg-yellow-500 animate-spin shadow-sm shadow-yellow-400' :
                    connectionStatus === 'error' ? 'bg-red-500 shadow-sm shadow-red-400' : 'bg-gray-500'
                  }`}></div>
                  <span className="text-sm font-medium capitalize">{connectionStatus}</span>
                </div>
                
                {connectionStatus !== 'connected' && (
                  <button
                    onClick={reconnect}
                    className="px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-sm rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
                  >
                    Reconnect
                  </button>
                )}
              </div>
            </div>

            {/* Feature Navigation Tabs */}
            <div className="border-t border-gray-200/50 pt-4 pb-4">
              <div className="flex space-x-2 bg-white/60 backdrop-blur-sm p-2 rounded-xl max-w-fit shadow-lg border border-white/50">
                <button
                  onClick={() => setActiveTab('chat')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                    activeTab === 'chat'
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/30 transform scale-105'
                      : 'text-gray-600 hover:text-indigo-600 hover:bg-indigo-50/50'
                  }`}
                >
                  💬 Chat
                  {messages.length > 0 && (
                    <span className="ml-2 bg-white text-indigo-600 text-xs rounded-full h-5 w-5 flex items-center justify-center inline-flex font-semibold shadow-sm">
                      {messages.length}
                    </span>
                  )}
                </button>
                
                <button
                  onClick={() => setActiveTab('documents')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                    activeTab === 'documents'
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/30 transform scale-105'
                      : 'text-gray-600 hover:text-indigo-600 hover:bg-indigo-50/50'
                  }`}
                >
                  📎 Documents
                  {uploadedFiles.length > 0 && (
                    <span className="ml-2 bg-white text-indigo-600 text-xs rounded-full h-5 w-5 flex items-center justify-center inline-flex font-semibold shadow-sm">
                      {uploadedFiles.length}
                    </span>
                  )}
                </button>
                
                <button
                  onClick={() => setActiveTab('expertise')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                    activeTab === 'expertise'
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/30 transform scale-105'
                      : 'text-gray-600 hover:text-indigo-600 hover:bg-indigo-50/50'
                  }`}
                >
                  👥 Team
                  {activeAgents.length > 0 && (
                    <span className="ml-2 bg-white text-indigo-600 text-xs rounded-full h-5 w-5 flex items-center justify-center inline-flex font-semibold shadow-sm">
                      {activeAgents.length}
                    </span>
                  )}
                </button>
                
                <button
                  onClick={() => setActiveTab('workflow')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                    activeTab === 'workflow'
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/30 transform scale-105'
                      : 'text-gray-600 hover:text-indigo-600 hover:bg-indigo-50/50'
                  }`}
                >
                  📊 Workflow
                </button>

                <button
                  onClick={() => setActiveTab('github')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                    activeTab === 'github'
                      ? 'bg-gradient-to-r from-gray-800 to-gray-900 text-white shadow-lg shadow-gray-800/30 transform scale-105'
                      : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50/50'
                  }`}
                >
                  � GitHub
                </button>
                
                <button
                  onClick={() => setActiveTab('history')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                    activeTab === 'history'
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/30 transform scale-105'
                      : 'text-gray-600 hover:text-indigo-600 hover:bg-indigo-50/50'
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
          {/* Tab Content */}
          <div className="min-h-screen">
            {/* Chat Tab */}
            {activeTab === 'chat' && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-180px)]">
                {/* Left Sidebar - Agent Selection & Context */}
                <div className="lg:col-span-3 space-y-4">
                  {/* Agent Selector */}
                  <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-lg border border-white/50 hover:shadow-xl transition-all duration-300">
                    <AgentSelector
                      agents={[
                        { id: 'requirements_analyst', name: 'Sara', role: 'Requirements Analyst', expertise: [] },
                        { id: 'software_architect', name: 'Marc', role: 'Software Architect', expertise: [] },
                        { id: 'developer', name: 'Alex', role: 'Senior Developer', expertise: [] },
                        { id: 'qa_tester', name: 'Jess', role: 'QA Engineer', expertise: [] },
                        { id: 'devops_engineer', name: 'Dave', role: 'DevOps Engineer', expertise: [] },
                        { id: 'project_manager', name: 'Emma', role: 'Project Manager', expertise: [] },
                        { id: 'security_expert', name: 'Robt', role: 'Security Expert', expertise: [] }
                      ]}
                      activeAgents={activeAgents}
                      selectedAgents={selectedAgents}
                      onAgentToggle={(agentId) => {
                        setSelectedAgents(prev =>
                          prev.includes(agentId)
                            ? prev.filter(id => id !== agentId)
                            : [...prev, agentId]
                        );
                      }}
                    />
                  </div>

                  {/* Project Context Panel */}
                  <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-lg border border-white/50 hover:shadow-xl transition-all duration-300">
                    <ProjectContextPanel
                      projectInfo={projectContext}
                      messages={messages}
                      activeAgents={activeAgents}
                      onUpdateProject={(updates) => {
                        setProjectContext(prev => ({ ...prev, ...updates }));
                        if (updates.phase) setCurrentPhase(updates.phase);
                      }}
                    />
                  </div>
                </div>

                {/* Main Content - Chat Interface */}
                <div className="lg:col-span-6 flex flex-col space-y-4 h-full">
                  {/* Chat Input */}
                  <div className="bg-gradient-to-br from-white/95 via-white/90 to-indigo-50/50 backdrop-blur-sm rounded-xl shadow-xl border border-white/50 hover:shadow-2xl transition-all duration-300">
                    <div className="p-4 border-b border-gray-100/50 bg-gradient-to-r from-transparent to-indigo-50/30">
                      <h3 className="text-lg font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">Chat with SDLC Team</h3>
                      <p className="text-sm text-gray-600">Ask questions, request analysis, or get project guidance</p>
                    </div>
                    
                    <div className="p-4 space-y-4">
                      {/* Message Input */}
                      <div className="relative">
                        <textarea
                          ref={textareaRef}
                          value={currentMessage}
                          onChange={handleTextareaChange}
                          onKeyPress={handleKeyPress}
                          placeholder="Describe your project needs, ask questions, or request specific analysis..."
                          className="w-full p-4 border border-indigo-200/50 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none transition-all duration-300 bg-white/80 backdrop-blur-sm hover:bg-white/90 focus:bg-white"
                          style={{ minHeight: '80px', maxHeight: '200px' }}
                        />
                        
                        {/* Character count */}
                        <div className="absolute bottom-3 right-3 text-xs text-gray-400 bg-white px-2 py-1 rounded">
                          {currentMessage.length}/2000
                        </div>
                      </div>

                      {/* Selected Agents & Upload Status */}
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          {selectedAgents.length > 0 && (
                            <div className="flex items-center space-x-2">
                              <span className="text-sm text-gray-600 font-medium">To:</span>
                              <div className="flex flex-wrap gap-1">
                                {selectedAgents.map(agentId => (
                                  <span
                                    key={agentId}
                                    className="px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full font-medium"
                                  >
                                    {agentId.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          {uploadedFiles.length > 0 && (
                            <div className="flex items-center space-x-2 text-sm text-gray-600">
                              <span>📎</span>
                              <span className="font-medium">{uploadedFiles.length} file{uploadedFiles.length !== 1 ? 's' : ''}</span>
                            </div>
                          )}
                        </div>

                        {/* Send Button */}
                        <button
                          onClick={handleSendMessage}
                          disabled={!currentMessage.trim() && uploadedFiles.length === 0}
                          className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-xl hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 font-medium shadow-lg hover:shadow-xl transform hover:scale-105 disabled:transform-none"
                        >
                          <span>Send</span>
                          <span className="ml-2">✨</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Response Preview Panel */}
                  <div className="flex-1 min-h-0">
                    <div className="bg-gradient-to-br from-white/95 via-white/90 to-purple-50/30 backdrop-blur-sm rounded-xl shadow-xl border border-white/50 h-full hover:shadow-2xl transition-all duration-300">
                      <ResponsePreviewPanel
                        messages={messages}
                        className="h-full"
                        onCopyResponse={(content) => {
                          navigator.clipboard.writeText(content);
                        }}
                        onRegenerateResponse={(messageId: any) => {
                          console.log('Regenerate:', messageId);
                        }}
                      />
                    </div>
                  </div>
                </div>

                {/* Right Sidebar - Quick Actions */}
                <div className="lg:col-span-3 space-y-4">
                  {/* Quick Action Buttons */}
                  <QuickActionButtons
                    currentPhase={currentPhase}
                    onActionClick={(action) => {
                      setCurrentMessage(action.template);
                      setSelectedAgents(action.suggestedAgents);
                      textareaRef.current?.focus();
                    }}
                  />

                  {/* Additional Features Panel */}
                  <div className="bg-gradient-to-br from-white/95 via-white/90 to-indigo-50/50 backdrop-blur-sm rounded-xl shadow-lg border border-white/50 p-6 hover:shadow-xl transition-all duration-300">
                    <div className="text-center">
                      <div className="text-4xl mb-4">🎯</div>
                      <h3 className="text-lg font-semibold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">More Features</h3>
                      <p className="text-gray-600 text-sm mb-4">
                        Explore additional tools and insights
                      </p>
                      <div className="space-y-3">
                        <button
                          onClick={() => setActiveTab('documents')}
                          className="w-full flex items-center justify-center space-x-2 p-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium"
                        >
                          <span>📎</span>
                          <span>Upload Documents</span>
                        </button>
                        <button
                          onClick={() => setActiveTab('expertise')}
                          className="w-full flex items-center justify-center space-x-2 p-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors text-sm font-medium"
                        >
                          <span>👥</span>
                          <span>Team Expertise</span>
                        </button>
                        <button
                          onClick={() => setActiveTab('workflow')}
                          className="w-full flex items-center justify-center space-x-2 p-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors text-sm font-medium"
                        >
                          <span>📊</span>
                          <span>View Workflow</span>
                        </button>
                        <button
                          onClick={() => setActiveTab('history')}
                          className="w-full flex items-center justify-center space-x-2 p-3 bg-indigo-50 text-indigo-700 rounded-lg hover:bg-indigo-100 transition-colors text-sm font-medium"
                        >
                          <span>🔍</span>
                          <span>Message History</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Connection & Stats Panel */}
                  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    <div className="text-center">
                      <div className="text-2xl mb-3">📊</div>
                      <h4 className="font-semibold text-gray-900 mb-3">Session Stats</h4>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <div className="text-2xl font-bold text-blue-600">{messages.length}</div>
                          <div className="text-gray-600">Messages</div>
                        </div>
                        <div>
                          <div className="text-2xl font-bold text-green-600">{activeAgents.length}</div>
                          <div className="text-gray-600">Active Agents</div>
                        </div>
                        <div>
                          <div className="text-2xl font-bold text-purple-600">{uploadedFiles.length}</div>
                          <div className="text-gray-600">Files</div>
                        </div>
                        <div>
                          <div className="text-2xl font-bold text-orange-600">{selectedAgents.length}</div>
                          <div className="text-gray-600">Selected</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Documents Tab */}
            {activeTab === 'documents' && (
              <div className="max-w-4xl mx-auto">
                <div className="bg-gradient-to-br from-white/95 via-white/90 to-blue-50/50 backdrop-blur-sm rounded-xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300">
                  <DocumentUpload
                    onFilesUploaded={setUploadedFiles}
                    maxFiles={10}
                    maxFileSize={30 * 1024 * 1024}
                  />
                </div>
              </div>
            )}

            {/* Team Expertise Tab */}
            {activeTab === 'expertise' && (
              <div className="max-w-6xl mx-auto">
                <div className="bg-gradient-to-br from-white/95 via-white/90 to-purple-50/50 backdrop-blur-sm rounded-xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300">
                  <AgentExpertiseCards
                    messages={messages}
                    activeAgents={activeAgents}
                    onAgentSelect={(agentId) => {
                      setSelectedAgents(prev =>
                        prev.includes(agentId) ? prev : [...prev, agentId]
                      );
                      setActiveTab('chat'); // Switch back to chat after selecting agent
                    }}
                  />
                </div>
              </div>
            )}

            {/* Workflow Tab */}
            {activeTab === 'workflow' && (
              <div className="max-w-6xl mx-auto">
                <div className="bg-gradient-to-br from-white/95 via-white/90 to-green-50/50 backdrop-blur-sm rounded-xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300">
                  <WorkflowVisualization
                    messages={messages}
                    activeAgents={activeAgents}
                    currentPhase={currentPhase}
                    onPhaseSelect={(phase) => {
                      setCurrentPhase(phase);
                      // Update project context
                    setProjectContext(prev => ({ ...prev, phase }));
                  }}
                  />
                </div>
              </div>
            )}

            {/* GitHub Tab */}
            {activeTab === 'github' && (
              <div className="max-w-7xl mx-auto">
                <GitHubIntegration
                  onRepositorySelect={(repo) => {
                    // Handle repository selection
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

            {/* History Tab */}
            {activeTab === 'history' && (
              <div className="max-w-4xl mx-auto">
                <div className="bg-gradient-to-br from-white/95 via-white/90 to-amber-50/50 backdrop-blur-sm rounded-xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300">
                  <MessageThreading
                    messages={messages}
                  onThreadSelect={(threadId) => {
                    console.log('Selected thread:', threadId);
                    setActiveTab('chat'); // Switch back to chat after selecting thread
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
    </div>
  );
};