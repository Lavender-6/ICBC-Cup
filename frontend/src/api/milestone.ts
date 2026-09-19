import request from './request'

export interface Milestone {
  id: string
  enterprise_id: string
  name: string
  stage: string
  description?: string
  progress: number
  status: string
  is_verified: boolean
  expected_date?: string
  actual_date?: string
}

export interface FinancialTool {
  id: string
  tool_type: string
  tool_name: string
  amount: number
  conditions?: string
  is_triggered: boolean
}

export function getMilestones(enterpriseId: string) {
  return request.get<Milestone[]>(`/milestones/${enterpriseId}`)
}

export function createMilestone(enterpriseId: string, data: { name: string; stage: string; description?: string }) {
  return request.post<Milestone>(`/milestones/${enterpriseId}`, data)
}

export function updateProgress(milestoneId: string, progress: number) {
  return request.put<Milestone>(`/milestones/${milestoneId}/progress?progress=${progress}`)
}

export function deleteMilestone(milestoneId: string) {
  return request.delete(`/milestones/${milestoneId}`)
}

export function getTools(milestoneId: string) {
  return request.get<FinancialTool[]>(`/milestones/${milestoneId}/tools`)
}

export function getStages() {
  return request.get<string[]>('/milestones/stages/list')
}
