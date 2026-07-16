import { useState } from "react";
import { toast } from "sonner";
import { GitBranch, Loader2, Sparkles, Info } from "lucide-react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { EmptyState } from "@/components/common/EmptyState";
import { MarkdownRenderer } from "@/features/assistant/components/MarkdownRenderer";
import { SourcesPanel } from "@/features/assistant/components/SourcesPanel";
import { RecommendationsList } from "@/features/assistant/components/RecommendationsList";
import { assistantService } from "@/services/assistant.service";
import { ApiError } from "@/services/apiClient";
import type { AssistantChatResponse } from "@/types/api";

const EXAMPLES = [
  "What happens to revenue if we raise prices by 8% next quarter?",
  "Model the impact of a 15% increase in delivery delays on customer churn.",
  "What if we reduce marketing spend by 20% for two quarters?",
];

export default function ScenarioPage() {
  const [scenario, setScenario] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState<AssistantChatResponse | null>(null);

  async function handleRun() {
    const trimmed = scenario.trim();
    if (!trimmed) return;
    setIsRunning(true);
    setResult(null);
    try {
      const response = await assistantService.chat({
        message: `Scenario planning request: ${trimmed}`,
        metadata: { intent: "scenario_planning" },
      });
      setResult(response);
    } catch (err) {
      toast.error(err instanceof ApiError ? err.detail : "The scenario could not be modeled.");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <div>
      <PageHeader
        title="Scenario Planner"
        description="Model 'what-if' business scenarios using SynapseOS's multi-agent reasoning."
      />

      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Describe your scenario</CardTitle>
          <CardDescription className="mt-1">
            Be specific about the variable you're changing and the timeframe.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-1.5">
            <Label htmlFor="scenario">Scenario</Label>
            <Textarea
              id="scenario"
              rows={4}
              placeholder="e.g. What if we expand into the Southeast region next quarter?"
              value={scenario}
              onChange={(e) => setScenario(e.target.value)}
            />
          </div>
          {scenario.length === 0 && (
            <div className="flex flex-wrap gap-2">
              {EXAMPLES.map((example) => (
                <button
                  key={example}
                  onClick={() => setScenario(example)}
                  className="rounded-full border border-border bg-muted/40 px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:border-primary/40 hover:text-foreground"
                >
                  {example}
                </button>
              ))}
            </div>
          )}
          <Button onClick={handleRun} disabled={!scenario.trim() || isRunning}>
            {isRunning ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
            Run scenario
          </Button>
        </CardContent>
      </Card>

      {isRunning ? (
        <Card>
          <CardContent className="p-6 text-sm text-muted-foreground">
            Modeling your scenario across the relevant agents…
          </CardContent>
        </Card>
      ) : result ? (
        <Card>
          <CardContent className="space-y-3 p-5">
            <MarkdownRenderer content={result.answer} />
            <SourcesPanel sources={result.sources} />
            <RecommendationsList recommendations={result.recommendations} />
          </CardContent>
        </Card>
      ) : (
        <EmptyState
          icon={GitBranch}
          title="No scenario modeled yet"
          description="Describe a scenario above and run it to see the projected impact."
        />
      )}

      <p className="mt-6 flex items-start gap-2 text-xs text-muted-foreground">
        <Info className="mt-0.5 h-3.5 w-3.5 shrink-0" />
        Scenario Planning does not have a dedicated backend endpoint yet — this workspace routes your scenario
        through the AI Assistant's Scenario Agent via the existing /assistant/chat contract. TODO: backend —
        add a first-class /scenarios endpoint for structured scenario runs.
      </p>
    </div>
  );
}
