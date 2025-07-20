import { useState } from 'react';
import { apiClient, ChatMessage, ChatResponse } from '@/lib/api';

export interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  source?: string;
  timestamp: Date;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'assistant',
      content: "Welcome! I'm your Knowledge Assistant. I can help answer questions about your documents. Try asking me something about your uploaded files.",
      timestamp: new Date(),
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    setError(null);

    try {
      // Prepare conversation history for API
      const conversationHistory = messages.map(msg => ({
        type: msg.type,
        content: msg.content,
        source: msg.source,
      }));

      const chatMessage: ChatMessage = {
        content: content.trim(),
        conversation_history: conversationHistory,
      };

      const response: ChatResponse = await apiClient.sendMessage(chatMessage);

      // Add assistant response
      const assistantMessage: Message = {
        id: Date.now() + 1,
        type: 'assistant',
        content: response.content,
        source: response.source,
        timestamp: new Date(response.timestamp),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);
      
      // Add error message
      const errorMsg: Message = {
        id: Date.now() + 1,
        type: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}. Please try again.`,
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        type: 'assistant',
        content: "Welcome! I'm your Knowledge Assistant. I can help answer questions about your documents. Try asking me something about your uploaded files.",
        timestamp: new Date(),
      },
    ]);
    setError(null);
  };

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearChat,
  };
}
