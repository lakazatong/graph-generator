from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    import networkx as nx
    import numpy as np

from ggen.graphs.interfaces import TransformSpec

Order = Literal["keep", "shuffle"]


@dataclass(frozen=True)
class Params:
    order: Order = "keep"


def parse_params(raw: dict[str, Any]) -> Params:
    o = raw.get("order", "keep")
    if o not in ("keep", "shuffle"):
        raise ValueError(f"Unknown relabel order: {o!r}")
    return Params(order=o)


def apply(graph: nx.Graph, params: Params, rng: np.random.Generator) -> nx.Graph:
    import networkx as nx

    nodes = list(graph.nodes)
    if params.order == "shuffle":
        rng.shuffle(nodes)
    mapping = {old: i for i, old in enumerate(nodes)}
    return nx.relabel_nodes(graph, mapping)


def spec():
    return TransformSpec(
        name=__name__.rsplit(".", 1)[-1],
        accepts=frozenset({"undirected", "directed", "dag"}),
        parse_params=parse_params,
        apply=apply,
    )
