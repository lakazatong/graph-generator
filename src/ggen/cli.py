from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from pathlib import Path

from ggen.core.config import load
from ggen.graphs.record import GraphRecord
from ggen.pipeline.runner import run


def _seed_range(value: str) -> tuple[int, int]:
    try:
        start, stop = map(int, value.split(":"))
        if start >= stop:
            raise ValueError
        return start, stop
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Expected a seed range in the form START:STOP (exclusive)."
        ) from None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ggen")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="Run a pipeline config.")
    r.add_argument("config", type=Path)

    seeds = r.add_mutually_exclusive_group(required=True)
    seeds.add_argument("--seed", type=int)
    seeds.add_argument("--seeds", type=_seed_range)

    c = sub.add_parser("check", help="Validate a config without running.")
    c.add_argument("config", type=Path)

    i = sub.add_parser("inspect", help="Print a graph artifact.")
    i.add_argument("artifact", type=Path)

    args = p.parse_args(argv)

    if args.cmd == "run":
        cfg = load(args.config)

        selected_seeds: Iterable[int] = (
            range(*args.seeds) if args.seeds is not None else [int(args.seed)]
        )

        for seed in selected_seeds:
            out = run(cfg, seed=seed)
            print(out)

        return 0

    if args.cmd == "check":
        cfg = load(args.config)
        print(f"ok (generator={cfg.generator.name})")
        return 0

    if args.cmd == "inspect":
        rec = GraphRecord.read(args.artifact)
        print(json.dumps(rec.to_dict(), indent=2, sort_keys=True))
        return 0

    return 1
