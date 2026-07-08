'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { ChatCitation, DocumentResponse, Message } from './types';
import { sendMessage, uploadDocument } from './api';

interface ChatContextType {
  documents: DocumentResponse[];
  messages: Message[];
  isLoading: boolean;
  isUploading: boolean;
  uploadError: string | null;
  selectedCitations: ChatCitation[] | null;
  handleUpload: (file: File) => Promise<void>;
  handleSendMessage: (text: string) => Promise<void>;
  setSelectedCitations: (citations: ChatCitation[] | null) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export function ChatProvider({ children }: { children: ReactNode }) {
  const [documents, setDocuments] = useState<DocumentResponse[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [selectedCitations, setSelectedCitations] = useState<ChatCitation[] | null>(null);

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setUploadError(null);
    try {
      const response = await uploadDocument(file);
      if (!response.duplicate) {
        setDocuments((prev) => [...prev, response.document]);
      }
    } catch (err: any) {
      setUploadError(err.message || 'An error occurred during upload.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setSelectedCitations(null); // Clear previous citations while loading

    try {
      const response = await sendMessage(text);
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        citations: response.retrieved_chunks,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setSelectedCitations(response.retrieved_chunks);
    } catch (err: any) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Error: ${err.message || 'Failed to fetch response.'}`,
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChatContext.Provider
      value={{
        documents,
        messages,
        isLoading,
        isUploading,
        uploadError,
        selectedCitations,
        handleUpload,
        handleSendMessage,
        setSelectedCitations,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}
