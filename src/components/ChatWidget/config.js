/**
 * ChatWidget configuration for the RAG Chatbot frontend.
 *
 * This module provides configuration options for the ChatWidget component
 * including API endpoints, default settings, and UI customization options.
 */

// Get the API URL from environment or Docusaurus config
const getApiUrl = () => {
  // First, try to get from Docusaurus customFields
  if (typeof window !== 'undefined' && window.__docusaurus) {
    const docusaurusConfig = window.__docusaurus.siteConfig;
    if (docusaurusConfig && docusaurusConfig.customFields && docusaurusConfig.customFields.apiUrl) {
      return docusaurusConfig.customFields.apiUrl;
    }
  }

  // Fallback to environment variable
  return process.env.REACT_APP_API_URL || 'http://localhost:8000';
};

// ChatWidget configuration object
const chatWidgetConfig = {
  // API configuration
  apiUrl: getApiUrl(),
  endpoints: {
    chat: '/api/chat',
    chatStream: '/api/chat/stream',
    history: '/api/history',
    health: '/health'
  },

  // UI configuration
  ui: {
    buttonPosition: {
      bottom: '30px',
      right: '30px'
    },
    containerSize: {
      width: '400px',
      height: '600px'
    },
    colors: {
      primary: '#10a37f',      // Green color matching OpenAI brand
      secondary: '#f3f4f6',    // Light gray for backgrounds
      userMessage: '#10a37f',  // Green for user messages
      assistantMessage: '#ffffff', // White for assistant messages
      systemMessage: '#fef3c7' // Yellow for system messages
    },
    borderRadius: '12px',
    boxShadow: '0 8px 30px rgba(0, 0, 0, 0.12)',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
  },

  // Behavior configuration
  behavior: {
    // Animation settings
    animations: {
      messageFadeInDuration: '0.2s',
      buttonHoverScale: '1.05'
    },

    // Message settings
    messages: {
      maxDisplayLength: 1000, // Maximum characters to display before truncating
      autoScroll: true,        // Automatically scroll to bottom when new messages arrive
      showTimestamps: false,   // Whether to show timestamps for messages
      typingIndicator: true    // Show typing indicator when waiting for response
    },

    // Session settings
    session: {
      autoRestore: true,       // Automatically restore last session when widget opens
      autoSave: true,          // Automatically save session when widget closes
      timeout: 30 * 60 * 1000  // Session timeout in milliseconds (30 minutes)
    }
  },

  // Validation and limits
  validation: {
    maxMessageLength: 2000,    // Maximum length of user messages
    maxHistoryLength: 50,      // Maximum number of messages to keep in history
    rateLimit: {
      maxRequests: 10,         // Maximum requests per minute per user
      windowMs: 60 * 1000      // Time window in milliseconds
    }
  },

  // Error handling
  errorHandling: {
    retryAttempts: 3,          // Number of retry attempts for failed requests
    retryDelay: 1000,          // Delay between retries in milliseconds
    showErrorDetails: false     // Whether to show detailed error messages to users
  },

  // Accessibility
  accessibility: {
    keyboardNavigation: true,  // Enable keyboard navigation
    screenReaderSupport: true, // Support for screen readers
    highContrastMode: false    // High contrast mode for better accessibility
  }
};

// Export the configuration
export default chatWidgetConfig;

// Export individual configuration sections for selective imports
export const apiConfig = chatWidgetConfig.endpoints;
export const uiConfig = chatWidgetConfig.ui;
export const behaviorConfig = chatWidgetConfig.behavior;
export const validationConfig = chatWidgetConfig.validation;
export const errorConfig = chatWidgetConfig.errorHandling;
export const accessibilityConfig = chatWidgetConfig.accessibility;