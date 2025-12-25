import React, { useState, useEffect, useRef } from 'react';
import ChatWidget from '../components/ChatWidget';
import TextSelectionPopup from '../components/TextSelectionPopup';

// Root component that wraps the entire Docusaurus app
// This allows us to inject the ChatWidget and TextSelectionPopup globally across all pages
export default function Root({ children }) {
  const [isClient, setIsClient] = useState(false);
  const chatWidgetRef = useRef(null);

  // This ensures the ChatWidget only renders on the client side
  // to avoid SSR issues with browser-specific APIs
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Handle "Ask AI" click from text selection popup
  const handleAskAI = (selectedText) => {
    if (chatWidgetRef.current && chatWidgetRef.current.attachContext) {
      chatWidgetRef.current.attachContext(selectedText);
    }
  };

  return (
    <>
      {children}
      {isClient && (
        <>
          <TextSelectionPopup onAskAI={handleAskAI} />
          <ChatWidget ref={chatWidgetRef} />
        </>
      )}
    </>
  );
}