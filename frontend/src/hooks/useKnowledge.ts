import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { knowledgeService } from "@/services/knowledge.service";
import type { QueryRequest } from "@/types/api";

export function useIngestDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ file, collectionName }: { file: File; collectionName?: string }) =>
      knowledgeService.ingest(file, collectionName),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["knowledge-documents"] });
    },
  });
}

export function useQueryKnowledge() {
  return useMutation({
    mutationFn: (payload: QueryRequest) => knowledgeService.query(payload),
  });
}

export function useKnowledgeDocuments() {
  return useQuery({
    queryKey: ["knowledge-documents"],
    queryFn: () => knowledgeService.getDocuments(),
  });
}

export function useDeleteDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (documentId: string) => knowledgeService.deleteDocument(documentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["knowledge-documents"] });
    },
  });
}