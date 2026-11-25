from __future__ import annotations

from variable_resolver import VariableResolver, int_at_least, probability
from variable_resolver.distributions import Const, Uniform

from ggen.graphs.interfaces import GeneratorSpec


def build(params, rng):
    import networkx as nx

    return nx.gnp_random_graph(
        params["n"],
        params["p"],
        seed=int(rng.integers(2**32)),
        directed=True,
    )


def spec():
    schema = VariableResolver()
    schema.add_variable("n", validate=int_at_least(2))
    schema.add_variable("p", validate=probability)
    schema.add_variable("branching", validate=lambda v, _: None)
    schema.add_variable("mean_out", validate=lambda v, _: None)
    schema.add_equation("branching = n * p")
    schema.add_equation("mean_out = (n - 1) * p")

    regimes = {
        "subcritical": {"branching": Uniform(0.0, 1.0)},
        "critical": {"branching": Const(1.0)},
        "supercritical": {"branching": Uniform(1.0, lambda values: values["n"])},
    }

    return GeneratorSpec(
        name=__name__.rsplit(".", 1)[-1], schema=schema, regimes=regimes, build=build
    )
