import { useState } from "react";
import { toast } from "sonner";
import { Loader2, BookOpen, Info } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { UploadZone } from "@/components/common/UploadZone";
import { EmptyState } from "@/components/common/EmptyState";
import { useIngestDocument } from "@/hooks/useKnowledge";
import { ApiError } from "@/services/apiClient";
import type { DocumentUploadResponse } from "@/types/api";

interface IngestedDocument extends DocumentUploadResponse {
  fileName: string;
  ingestedAt: string;
}

export function DocumentIngestPanel() {
  const [pending, setPending] = useState<File[]>([]);
  const [ingested, setIngested] = useState<IngestedDocument[]>([]);
  const ingestDocument = useIngestDocument();

  function handleIngest() {
    if (pending.length === 0) return;
    const file = pending[0];
    ingestDocument.mutate(
      { file, collectionName: "enterprise_docs" },
      {
        onSuccess: (data) => {
          setIngested((prev) => [
            { ...data, fileName: file.name, ingestedAt: new Date().toISOString() },
            ...prev,
          ]);
          setPending((prev) => prev.slice(1));
          toast.success(`Ingested ${file.name} (${data.chunks_processed} chunks)`);
        },
        onError: (err) => {
          toast.error(err instanceof ApiError ? err.detail : "Failed to ingest document.");
          setPending((prev) => prev.slice(1));
        },
      }
    );
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
        <p className="mb-2 text-sm font-medium text-foreground">Document library (this session)</p>
        {ingested.length === 0 ? (
          <EmptyState
            icon={BookOpen}
            title="No documents ingested yet"
            description="Documents you ingest will appear here for this session."
          />
        ) : (
          <ul className="space-y-1.5">
            {ingested.map((doc) => (
              <li
                key={doc.document_id}
                className="flex items-center justify-between rounded-lg border border-border px-3 py-2.5 text-sm"
              >
                <span className="min-w-0 truncate font-medium text-foreground">{doc.fileName}</span>
                <Badge variant="secondary">{doc.chunks_processed} chunks</Badge>
              </li>
            ))}
          </ul>
        )}
        <p className="mt-3 flex items-start gap-2 text-xs text-muted-foreground">
          <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" />
          The backend does not yet expose an endpoint to list previously ingested documents, so this library
          reflects only documents ingested during your current session.
        </p>
      </div>
    </div>
  );
}
