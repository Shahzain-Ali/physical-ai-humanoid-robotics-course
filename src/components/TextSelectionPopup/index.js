import React, { useState, useEffect } from 'react';
import './TextSelectionPopup.css';

const TextSelectionPopup = ({ onAskAI }) => {
  const [selectedText, setSelectedText] = useState('');
  const [popupPosition, setPopupPosition] = useState({ top: 0, left: 0 });
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleSelectionChange = () => {
      // Small delay to ensure selection is complete
      setTimeout(() => {
        const selection = window.getSelection();
        const text = selection.toString().trim();

        if (text.length > 10) { // Minimum 10 chars to show popup
          try {
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();

            // Position popup below selection with scroll offset
            setPopupPosition({
              top: rect.bottom + window.scrollY + 8,
              left: rect.left + window.scrollX
            });

            setSelectedText(text);
            setIsVisible(true);
          } catch (e) {
            // Handle edge case where range is not available
            setIsVisible(false);
          }
        } else {
          setIsVisible(false);
          setSelectedText('');
        }
      }, 10);
    };

    // Listen to both events for better coverage
    document.addEventListener('selectionchange', handleSelectionChange);
    document.addEventListener('mouseup', handleSelectionChange);

    // Hide popup when clicking anywhere
    const handleClickOutside = (e) => {
      if (isVisible && !e.target.closest('.text-selection-popup')) {
        setIsVisible(false);
        setSelectedText('');
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isVisible]);

  const handleAskClick = () => {
    if (onAskAI && selectedText) {
      onAskAI(selectedText);
      setIsVisible(false);
      setSelectedText('');
      // Clear the selection
      window.getSelection().removeAllRanges();
    }
  };

  if (!isVisible) return null;

  return (
    <div
      className="text-selection-popup"
      style={{ top: `${popupPosition.top}px`, left: `${popupPosition.left}px` }}
    >
      <button
        className="ask-ai-button"
        onClick={handleAskClick}
        aria-label="Ask AI about selected text"
      >
        💬 Ask AI
      </button>
    </div>
  );
};

export default TextSelectionPopup;
