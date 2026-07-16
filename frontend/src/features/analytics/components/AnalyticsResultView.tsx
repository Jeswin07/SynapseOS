import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { DollarSign, Users, Star, Truck } from "lucide-react";
import { MetricCard } from "@/components/common/MetricCard";
import { ChartCard } from "@/components/common/ChartCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { EmptyState } from "@/components/common/EmptyState";
import type { AnalyticsResult } from "@/types/api";
import { formatCurrency, formatCompactNumber, formatPercent } from "@/utils/format";

const CHART_COLOR = "hsl(221 83% 45%)";

function objectToChartData(obj?: Record<string, number>) {
  if (!obj) return [];
  return Object.entries(obj).map(([name, value]) => ({ name, value }));
}

export function AnalyticsResultView({ result }: { result: AnalyticsResult }) {
  const hasAnyData = Object.keys(result).length > 0;

  if (!hasAnyData) {
    return <EmptyState title="No analytics available" description="This dataset returned no analyzable metrics." />;
  }

  const revenueTrend = objectToChartData(result.trends?.monthly_revenue);
  const topCategories = objectToChartData(result.products?.top_categories_by_revenue);
  const topSellers = objectToChartData(result.sellers?.top_sellers_by_revenue);
  const geography = objectToChartData(result.geography?.top_regions);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {result.revenue && (
          <MetricCard label="Total revenue" value={formatCurrency(result.revenue.total_revenue)} icon={DollarSign} />
        )}
        {result.customers && (
          <MetricCard label="Total customers" value={formatCompactNumber(result.customers.total_customers)} icon={Users} />
        )}
        {result.reviews && (
          <MetricCard label="Average rating" value={result.reviews.average_rating.toFixed(1)} icon={Star} />
        )}
        {result.operations?.average_delivery_days !== undefined && (
          <MetricCard
            label="Avg. delivery days"
            value={result.operations.average_delivery_days.toFixed(1)}
            icon={Truck}
          />
        )}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {revenueTrend.length > 0 && (
          <ChartCard title="Monthly revenue trend" description="Revenue over time" className="lg:col-span-2">
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={revenueTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <YAxis tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" tickFormatter={(v) => formatCompactNumber(v)} />
                <Tooltip
                  contentStyle={{ borderRadius: 8, borderColor: "hsl(var(--border))", fontSize: 13 }}
                  formatter={(v: number) => formatCurrency(v)}
                />
                <Line type="monotone" dataKey="value" stroke={CHART_COLOR} strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>
        )}

        {topCategories.length > 0 && (
          <ChartCard title="Top categories by revenue">
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={topCategories} layout="vertical" margin={{ left: 24 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" tickFormatter={(v) => formatCompactNumber(v)} />
                <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <Tooltip contentStyle={{ borderRadius: 8, borderColor: "hsl(var(--border))", fontSize: 13 }} formatter={(v: number) => formatCurrency(v)} />
                <Bar dataKey="value" fill={CHART_COLOR} radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        )}

        {topSellers.length > 0 && (
          <ChartCard title="Top sellers by revenue">
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={topSellers} layout="vertical" margin={{ left: 24 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" tickFormatter={(v) => formatCompactNumber(v)} />
                <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <Tooltip contentStyle={{ borderRadius: 8, borderColor: "hsl(var(--border))", fontSize: 13 }} formatter={(v: number) => formatCurrency(v)} />
                <Bar dataKey="value" fill="hsl(152 60% 36%)" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        )}

        {geography.length > 0 && (
          <ChartCard title="Top regions" description="Order volume by region">
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={geography}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="name" tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <YAxis tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" tickFormatter={(v) => formatCompactNumber(v)} />
                <Tooltip contentStyle={{ borderRadius: 8, borderColor: "hsl(var(--border))", fontSize: 13 }} />
                <Bar dataKey="value" fill="hsl(38 92% 50%)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        )}
      </div>

      {result.customers && (
        <Card>
          <CardHeader>
            <CardTitle>Customer retention</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-6 text-sm">
            <div>
              <p className="text-muted-foreground">Repeat customers</p>
              <p className="text-lg font-semibold text-foreground">{formatCompactNumber(result.customers.repeat_customers)}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Repeat rate</p>
              <p className="text-lg font-semibold text-foreground">{formatPercent(result.customers.repeat_customer_rate, false)}</p>
            </div>
          </CardContent>
        </Card>
      )}

      {result.insights && result.insights.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>AI-generated insights</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {result.insights.map((insight, idx) => (
                <li key={idx} className="flex gap-2 text-sm text-foreground">
                  <span className="text-primary">•</span>
                  {insight}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
