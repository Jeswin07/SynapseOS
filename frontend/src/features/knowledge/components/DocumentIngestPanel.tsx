import { useState } from "react";
import { toast } from "sonner";
import { Loader2, BookOpen, Trash2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { UploadZone } from "@/components/common/UploadZone";
import { EmptyState } from "@/components/common/EmptyState";
import { useIngestDocument, useKnowledgeDocuments, useDeleteDocument } from "@/hooks/useKnowledge";
import { ApiError } from "@/services/apiClient";

export function DocumentIngestPanel() {
  const [pending, setPending] = useState<File[]>([]);
  
  const { data, isLoading } = useKnowledgeDocuments();
  const ingestDocument = useIngestDocument();
  const deleteDocument = useDeleteDocument();

  const documents = data?.documents || [];

  function handleIngest() {
    if (pending.length === 0) return;
    const file = pending[0];
    ingestDocument.mutate(
      { file, collectionName: "enterprise_docs" },
      {
        onSuccess: (res) => {
          setPending((prev) => prev.slice(1));
          toast.success(`Ingested ${file.name} (${res.chunks_processed} chunks)`);
        },
        onError: (err) => {
          toast.error(err instanceof ApiError ? err.detail : "Failed to ingest document.");
          setPending((prev) => prev.slice(1));
        },
      }
    );
  }

  function handleDelete(documentId: string, filename: string) {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) return;
    
    deleteDocument.mutate(documentId, {
      onSuccess: () => {
        toast.success(`Deleted ${filename}`);
      },
      onError: (err) => {
        toast.error(err instanceof ApiError ? err.detail : "Failed to delete document.");
      },
    });
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardContent className="space-y-4 p-5">
          <UploadZone
            onFilesSelected={(files) => setPending((prev) => [...prev, ...files])}
            files={pending}
            onRemove={(idx) => setPending((prev) => prev.filter((_, i) => i !== idx))}
            multiple={false}
            hint="PDF, DOCX, TXT, or Markdown"
            accept=".pdf,.docx,.txt,.md"
          />
          <Button onClick={handleIngest} disabled={pending.length === 0 || ingestDocument.isPending}>
            {ingestDocument.isPending && <Loader2 className="h-4 w-4 animate-spin" />}
            Ingest document
          </Button>
        </CardContent>
      </Card>

      <div>
        <p className="mb-2 text-sm font-medium text-foreground">Enterprise Knowledge Library</p>
        
        {isLoading ? (
          <div className="flex items-center justify-center py-8 text-sm text-muted-foreground">
            <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Loading library...
          </div>
        ) : documents.length === 0 ? (
          <EmptyState
            icon={BookOpen}
            title="No documents ingested yet"
            description="Documents you ingest will be persistently stored here."
          />
        ) : (
          <ul className="space-y-1.5">
            {documents.map((doc) => (
              <li
                key={doc.document_id}
                className="flex items-center justify-between rounded-lg border border-border px-3 py-2.5 text-sm"
              >
                <div className="flex min-w-0 flex-1 flex-col sm:flex-row sm:items-center gap-1 sm:gap-3">
                  <span className="min-w-0 truncate font-medium text-foreground">{doc.filename}</span>
                  <div className="flex gap-1.5">
                    <Badge variant="secondary">{doc.chunk_count} chunks</Badge>
                    <Badge variant={doc.status === "READY" ? "default" : "danger"}>
                    </Badge>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 text-muted-foreground hover:text-destructive"
                  onClick={() => handleDelete(doc.document_id, doc.filename)}
                  disabled={deleteDocument.isPending}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}