from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import networkx as nx

Histogram = dict[int, float]
Fingerprint = dict[str, Histogram]


def _histogram(values) -> Histogram:
    counts = Counter(values)
    total = sum(counts.values()) or 1
    return {v: c / total for v, c in sorted(counts.items())}


def compute(graph: nx.Graph) -> Fingerprint:
    import networkx as nx

    if graph.is_directed():
        assert isinstance(graph, nx.DiGraph)
        in_d = dict(graph.in_degree())
        out_d = dict(graph.out_degree())
    else:
        in_d = out_d = dict(graph.degree())
    return {
        "in_degree": _histogram(in_d.values()),
        "out_degree": _histogram(out_d.values()),
    }
