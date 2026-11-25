from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol

from variable_resolver import VariableResolver
from variable_resolver.distributions import Distribution

from ggen.core.types import GraphKind

if TYPE_CHECKING:
    import networkx as nx
    import numpy as np


class GeneratorCallable(Protocol):
    def __call__(
        self, params: Mapping[str, Any], rng: np.random.Generator
    ) -> nx.Graph: ...


class TransformCallable(Protocol):
    def __call__(
        self, graph: nx.Graph, params: Any, rng: np.random.Generator
    ) -> nx.Graph: ...


class AnalysisCallable(Protocol):
    def __call__(self, graph: nx.Graph, params: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True)
class GeneratorSpec:
    name: str
    schema: VariableResolver
    regimes: Mapping[str, Mapping[str, Distribution]]
    build: GeneratorCallable


@dataclass(frozen=True)
class TransformSpec:
    name: str
    accepts: frozenset[GraphKind]
    parse_params: Callable[[dict[str, Any]], Any]
    apply: TransformCallable


@dataclass(frozen=True)
class AnalysisSpec:
    name: str
    compute: AnalysisCallable
