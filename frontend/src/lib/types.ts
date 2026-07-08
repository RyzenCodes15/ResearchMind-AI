export interface DocumentChunkResponse {
  chunk_index: number;
  page_start: number | null;
  page_end: number | null;
  content_length: number;
}

export interface DocumentResponse {
  id: number;
  original_filename: string;
  stored_filename: string;
  storage_path: string;
  file_hash: string;
  file_size_bytes: number;
  page_count: number | null;
  chunk_count: number;
  embedding_model: string | null;
  chunk_size: number;
  chunk_overlap: number;
  status: string;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface DocumentIngestionResponse {
  duplicate: boolean;
  document: DocumentResponse;
  chunks: DocumentChunkResponse[];
  message: string;
}

export interface ChatCitation {
  chunk_id: number;
  document_id: number;
  document_name: string;
  chunk_index: number;
  page_start: number | null;
  page_end: number | null;
  similarity_score: number;
  content: string;
}

export interface ChatResponse {
  question: string;
  answer: string;
  insufficient_context: boolean;
  model_name: string;
  retrieved_chunks: ChatCitation[];
  created_at: string;
}

export interface ChatRequest {
  question: string;
  top_k?: number;
}

// Frontend specific types
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: ChatCitation[];
  isError?: boolean;
}
