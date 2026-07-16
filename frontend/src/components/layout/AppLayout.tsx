import { Outlet } from "react-router-dom";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopNavbar } from "@/components/layout/TopNavbar";
import { useLayoutStore } from "@/stores/layout.store";
import { cn } from "@/utils/cn";

export function AppLayout() {
  const sidebarCollapsed = useLayoutStore((s) => s.sidebarCollapsed);

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <div className={cn("flex min-h-screen flex-col transition-all duration-200", sidebarCollapsed ? "lg:pl-[72px]" : "lg:pl-64")}>
        <TopNavbar />
        <main className="flex-1 p-4 sm:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
