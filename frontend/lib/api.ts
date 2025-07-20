const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Document {
  id: string;
  name: string;
  size: number;
  modified: string;
  type: string;
}

export interface ChatMessage {
  content: string;
  conversation_history?: Array<{
    type: 'user' | 'assistant';
    content: string;
    source?: string;
  }>;
}

export interface ChatResponse {
  content: string;
  source?: string;
  timestamp: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // Document management
  async getDocuments(): Promise<Document[]> {
    return this.request<Document[]>('/api/documents');
  }

  async uploadDocument(file: File): Promise<{ message: string; filename: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/api/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Upload failed: ${response.status}`);
    }

    return response.json();
  }

  async deleteDocument(documentId: string): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/api/documents/${documentId}`, {
      method: 'DELETE',
    });
  }

  // Chat functionality
  async sendMessage(message: ChatMessage): Promise<ChatResponse> {
    return this.request<ChatResponse>('/api/chat', {
      method: 'POST',
      body: JSON.stringify(message),
    });
  }

  // Health check
  async healthCheck(): Promise<{ status: string; documents_count: number; timestamp: string }> {
    return this.request<{ status: string; documents_count: number; timestamp: string }>('/api/health');
  }
}

export const apiClient = new ApiClient();
