import { Lightbulb } from "lucide-react";

export function RecommendationsList({ recommendations }: { recommendations: string[] }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="mt-3 space-y-2 rounded-lg border border-primary/20 bg-primary/5 p-3">
      <p className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-primary">
        <Lightbulb className="h-3.5 w-3.5" /> Recommendations
      </p>
      <ul className="space-y-1.5">
        {recommendations.map((rec, idx) => (
          <li key={idx} className="flex gap-2 text-sm text-foreground">
            <span className="text-primary">•</span>
            {rec}
          </li>
        ))}
      </ul>
    </div>
  );
}
