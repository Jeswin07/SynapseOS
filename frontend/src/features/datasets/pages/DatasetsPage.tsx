import { useNavigate } from "react-router-dom";
import { Database, Trash2 } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { DataTable, type DataTableColumn } from "@/components/common/DataTable";
import { CardGridSkeleton, TableSkeleton } from "@/components/common/LoadingSkeleton";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { ConfirmationDialog } from "@/components/common/ConfirmationDialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CreateDatasetDialog } from "@/features/datasets/components/CreateDatasetDialog";
import { useDatasets, useDeleteDataset } from "@/hooks/useDatasets";
import { formatDate, titleCase } from "@/utils/format";
import type { DatasetResponse } from "@/types/api";
import { useState } from "react";
import { toast } from "sonner";
import { ApiError } from "@/services/apiClient";

export default function DatasetsPage() {
  const navigate = useNavigate();
  const { data, isLoading, isError, refetch } = useDatasets();
  const deleteDataset = useDeleteDataset();
  const [pendingDelete, setPendingDelete] = useState<DatasetResponse | null>(null);

  const columns: DataTableColumn<DatasetResponse>[] = [
    {
      key: "name",
      header: "Name",
      render: (row) => (
        <div>
          <p className="font-medium text-foreground">{row.name}</p>
          {row.description && <p className="max-w-xs truncate text-xs text-muted-foreground">{row.description}</p>}
        </div>
      ),
      sortValue: (row) => row.name,
    },
    {
      key: "dataset_type",
      header: "Type",
      render: (row) => <Badge variant="secondary">{titleCase(row.dataset_type)}</Badge>,
      sortValue: (row) => row.dataset_type,
    },
    {
      key: "business_domain",
      header: "Domain",
      render: (row) => <Badge variant="outline">{titleCase(row.business_domain)}</Badge>,
      sortValue: (row) => row.business_domain,
    },
    {
      key: "created_at",
      header: "Created",
      render: (row) => <span className="text-sm text-muted-foreground">{formatDate(row.created_at)}</span>,
      sortValue: (row) => row.created_at,
    },
    {
      key: "actions",
      header: "",
      render: (row) => (
        <Button
          variant="ghost"
          size="icon"
          onClick={(e) => {
            e.stopPropagation();
            setPendingDelete(row);
          }}
        >
          <Trash2 className="h-4 w-4 text-muted-foreground hover:text-destructive" />
        </Button>
      ),
      className: "w-10",
    },
  ];

  return (
    <div>
      <PageHeader
        title="Datasets"
        description="Manage the source data powering analytics, forecasting, and predictions."
        actions={<CreateDatasetDialog onCreated={(id) => navigate(`/datasets/${id}`)} />}
      />

      {isLoading ? (
        <>
          <CardGridSkeleton count={3} />
          <div className="mt-6">
            <TableSkeleton />
          </div>
        </>
      ) : isError ? (
        <ErrorState onRetry={() => refetch()} />
      ) : data && data.length > 0 ? (
        <DataTable
          columns={columns}
          data={data}
          rowKey={(row) => row.id}
          onRowClick={(row) => navigate(`/datasets/${row.id}`)}
          searchFilter={(row, q) => row.name.toLowerCase().includes(q.toLowerCase())}
          searchPlaceholder="Search datasets…"
          emptyTitle="No datasets found"
        />
      ) : (
        <EmptyState
          icon={Database}
          title="No datasets yet"
          description="Create your first dataset to start uploading data and unlocking AI-powered insights."
        />
      )}

      <ConfirmationDialog
        open={Boolean(pendingDelete)}
        onOpenChange={(open) => !open && setPendingDelete(null)}
        title="Delete dataset"
        description={`This will permanently delete "${pendingDelete?.name}" and all of its versions. This action cannot be undone.`}
        confirmLabel="Delete"
        destructive
        loading={deleteDataset.isPending}
        onConfirm={() => {
          if (!pendingDelete) return;
          deleteDataset.mutate(pendingDelete.id, {
            onSuccess: () => {
              toast.success("Dataset deleted");
              setPendingDelete(null);
            },
            onError: (err) => {
              toast.error(err instanceof ApiError ? err.detail : "Unable to delete dataset.");
            },
          });
        }}
      />
    </div>
  );
}
