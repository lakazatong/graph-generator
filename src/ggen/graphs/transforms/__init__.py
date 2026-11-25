from functools import cache

from ggen.graphs.interfaces import TransformSpec

from . import make_cyclic, orient, preserve, relabel, remove_isolated, to_dag

_MODULES = (make_cyclic, orient, preserve, relabel, remove_isolated, to_dag)


@cache
def get_transforms() -> dict[str, TransformSpec]:
    return {
        transform.name: transform for module in _MODULES if (transform := module.spec())
    }


def get_transform(name: str) -> TransformSpec:
    try:
        return get_transforms()[name]
    except KeyError:
        raise ValueError(f"Unknown transform: {name!r}") from None
