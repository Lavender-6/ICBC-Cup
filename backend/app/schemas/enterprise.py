from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EnterpriseBase(BaseModel):
    name: str
    industry: str
    stage: str = "立项预研"
    description: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    rd_ratio: Optional[float] = 0.0
    patent_count: Optional[int] = 10


class EnterpriseResponse(EnterpriseBase):
    id: str
    base_valuation: float = 0
    current_valuation: float = 0
    risk_score: float = 0
    created_at: datetime

    class Config:
        from_attributes = True


class ValuationResponse(BaseModel):
    base_valuation: float
    current_valuation: float
    risk_score: float
    patent_count: int
    avg_patent_quality: float
    team_score: float
    industry_multiplier: float
    stage_multiplier: float
    components: dict


class TeamPortraitResponse(BaseModel):
    members: list[dict]
    team_score: float
    total_papers: int
    total_patents: int
    total_citations: int
    avg_h_index: float


class PatentNetworkResponse(BaseModel):
    nodes: list[dict]
    edges: list[dict]
    total_patents: int
    total_citations: int
    avg_cited: float
    max_pagerank: float


class MilestoneResponse(BaseModel):
    id: str
    enterprise_id: str
    name: str
    stage: str
    description: Optional[str] = None
    progress: float
    status: str
    is_verified: bool
    expected_date: Optional[datetime] = None
    actual_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class FinancialToolResponse(BaseModel):
    id: str
    tool_type: str
    tool_name: str
    amount: float
    conditions: Optional[str] = None
    is_triggered: bool

    class Config:
        from_attributes = True


class CreditSimulateRequest(BaseModel):
    enterprise_id: str
    milestone_progress: float = 0.0


class CreditResponse(BaseModel):
    base_amount: float
    progress_factor: float
    risk_factor: float
    final_amount: float
    enterprise_name: Optional[str] = None
    base_valuation: Optional[float] = None
    risk_score: Optional[float] = None


class RiskAlertResponse(BaseModel):
    id: str
    alert_type: str
    severity: str
    message: str
    is_resolved: str
    created_at: datetime

    class Config:
        from_attributes = True
