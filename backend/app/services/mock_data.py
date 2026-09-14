import uuid
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.enterprise import Enterprise
from app.models.patent import Patent, PatentCitation
from app.models.team import TeamMember
from app.models.milestone import Milestone, MILESTONE_STAGES

INDUSTRIES = ["半导体", "航天", "生物医药", "高端装备", "新材料", "人工智能"]

SAMPLE_ENTERPRISES = [
    {
        "name": "芯动微电子",
        "industry": "半导体",
        "stage": "流片成功",
        "description": "专注于高性能模拟芯片设计，产品覆盖信号链和电源管理",
        "founded_year": 2018,
        "employee_count": 120,
        "rd_ratio": 0.35,
    },
    {
        "name": "星河航天科技",
        "industry": "航天",
        "stage": "原型验证",
        "description": "商业微小卫星研发与星座运营服务提供商",
        "founded_year": 2019,
        "employee_count": 80,
        "rd_ratio": 0.40,
    },
    {
        "name": "基因未来生物",
        "industry": "生物医药",
        "stage": "立项预研",
        "description": "基因编辑技术研发与基因治疗药物开发",
        "founded_year": 2021,
        "employee_count": 45,
        "rd_ratio": 0.50,
    },
]


def seed_mock_data(db: Session):
    if db.query(Enterprise).count() > 0:
        return

    for ep_data in SAMPLE_ENTERPRISES:
        eid = str(uuid.uuid4())
        enterprise = Enterprise(id=eid, **ep_data)
        db.add(enterprise)

        patent_count = random.randint(8, 20)
        patent_ids = []
        for i in range(patent_count):
            pid = str(uuid.uuid4())
            patent_ids.append(pid)
            patent = Patent(
                id=pid,
                enterprise_id=eid,
                patent_number=f"CN{random.randint(10000000, 99999999)}A",
                title=f"{ep_data['industry']}核心专利-{i+1}",
                ipc_class=f"H0{random.randint(1,9)}L{random.randint(1,99)}/{random.randint(1,99)}",
                cited_count=random.randint(0, 30),
                cites_count=random.randint(0, 15),
                family_size=random.randint(1, 8),
                has_international=random.random() > 0.5,
                litigation_risk=random.random() * 0.3,
                filed_at=datetime.now() - timedelta(days=random.randint(100, 1000)),
            )
            db.add(patent)

        for _ in range(patent_count * 2):
            src, tgt = random.sample(patent_ids, 2)
            db.add(PatentCitation(source_patent_id=src, target_patent_id=tgt))

        member_count = random.randint(5, 12)
        roles = ["CEO", "CTO", "首席科学家", "研发总监", "高级工程师", "算法研究员"]
        for i in range(member_count):
            db.add(TeamMember(
                id=str(uuid.uuid4()),
                enterprise_id=eid,
                name=f"成员{i+1}",
                role=roles[i % len(roles)] if i < len(roles) else "工程师",
                education=random.choice(["博士", "硕士", "博士后", "博士"]),
                is_founder=i < 2,
                paper_count=random.randint(0, 60),
                citation_count=random.randint(0, 800),
                h_index=random.randint(0, 35),
                patent_count=random.randint(0, 25),
                experience_years=random.randint(3, 20),
            ))

        for idx, stage in enumerate(MILESTONE_STAGES):
            progress = 0.0
            status = "pending"
            if idx < MILESTONE_STAGES.index(ep_data["stage"]):
                progress = 1.0
                status = "completed"
            elif idx == MILESTONE_STAGES.index(ep_data["stage"]):
                progress = random.uniform(0.3, 0.8)
                status = "in_progress"

            db.add(Milestone(
                id=str(uuid.uuid4()),
                enterprise_id=eid,
                name=f"{stage}阶段里程碑",
                stage=stage,
                description=f"{ep_data['name']}的{stage}阶段关键节点",
                expected_date=datetime.now() + timedelta(days=random.randint(-60, 180)),
                actual_date=datetime.now() - timedelta(days=random.randint(0, 90)) if status == "completed" else None,
                progress=progress,
                status=status,
                is_verified=status == "completed",
            ))

    db.commit()
