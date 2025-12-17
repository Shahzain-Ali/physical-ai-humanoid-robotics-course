import React, { useState, useEffect } from 'react';
import ChatWidget from '../components/ChatWidget';

// Root component that wraps the entire Docusaurus app
// This allows us to inject the ChatWidget globally across all pages
export default function Root({ children }) {
  const [isClient, setIsClient] = useState(false);

  // This ensures the ChatWidget only renders on the client side
  // to avoid SSR issues with browser-specific APIs
  useEffect(() => {
    setIsClient(true);
  }, []);

  return (
    <>
      {children}
      {isClient && <ChatWidget />}
    </>
  );
}