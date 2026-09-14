from sqlalchemy.orm import Session
from app.models.milestone import Milestone, FinancialTool, MILESTONE_STAGES
from app.models.enterprise import Enterprise

MILESTONE_TOOLS = {
    "立项预研": [
        {"type": "知识产权质押贷", "name": "专利质押贷款", "amount_ratio": 0.15},
        {"type": "政府补贴", "name": "研发补贴对接", "amount_ratio": 0.05},
    ],
    "原型验证": [
        {"type": "AI动态估值授信", "name": "AI估值授信贷款", "amount_ratio": 0.25},
        {"type": "股权融资", "name": "VC跟投", "amount_ratio": 0.20},
    ],
    "流片成功": [
        {"type": "投贷联动", "name": "银行授信+VC跟投", "amount_ratio": 0.40},
        {"type": "保险", "name": "研发中断险", "amount_ratio": 0.10},
    ],
    "商业化量产": [
        {"type": "供应链金融", "name": "供应链票据", "amount_ratio": 0.30},
        {"type": "订单融资", "name": "订单融资贷款", "amount_ratio": 0.25},
    ],
    "上市预备": [
        {"type": "可转债", "name": "科创可转债", "amount_ratio": 0.50},
        {"type": "债券", "name": "科创专项债券", "amount_ratio": 0.30},
    ],
}


def get_tools_for_stage(stage: str) -> list[dict]:
    return MILESTONE_TOOLS.get(stage, [])


def trigger_financial_tools(db: Session, milestone_id: str) -> list[FinancialTool]:
    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone or not milestone.is_verified:
        return []

    enterprise = db.query(Enterprise).filter(Enterprise.id == milestone.enterprise_id).first()
    if not enterprise:
        return []

    base_valuation = enterprise.current_valuation or enterprise.base_valuation or 0
    tools_config = get_tools_for_stage(milestone.stage)

    existing = db.query(FinancialTool).filter(FinancialTool.milestone_id == milestone_id).all()
    if existing:
        return existing

    created = []
    for cfg in tools_config:
        tool = FinancialTool(
            id=milestone_id + "_" + cfg["type"],
            milestone_id=milestone_id,
            tool_type=cfg["type"],
            tool_name=cfg["name"],
            amount=round(base_valuation * cfg["amount_ratio"], 2),
            conditions=f"触发条件: {milestone.name}验收通过",
            is_triggered=True,
        )
        db.add(tool)
        created.append(tool)

    db.commit()
    return created


def check_milestone_alerts(milestone: Milestone) -> list[dict]:
    alerts = []
    if milestone.expected_date and milestone.actual_date:
        if milestone.actual_date > milestone.expected_date:
            delay_days = (milestone.actual_date - milestone.expected_date).days
            alerts.append({
                "type": "milestone_delay",
                "severity": "warning" if delay_days < 30 else "critical",
                "message": f"里程碑 '{milestone.name}' 延迟 {delay_days} 天",
            })
    if milestone.progress < 0.3 and milestone.status == "in_progress":
        alerts.append({
            "type": "low_progress",
            "severity": "warning",
            "message": f"里程碑 '{milestone.name}' 进度偏低 ({milestone.progress:.0%})",
        })
    return alerts
