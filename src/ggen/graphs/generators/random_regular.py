from __future__ import annotations

from variable_resolver import VariableResolver, int_at_least
from variable_resolver.distributions import ChoiceFeasible

from ggen.graphs.interfaces import GeneratorSpec


def _check_d(value, values):
    n = values["n"]
    if not isinstance(value, int) or not 1 <= value < n or (n * value) % 2 != 0:
        raise ValueError(f"d={value!r} infeasible for n={n}")


def _fallback_d(values, rng):
    n = values["n"]
    options = [d for d in (1, 2, 3) if d < n and (n * d) % 2 == 0]
    if not options:
        raise ValueError(f"No feasible d for n={n}.")
    return options[int(rng.integers(len(options)))]


def _feasible(options):
    return lambda v, vals: v < vals["n"] and (vals["n"] * v) % 2 == 0


def build(params, rng):
    import networkx as nx

    return nx.random_regular_graph(
        params["d"], params["n"], seed=int(rng.integers(2**32))
    )


def spec():
    schema = VariableResolver()
    schema.add_variable("n", validate=int_at_least(3))
    schema.add_variable(
        "d",
        sample=lambda vals, rng: _fallback_d(vals, rng),
        validate=lambda v, vals: _check_d(v, vals),
    )

    regimes = {
        "matching": {"d": ChoiceFeasible((1,), _feasible((1,)))},
        "cycles": {"d": ChoiceFeasible((2,), _feasible((2,)))},
        "moderate_degree": {"d": ChoiceFeasible((3, 4), _feasible((3, 4)))},
        "higher_degree": {"d": ChoiceFeasible((5, 6), _feasible((5, 6)))},
    }

    return GeneratorSpec(
        name=__name__.rsplit(".", 1)[-1], schema=schema, regimes=regimes, build=build
    )
