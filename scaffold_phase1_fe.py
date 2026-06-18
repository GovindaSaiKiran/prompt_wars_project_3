import os

def write_file(path, content):
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

write_file("frontend/src/features/ai-coach/hooks/useCoachChat.ts", """// purpose: Manage SSE and fallback for Coach | enforces: Quality-first
import { useState, useCallback } from 'react';

export const useCoachChat = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = useCallback(async (text: string) => {
    // 1. Fire GA4 Event
    console.log('Fired GA4 Event: ai_coach_interaction');
    
    // 2. Add user message
    setMessages(prev => [...prev, { role: 'user', content: text, id: Date.now().toString() }]);
    
    setIsStreaming(true);
    
    try {
      const response = await fetch('/api/v1/coach/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      
      if (!response.body) throw new Error('No readable stream');
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      
      setMessages(prev => [...prev, { role: 'model', content: '', id: (Date.now() + 1).toString() }]);
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        try {
          const data = JSON.parse(chunk);
          setMessages(prev => {
            const newMessages = [...prev];
            newMessages[newMessages.length - 1].content += data.text;
            return newMessages;
          });
        } catch (e) {
          // ignore parse error on incomplete chunks for dummy implementation
        }
      }
    } catch (error) {
      console.error('Streaming failed, fallback to normal fetch', error);
      // Fallback
      const fallbackRes = await fetch('/api/v1/coach/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await fallbackRes.json();
      setMessages(prev => [...prev, { role: 'model', content: data.text, id: (Date.now() + 1).toString() }]);
    } finally {
      setIsStreaming(false);
      // Persist to firestore (dummy)
      console.log('Saved to Firestore users/UID/ai_conversations');
    }
  }, []);

  return { messages, sendMessage, isStreaming };
};
""")

write_file("frontend/src/features/ai-coach/CoachChat.tsx", """// purpose: AI Coach UI | enforces: Accessibility-first
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
""")

write_file("frontend/src/features/ai-coach/ConversationHistory.tsx", """// purpose: Manage AI Conversations | enforces: Quality-first
import React from 'react';

export const ConversationHistory: React.FC = () => {
  return (
    <div className="conversation-history">
      <h2>Your Conversations</h2>
      <ul>
        <li>
          <span>Commute Advice (12:00 PM)</span>
          <button>Resume</button>
          <button>Export</button>
          <button className="delete-btn">Delete</button>
        </li>
      </ul>
    </div>
  );
};
""")

print("Phase 1 FE scaffolding completed.")
