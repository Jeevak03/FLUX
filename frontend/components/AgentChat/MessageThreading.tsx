// components/AgentChat/MessageThreading.tsx
import React, { useState, useMemo, useCallback } from 'react';
import { AgentMessage } from '../../types/agents';

interface MessageThread {
  id: string;
  title: string;
  messages: AgentMessage[];
  agents: string[];
  timestamp: Date;
  isActive: boolean;
}

interface MessageThreadingProps {
  messages: AgentMessage[];
  onThreadSelect?: (threadId: string) => void;
  onMessageSearch?: (query: string) => void;
}

export const MessageThreading: React.FC<MessageThreadingProps> = ({
  messages,
  onThreadSelect,
  onMessageSearch
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedThread, setSelectedThread] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const generateThreadTitle = useCallback((messages: AgentMessage[]): string => {
    if (messages.length === 0) return 'Empty Thread';
    
    const firstMessage = messages[0].message.toLowerCase();
    
    // Extract key topics from first message
    if (firstMessage.includes('feature') || firstMessage.includes('requirement')) {
      return '🆕 Feature Planning';
    } else if (firstMessage.includes('bug') || firstMessage.includes('fix') || firstMessage.includes('error')) {
      return '🐛 Bug Investigation';
    } else if (firstMessage.includes('deploy') || firstMessage.includes('release')) {
      return '🚀 Deployment Discussion';
    } else if (firstMessage.includes('test') || firstMessage.includes('qa')) {
      return '🧪 Testing & QA';
    } else if (firstMessage.includes('architecture') || firstMessage.includes('design')) {
      return '🏗️ Architecture Review';
    } else if (firstMessage.includes('performance') || firstMessage.includes('optimize')) {
      return '⚡ Performance Analysis';
    } else {
      // Use first few words as title
      const words = firstMessage.split(' ').slice(0, 4);
      return `💬 ${words.join(' ')}...`;
    }
  }, []);

  // Group messages into threads based on time gaps and topic changes
  const messageThreads = useMemo(() => {
    if (messages.length === 0) return [];

    const threads: MessageThread[] = [];
    let currentThread: AgentMessage[] = [];
    let currentAgents: Set<string> = new Set();
    
    const THREAD_BREAK_TIME = 5 * 60 * 1000; // 5 minutes

    messages.forEach((message, index) => {
      const prevMessage = messages[index - 1];
      
      // Start new thread if:
      // 1. First message
      // 2. Large time gap
      // 3. Major topic change (detected by keywords)
      const shouldStartNewThread = 
        index === 0 ||
        (prevMessage && 
          (new Date(message.timestamp).getTime() - new Date(prevMessage.timestamp).getTime() > THREAD_BREAK_TIME));

      if (shouldStartNewThread && currentThread.length > 0) {
        // Save current thread
        threads.push({
          id: `thread-${threads.length}`,
          title: generateThreadTitle(currentThread),
          messages: [...currentThread],
          agents: Array.from(currentAgents),
          timestamp: new Date(currentThread[0].timestamp),
          isActive: threads.length === 0
        });
        
        currentThread = [];
        currentAgents.clear();
      }

      currentThread.push(message);
      currentAgents.add(message.agent);
    });

    // Add final thread
    if (currentThread.length > 0) {
      threads.push({
        id: `thread-${threads.length}`,
        title: generateThreadTitle(currentThread),
        messages: [...currentThread],
        agents: Array.from(currentAgents),
        timestamp: new Date(currentThread[0].timestamp),
        isActive: true
      });
    }

    return threads.reverse(); // Most recent first
  }, [messages, generateThreadTitle]);

  const filteredThreads = useMemo(() => {
    if (!searchQuery) return messageThreads;
    
    return messageThreads.filter(thread =>
      thread.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      thread.messages.some(msg => 
        msg.message.toLowerCase().includes(searchQuery.toLowerCase()) ||
        msg.agent.toLowerCase().includes(searchQuery.toLowerCase())
      )
    );
  }, [messageThreads, searchQuery]);

  const getAgentColor = (agent: string): string => {
    const colors: { [key: string]: string } = {
      'requirements_analyst': 'bg-gradient-to-r from-purple-500/10 to-purple-600/10 text-purple-400 border border-purple-500/20',
      'software_architect': 'bg-gradient-to-r from-blue-500/10 to-cyan-500/10 text-cyan-400 border border-blue-500/20',
      'developer': 'bg-gradient-to-r from-green-500/10 to-emerald-500/10 text-emerald-400 border border-green-500/20',
      'qa_tester': 'bg-gradient-to-r from-yellow-500/10 to-amber-500/10 text-amber-400 border border-yellow-500/20',
      'devops_engineer': 'bg-gradient-to-r from-red-500/10 to-rose-500/10 text-rose-400 border border-red-500/20',
      'project_manager': 'bg-gradient-to-r from-indigo-500/10 to-purple-500/10 text-indigo-400 border border-indigo-500/20',
      'security_expert': 'bg-gradient-to-r from-slate-500/10 to-gray-500/10 text-slate-400 border border-slate-500/20'
    };
    return colors[agent] || 'bg-gradient-to-r from-gray-500/10 to-slate-500/10 text-slate-400 border border-gray-500/20';
  };

  const formatTimeAgo = (date: Date): string => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  };

  return (
    <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-2xl shadow-2xl border border-slate-700/50 overflow-hidden backdrop-blur-xl">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-800/80 via-slate-700/80 to-slate-800/80 backdrop-blur-sm border-b border-slate-600/30 p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-br from-cyan-400/20 to-blue-500/20 rounded-xl flex items-center justify-center border border-cyan-400/30 shadow-lg">
              <svg className="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <h3 className="font-bold text-xl text-white bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
                Conversation History
              </h3>
              <p className="text-sm text-slate-400 font-medium">
                {messageThreads.length} threads • {messages.length} messages
              </p>
            </div>
          </div>
          <button 
            onClick={() => setIsExpanded(!isExpanded)}
            className="w-10 h-10 rounded-xl bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 hover:text-white transition-all duration-200 flex items-center justify-center border border-slate-600/30 hover:border-slate-500/50 shadow-lg hover:shadow-xl"
          >
            <svg 
              className={`w-5 h-5 transition-transform duration-200 ${isExpanded ? 'rotate-180' : ''}`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
      </div>

      {/* Search Bar */}
      {isExpanded && (
        <div className="p-6 border-b border-slate-700/30">
          <div className="relative">
            <input
              type="text"
              placeholder="Search conversations..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                onMessageSearch?.(e.target.value);
              }}
              className="w-full pl-12 pr-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white placeholder-slate-400 focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 transition-all duration-200 backdrop-blur-sm shadow-inner"
            />
            <div className="absolute left-4 top-1/2 transform -translate-y-1/2">
              <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>
      )}

      {/* Thread List */}
      {isExpanded && (
        <div className="max-h-96 overflow-y-auto scrollbar-thin scrollbar-track-slate-800 scrollbar-thumb-slate-600">
          {filteredThreads.length === 0 ? (
            <div className="p-8 text-center">
              <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-slate-700/50 to-slate-800/50 rounded-2xl flex items-center justify-center border border-slate-600/30">
                <svg className="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <p className="text-slate-400 font-medium">
                {searchQuery ? 'No matching conversations found' : 'No conversations yet'}
              </p>
              <p className="text-slate-500 text-sm mt-1">
                {searchQuery ? 'Try adjusting your search terms' : 'Start a conversation to see it here'}
              </p>
            </div>
          ) : (
            <div className="divide-y divide-slate-700/30">
              {filteredThreads.map((thread) => (
                <div
                  key={thread.id}
                  onClick={() => {
                    setSelectedThread(thread.id);
                    onThreadSelect?.(thread.id);
                  }}
                  className={`p-6 cursor-pointer transition-all duration-200 hover:bg-slate-800/50 group ${
                    selectedThread === thread.id 
                      ? 'bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border-r-4 border-cyan-400 shadow-lg' 
                      : ''
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <h4 className="font-semibold text-white text-sm group-hover:text-cyan-300 transition-colors duration-200">
                      {thread.title}
                    </h4>
                    <div className="flex items-center space-x-3">
                      <span className="text-xs text-slate-400 font-medium bg-slate-800/50 px-2 py-1 rounded-lg">
                        {formatTimeAgo(thread.timestamp)}
                      </span>
                      {thread.isActive && (
                        <div className="relative">
                          <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-emerald-400 rounded-full animate-pulse shadow-lg"></div>
                          <div className="absolute inset-0 w-3 h-3 bg-green-400 rounded-full animate-ping opacity-30"></div>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex flex-wrap gap-2">
                      {thread.agents.slice(0, 3).map((agent) => (
                        <span
                          key={agent}
                          className={`px-3 py-1 text-xs rounded-lg font-medium ${getAgentColor(agent)} backdrop-blur-sm`}
                        >
                          {agent.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                      ))}
                      {thread.agents.length > 3 && (
                        <span className="px-3 py-1 text-xs bg-gradient-to-r from-slate-600/50 to-slate-700/50 text-slate-300 rounded-lg font-medium border border-slate-600/30">
                          +{thread.agents.length - 3}
                        </span>
                      )}
                    </div>
                    
                    <div className="flex items-center space-x-2 bg-slate-800/50 px-3 py-1 rounded-lg border border-slate-600/30">
                      <span className="text-xs text-slate-300 font-medium">{thread.messages.length}</span>
                      <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                      </svg>
                    </div>
                  </div>
                  
                  {/* Preview of last message */}
                  <div className="bg-slate-800/30 rounded-lg p-3 border border-slate-700/30">
                    <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed">
                      {thread.messages[thread.messages.length - 1]?.message.substring(0, 120)}...
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Quick Stats */}
      {!isExpanded && (
        <div className="p-6">
          <div className="grid grid-cols-3 gap-6">
            <div className="text-center group">
              <div className="bg-gradient-to-br from-cyan-500/20 to-blue-500/20 rounded-2xl p-4 mb-3 border border-cyan-500/30 group-hover:border-cyan-400/50 transition-all duration-200 shadow-lg">
                <div className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
                  {messageThreads.length}
                </div>
              </div>
              <div className="text-xs text-slate-400 font-medium uppercase tracking-wider">Threads</div>
            </div>
            <div className="text-center group">
              <div className="bg-gradient-to-br from-emerald-500/20 to-green-500/20 rounded-2xl p-4 mb-3 border border-emerald-500/30 group-hover:border-emerald-400/50 transition-all duration-200 shadow-lg">
                <div className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-green-400 bg-clip-text text-transparent">
                  {messages.length}
                </div>
              </div>
              <div className="text-xs text-slate-400 font-medium uppercase tracking-wider">Messages</div>
            </div>
            <div className="text-center group">
              <div className="bg-gradient-to-br from-purple-500/20 to-indigo-500/20 rounded-2xl p-4 mb-3 border border-purple-500/30 group-hover:border-purple-400/50 transition-all duration-200 shadow-lg">
                <div className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-indigo-400 bg-clip-text text-transparent">
                  {new Set(messages.map(m => m.agent)).size}
                </div>
              </div>
              <div className="text-xs text-slate-400 font-medium uppercase tracking-wider">Participants</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};