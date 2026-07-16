import { useQuery } from "@tanstack/react-query";
import { riskService } from "@/services/risk.service";

export function useRiskAnalysis(enabled = true) {
  return useQuery({ queryKey: ["risks", "analyze"], queryFn: riskService.analyze, enabled });
}
