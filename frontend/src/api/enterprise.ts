import request from './request'

export interface Enterprise {
  id: string
  name: string
  industry: string
  stage: string
  description?: string
  founded_year?: number
  employee_count?: number
  rd_ratio?: number
  base_valuation: number
  current_valuation: number
  risk_score: number
  created_at: string
}

export interface Valuation {
  base_valuation: number
  current_valuation: number
  risk_score: number
  patent_count: number
  avg_patent_quality: number
  team_score: number
  industry_multiplier: number
  stage_multiplier: number
  components: {
    patent_valuation: number
    team_valuation: number
    rd_valuation: number
  }
}

export interface TeamPortrait {
  members: any[]
  team_score: number
  total_papers: number
  total_patents: number
  total_citations: number
  avg_h_index: number
}

export interface PatentNetwork {
  nodes: any[]
  edges: any[]
  total_patents: number
  total_citations: number
  avg_cited: number
  max_pagerank: number
}

export function getEnterprises() {
  return request.get<Enterprise[]>('/enterprises')
}

export function getEnterprise(id: string) {
  return request.get<Enterprise>(`/enterprises/${id}`)
}

export function getValuation(id: string) {
  return request.get<Valuation>(`/enterprises/${id}/valuation`)
}

export function getTeam(id: string) {
  return request.get<TeamPortrait>(`/enterprises/${id}/team`)
}

export function getPatents(id: string) {
  return request.get<PatentNetwork>(`/enterprises/${id}/patents`)
}
