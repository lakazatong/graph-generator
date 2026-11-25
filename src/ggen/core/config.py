from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GeneratorConfig:
    name: str
    regime: str | None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TransformConfig:
    name: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AnalysisConfig:
    roles: bool = True
    fingerprint: bool = False


@dataclass(frozen=True)
class Config:
    generator: GeneratorConfig
    transforms: list[TransformConfig]
    analysis: AnalysisConfig
    output: Path


def load(path: Path) -> Config:
    import yaml
    from dacite import from_dict
    from dacite.config import Config as DaciteConfig

    data = yaml.safe_load(path.read_text())
    return from_dict(
        Config,
        data,
        config=DaciteConfig(
            strict=True,
            type_hooks={Path: Path},
        ),
    )
