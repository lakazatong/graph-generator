from __future__ import annotations

from variable_resolver import VariableResolver, int_at_least, probability
from variable_resolver.distributions import Uniform

from ggen.graphs.interfaces import GeneratorSpec


def _check_count(value, values):
    n = values["n"]
    if not isinstance(value, int) or not 2 <= value <= n:
        raise ValueError(f"count must satisfy 2 <= count <= n; got {value!r}")


def _check_sizes(value, values):
    if (
        not isinstance(value, list)
        or not all(isinstance(x, int) and x >= 1 for x in value)
        or sum(value) != values["n"]
    ):
        raise ValueError(f"sizes must be positive ints summing to n={values['n']}")
    if len(value) != values["count"]:
        raise ValueError(f"len(sizes) must equal count={values['count']}")


def _even_split(n, count):
    if count > n:
        raise ValueError(f"count={count} > n={n}")
    base, extra = divmod(n, count)
    return [base + (1 if i < extra else 0) for i in range(count)]


def build(params, rng):
    import networkx as nx

    count = params["count"]
    p = [
        [params["p_in"] if i == j else params["p_out"] for j in range(count)]
        for i in range(count)
    ]
    G = nx.stochastic_block_model(
        params["sizes"],
        p,
        seed=int(rng.integers(2**32)),
        directed=True,
    )
    if "partition" in G.graph:
        G.graph["partition"] = [sorted(s) for s in G.graph["partition"]]
    return G


def spec():
    schema = VariableResolver()
    schema.add_variable("n", validate=int_at_least(2))
    schema.add_variable(
        "count",
        sample=lambda vals, rng: int(
            rng.integers(2, max(3, int(vals["n"] ** 0.5) + 1))
        ),
        validate=lambda v, vals: _check_count(v, vals),
    )
    schema.add_variable(
        "sizes",
        sample=lambda vals, rng: _even_split(vals["n"], vals["count"]),
        validate=lambda v, vals: _check_sizes(v, vals),
    )
    schema.add_variable("p_in", validate=probability, sample=lambda vals, rng: 0.3)
    schema.add_variable(
        "p_out_ratio", validate=probability, sample=lambda vals, rng: 0.5
    )
    schema.add_variable("p_out", validate=probability)
    schema.add_equation("p_out = p_in * p_out_ratio")

    regimes = {
        "weak_assortative": {
            "p_in": Uniform(0.15, 0.4),
            "p_out_ratio": Uniform(0.4, 0.7),
        },
        "strong_assortative": {
            "p_in": Uniform(0.35, 0.7),
            "p_out_ratio": Uniform(0.03, 0.2),
        },
        "near_uniform": {"p_in": Uniform(0.05, 0.6), "p_out_ratio": Uniform(0.9, 1.0)},
        "disassortative": {
            "p_in": Uniform(0.01, 0.08),
            "p_out_ratio": Uniform(2.5, 50.0),
        },
    }

    return GeneratorSpec(
        name=__name__.rsplit(".", 1)[-1], schema=schema, regimes=regimes, build=build
    )
