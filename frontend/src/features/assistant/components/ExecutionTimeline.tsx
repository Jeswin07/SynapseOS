import {
  Check,
  Loader2,
  AlertCircle,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { StreamEvent } from "@/types/api";

interface Props {
  events: StreamEvent[];
  isActive: boolean;
}

type StageStatus = "running" | "completed" | "error";

interface Stage {
  id: string;
  label: string;
  status: StageStatus;
}

const AGENT_LABELS: Record<string, string> = {
  knowledge: "Knowledge Agent",
  intelligence: "Intelligence Agent",
  analytics: "Analytics Agent",
  forecast: "Forecast Agent",
  prediction: "Prediction Agent",
  risk: "Risk Agent",
  scenario: "Scenario Agent",
};

export function ExecutionTimeline({
  events,
  isActive,
}: Props) {
  if (!events.length) return null;

  const stages: Stage[] = [];

  const getStage = (
    id: string,
    label: string,
  ): Stage => {
    let stage = stages.find((s) => s.id === id);

    if (!stage) {
      stage = {
        id,
        label,
        status: "running",
      };

      stages.push(stage);
    }

    return stage;
  };

  const getAgentLabel = (
    agent: string | null,
  ) => {
    if (!agent) return "Agent";

    return (
      AGENT_LABELS[
        agent.toLowerCase()
      ] ?? agent
    );
  };

  for (const event of events) {
    switch (event.type) {
      case "status": {
        const message =
          event.message.toLowerCase();

        if (
          message.includes("planning")
        ) {
          getStage(
            "planning",
            "Planning",
          ).status = "running";
        }

        else if (
          message.includes(
            "planner selected",
          )
        ) {
          getStage(
            "planning",
            "Planning",
          ).status = "completed";

          getStage(
            "selection",
            "Selecting Agents",
          ).status = "completed";
        }

        else if (
          message.includes(
            "executive",
          )
        ) {
          getStage(
            "executive",
            "Executive Generator",
          ).status = "running";
        }

        break;
      }

      case "agent_started": {
        const id =
          event.agent ?? "agent";

        getStage(
          id,
          getAgentLabel(
            event.agent,
          ),
        ).status = "running";

        break;
      }

      case "agent_completed": {
        const id =
          event.agent ?? "agent";

        getStage(
          id,
          getAgentLabel(
            event.agent,
          ),
        ).status = "completed";

        break;
      }

      case "error": {
        getStage(
          "error",
          "Error",
        ).status = "error";

        break;
      }

      case "complete": {
        getStage(
          "executive",
          "Executive Generator",
        ).status = "completed";

        getStage(
          "completed",
          "Completed",
        ).status = "completed";

        break;
      }
    }
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-border bg-muted/20">

      {/* Header */}

      <div className="border-b border-border bg-muted/30 px-4 py-3">

        <div className="flex items-center justify-between">

          <div>

            <h4 className="text-sm font-semibold">
              Agent Workflow
            </h4>

            <p className="text-xs text-muted-foreground">
              Multi-agent execution pipeline
            </p>

          </div>

          {isActive && (
            <div className="flex items-center gap-2 rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary">

              <Loader2 className="h-3.5 w-3.5 animate-spin" />

              Running

            </div>
          )}

        </div>

      </div>

      {/* Stages */}

      <div className="space-y-3 p-4">

        {stages.map((stage) => {

          let icon;

          let iconColor = "";

          let badgeText = "";

          switch (stage.status) {

            case "completed":

              icon = <Check className="h-4 w-4" />;

              iconColor =
                "bg-green-500 text-white";

              badgeText = "Completed";

              break;

            case "running":

              icon = (
                <Loader2 className="h-4 w-4 animate-spin" />
              );

              iconColor =
                "bg-blue-500 text-white";

              badgeText = "Running";

              break;

            case "error":

              icon = (
                <AlertCircle className="h-4 w-4" />
              );

              iconColor =
                "bg-red-500 text-white";

              badgeText = "Error";

              break;

          }

          return (

            <div
              key={stage.id}
              className="flex items-center gap-4 rounded-xl border border-border bg-background px-4 py-3 transition-all"
            >

              <div
                className={`flex h-9 w-9 items-center justify-center rounded-full ${iconColor}`}
              >
                {icon}
              </div>

              <div className="flex-1">

                <div className="font-medium">

                  {stage.label}

                </div>

                <div className="text-xs text-muted-foreground">

                  {badgeText}

                </div>

              </div>

              {stage.status === "completed" && (

                <Badge
                  variant="secondary"
                  className="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300"
                >
                  Done
                </Badge>

              )}

              {stage.status === "running" && (

                <Badge>

                  Active

                </Badge>

              )}

              {stage.status === "error" && (

                <Badge variant="danger" className="font-medium">

                  Failed

                </Badge>

              )}

            </div>

          );

        })}

      </div>

    </div>
  );
}