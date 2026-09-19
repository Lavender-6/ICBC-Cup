import request from './request'

export interface DashboardStats {
  total_enterprises: number
  avg_valuation: number
  max_valuation: number
  min_valuation: number
  industry_dist: Record<string, number>
  stage_dist: Record<string, number>
  risk_levels: { low: number; medium: number; high: number }
  milestone_stats: { completed: number; in_progress: number; pending: number }
  total_patents: number
  total_members: number
}

export function getDashboardStats() {
  return request.get<DashboardStats>('/stats/dashboard')
}
