import { useState, useEffect } from 'react';
import { apiClient, Document } from '@/lib/api';

export function useDocuments() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      setError(null);
      const docs = await apiClient.getDocuments();
      setDocuments(docs);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch documents');
    } finally {
      setLoading(false);
    }
  };

  const uploadDocument = async (file: File) => {
    try {
      setError(null);
      setIsUploading(true);
      setUploadProgress(0);
      
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90));
      }, 200);
      
      const result = await apiClient.uploadDocument(file);
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      // Wait a moment to show completion
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
      }, 1000);
      
      await fetchDocuments(); // Refresh the list
      return result;
    } catch (err) {
      setIsUploading(false);
      setUploadProgress(0);
      const errorMessage = err instanceof Error ? err.message : 'Failed to upload document';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const deleteDocument = async (documentId: string) => {
    try {
      setError(null);
      await apiClient.deleteDocument(documentId);
      await fetchDocuments(); // Refresh the list
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete document';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return {
    documents,
    loading,
    error,
    isUploading,
    uploadProgress,
    uploadDocument,
    deleteDocument,
    refetch: fetchDocuments,
  };
}
