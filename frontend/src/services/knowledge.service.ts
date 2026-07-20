import { apiClient } from "@/services/apiClient";
import type { 
  DocumentUploadResponse, 
  QueryRequest, 
  QueryResponse,
  KnowledgeDocumentListResponse,
  DeleteDocumentResponse 
} from "@/types/api";

export const knowledgeService = {
  ingest(file: File, collectionName = "enterprise_docs") {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("collection_name", collectionName);
    return apiClient
      .post<DocumentUploadResponse>("/knowledge/ingest", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((r) => r.data);
  },

  query(payload: QueryRequest) {
    return apiClient.post<QueryResponse>("/knowledge/query", payload).then((r) => r.data);
  },

  getDocuments() {
    return apiClient.get<KnowledgeDocumentListResponse>("/knowledge/documents").then((r) => r.data);
  },

  deleteDocument(documentId: string) {
    return apiClient.delete<DeleteDocumentResponse>(`/knowledge/documents/${documentId}`).then((r) => r.data);
  }
};