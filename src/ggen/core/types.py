from __future__ import annotations

from typing import Literal

GraphKind = Literal["undirected", "directed", "dag"]


def kind_of(graph) -> GraphKind:
    import networkx as nx

    if not graph.is_directed():
        return "undirected"
    if nx.is_directed_acyclic_graph(graph):
        return "dag"
    return "directed"
