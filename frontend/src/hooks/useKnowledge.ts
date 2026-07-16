import { useMutation } from "@tanstack/react-query";
import { knowledgeService } from "@/services/knowledge.service";
import type { QueryRequest } from "@/types/api";

export function useIngestDocument() {
  return useMutation({
    mutationFn: ({ file, collectionName }: { file: File; collectionName?: string }) =>
      knowledgeService.ingest(file, collectionName),
  });
}

export function useQueryKnowledge() {
  return useMutation({
    mutationFn: (payload: QueryRequest) => knowledgeService.query(payload),
  });
}
