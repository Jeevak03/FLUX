// components/AgentChat/MessageThreading.tsx
import React, { useState, useMemo } from 'react';
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
  }, [messages]);

  const generateThreadTitle = (messages: AgentMessage[]): string => {
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
  };

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
      'requirements_analyst': 'bg-purple-100 text-purple-800',
      'software_architect': 'bg-blue-100 text-blue-800',
      'developer': 'bg-green-100 text-green-800',
      'qa_tester': 'bg-yellow-100 text-yellow-800',
      'devops_engineer': 'bg-red-100 text-red-800',
      'project_manager': 'bg-indigo-100 text-indigo-800',
      'security_expert': 'bg-gray-100 text-gray-800'
    };
    return colors[agent] || 'bg-gray-100 text-gray-800';
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
    <div className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-4">
        <div className="flex items-center justify-between text-white">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
              💬
            </div>
            <div>
              <h3 className="font-semibold text-lg">Conversation History</h3>
              <p className="text-sm text-white/80">{messageThreads.length} threads • {messages.length} messages</p>
            </div>
          </div>
          <button 
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-white/80 hover:text-white transition-colors"
          >
            {isExpanded ? '⬆️' : '⬇️'}
          </button>
        </div>
      </div>

      {/* Search Bar */}
      {isExpanded && (
        <div className="p-4 border-b border-gray-200">
          <div className="relative">
            <input
              type="text"
              placeholder="Search conversations..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                onMessageSearch?.(e.target.value);
              }}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <div className="absolute left-3 top-2.5 text-gray-400">
              🔍
            </div>
          </div>
        </div>
      )}

      {/* Thread List */}
      {isExpanded && (
        <div className="max-h-96 overflow-y-auto">
          {filteredThreads.length === 0 ? (
            <div className="p-6 text-center text-gray-500">
              {searchQuery ? 'No matching conversations found' : 'No conversations yet'}
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {filteredThreads.map((thread) => (
                <div
                  key={thread.id}
                  onClick={() => {
                    setSelectedThread(thread.id);
                    onThreadSelect?.(thread.id);
                  }}
                  className={`p-4 cursor-pointer transition-colors hover:bg-gray-50 ${
                    selectedThread === thread.id ? 'bg-blue-50 border-r-4 border-blue-500' : ''
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-medium text-gray-900 text-sm">{thread.title}</h4>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-gray-500">{formatTimeAgo(thread.timestamp)}</span>
                      {thread.isActive && (
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex flex-wrap gap-1">
                      {thread.agents.slice(0, 3).map((agent) => (
                        <span
                          key={agent}
                          className={`px-2 py-0.5 text-xs rounded-full ${getAgentColor(agent)}`}
                        >
                          {agent.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </span>
                      ))}
                      {thread.agents.length > 3 && (
                        <span className="px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded-full">
                          +{thread.agents.length - 3}
                        </span>
                      )}
                    </div>
                    
                    <div className="flex items-center space-x-1 text-xs text-gray-500">
                      <span>{thread.messages.length}</span>
                      <span>💬</span>
                    </div>
                  </div>
                  
                  {/* Preview of last message */}
                  <p className="text-xs text-gray-600 mt-2 line-clamp-2">
                    {thread.messages[thread.messages.length - 1]?.message.substring(0, 100)}...
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Quick Stats */}
      {!isExpanded && (
        <div className="p-4">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-lg font-semibold text-blue-600">{messageThreads.length}</div>
              <div className="text-xs text-gray-500">Threads</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-green-600">{messages.length}</div>
              <div className="text-xs text-gray-500">Messages</div>
            </div>
            <div>
              <div className="text-lg font-semibold text-purple-600">
                {new Set(messages.map(m => m.agent)).size}
              </div>
              <div className="text-xs text-gray-500">Participants</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};