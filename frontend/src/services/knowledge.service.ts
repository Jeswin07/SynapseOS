import { apiClient } from "@/services/apiClient";
import type { DocumentUploadResponse, QueryRequest, QueryResponse } from "@/types/api";

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
  // NOTE: no GET /knowledge/documents (list) endpoint exists on the backend,
  // so the Document Library table can only reflect documents ingested in the
  // current session. TODO: backend — add a listing endpoint.
};
