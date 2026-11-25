from __future__ import annotations

from variable_resolver import VariableResolver, int_at_least

from ggen.graphs.interfaces import GeneratorSpec


def build(params, rng):
    import networkx as nx

    n = params["n"]
    if n == 1:
        return nx.empty_graph(1)
    seq = [int(rng.integers(n)) for _ in range(n - 2)]
    return nx.from_prufer_sequence(seq)


def spec():
    schema = VariableResolver()
    schema.add_variable("n", validate=int_at_least(1))

    regimes = {"uniform_labeled_tree": {}}

    return GeneratorSpec(
        name=__name__.rsplit(".", 1)[-1], schema=schema, regimes=regimes, build=build
    )
