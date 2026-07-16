import { useState, type KeyboardEvent } from "react";
import { ArrowUp, Square, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

interface ChatComposerProps {
  onSend: (text: string) => void;
  isSending: boolean;
  onCancel: () => void;
  streamingMode: boolean;
  onToggleStreaming: (value: boolean) => void;
}

const SUGGESTIONS = [
  "Summarize this month's revenue performance",
  "Which customers are at risk of churn?",
  "Forecast next quarter's demand",
  "What are the top operational risks right now?",
];

export function ChatComposer({ onSend, isSending, onCancel, streamingMode, onToggleStreaming }: ChatComposerProps) {
  const [value, setValue] = useState("");

  function submit() {
    const trimmed = value.trim();
    if (!trimmed || isSending) return;
    onSend(trimmed);
    setValue("");
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  return (
    <div className="border-t border-border bg-background p-4">
      {value.length === 0 && (
        <div className="mb-3 flex flex-wrap gap-2">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => setValue(s)}
              className="rounded-full border border-border bg-muted/40 px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground"
            >
              {s}
            </button>
          ))}
        </div>
      )}
      <div className="flex items-end gap-2 rounded-xl border border-border bg-card p-2 shadow-soft focus-within:ring-2 focus-within:ring-ring">
        <Textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask SynapseOS about your business…"
          className="min-h-[44px] flex-1 resize-none border-0 shadow-none focus-visible:ring-0"
          rows={1}
        />
        <Tooltip>
          <TooltipTrigger asChild>
            <div className="flex items-center gap-1.5 px-1 pb-1.5 text-muted-foreground">
              <Zap className="h-3.5 w-3.5" />
              <Switch checked={streamingMode} onCheckedChange={onToggleStreaming} />
            </div>
          </TooltipTrigger>
          <TooltipContent>{streamingMode ? "Streaming responses on" : "Streaming responses off"}</TooltipContent>
        </Tooltip>
        {isSending ? (
          <Button size="icon" variant="outline" onClick={onCancel} className="shrink-0">
            <Square className="h-3.5 w-3.5" />
          </Button>
        ) : (
          <Button size="icon" onClick={submit} disabled={!value.trim()} className="shrink-0">
            <ArrowUp className="h-4 w-4" />
          </Button>
        )}
      </div>
      <p className="mt-2 text-center text-[11px] text-muted-foreground">
        SynapseOS can make mistakes. Verify important decisions.
      </p>
    </div>
  );
}
