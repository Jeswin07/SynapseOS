import { useState } from "react";
import { toast } from "sonner";
import { Loader2, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { UploadZone } from "@/components/common/UploadZone";
import { useUploadDatasetVersion } from "@/hooks/useDatasets";
import { ApiError } from "@/services/apiClient";

interface UploadVersionDialogProps {
  datasetId: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function UploadVersionDialog({ datasetId, open, onOpenChange }: UploadVersionDialogProps) {
  const [files, setFiles] = useState<File[]>([]);
  const upload = useUploadDatasetVersion();

  function handleUpload() {
    if (files.length === 0) return;
    upload.mutate(
      { datasetId, files },
      {
        onSuccess: () => {
          toast.success("Version uploaded. Profiling will begin shortly.");
          setFiles([]);
          onOpenChange(false);
        },
        onError: (err) => {
          toast.error(err instanceof ApiError ? err.detail : "Upload failed. Please try again.");
        },
      }
    );
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Upload new version</DialogTitle>
          <DialogDescription>
            Add one or more files as a new version of this dataset. Supported formats: CSV, XLSX, JSON.
          </DialogDescription>
        </DialogHeader>
        <UploadZone
          onFilesSelected={(newFiles) => setFiles((prev) => [...prev, ...newFiles])}
          files={files}
          onRemove={(idx) => setFiles((prev) => prev.filter((_, i) => i !== idx))}
          hint="CSV, XLSX, or JSON up to your organization's size limit"
          accept=".csv,.xlsx,.json"
        />
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleUpload} disabled={files.length === 0 || upload.isPending}>
            {upload.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Upload className="h-4 w-4" />}
            Upload version
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
