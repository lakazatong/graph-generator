from __future__ import annotations

from pathlib import Path

from variable_resolver import VariableResolver, string

from ggen.graphs.interfaces import GeneratorSpec


def build(params, rng):
    import networkx as nx

    path = Path(params["path"])
    suffix = path.suffix.lower()
    if suffix == ".edgelist":
        return nx.read_edgelist(path, create_using=nx.DiGraph(), nodetype=int)
    if suffix == ".graph":
        from ggen.graphs.record import GraphRecord

        return GraphRecord.read(path).graph
    if suffix in (".graphml", ".xml"):
        return nx.read_graphml(path)
    if suffix == ".gml":
        return nx.read_gml(path)
    raise ValueError(f"Unsupported file format: {suffix!r}")


def spec():
    schema = VariableResolver()
    schema.add_variable("path", validate=string)

    regimes = {"default": {}}

    return GeneratorSpec(
        name=__name__.rsplit(".", 1)[-1], schema=schema, regimes=regimes, build=build
    )
