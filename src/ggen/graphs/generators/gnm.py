from __future__ import annotations

from variable_resolver import VariableResolver, int_at_least
from variable_resolver.distributions import Const, IntRange

from ggen.graphs.interfaces import GeneratorSpec


def _check_m(value, values):
    n = values["n"]
    if not isinstance(value, int) or not 0 <= value <= n * (n - 1):
        raise ValueError(f"m must satisfy 0 <= m <= {n * (n - 1)}; got {value!r}")


def _fallback_m(values, rng):
    n = values["n"]
    return int(rng.integers(0, n * (n - 1) + 1))


def build(params, rng):
    import networkx as nx

    return nx.gnm_random_graph(
        params["n"],
        params["m"],
        seed=int(rng.integers(2**32)),
        directed=True,
    )


def spec():
    schema = VariableResolver()
    schema.add_variable("n", validate=int_at_least(2))
    schema.add_variable(
        "m",
        sample=lambda vals, rng: _fallback_m(vals, rng),
        validate=lambda v, vals: _check_m(v, vals),
    )
    schema.add_variable("mean_out", validate=lambda v, _: None)
    schema.add_equation("mean_out = m / n")

    regimes = {
        "subcritical": {
            "m": IntRange(0, lambda values: max(0, values["n"] - 1)),
        },
        "critical": {
            "m": Const(lambda values: values["n"]),
        },
        "supercritical": {
            "m": IntRange(
                lambda values: values["n"] + 1,
                lambda values: values["n"] * (values["n"] - 1),
            ),
        },
    }

    return GeneratorSpec(
        name=__name__.rsplit(".", 1)[-1], schema=schema, regimes=regimes, build=build
    )
