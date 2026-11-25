from __future__ import annotations

from variable_resolver import VariableResolver, int_at_least

from ggen.graphs.interfaces import GeneratorSpec


def build(params, rng):
    import networkx as nx

    return nx.empty_graph(params["n"])


def spec():
    schema = VariableResolver()
    schema.add_variable("n", validate=int_at_least(0))

    regimes = {"default": {}}

    return GeneratorSpec(
        name=__name__.rsplit(".", 1)[-1], schema=schema, regimes=regimes, build=build
    )
