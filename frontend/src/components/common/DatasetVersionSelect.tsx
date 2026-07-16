import { Database } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { EmptyState } from "@/components/common/EmptyState";
import { useDatasets, useDatasetVersions } from "@/hooks/useDatasets";
import { titleCase } from "@/utils/format";

interface DatasetVersionSelectProps {
  datasetId: string | null;
  versionId: string | null;
  onDatasetChange: (datasetId: string) => void;
  onVersionChange: (versionId: string) => void;
}

export function DatasetVersionSelect({
  datasetId,
  versionId,
  onDatasetChange,
  onVersionChange,
}: DatasetVersionSelectProps) {
  const datasets = useDatasets();
  const versions = useDatasetVersions(datasetId ?? undefined);

  if (datasets.isLoading) {
    return <Skeleton className="h-9 w-full max-w-sm" />;
  }

  if (!datasets.data || datasets.data.length === 0) {
    return (
      <EmptyState
        icon={Database}
        title="No datasets available"
        description="Create and upload a dataset first to run this workflow."
      />
    );
  }

  return (
    <div className="flex flex-col gap-3 sm:flex-row">
      <div className="w-full sm:w-64">
        <Select value={datasetId ?? undefined} onValueChange={onDatasetChange}>
          <SelectTrigger>
            <SelectValue placeholder="Select dataset" />
          </SelectTrigger>
          <SelectContent>
            {datasets.data.map((d) => (
              <SelectItem key={d.id} value={d.id}>
                {d.name} · {titleCase(d.dataset_type)}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="w-full sm:w-56">
        <Select value={versionId ?? undefined} onValueChange={onVersionChange} disabled={!datasetId}>
          <SelectTrigger>
            <SelectValue placeholder={versions.isLoading ? "Loading versions…" : "Select version"} />
          </SelectTrigger>
          <SelectContent>
            {versions.data?.map((v) => (
              <SelectItem key={v.id} value={v.id}>
                Version {v.version} · {titleCase(v.status)}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
