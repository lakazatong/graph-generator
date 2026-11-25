from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    import networkx as nx
    import numpy as np

from ggen.graphs.interfaces import TransformSpec

Strategy = Literal["by_label", "random_order", "min_in_degree"]


@dataclass(frozen=True)
class Params:
    strategy: Strategy


def parse_params(raw: dict[str, Any]) -> Params:
    s = raw.get("strategy", "random_order")
    if s not in ("by_label", "random_order", "min_in_degree"):
        raise ValueError(f"Unknown to_dag strategy: {s!r}")
    return Params(strategy=s)


def apply(graph: nx.Graph, params: Params, rng: np.random.Generator) -> nx.DiGraph:
    import networkx as nx

    if not graph.is_directed():
        raise TypeError("to_dag expects a directed graph")
    assert isinstance(graph, nx.DiGraph)

    out = nx.DiGraph()
    out.add_nodes_from(graph.nodes(data=True))

    for comp in nx.weakly_connected_components(graph):
        sub = graph.subgraph(comp)
        if params.strategy == "by_label":
            order = sorted(comp)
        elif params.strategy == "random_order":
            order = list(comp)
            rng.shuffle(order)
        else:  # min_in_degree
            remaining = set(comp)
            order = []
            while remaining:
                deg = {
                    n: sum(p in remaining for p in sub.predecessors(n))
                    for n in remaining
                }
                low = min(deg.values())
                candidates = [n for n in remaining if deg[n] == low]
                pick = candidates[int(rng.integers(len(candidates)))]
                order.append(pick)
                remaining.remove(pick)
        rank = {n: i for i, n in enumerate(order)}
        out.add_edges_from((u, v) for u, v in sub.edges if rank[u] < rank[v])

    return out


def spec():
    return TransformSpec(
        name=__name__.rsplit(".", 1)[-1],
        accepts=frozenset({"directed", "dag"}),
        parse_params=parse_params,
        apply=apply,
    )
