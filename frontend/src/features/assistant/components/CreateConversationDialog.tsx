import { useEffect, useMemo, useState } from "react";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { DatasetVersionSelect } from "@/components/common/DatasetVersionSelect";

import { conversationService } from "@/services/conversation.service";
import { useAssistantStore } from "@/stores/assistant.store";

import type { Conversation } from "@/types/domain";

interface CreateConversationDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CreateConversationDialog({
  open,
  onOpenChange,
}: CreateConversationDialogProps) {
  const addConversation = useAssistantStore(
    (state) => state.addConversation
  );

  const setActiveConversation = useAssistantStore(
    (state) => state.setActiveConversation
  );

  const [datasetId, setDatasetId] =
    useState<string | null>(null);

  const [versionId, setVersionId] =
    useState<string | null>(null);

  const [title, setTitle] = useState("");

  const [titleEdited, setTitleEdited] =
    useState(false);

  const [loading, setLoading] = useState(false);

  const canCreate = useMemo(() => {
    return !!versionId && !loading;
  }, [versionId, loading]);

  useEffect(() => {
    if (!open) {
      setDatasetId(null);
      setVersionId(null);
      setTitle("");
      setTitleEdited(false);
      setLoading(false);
    }
  }, [open]);

  useEffect(() => {
    if (titleEdited) return;

    if (versionId) {
      setTitle("New Conversation");
    }
  }, [versionId, titleEdited]);

  async function handleCreate() {
    if (!versionId) {
      return;
    }

    try {
      setLoading(true);

      const response =
        await conversationService.create({
          dataset_version_id: versionId,
          title:
            title.trim() || "New Conversation",
        });

      const conversation: Conversation = {
        id: response.id,
        title: response.title,
        pinned: false,
        updatedAt: response.updated_at,
        messages: [],
      };

      addConversation(conversation);

      setActiveConversation(conversation.id);

      onOpenChange(false);
    } catch (error) {
      console.error(error);
      alert("Failed to create conversation.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Dialog
      open={open}
      onOpenChange={onOpenChange}
    >
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>
            Create Conversation
          </DialogTitle>

          <DialogDescription>
            Choose the dataset version that this
            conversation should use.
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-5">

          <div className="space-y-2">
            <Label>
              Dataset Version
            </Label>

            <DatasetVersionSelect
              datasetId={datasetId}
              versionId={versionId}
              onDatasetChange={(id) => {
                setDatasetId(id);
                setVersionId(null);
              }}
              onVersionChange={setVersionId}
            />
          </div>

          <div className="space-y-2">
            <Label>
              Conversation Title
            </Label>

            <Input
              value={title}
              placeholder="Sales Analysis"
              onChange={(e) => {
                setTitleEdited(true);
                setTitle(e.target.value);
              }}
            />
          </div>
        </div>

        <DialogFooter className="mt-2">

          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={loading}
          >
            Cancel
          </Button>

          <Button
            onClick={handleCreate}
            disabled={!canCreate}
          >
            {loading
              ? "Creating..."
              : "Create Conversation"}
          </Button>

        </DialogFooter>

      </DialogContent>
    </Dialog>
  );
}