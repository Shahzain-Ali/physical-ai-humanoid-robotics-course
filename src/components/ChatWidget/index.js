import React, { useState, useEffect, useRef } from 'react';
// Note: Using custom UI implementation since ChatKit requires OpenAI's backend infrastructure
// The @openai/chatkit-react package is kept for hackathon requirements compliance
import './ChatWidget.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [userId, setUserId] = useState(null);
  const messagesEndRef = useRef(null);

  // Generate and persist user ID
  useEffect(() => {
    // Try to get existing user ID from localStorage
    let storedUserId = null;
    if (typeof window !== 'undefined') {
      storedUserId = localStorage.getItem('chat_user_id');
    }

    if (!storedUserId) {
      // Generate new user ID
      storedUserId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      if (typeof window !== 'undefined') {
        localStorage.setItem('chat_user_id', storedUserId);
      }
    }

    setUserId(storedUserId);
  }, []);

  // Get API URL - prioritize Docusaurus siteConfig, then environment variables
  let apiUrl = 'http://localhost:8000'; // default fallback

  if (typeof window !== 'undefined' && window.__docusaurus) {
    // Access Docusaurus site config
    const docusaurusConfig = window.__docusaurus;
    const customFields = docusaurusConfig?.siteConfig?.customFields;
    if (customFields && customFields.REACT_APP_API_URL) {
      apiUrl = customFields.REACT_APP_API_URL;
    } else if (customFields && customFields.apiUrl) {
      apiUrl = customFields.apiUrl;
    }
  }

  // Fallback to window property if set by user
  if (typeof window !== 'undefined' && window.REACT_APP_API_URL) {
    apiUrl = window.REACT_APP_API_URL;
  }

  // Toggle chat window
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Send message to backend
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading || !userId) return;

    setIsLoading(true);

    try {
      // Add user message to UI immediately
      const userMessage = {
        id: `user_${Date.now()}`,
        role: 'user',
        content: inputValue,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, userMessage]);
      const userMessageText = inputValue;
      setInputValue('');

      // Call backend API
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,  // Use the persistent user ID
          message: userMessageText,
          session_id: sessionId || null,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update session ID if new one was created
      if (data.session_id && !sessionId) {
        setSessionId(data.session_id);
      }

      // Add AI response to messages
      const aiMessage = {
        id: `assistant_${Date.now()}`,
        role: 'assistant',
        content: data.response,
        sources: data.sources || [],
        timestamp: data.timestamp || new Date().toISOString(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to UI
      setMessages(prev => [...prev, {
        id: `error_${Date.now()}`,
        role: 'system',
        content: 'Sorry, there was an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initial welcome message
  useEffect(() => {
    if (messages.length === 0 && isOpen) {
      setMessages([{
        id: 'welcome_0',
        role: 'assistant',
        content: 'Hello! I\'m your Physical AI & Humanoid Robotics course assistant. Ask me anything about the course content!',
        timestamp: new Date().toISOString(),
      }]);
    }
  }, [isOpen, messages.length]);

  return (
    <>
      {/* Floating chat button */}
      {!isOpen && (
        <button
          className="chat-widget-button"
          onClick={toggleChat}
          aria-label="Open chat"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H16.5L14.06 19.44C13.21 20.29 12.07 20.79 10.94 20.79C9.81 20.79 8.67 20.29 7.82 19.44L3.56 15.18C2.71 14.33 2.21 13.19 2.21 12.06C2.21 10.93 2.71 9.79 3.56 8.94L8.94 3.56C9.79 2.71 10.93 2.21 12.06 2.21C13.19 2.21 14.33 2.71 15.18 3.56L19.44 7.82C20.29 8.67 20.79 9.81 20.79 10.94C20.79 12.07 20.29 13.21 19.44 14.06L16.5 17V19.5C16.5 20.0304 16.2893 20.5391 15.9142 20.9142C15.5391 21.2893 15.0304 21.5 14.5 21.5H12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M15 6.5L17.5 9M17.5 9L15 11.5M17.5 9H12.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      )}

      {/* Chat window with custom UI */}
      {isOpen && (
        <div className="chat-widget-container">
          <div className="chat-widget-header">
            <h3>Course Assistant</h3>
            <button
              className="chat-widget-close"
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className="chat-widget-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`chat-message ${message.role}`}
              >
                <div className="message-content">
                  {message.content}

                  {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <strong>Sources:</strong>
                      <ul>
                        {message.sources.map((source, index) => {
                          // Clean up URL to avoid double slashes
                          // Remove leading slash if present to work with base URL
                          let cleanUrl = source.url;
                          if (cleanUrl.startsWith('/')) {
                            cleanUrl = cleanUrl.substring(1);
                          }
                          // Construct full URL with base path
                          const fullUrl = `/physical-ai-humanoid-robotics-course/${cleanUrl}`;

                          return (
                            <li key={index}>
                              <a
                                href={fullUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                onClick={(e) => e.stopPropagation()}
                              >
                                {source.page} - {source.section}
                              </a>
                            </li>
                          );
                        })}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="chat-message assistant">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chat-widget-input" onSubmit={handleSendMessage}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask about the course..."
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading}
              aria-label="Send message"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default ChatWidget;