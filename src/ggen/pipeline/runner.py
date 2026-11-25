from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from ggen.core.config import Config
from ggen.graphs.stage import run_instance


def _config_to_dict(cfg: Config) -> dict[str, Any]:
    data = asdict(cfg)
    data["graph"]["output"] = str(cfg.output)
    return data


def _versions() -> dict[str, str]:
    import sys

    import networkx
    import numpy
    import sympy

    from ggen import __version__

    return {
        "python": sys.version.split()[0],
        "networkx": networkx.__version__,
        "numpy": numpy.__version__,
        "sympy": sympy.__version__,
        "ggen": __version__,
    }


def run(cfg: Config, seed: int) -> Path:
    from seedstream import SeedStream

    out = cfg.output
    out.mkdir(parents=True, exist_ok=True)

    versions = _versions()
    target = out / f"g_{seed}.json"

    if target.exists():
        return target

    record = run_instance(
        cfg,
        SeedStream(seed),
        versions=versions,
    )
    record.write(target)

    return target
