#!/usr/bin/env python3
"""Canonical training entrypoint for A2C experiments."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from claude_a2c_online import run_experiment
from config import load_experiment_config
from utils import ensure_dir, setup_run_logging, to_project_relative_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run A2C experiment from YAML config")
    parser.add_argument("--config", required=True, help="YAML config path")
    parser.add_argument("--run-id", default=None, help="Optional run id")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config, run_id = load_experiment_config(args.config, args.run_id)

    run_root = config.model_dir.parent
    ensure_dir(run_root)
    ensure_dir(config.log_dir)
    setup_run_logging(config.log_dir / f"{run_id}.log")
    config.save_resolved()

    # Some plotting helpers write to relative plot/ paths, so execute from run root.
    os.chdir(run_root)

    run_experiment(config, run_id=run_id)

    print(f"run_id={run_id}")
    print(f"run_dir={to_project_relative_path(run_root)}")
    print(f"log_file={to_project_relative_path(config.log_dir / f'{run_id}.log')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
