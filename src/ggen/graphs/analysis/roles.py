from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import networkx as nx

NodeRole = Literal["root", "hidden", "sink", "isolated"]


def compute(graph: nx.Graph) -> dict[int, NodeRole]:
    import networkx as nx

    out: dict[int, NodeRole] = {}
    for n in graph.nodes:
        if graph.is_directed():
            assert isinstance(graph, nx.DiGraph)
            i, o = graph.in_degree(n), graph.out_degree(n)
        else:
            i = o = graph.degree(n)
        if i == 0 and o == 0:
            out[n] = "isolated"
        elif i == 0:
            out[n] = "root"
        elif o == 0:
            out[n] = "sink"
        else:
            out[n] = "hidden"
    return out
