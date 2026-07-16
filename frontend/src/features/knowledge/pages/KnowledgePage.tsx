import { PageHeader } from "@/components/common/PageHeader";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { KnowledgeQueryPanel } from "@/features/knowledge/components/KnowledgeQueryPanel";
import { DocumentIngestPanel } from "@/features/knowledge/components/DocumentIngestPanel";

export default function KnowledgePage() {
  return (
    <div>
      <PageHeader
        title="Knowledge"
        description="Ingest enterprise documents and query them with retrieval-augmented generation."
      />
      <Tabs defaultValue="ask">
        <TabsList>
          <TabsTrigger value="ask">Ask</TabsTrigger>
          <TabsTrigger value="documents">Documents</TabsTrigger>
        </TabsList>
        <TabsContent value="ask">
          <KnowledgeQueryPanel />
        </TabsContent>
        <TabsContent value="documents">
          <DocumentIngestPanel />
        </TabsContent>
      </Tabs>
    </div>
  );
}
