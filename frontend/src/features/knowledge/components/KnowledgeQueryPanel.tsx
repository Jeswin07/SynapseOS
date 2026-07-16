import { useState } from "react";
import { Search, Loader2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { MarkdownRenderer } from "@/features/assistant/components/MarkdownRenderer";
import { SourcesPanel } from "@/features/assistant/components/SourcesPanel";
import { EmptyState } from "@/components/common/EmptyState";
import { useQueryKnowledge } from "@/hooks/useKnowledge";
import { ApiError } from "@/services/apiClient";
import { toast } from "sonner";

export function KnowledgeQueryPanel() {
  const [query, setQuery] = useState("");
  const queryKnowledge = useQueryKnowledge();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) return;
    queryKnowledge.mutate(
      { query: trimmed, collection_name: "enterprise_docs", top_k: 5 },
      {
        onError: (err) => {
          toast.error(err instanceof ApiError ? err.detail : "The knowledge base could not be queried.");
        },
      }
    );
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <div className="relative flex-1">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your knowledge base…"
            className="pl-9"
          />
        </div>
        <Button type="submit" disabled={!query.trim() || queryKnowledge.isPending}>
          {queryKnowledge.isPending && <Loader2 className="h-4 w-4 animate-spin" />}
          Ask
        </Button>
      </form>

      {queryKnowledge.isPending && (
        <Card>
          <CardContent className="p-5 text-sm text-muted-foreground">Searching your knowledge base…</CardContent>
        </Card>
      )}

      {queryKnowledge.data && (
        <Card>
          <CardContent className="space-y-3 p-5">
            <MarkdownRenderer content={queryKnowledge.data.answer} />
            <SourcesPanel sources={queryKnowledge.data.sources} />
            <div className="flex flex-wrap gap-2 border-t border-border pt-3">
              <Badge variant="outline">{queryKnowledge.data.metrics.total_time_ms.toFixed(0)}ms total</Badge>
              <Badge variant="outline">{queryKnowledge.data.metrics.chunks_retrieved} chunks retrieved</Badge>
              <Badge variant="outline">
                {(queryKnowledge.data.metrics.average_similarity * 100).toFixed(0)}% avg. similarity
              </Badge>
            </div>
          </CardContent>
        </Card>
      )}

      {!queryKnowledge.data && !queryKnowledge.isPending && (
        <EmptyState
          icon={Search}
          title="Ask anything about your knowledge base"
          description="Query ingested documents and get grounded answers with cited sources."
        />
      )}
    </div>
  );
}
