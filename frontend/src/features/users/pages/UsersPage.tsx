import { Users as UsersIcon, Info } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { DataTable, type DataTableColumn } from "@/components/common/DataTable";
import { TableSkeleton } from "@/components/common/LoadingSkeleton";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { CreateUserDialog } from "@/features/users/components/CreateUserDialog";
import { useUsers } from "@/hooks/useUsers";
import { useAuthStore } from "@/stores/auth.store";
import { initials } from "@/utils/format";
import type { UserResponse } from "@/types/api";

const ROLE_VARIANT: Record<string, "default" | "secondary" | "outline"> = {
  ADMIN: "default",
  ANALYST: "secondary",
  EXECUTIVE: "outline",
};

export default function UsersPage() {
  const { data, isLoading, isError, refetch } = useUsers();
  const role = useAuthStore((s) => s.role);
  const canManage = role === "ADMIN";

  const columns: DataTableColumn<UserResponse>[] = [
    {
      key: "full_name",
      header: "User",
      render: (row) => (
        <div className="flex items-center gap-2.5">
          <Avatar className="h-8 w-8">
            <AvatarFallback>{initials(row.full_name)}</AvatarFallback>
          </Avatar>
          <div>
            <p className="font-medium text-foreground">{row.full_name}</p>
            <p className="text-xs text-muted-foreground">{row.email}</p>
          </div>
        </div>
      ),
      sortValue: (row) => row.full_name,
    },
    {
      key: "role",
      header: "Role",
      render: (row) => <Badge variant={ROLE_VARIANT[row.role] ?? "secondary"}>{row.role}</Badge>,
      sortValue: (row) => row.role,
    },
  ];

  return (
    <div>
      <PageHeader
        title="Users"
        description="Manage who has access to your SynapseOS workspace."
        actions={canManage ? <CreateUserDialog /> : undefined}
      />

      {isLoading ? (
        <TableSkeleton />
      ) : isError ? (
        <ErrorState onRetry={() => refetch()} />
      ) : data && data.length > 0 ? (
        <DataTable
          columns={columns}
          data={data}
          rowKey={(row) => row.id}
          searchFilter={(row, q) =>
            row.full_name.toLowerCase().includes(q.toLowerCase()) || row.email.toLowerCase().includes(q.toLowerCase())
          }
          searchPlaceholder="Search users…"
          emptyTitle="No users found"
        />
      ) : (
        <EmptyState icon={UsersIcon} title="No users yet" description="Invite your team to get started." />
      )}

      {!canManage && (
        <p className="mt-4 flex items-start gap-2 text-xs text-muted-foreground">
          <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" />
          Only administrators can add new users.
        </p>
      )}
    </div>
  );
}
