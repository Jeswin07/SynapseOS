import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, Award, BarChart3, Activity } from "lucide-react";

interface Props {
  summary?: {
    forecast_days: number;
    total_expected_value: number;
    average_daily_value: number;
    highest_period: {
      prediction: number;
    };
    lowest_expected_period: {
      prediction: number;
    };
  };

  evaluation?: {
    performance_score: number;
    performance_label: string;
  };
}

export function ForecastSummaryCards({
  summary,
  evaluation,
}: Props) {
  if (!summary || !evaluation) return null;

  return (
    <div className="mb-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm">
            Model Performance
          </CardTitle>
          <Award className="h-4 w-4" />
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            {evaluation.performance_score}/100
          </p>

          <p className="text-muted-foreground">
            {evaluation.performance_label}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm">
            Expected Total
          </CardTitle>

          <TrendingUp className="h-4 w-4" />
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            {summary.total_expected_value.toLocaleString()}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm">
            Average / Period
          </CardTitle>

          <BarChart3 className="h-4 w-4" />
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            {summary.average_daily_value.toLocaleString()}
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm">
            Highest Forecast
          </CardTitle>

          <Activity className="h-4 w-4" />
        </CardHeader>

        <CardContent>
          <p className="text-3xl font-bold">
            {summary.highest_period.prediction.toLocaleString()}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}