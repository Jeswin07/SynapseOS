import { apiClient } from "@/services/apiClient";
import type {
  DatasetCreateRequest,
  DatasetCreateResponse,
  DatasetFileResponse,
  DatasetResponse,
  DatasetVersionItem,
  DatasetVersionUploadResponse,
} from "@/types/api";

export const datasetService = {
  list() {
    return apiClient.get<DatasetResponse[]>("/datasets").then((r) => r.data);
  },
  get(datasetId: string) {
    return apiClient.get<DatasetResponse>(`/datasets/${datasetId}`).then((r) => r.data);
  },
  create(payload: DatasetCreateRequest) {
    return apiClient.post<DatasetCreateResponse>("/datasets", payload).then((r) => r.data);
  },
  uploadVersion(datasetId: string, files: File[]) {
    const formData = new FormData();
    files.forEach((f) => formData.append("files", f));
    return apiClient
      .post<DatasetVersionUploadResponse>(`/datasets/${datasetId}/versions`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((r) => r.data);
  },
  listVersions(datasetId: string) {
    return apiClient.get<DatasetVersionItem[]>(`/datasets/${datasetId}/versions`).then((r) => r.data);
  },
  listVersionFiles(versionId: string) {
    return apiClient.get<DatasetFileResponse[]>(`/datasets/versions/${versionId}/files`).then((r) => r.data);
  },
  downloadFileUrl(fileId: string) {
    return `/datasets/files/${fileId}/download`;
  },
  remove(datasetId: string) {
    return apiClient.delete(`/datasets/${datasetId}`).then((r) => r.data);
  },
};
