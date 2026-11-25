from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from ggen.graphs.interfaces import TransformSpec

if TYPE_CHECKING:
    import networkx as nx
    import numpy as np


@dataclass(frozen=True)
class Params:
    n_cycles: int = 1


def parse_params(raw: dict[str, Any]) -> Params:
    n = int(raw.get("n_cycles", 1))
    if n < 1:
        raise ValueError(f"n_cycles must be >= 1, got {n!r}")
    return Params(n_cycles=n)


def apply(graph: nx.Graph, params: Params, rng: np.random.Generator) -> nx.DiGraph:
    import networkx as nx

    out = graph.copy()
    if not out.is_directed():
        raise TypeError("make_cyclic expects a directed graph")
    assert isinstance(out, nx.DiGraph)

    for _ in range(params.n_cycles):
        if any(True for _ in nx.simple_cycles(out)):
            continue
        nodes = list(out.nodes)
        if len(nodes) < 2:
            break
        i = int(rng.integers(len(nodes)))
        j = (i + 1) % len(nodes)
        u, v = nodes[i], nodes[j]
        if out.has_edge(v, u):
            out.remove_edge(v, u)
        out.add_edge(u, v)
    return out


def spec():
    return TransformSpec(
        name=__name__.rsplit(".", 1)[-1],
        accepts=frozenset({"directed", "dag"}),
        parse_params=parse_params,
        apply=apply,
    )
