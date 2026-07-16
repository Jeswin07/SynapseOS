import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { datasetService } from "@/services/dataset.service";
import type { DatasetCreateRequest } from "@/types/api";

export const datasetKeys = {
  all: ["datasets"] as const,
  detail: (id: string) => ["datasets", id] as const,
  versions: (id: string) => ["datasets", id, "versions"] as const,
  versionFiles: (versionId: string) => ["datasets", "versions", versionId, "files"] as const,
};

export function useDatasets() {
  return useQuery({ queryKey: datasetKeys.all, queryFn: datasetService.list });
}

export function useDataset(datasetId?: string) {
  return useQuery({
    queryKey: datasetId ? datasetKeys.detail(datasetId) : ["datasets", "none"],
    queryFn: () => datasetService.get(datasetId!),
    enabled: Boolean(datasetId),
  });
}

export function useDatasetVersions(datasetId?: string) {
  return useQuery({
    queryKey: datasetId ? datasetKeys.versions(datasetId) : ["datasets", "none", "versions"],
    queryFn: () => datasetService.listVersions(datasetId!),
    enabled: Boolean(datasetId),
  });
}

export function useDatasetVersionFiles(versionId?: string) {
  return useQuery({
    queryKey: versionId ? datasetKeys.versionFiles(versionId) : ["versions", "none", "files"],
    queryFn: () => datasetService.listVersionFiles(versionId!),
    enabled: Boolean(versionId),
  });
}

export function useCreateDataset() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: DatasetCreateRequest) => datasetService.create(payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: datasetKeys.all }),
  });
}

export function useUploadDatasetVersion() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ datasetId, files }: { datasetId: string; files: File[] }) =>
      datasetService.uploadVersion(datasetId, files),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: datasetKeys.versions(variables.datasetId) });
      queryClient.invalidateQueries({ queryKey: datasetKeys.all });
    },
  });
}

export function useDeleteDataset() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (datasetId: string) => datasetService.remove(datasetId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: datasetKeys.all }),
  });
}
