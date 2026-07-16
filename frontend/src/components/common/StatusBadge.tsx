import { Badge } from "@/components/ui/badge";
import { titleCase } from "@/utils/format";

const STATUS_MAP: Record<string, "default" | "secondary" | "outline" | "success" | "warning" | "danger"> = {
  READY: "success",
  UPLOADED: "secondary",
  UPLOADING: "warning",
  PROFILING: "warning",
  FAILED: "danger",
  ARCHIVED: "outline",
  LOW: "success",
  MEDIUM: "warning",
  HIGH: "danger",
  ACTIVE: "success",
  INACTIVE: "outline",
  PENDING: "warning",
  COMPLETED: "success",
  ERROR: "danger",
};

export function StatusBadge({ status }: { status: string }) {
  const key = status?.toUpperCase?.() ?? "";
  const variant = STATUS_MAP[key] ?? "secondary";
  return <Badge variant={variant}>{titleCase(status)}</Badge>;
}
