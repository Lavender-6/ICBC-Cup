import networkx as nx
import numpy as np
from sqlalchemy.orm import Session
from app.models.patent import Patent, PatentCitation


def build_patent_graph(patents: list[Patent], citations: list[PatentCitation]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for p in patents:
        graph.add_node(
            p.id,
            title=p.title or p.patent_number,
            ipc=p.ipc_class or "",
            cited_count=p.cited_count or 0,
            quality=p.quality_score or 0.0,
        )
    for c in citations:
        if graph.has_node(c.source_patent_id) and graph.has_node(c.target_patent_id):
            graph.add_edge(c.source_patent_id, c.target_patent_id)
    return graph


def compute_pagerank(graph: nx.DiGraph) -> dict[str, float]:
    if graph.number_of_nodes() == 0:
        return {}
    try:
        return nx.pagerank(graph, alpha=0.85, max_iter=100)
    except nx.PowerIterationFailedConvergence:
        return {n: 1.0 / graph.number_of_nodes() for n in graph.nodes()}


def compute_network_metrics(graph: nx.DiGraph) -> dict:
    pagerank = compute_pagerank(graph)
    in_degree = dict(graph.in_degree())
    out_degree = dict(graph.out_degree())

    try:
        betweenness = nx.betweenness_centrality(graph)
    except Exception:
        betweenness = {n: 0.0 for n in graph.nodes()}

    nodes = []
    for node_id in graph.nodes():
        data = graph.nodes[node_id]
        nodes.append({
            "id": node_id,
            "title": data.get("title", ""),
            "ipc": data.get("ipc", ""),
            "pagerank": round(pagerank.get(node_id, 0.0), 6),
            "in_degree": in_degree.get(node_id, 0),
            "out_degree": out_degree.get(node_id, 0),
            "betweenness": round(betweenness.get(node_id, 0.0), 6),
            "quality": data.get("quality", 0.0),
        })

    edges = [{"source": u, "target": v} for u, v in graph.edges()]

    return {
        "nodes": nodes,
        "edges": edges,
        "total_patents": graph.number_of_nodes(),
        "total_citations": graph.number_of_edges(),
        "avg_cited": round(np.mean(list(in_degree.values())) if in_degree else 0, 2),
        "max_pagerank": round(max(pagerank.values()) if pagerank else 0, 6),
    }


def evaluate_patent_quality(patent: Patent, pagerank_score: float = 0.0) -> float:
    cited_score = min((patent.cited_count or 0) / 20.0, 1.0)
    family_score = min((patent.family_size or 1) / 10.0, 1.0)
    intl_score = 1.0 if patent.has_international else 0.5
    litigation_penalty = 1.0 - (patent.litigation_risk or 0.0)
    pr_score = min(pagerank_score * 100, 1.0)

    quality = (
        0.30 * cited_score
        + 0.20 * family_score
        + 0.15 * intl_score
        + 0.25 * pr_score
        + 0.10 * litigation_penalty
    )
    return round(max(0.0, min(1.0, quality)), 4)


def get_enterprise_patent_network(db: Session, enterprise_id: str) -> dict:
    patents = db.query(Patent).filter(Patent.enterprise_id == enterprise_id).all()
    if not patents:
        return {"nodes": [], "edges": [], "total_patents": 0, "total_citations": 0, "avg_cited": 0, "max_pagerank": 0}

    patent_ids = [p.id for p in patents]
    citations = (
        db.query(PatentCitation)
        .filter(PatentCitation.source_patent_id.in_(patent_ids))
        .filter(PatentCitation.target_patent_id.in_(patent_ids))
        .all()
    )

    graph = build_patent_graph(patents, citations)
    metrics = compute_network_metrics(graph)

    pagerank = compute_pagerank(graph)
    for p in patents:
        pr = pagerank.get(p.id, 0.0)
        p.quality_score = evaluate_patent_quality(p, pr)
    db.commit()

    return metrics
