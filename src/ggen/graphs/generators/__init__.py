from functools import cache

from ggen.graphs.interfaces import GeneratorSpec

from . import (
    barabasi_albert,
    complete,
    empty,
    erdos_renyi,
    from_file,
    gnm,
    random_regular,
    random_tree,
    stochastic_block,
    watts_strogatz,
)

_MODULES = (
    barabasi_albert,
    complete,
    empty,
    erdos_renyi,
    from_file,
    gnm,
    random_regular,
    random_tree,
    stochastic_block,
    watts_strogatz,
)


@cache
def get_generators() -> dict[str, GeneratorSpec]:
    return {
        generator.name: generator for module in _MODULES if (generator := module.spec())
    }


def get_generator(name: str) -> GeneratorSpec:
    try:
        return get_generators()[name]
    except KeyError:
        raise ValueError(f"Unknown generator: {name!r}") from None
