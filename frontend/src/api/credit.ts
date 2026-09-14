import request from './request'

export interface CreditResult {
  base_amount: number
  progress_factor: number
  risk_factor: number
  final_amount: number
  enterprise_name?: string
  base_valuation?: number
  risk_score?: number
}

export interface RiskAlert {
  id: string
  alert_type: string
  severity: string
  message: string
  is_resolved: string
  created_at: string
}

export function simulateCredit(enterpriseId: string, progress: number) {
  return request.post<CreditResult>('/credit/simulate', {
    enterprise_id: enterpriseId,
    milestone_progress: progress,
  })
}

export function getCreditHistory(enterpriseId: string) {
  return request.get(`/credit/history/${enterpriseId}`)
}

export function getAlerts(enterpriseId: string) {
  return request.get<RiskAlert[]>(`/credit/alerts/${enterpriseId}`)
}

export function checkAlerts(enterpriseId: string) {
  return request.post(`/credit/alerts/${enterpriseId}/check`)
}
