import { ChatRequest, ChatResponse, DocumentIngestionResponse, DocumentResponse } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export async function uploadDocument(file: File): Promise<DocumentIngestionResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/documents/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Upload failed: ${response.status} ${errorText}`);
  }

  return response.json();
}

export async function fetchDocuments(): Promise<DocumentResponse[]> {
  const response = await fetch(`${API_BASE_URL}/documents`);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to fetch documents: ${response.status} ${errorText}`);
  }

  return response.json();
}

export async function deleteDocument(id: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/documents/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to delete document: ${response.status} ${errorText}`);
  }
}

export async function sendMessage(question: string, documentIds: number[], topK?: number): Promise<ChatResponse> {
  const payload: ChatRequest = { question, document_ids: documentIds };
  if (topK !== undefined) {
    payload.top_k = topK;
  }

  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Chat request failed: ${response.status} ${errorText}`);
  }

  return response.json();
}
