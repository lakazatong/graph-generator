from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import networkx as nx

from ggen.core.types import GraphKind, kind_of


@dataclass(frozen=True)
class Snapshot:
    n: int
    edges: int
    density: float
    kind: GraphKind
    is_dag: bool
    components: int


@dataclass(frozen=True)
class GraphStats:
    before_transforms: Snapshot
    after_transforms: Snapshot


def snapshot(graph: nx.Graph) -> Snapshot:
    import networkx as nx

    k = kind_of(graph)
    if graph.is_directed():
        assert isinstance(graph, nx.DiGraph)
        comps = nx.number_weakly_connected_components(graph)
    else:
        comps = nx.number_connected_components(graph)
    return Snapshot(
        n=graph.number_of_nodes(),
        edges=graph.number_of_edges(),
        density=nx.density(graph),
        kind=k,
        is_dag=(k == "dag"),
        components=comps,
    )
