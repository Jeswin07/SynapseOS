import { Dispatch, SetStateAction, useEffect } from "react";

import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import type { DatasetFilters } from "@/types/api";
import type { AnalyticsFilterOptions } from "@/services/analytics.service";

interface Props {
  filters: DatasetFilters;
  setFilters: Dispatch<SetStateAction<DatasetFilters>>;

  filterOptions?: AnalyticsFilterOptions;
  isLoading?: boolean;
}

export function AnalyticsFilters({
  filters,
  setFilters,
  filterOptions,
  isLoading = false,
}: Props) {
  function update<K extends keyof DatasetFilters>(
    key: K,
    value: DatasetFilters[K],
  ) {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  }

  function resetFilters() {
    setFilters({
      date_from: filterOptions?.date?.min ?? undefined,
      date_to: filterOptions?.date?.max ?? undefined,
    });
  }

  useEffect(() => {
    if (!filterOptions?.date) return;

    setFilters((prev) => ({
      ...prev,
      date_from: prev.date_from ?? filterOptions.date.min ?? undefined,
      date_to: prev.date_to ?? filterOptions.date.max ?? undefined,
    }));
  }, [filterOptions, setFilters]);

  return (
    <Card className="mb-6">
      <CardContent className="grid gap-4 pt-6 md:grid-cols-2 lg:grid-cols-4">

        {/* ---------------- DATE FROM ---------------- */}

        <div className="space-y-2">
          <Label>Date From</Label>

          <Input
            type="date"
            value={filters.date_from ?? ""}
            min={filterOptions?.date?.min ?? undefined}
            max={filterOptions?.date?.max ?? undefined}
            onChange={(e) =>
              update(
                "date_from",
                e.target.value || undefined,
              )
            }
          />

          {filterOptions?.date?.enabled && (
            <p className="text-xs text-muted-foreground">
              Earliest: {filterOptions.date.min}
            </p>
          )}
        </div>

        {/* ---------------- DATE TO ---------------- */}

        <div className="space-y-2">
          <Label>Date To</Label>

          <Input
            type="date"
            value={filters.date_to ?? ""}
            min={filterOptions?.date?.min ?? undefined}
            max={filterOptions?.date?.max ?? undefined}
            onChange={(e) =>
              update(
                "date_to",
                e.target.value || undefined,
              )
            }
          />

          {filterOptions?.date?.enabled && (
            <p className="text-xs text-muted-foreground">
              Latest: {filterOptions.date.max}
            </p>
          )}
        </div>

        {/* ---------------- STATES ---------------- */}

        <div className="space-y-2">
          <Label>State</Label>

          <Select
            disabled={
              isLoading ||
              !filterOptions?.states?.enabled
            }
            value={filters.states?.[0] ?? ""}
            onValueChange={(value) =>
              update(
                "states",
                value === "__all__"
                    ? undefined
                    : [value],
                )
            }
          >
            <SelectTrigger>
              <SelectValue placeholder="All States" />
            </SelectTrigger>

            <SelectContent>

              <SelectItem value="__all__">
                All States
              </SelectItem>

              {filterOptions?.states?.values.map(
                (state) => (
                  <SelectItem
                    key={state}
                    value={state}
                  >
                    {state}
                  </SelectItem>
                ),
              )}

            </SelectContent>
          </Select>
        </div>

        {/* ---------------- CATEGORY ---------------- */}

        <div className="space-y-2">
          <Label>Category</Label>

          <Select
            disabled={
              isLoading ||
              !filterOptions?.categories?.enabled
            }
            value={filters.categories?.[0] ?? ""}
            onValueChange={(value) =>
              update(
                "categories",
                value === "__all__"
                    ? undefined
                    : [value],
                )
            }
          >
            <SelectTrigger>
              <SelectValue placeholder="All Categories" />
            </SelectTrigger>

            <SelectContent>

              <SelectItem value="__all__">
                All Categories
              </SelectItem>

              {filterOptions?.categories?.values.map(
                (category) => (
                  <SelectItem
                    key={category}
                    value={category}
                  >
                    {category}
                  </SelectItem>
                ),
              )}

            </SelectContent>
          </Select>
        </div>

        {/* ---------------- MIN REVENUE ---------------- */}

        <div className="space-y-2">
          <Label>Minimum Revenue</Label>

          <Input
            type="number"
            min={
              filterOptions?.revenue?.min ??
              undefined
            }
            max={
              filterOptions?.revenue?.max ??
              undefined
            }
            placeholder={
              filterOptions?.revenue?.enabled
                ? String(
                    filterOptions.revenue.min,
                  )
                : "Minimum"
            }
            value={filters.min_revenue ?? ""}
            onChange={(e) =>
              update(
                "min_revenue",
                e.target.value
                  ? Number(e.target.value)
                  : undefined,
              )
            }
          />

          {filterOptions?.revenue?.enabled && (
            <p className="text-xs text-muted-foreground">
              Dataset Range:
              {" "}
              {filterOptions.revenue.min}
              {" - "}
              {filterOptions.revenue.max}
            </p>
          )}
        </div>

        {/* ---------------- MAX REVENUE ---------------- */}

        <div className="space-y-2">
          <Label>Maximum Revenue</Label>

          <Input
            type="number"
            min={
              filterOptions?.revenue?.min ??
              undefined
            }
            max={
              filterOptions?.revenue?.max ??
              undefined
            }
            placeholder={
              filterOptions?.revenue?.enabled
                ? String(
                    filterOptions.revenue.max,
                  )
                : "Maximum"
            }
            value={filters.max_revenue ?? ""}
            onChange={(e) =>
              update(
                "max_revenue",
                e.target.value
                  ? Number(e.target.value)
                  : undefined,
              )
            }
          />
        </div>

        {/* ---------------- MIN REVIEW ---------------- */}

        <div className="space-y-2">
          <Label>Minimum Review</Label>

          <Input
            type="number"
            step="0.1"
            min={
              filterOptions?.review_score
                ?.min ?? 1
            }
            max={
              filterOptions?.review_score
                ?.max ?? 5
            }
            value={
              filters.min_review_score ?? ""
            }
            onChange={(e) =>
              update(
                "min_review_score",
                e.target.value
                  ? Number(e.target.value)
                  : undefined,
              )
            }
          />

          {filterOptions?.review_score
            ?.enabled && (
            <p className="text-xs text-muted-foreground">
              Dataset Range:
              {" "}
              {filterOptions.review_score.min}
              {" - "}
              {filterOptions.review_score.max}
            </p>
          )}
        </div>

        {/* ---------------- MAX REVIEW ---------------- */}

        <div className="space-y-2">
          <Label>Maximum Review</Label>

          <Input
            type="number"
            step="0.1"
            min={
              filterOptions?.review_score
                ?.min ?? 1
            }
            max={
              filterOptions?.review_score
                ?.max ?? 5
            }
            value={
              filters.max_review_score ?? ""
            }
            onChange={(e) =>
              update(
                "max_review_score",
                e.target.value
                  ? Number(e.target.value)
                  : undefined,
              )
            }
          />
        </div>

        {/* ---------------- ACTIONS ---------------- */}

        <div className="flex items-end lg:col-span-4">
          <Button
            type="button"
            variant="outline"
            onClick={resetFilters}
          >
            Reset Filters
          </Button>
        </div>
              </CardContent>
    </Card>
  );
}
