import networkx as nx
import numpy as np


def build_citation_graph(patents: list[dict], citations: list[tuple]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for p in patents:
        graph.add_node(p["id"], **p)
    for src, tgt in citations:
        graph.add_edge(src, tgt)
    return graph


def compute_centrality(graph: nx.DiGraph) -> dict:
    try:
        pagerank = nx.pagerank(graph, alpha=0.85, max_iter=100)
    except Exception:
        pagerank = {n: 0 for n in graph.nodes()}

    try:
        betweenness = nx.betweenness_centrality(graph)
    except Exception:
        betweenness = {n: 0 for n in graph.nodes()}

    in_degree = dict(graph.in_degree())
    return {
        "pagerank": pagerank,
        "betweenness": betweenness,
        "in_degree": in_degree,
    }


def compute_network_value(graph: nx.DiGraph, centrality: dict) -> float:
    if graph.number_of_nodes() == 0:
        return 0.0
    pr_values = list(centrality["pagerank"].values())
    avg_pr = np.mean(pr_values)
    max_pr = np.max(pr_values)
    density = nx.density(graph)
    return float(avg_pr * 0.4 + max_pr * 0.3 + density * 0.3)


def identify_core_patents(graph: nx.DiGraph, centrality: dict, top_k: int = 5) -> list:
    nodes = []
    for node_id in graph.nodes():
        nodes.append({
            "id": node_id,
            "pagerank": centrality["pagerank"].get(node_id, 0),
            "betweenness": centrality["betweenness"].get(node_id, 0),
            "in_degree": centrality["in_degree"].get(node_id, 0),
        })
    nodes.sort(key=lambda x: x["pagerank"], reverse=True)
    return nodes[:top_k]


if __name__ == "__main__":
    sample_patents = [{"id": f"p{i}", "title": f"Patent {i}"} for i in range(10)]
    sample_citations = [(f"p{i}", f"p{(i+1)%10}") for i in range(10)]
    graph = build_citation_graph(sample_patents, sample_citations)
    centrality = compute_centrality(graph)
    print(f"Network value: {compute_network_value(graph, centrality):.4f}")
    print(f"Core patents: {[p['id'] for p in identify_core_patents(graph, centrality)]}")
