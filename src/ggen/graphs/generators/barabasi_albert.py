from __future__ import annotations

from variable_resolver import VariableResolver, int_at_least
from variable_resolver.distributions import ChoiceFeasible

from ggen.graphs.interfaces import GeneratorSpec


def _check_m(value, values):
    if not isinstance(value, int) or not 1 <= value < values["n"]:
        raise ValueError(f"m must satisfy 1 <= m < n; got {value!r}")


def _fallback_m(values, rng):
    n = values["n"]
    options = [m for m in (1, 2, 3) if m < n]
    if not options:
        raise ValueError(f"No feasible m for n={n}.")
    return options[int(rng.integers(len(options)))]


def build(params, rng):
    import networkx as nx

    return nx.barabasi_albert_graph(
        params["n"], params["m"], seed=int(rng.integers(2**32))
    )


def spec():
    schema = VariableResolver()
    schema.add_variable("n", validate=int_at_least(2))
    schema.add_variable(
        "m",
        sample=lambda vals, rng: _fallback_m(vals, rng),
        validate=lambda v, vals: _check_m(v, vals),
    )

    regimes = {
        "tree_like": {"m": ChoiceFeasible((1,), lambda v, vals: v < vals["n"])},
        "sparse_scale_free": {
            "m": ChoiceFeasible((2, 3), lambda v, vals: v < vals["n"])
        },
        "higher_attachment": {
            "m": ChoiceFeasible((4, 5, 6), lambda v, vals: v < vals["n"])
        },
    }

    return GeneratorSpec(
        name=__name__.rsplit(".", 1)[-1], schema=schema, regimes=regimes, build=build
    )
