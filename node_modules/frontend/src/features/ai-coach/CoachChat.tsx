// purpose: AI Coach UI | enforces: Accessibility-first
import React, { useState } from 'react';
import { useCoachChat } from './hooks/useCoachChat';

export const CoachChat: React.FC = () => {
  const { messages, sendMessage, isStreaming } = useCoachChat();
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      sendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="coach-chat-container" role="region" aria-label="AI Sustainability Coach">
      <div className="messages" aria-live="polite">
        {messages.map(m => (
          <div key={m.id} className={`message ${m.role}`}>
            <strong>{m.role === 'user' ? 'You' : 'EcoSphere Coach'}:</strong> {m.content}
          </div>
        ))}
        {isStreaming && <div className="streaming-indicator">Coach is typing...</div>}
      </div>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input 
          type="text" 
          value={input} 
          onChange={e => setInput(e.target.value)} 
          placeholder="Ask how to reduce your carbon footprint..."
          aria-label="Message to EcoSphere Coach"
        />
        <button type="submit" disabled={isStreaming || !input.trim()}>Send</button>
      </form>
    </div>
  );
};
