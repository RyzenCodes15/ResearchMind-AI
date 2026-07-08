'use client';

import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { ChatCitation, DocumentResponse, Message } from './types';
import { sendMessage, uploadDocument, fetchDocuments, deleteDocument } from './api';

interface ChatContextType {
  documents: DocumentResponse[];
  messages: Message[];
  isLoading: boolean;
  isUploading: boolean;
  uploadError: string | null;
  uploadSuccess: string | null;
  deleteError: string | null;
  deleteSuccess: string | null;
  isDeleting: number | null;
  selectedCitations: ChatCitation[] | null;
  handleUpload: (file: File) => Promise<void>;
  handleDeleteDocument: (id: number) => Promise<void>;
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
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);
  const [deleteSuccess, setDeleteSuccess] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState<number | null>(null);
  const [selectedCitations, setSelectedCitations] = useState<ChatCitation[] | null>(null);

  useEffect(() => {
    const loadDocuments = async () => {
      try {
        const docs = await fetchDocuments();
        setDocuments(docs);
      } catch (err) {
        console.error('Failed to load documents on mount:', err);
      }
    };
    loadDocuments();
  }, []);

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setUploadError(null);
    setUploadSuccess(null);
    try {
      const response = await uploadDocument(file);
      setDocuments((prev) => {
        if (!prev.some(d => d.id === response.document.id)) {
          return [...prev, response.document];
        }
        return prev;
      });
      setUploadSuccess(`Successfully uploaded ${file.name}`);
      setTimeout(() => setUploadSuccess(null), 3000);
    } catch (err: any) {
      setUploadError(err.message || 'An error occurred during upload.');
      setTimeout(() => setUploadError(null), 5000);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDeleteDocument = async (id: number) => {
    setIsDeleting(id);
    setDeleteError(null);
    setDeleteSuccess(null);
    try {
      await deleteDocument(id);
      setDocuments((prev) => {
        const next = prev.filter((d) => d.id !== id);
        if (next.length === 0) {
          setMessages([]);
          setSelectedCitations(null);
        }
        return next;
      });
      setDeleteSuccess('Document deleted successfully');
      setTimeout(() => setDeleteSuccess(null), 3000);
    } catch (err: any) {
      setDeleteError(err.message || 'An error occurred during deletion.');
      setTimeout(() => setDeleteError(null), 5000);
    } finally {
      setIsDeleting(null);
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
      const documentIds = documents.map(d => d.id);
      const response = await sendMessage(text, documentIds);
      
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
        uploadSuccess,
        deleteError,
        deleteSuccess,
        isDeleting,
        selectedCitations,
        handleUpload,
        handleDeleteDocument,
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
