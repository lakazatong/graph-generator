from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import networkx as nx
    import numpy as np

from ggen.graphs.interfaces import TransformSpec


def parse_params(raw: dict[str, Any]) -> None:
    if raw:
        raise ValueError("preserve takes no parameters")


def apply(graph: nx.Graph, params: None, rng: np.random.Generator) -> nx.Graph:
    return graph


def spec():
    return TransformSpec(
        name=__name__.rsplit(".", 1)[-1],
        accepts=frozenset({"undirected", "directed", "dag"}),
        parse_params=parse_params,
        apply=apply,
    )
