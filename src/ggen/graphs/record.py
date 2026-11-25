from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ggen.graphs.analysis.fingerprint import Fingerprint
from ggen.graphs.analysis.roles import NodeRole
from ggen.graphs.analysis.stats import GraphStats

if TYPE_CHECKING:
    import networkx as nx


@dataclass(frozen=True)
class GeneratorMeta:
    name: str
    regime: str | None
    resolved_params: dict[str, Any]


@dataclass(frozen=True)
class TransformMeta:
    name: str
    params: Any


@dataclass(frozen=True)
class GraphRecord:
    graph: nx.Graph
    generator: GeneratorMeta
    transforms: list[TransformMeta]
    seed: int
    stats: GraphStats
    roles: dict[int, NodeRole] | None
    fingerprint: Fingerprint | None
    versions: dict[str, str]
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        import networkx as nx

        data = asdict(self)
        data["graph"] = nx.node_link_data(self.graph, edges="edges")

        if self.roles is not None:
            data["roles"] = {str(k): v for k, v in self.roles.items()}

        if self.fingerprint is not None:
            data["fingerprint"] = {
                name: {str(k): v for k, v in hist.items()}
                for name, hist in self.fingerprint.items()
            }

        return data

    def write(self, path: Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True))

    @classmethod
    def read(cls, path: Path) -> GraphRecord:
        import networkx as nx
        from dacite import from_dict

        d = json.loads(path.read_text())

        d["graph"] = nx.node_link_graph(d["graph"], edges="edges")

        if d["roles"] is not None:
            d["roles"] = {int(k): v for k, v in d["roles"].items()}

        if d["fingerprint"] is not None:
            d["fingerprint"] = {
                name: {int(k): v for k, v in hist.items()}
                for name, hist in d["fingerprint"].items()
            }

        return from_dict(cls, d)
