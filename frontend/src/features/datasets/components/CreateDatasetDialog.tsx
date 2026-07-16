import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { Loader2, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useCreateDataset } from "@/hooks/useDatasets";
import { ApiError } from "@/services/apiClient";
import type { BusinessDomain, DatasetType } from "@/types/api";

const DATASET_TYPES: DatasetType[] = ["SALES", "INVENTORY", "CUSTOMER", "FINANCE", "GENERIC"];
const BUSINESS_DOMAINS: BusinessDomain[] = ["RETAIL", "ECOMMERCE", "FINANCE", "MANUFACTURING", "HEALTHCARE", "GENERIC"];

const schema = z.object({
  name: z.string().min(2, "Name is required"),
  description: z.string().optional(),
  dataset_type: z.enum(["SALES", "INVENTORY", "CUSTOMER", "FINANCE", "GENERIC"]),
  business_domain: z.enum(["RETAIL", "ECOMMERCE", "FINANCE", "MANUFACTURING", "HEALTHCARE", "GENERIC"]),
});

type FormValues = z.infer<typeof schema>;

export function CreateDatasetDialog({ onCreated }: { onCreated?: (datasetId: string) => void }) {
  const [open, setOpen] = useState(false);
  const createDataset = useCreateDataset();

  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { dataset_type: "SALES", business_domain: "RETAIL" },
  });

  function onSubmit(values: FormValues) {
    createDataset.mutate(
      { ...values, tags: [] },
      {
        onSuccess: (data) => {
          toast.success("Dataset created. Upload a version to profile it.");
          setOpen(false);
          reset();
          onCreated?.(data.dataset_id);
        },
        onError: (err) => {
          toast.error(err instanceof ApiError ? err.detail : "Unable to create dataset.");
        },
      }
    );
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="h-4 w-4" /> New dataset
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create dataset</DialogTitle>
          <DialogDescription>
            Define the dataset's identity. You'll upload files as a version in the next step.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-1.5">
            <Label htmlFor="name">Name</Label>
            <Input id="name" placeholder="Q3 Sales Data" {...register("name")} />
            {errors.name && <p className="text-xs text-destructive">{errors.name.message}</p>}
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="description">Description</Label>
            <Textarea id="description" placeholder="Optional context for this dataset" {...register("description")} />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <Label>Dataset type</Label>
              <Controller
                control={control}
                name="dataset_type"
                render={({ field }) => (
                  <Select value={field.value} onValueChange={field.onChange}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {DATASET_TYPES.map((t) => (
                        <SelectItem key={t} value={t}>
                          {t.charAt(0) + t.slice(1).toLowerCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            </div>
            <div className="space-y-1.5">
              <Label>Business domain</Label>
              <Controller
                control={control}
                name="business_domain"
                render={({ field }) => (
                  <Select value={field.value} onValueChange={field.onChange}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {BUSINESS_DOMAINS.map((d) => (
                        <SelectItem key={d} value={d}>
                          {d.charAt(0) + d.slice(1).toLowerCase()}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={createDataset.isPending}>
              {createDataset.isPending && <Loader2 className="h-4 w-4 animate-spin" />}
              Create dataset
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
