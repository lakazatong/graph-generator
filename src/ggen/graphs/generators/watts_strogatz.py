from __future__ import annotations

from variable_resolver import VariableResolver, int_at_least, probability
from variable_resolver.distributions import Const, Uniform

from ggen.graphs.interfaces import GeneratorSpec


def _check_k(value, values):
    n = values["n"]
    if not isinstance(value, int) or value < 2 or value % 2 != 0 or value >= n:
        raise ValueError(f"k must be even and 2 <= k < n; got {value!r}")


def build(params, rng):
    import networkx as nx

    return nx.watts_strogatz_graph(
        params["n"],
        params["k"],
        params["p"],
        seed=int(rng.integers(2**32)),
    )


def spec():
    schema = VariableResolver()
    schema.add_variable("n", validate=int_at_least(3))
    schema.add_variable(
        "k",
        sample=lambda vals, rng: 2 if vals["n"] > 2 else None,
        validate=lambda v, vals: _check_k(v, vals),
    )
    schema.add_variable("p", validate=probability, sample=lambda vals, rng: 0.1)

    regimes = {
        "lattice": {"p": Const(0.0), "k": Const(2)},
        "small_world": {"p": Uniform(0.01, 0.1), "k": Const(2)},
        "random": {"p": Const(1.0), "k": Const(2)},
    }

    return GeneratorSpec(
        name=__name__.rsplit(".", 1)[-1], schema=schema, regimes=regimes, build=build
    )
