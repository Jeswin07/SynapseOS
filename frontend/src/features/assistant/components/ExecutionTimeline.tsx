import {
  Check,
  Loader2,
  AlertCircle,
} from "lucide-react";

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
    <div className="rounded-xl border border-border bg-muted/30 p-4">
      <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
        Agent execution
      </p>

      <ol className="space-y-2">
        {stages.map((stage) => {
          let icon;
          let color = "";

          switch (stage.status) {
            case "completed":
              icon = (
                <Check className="h-3 w-3" />
              );

              color =
                "border-green-500 bg-green-500/10 text-green-600";

              break;

            case "running":
              icon = (
                <Loader2 className="h-3 w-3 animate-spin" />
              );

              color =
                "border-blue-500 bg-blue-500/10 text-blue-600";

              break;

            case "error":
              icon = (
                <AlertCircle className="h-3 w-3" />
              );

              color =
                "border-red-500 bg-red-500/10 text-red-600";

              break;
          }

          return (
            <li
              key={stage.id}
              className="flex items-center gap-2"
            >
              <span
                className={`flex h-5 w-5 items-center justify-center rounded-full border ${color}`}
              >
                {icon}
              </span>

              <span className="text-sm">
                {stage.label}
              </span>
            </li>
          );
        })}
      </ol>

      {isActive && (
        <p className="mt-3 flex items-center gap-2 text-xs text-muted-foreground">
          <Loader2 className="h-3 w-3 animate-spin" />
          Running...
        </p>
      )}
    </div>
  );
}