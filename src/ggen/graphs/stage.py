from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from ggen.core.config import Config, GeneratorConfig
from ggen.core.types import kind_of
from ggen.graphs.analysis import fingerprint as fp_mod
from ggen.graphs.analysis import roles as roles_mod
from ggen.graphs.analysis import stats as stats_mod
from ggen.graphs.generators import get_generator
from ggen.graphs.interfaces import GeneratorSpec
from ggen.graphs.record import GeneratorMeta, GraphRecord, TransformMeta
from ggen.graphs.transforms import get_transform

if TYPE_CHECKING:
    from seedstream import SeedStream


class ParameterError(ValueError): ...


def _resolve_generator_params(
    spec: GeneratorSpec,
    cfg: GeneratorConfig,
    ss: SeedStream,
) -> dict[str, Any]:
    supplied = dict(cfg.params)

    if cfg.regime is not None:
        if cfg.regime not in spec.regimes:
            raise ParameterError(
                f"Unknown regime {cfg.regime!r} for {spec.name!r}; "
                f"expected one of {sorted(spec.regimes)}."
            )
        for name, dist in spec.regimes[cfg.regime].items():
            if name not in supplied:
                try:
                    supplied[name] = dist.sample(supplied, ss.rng("prior", name))
                except KeyError as exc:
                    raise ParameterError(
                        f"Regime prior for {name!r} needs {exc} to be supplied first"
                    ) from exc

    return spec.schema.resolve(supplied, seed=ss.derive_master())


def _meta_from_params(name: str, params: Any) -> Any:
    if hasattr(params, "__dataclass_fields__"):
        return asdict(params)
    return params


def run_instance(
    cfg: Config,
    ss: SeedStream,
    versions: dict[str, str],
) -> GraphRecord:
    import networkx as nx

    gen_spec = get_generator(cfg.generator.name)
    params = _resolve_generator_params(gen_spec, cfg.generator, ss)
    graph = gen_spec.build(params, ss.rng("generator", "build"))
    if not isinstance(graph, nx.Graph):
        raise TypeError(f"Generator {gen_spec.name!r} did not return a graph.")

    stats_before = stats_mod.snapshot(graph)

    applied: list[TransformMeta] = []
    for i, t in enumerate(cfg.transforms):
        tspec = get_transform(t.name)
        current = kind_of(graph)
        if current not in tspec.accepts:
            raise TypeError(
                f"Transform {i} ({t.name!r}) accepts "
                f"{sorted(tspec.accepts)}, got {current!r}."
            )
        tparams = tspec.parse_params(t.params)
        graph = tspec.apply(graph, tparams, ss.rng("transform", str(i), t.name))
        if not isinstance(graph, nx.Graph):
            raise TypeError(f"Transform {t.name!r} did not return a graph.")
        applied.append(
            TransformMeta(name=t.name, params=_meta_from_params(t.name, tparams))
        )

    stats_after = stats_mod.snapshot(graph)

    roles_map = roles_mod.compute(graph) if cfg.analysis.roles else None
    fingerprint_map = fp_mod.compute(graph) if cfg.analysis.fingerprint else None

    return GraphRecord(
        graph=graph,
        generator=GeneratorMeta(
            name=cfg.generator.name,
            regime=cfg.generator.regime,
            resolved_params=params,
        ),
        transforms=applied,
        seed=ss.master,
        stats=stats_mod.GraphStats(
            before_transforms=stats_before,
            after_transforms=stats_after,
        ),
        roles=roles_map,
        fingerprint=fingerprint_map,
        versions=versions,
        timestamp=datetime.now(UTC).isoformat(),
    )
