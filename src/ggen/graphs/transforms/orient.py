from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    import networkx as nx
    import numpy as np

from ggen.graphs.interfaces import TransformSpec

Mode = Literal["by_label", "random_order", "random_edges"]


@dataclass(frozen=True)
class Params:
    mode: Mode


def parse_params(raw: dict[str, Any]) -> Params:
    mode = raw.get("mode")
    if mode not in ("by_label", "random_order", "random_edges"):
        raise ValueError(f"Unknown orient mode: {mode!r}")
    return Params(mode=mode)


def apply(graph: nx.Graph, params: Params, rng: np.random.Generator) -> nx.DiGraph:
    import networkx as nx

    out = nx.DiGraph()
    out.add_nodes_from(graph.nodes(data=True))
    if params.mode == "by_label":
        out.add_edges_from((u, v) for u, v in graph.edges if u < v)
    elif params.mode == "random_order":
        order = list(graph.nodes)
        rng.shuffle(order)
        rank = {n: i for i, n in enumerate(order)}
        out.add_edges_from(
            (u, v) if rank[u] < rank[v] else (v, u) for u, v in graph.edges
        )
    else:  # random_edges
        out.add_edges_from(
            (u, v) if rng.random() < 0.5 else (v, u) for u, v in graph.edges
        )
    return out


def spec():
    return TransformSpec(
        name=__name__.rsplit(".", 1)[-1],
        accepts=frozenset({"undirected"}),
        parse_params=parse_params,
        apply=apply,
    )
