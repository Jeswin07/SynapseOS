import type { ReactNode } from "react";
import { Boxes, Sparkles, TrendingUp, ShieldCheck } from "lucide-react";

const HIGHLIGHTS = [
  { icon: Sparkles, text: "Multi-agent AI assistant grounded in your enterprise data" },
  { icon: TrendingUp, text: "Forecasting, prediction, and scenario planning in one workspace" },
  { icon: ShieldCheck, text: "Enterprise-grade access control across teams and tenants" },
];

export function AuthLayout({ children, title, subtitle }: { children: ReactNode; title: string; subtitle: string }) {
  return (
    <div className="grid min-h-screen grid-cols-1 lg:grid-cols-2">
      <div className="hidden flex-col justify-between bg-sidebar p-10 text-sidebar-foreground lg:flex">
        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Boxes className="h-5 w-5" />
          </div>
          <span className="text-lg font-semibold text-white">SynapseOS</span>
        </div>
        <div className="space-y-6">
          <h2 className="text-3xl font-semibold leading-tight text-white text-balance">
            Enterprise decision intelligence, powered by AI.
          </h2>
          <ul className="space-y-4">
            {HIGHLIGHTS.map((h) => (
              <li key={h.text} className="flex items-start gap-3 text-sm text-sidebar-foreground/80">
                <div className="mt-0.5 rounded-md bg-sidebar-accent p-1.5 text-primary">
                  <h.icon className="h-3.5 w-3.5" />
                </div>
                {h.text}
              </li>
            ))}
          </ul>
        </div>
        <p className="text-xs text-sidebar-foreground/40">© {new Date().getFullYear()} SynapseOS. All rights reserved.</p>
      </div>

      <div className="flex flex-col items-center justify-center p-6 sm:p-10">
        <div className="w-full max-w-sm space-y-6">
          <div className="space-y-1.5 text-center lg:text-left">
            <h1 className="text-2xl font-semibold tracking-tight text-foreground">{title}</h1>
            <p className="text-sm text-muted-foreground">{subtitle}</p>
          </div>
          {children}
        </div>
      </div>
    </div>
  );
}
