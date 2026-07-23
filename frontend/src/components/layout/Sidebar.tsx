import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Sparkles,
  Database,
  BookOpen,
  BarChart3,
  TrendingUp,
  Target,
  Users,
  Settings,
  ChevronsLeft,
  ChevronsRight,
  Boxes,
} from "lucide-react";
import { useLayoutStore } from "@/stores/layout.store";
import { useAuthStore } from "@/stores/auth.store";
import { cn } from "@/utils/cn";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/assistant", label: "AI Assistant", icon: Sparkles, highlight: true },
  { to: "/datasets", label: "Datasets", icon: Database },
  { to: "/knowledge", label: "Knowledge", icon: BookOpen },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/forecasting", label: "Forecasting", icon: TrendingUp },
  { to: "/prediction", label: "Prediction", icon: Target },
  { to: "/users", label: "Users", icon: Users },
  { to: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar, mobileSidebarOpen, setMobileSidebarOpen } = useLayoutStore();
  const fullName = useAuthStore((s) => s.fullName);
  const role = useAuthStore((s) => s.role);

  return (
    <>
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-950/50 lg:hidden"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 flex flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground transition-all duration-200",
          sidebarCollapsed ? "w-[72px]" : "w-64",
          "lg:translate-x-0",
          mobileSidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        <div className="flex h-14 items-center gap-2 border-b border-sidebar-border px-4">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Boxes className="h-4 w-4" />
          </div>
          {!sidebarCollapsed && <span className="text-sm font-semibold tracking-tight">SynapseOS</span>}
        </div>

        <nav className="flex-1 space-y-0.5 overflow-y-auto px-2.5 py-4 scrollbar-thin">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={() => setMobileSidebarOpen(false)}
              className={({ isActive }) =>
                cn(
                  "group flex items-center gap-3 rounded-lg px-2.5 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-sidebar-accent text-white"
                    : "text-sidebar-foreground/70 hover:bg-sidebar-accent/60 hover:text-white"
                )
              }
            >
              <item.icon className={cn("h-4 w-4 shrink-0", item.highlight && "text-primary")} />
              {!sidebarCollapsed && <span className="truncate">{item.label}</span>}
              {!sidebarCollapsed && item.highlight && (
                <span className="ml-auto rounded bg-primary/20 px-1.5 py-0.5 text-[10px] font-semibold text-primary">
                  AI
                </span>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-sidebar-border p-3">
          {!sidebarCollapsed && (
            <div className="mb-2 rounded-lg bg-sidebar-accent/60 px-2.5 py-2">
              <p className="truncate text-xs font-medium text-white">{fullName ?? "Signed in"}</p>
              <p className="truncate text-[11px] text-sidebar-foreground/60">{role ?? ""}</p>
            </div>
          )}
          <button
            onClick={toggleSidebar}
            className="hidden w-full items-center justify-center gap-2 rounded-lg py-1.5 text-xs text-sidebar-foreground/60 transition-colors hover:bg-sidebar-accent/60 hover:text-white lg:flex"
          >
            {sidebarCollapsed ? <ChevronsRight className="h-4 w-4" /> : <ChevronsLeft className="h-4 w-4" />}
          </button>
        </div>
      </aside>
    </>
  );
}
