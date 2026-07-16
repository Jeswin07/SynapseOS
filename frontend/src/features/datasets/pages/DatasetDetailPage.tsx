import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { BarChart3, TrendingUp, Target, Upload, FileText, Download } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { StatusBadge } from "@/components/common/StatusBadge";
import { EmptyState } from "@/components/common/EmptyState";
import { ErrorState } from "@/components/common/ErrorState";
import { TableSkeleton } from "@/components/common/LoadingSkeleton";
import { Skeleton } from "@/components/ui/skeleton";
import { UploadVersionDialog } from "@/features/datasets/components/UploadVersionDialog";
import { useDataset, useDatasetVersionFiles, useDatasetVersions } from "@/hooks/useDatasets";
import { datasetService } from "@/services/dataset.service";
import { API_BASE_URL } from "@/services/apiClient";
import { titleCase, formatDate, formatCompactNumber } from "@/utils/format";

export default function DatasetDetailPage() {
  const { datasetId } = useParams<{ datasetId: string }>();
  const navigate = useNavigate();
  const [uploadOpen, setUploadOpen] = useState(false);
  const [selectedVersionId, setSelectedVersionId] = useState<string | null>(null);

  const dataset = useDataset(datasetId);
  const versions = useDatasetVersions(datasetId);
  const files = useDatasetVersionFiles(selectedVersionId ?? versions.data?.[0]?.id);

  const activeVersionId = selectedVersionId ?? versions.data?.[0]?.id ?? null;

  if (dataset.isLoading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-40 w-full" />
      </div>
    );
  }

  if (dataset.isError || !dataset.data) {
    return <ErrorState onRetry={() => dataset.refetch()} />;
  }

  const ds = dataset.data;

  return (
    <div>
      <PageHeader
        title={ds.name}
        description={ds.description ?? "No description provided."}
        crumbs={[{ label: "Datasets", to: "/datasets" }, { label: ds.name }]}
        actions={
          <>
            <Button variant="outline" onClick={() => setUploadOpen(true)}>
              <Upload className="h-4 w-4" /> Upload version
            </Button>
          </>
        }
      />

      <div className="mb-6 flex flex-wrap gap-2">
        <Badge variant="secondary">{titleCase(ds.dataset_type)}</Badge>
        <Badge variant="outline">{titleCase(ds.business_domain)}</Badge>
        <Badge variant="outline">Created {formatDate(ds.created_at)}</Badge>
      </div>

      {activeVersionId && (
        <div className="mb-6 grid grid-cols-1 gap-3 sm:grid-cols-3">
          <Card
            className="cursor-pointer transition-shadow hover:shadow-elevated"
            onClick={() => navigate(`/analytics?dataset_version_id=${activeVersionId}`)}
          >
            <CardContent className="flex items-center gap-3 p-4">
              <div className="rounded-lg bg-primary/10 p-2 text-primary">
                <BarChart3 className="h-4 w-4" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground">Run analytics</p>
                <p className="text-xs text-muted-foreground">Revenue, customers, products</p>
              </div>
            </CardContent>
          </Card>
          <Card
            className="cursor-pointer transition-shadow hover:shadow-elevated"
            onClick={() => navigate(`/forecasting?dataset_version_id=${activeVersionId}`)}
          >
            <CardContent className="flex items-center gap-3 p-4">
              <div className="rounded-lg bg-primary/10 p-2 text-primary">
                <TrendingUp className="h-4 w-4" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground">Train forecast</p>
                <p className="text-xs text-muted-foreground">Project future trends</p>
              </div>
            </CardContent>
          </Card>
          <Card
            className="cursor-pointer transition-shadow hover:shadow-elevated"
            onClick={() => navigate(`/prediction?dataset_version_id=${activeVersionId}`)}
          >
            <CardContent className="flex items-center gap-3 p-4">
              <div className="rounded-lg bg-primary/10 p-2 text-primary">
                <Target className="h-4 w-4" />
              </div>
              <div>
                <p className="text-sm font-medium text-foreground">Run prediction</p>
                <p className="text-xs text-muted-foreground">Churn, delivery delay</p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Versions</CardTitle>
            <CardDescription className="mt-1">Every uploaded snapshot of this dataset.</CardDescription>
          </CardHeader>
          <CardContent>
            {versions.isLoading ? (
              <TableSkeleton rows={3} />
            ) : versions.isError ? (
              <ErrorState onRetry={() => versions.refetch()} />
            ) : versions.data && versions.data.length > 0 ? (
              <ul className="space-y-1.5">
                {versions.data.map((v) => (
                  <li key={v.id}>
                    <button
                      onClick={() => setSelectedVersionId(v.id)}
                      className={`flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition-colors ${
                        v.id === activeVersionId ? "bg-accent text-accent-foreground" : "hover:bg-muted"
                      }`}
                    >
                      <span className="font-medium">Version {v.version}</span>
                      <StatusBadge status={v.status} />
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <EmptyState
                title="No versions yet"
                description="Upload a file to create the first version of this dataset."
                actionLabel="Upload version"
                onAction={() => setUploadOpen(true)}
              />
            )}
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Files</CardTitle>
            <CardDescription className="mt-1">Files included in the selected version.</CardDescription>
          </CardHeader>
          <CardContent>
            {!activeVersionId ? (
              <EmptyState title="Select a version" description="Choose a version on the left to see its files." />
            ) : files.isLoading ? (
              <TableSkeleton rows={3} />
            ) : files.isError ? (
              <ErrorState onRetry={() => files.refetch()} />
            ) : files.data && files.data.length > 0 ? (
              <ul className="space-y-1.5">
                {files.data.map((f) => (
                  <li
                    key={f.id}
                    className="flex items-center justify-between rounded-lg border border-border px-3 py-2.5 text-sm"
                  >
                    <span className="flex min-w-0 items-center gap-2">
                      <FileText className="h-4 w-4 shrink-0 text-muted-foreground" />
                      <span className="min-w-0">
                        <span className="block truncate font-medium text-foreground">{f.original_filename}</span>
                        <span className="block text-xs text-muted-foreground">
                          {f.rows_count ? `${formatCompactNumber(f.rows_count)} rows` : "—"} ·{" "}
                          {f.columns_count ?? "—"} columns
                        </span>
                      </span>
                    </span>
                    <Button variant="ghost" size="icon" asChild>
                      <a href={`${API_BASE_URL}${datasetService.downloadFileUrl(f.id)}`} target="_blank" rel="noreferrer">
                        <Download className="h-4 w-4" />
                      </a>
                    </Button>
                  </li>
                ))}
              </ul>
            ) : (
              <EmptyState title="No files" description="This version has no files on record." />
            )}
          </CardContent>
        </Card>
      </div>

      {datasetId && (
        <UploadVersionDialog datasetId={datasetId} open={uploadOpen} onOpenChange={setUploadOpen} />
      )}

      <p className="mt-4 text-xs text-muted-foreground">
        <Link to="/datasets" className="hover:underline">
          ← Back to all datasets
        </Link>
      </p>
    </div>
  );
}
