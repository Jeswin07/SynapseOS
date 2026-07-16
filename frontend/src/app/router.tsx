import { lazy, Suspense } from "react";
import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { ProtectedRoute } from "@/app/ProtectedRoute";
import { PageSkeleton } from "@/components/common/LoadingSkeleton";

const LoginPage = lazy(() => import("@/features/auth/pages/LoginPage"));
const RegisterPage = lazy(() => import("@/features/auth/pages/RegisterPage"));
const DashboardPage = lazy(() => import("@/features/dashboard/pages/DashboardPage"));
const AssistantPage = lazy(() => import("@/features/assistant/pages/AssistantPage"));
const DatasetsPage = lazy(() => import("@/features/datasets/pages/DatasetsPage"));
const DatasetDetailPage = lazy(() => import("@/features/datasets/pages/DatasetDetailPage"));
const KnowledgePage = lazy(() => import("@/features/knowledge/pages/KnowledgePage"));
const AnalyticsPage = lazy(() => import("@/features/analytics/pages/AnalyticsPage"));
const ForecastingPage = lazy(() => import("@/features/forecasting/pages/ForecastingPage"));
const PredictionPage = lazy(() => import("@/features/prediction/pages/PredictionPage"));
const ScenarioPage = lazy(() => import("@/features/scenario/pages/ScenarioPage"));
const UsersPage = lazy(() => import("@/features/users/pages/UsersPage"));
const SettingsPage = lazy(() => import("@/features/settings/pages/SettingsPage"));
const NotFoundPage = lazy(() => import("@/features/misc/NotFoundPage"));

function withSuspense(node: React.ReactNode) {
  return <Suspense fallback={<PageSkeleton />}>{node}</Suspense>;
}

const router = createBrowserRouter([
  { path: "/", element: <Navigate to="/dashboard" replace /> },
  { path: "/login", element: withSuspense(<LoginPage />) },
  { path: "/register", element: withSuspense(<RegisterPage />) },
  {
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      { path: "/dashboard", element: withSuspense(<DashboardPage />) },
      { path: "/assistant", element: withSuspense(<AssistantPage />) },
      { path: "/datasets", element: withSuspense(<DatasetsPage />) },
      { path: "/datasets/:datasetId", element: withSuspense(<DatasetDetailPage />) },
      { path: "/knowledge", element: withSuspense(<KnowledgePage />) },
      { path: "/analytics", element: withSuspense(<AnalyticsPage />) },
      { path: "/forecasting", element: withSuspense(<ForecastingPage />) },
      { path: "/prediction", element: withSuspense(<PredictionPage />) },
      { path: "/scenario", element: withSuspense(<ScenarioPage />) },
      { path: "/users", element: withSuspense(<UsersPage />) },
      { path: "/settings", element: withSuspense(<SettingsPage />) },
    ],
  },
  { path: "*", element: withSuspense(<NotFoundPage />) },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
