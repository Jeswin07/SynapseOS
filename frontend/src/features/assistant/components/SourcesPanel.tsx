import { FileText } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { SourceChunk } from "@/types/api";

interface LegacySource {
  file_name?: string;
  name?: string;
  page_label?: string;
  score?: number;
}

interface SourcesPanelProps {
  sources: (SourceChunk | LegacySource)[];
}

export function SourcesPanel({ sources }: SourcesPanelProps) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 space-y-2">
      <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
        Sources
      </p>

      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
        {sources.map((source, idx) => {
          const fileName =
            source.file_name ??
            ("name" in source ? source.name : undefined) ??
            `Source ${idx + 1}`;

          const page = source.page_label;
          const score = source.score;

          return (
            <div
              key={idx}
              className="flex items-start gap-2 rounded-lg border border-border bg-muted/30 p-2.5 text-xs"
            >
              <FileText className="mt-0.5 h-3.5 w-3.5 shrink-0 text-muted-foreground" />

              <div className="min-w-0">
                <p className="truncate font-medium text-foreground">
                  {fileName}
                </p>

                <div className="mt-1 flex items-center gap-1.5">
                  {page && <Badge variant="outline">{page}</Badge>}

                  {typeof score === "number" && (
                    <Badge variant="secondary">
                      {(score * 100).toFixed(0)}% match
                    </Badge>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}