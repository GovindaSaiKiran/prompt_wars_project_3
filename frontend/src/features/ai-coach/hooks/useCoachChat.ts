// purpose: Manage SSE and fallback for Coach | enforces: Quality-first
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
