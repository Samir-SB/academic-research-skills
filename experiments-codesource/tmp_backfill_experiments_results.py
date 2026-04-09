#!/usr/bin/env python3
"""Temporary utility to rebuild experiments_results.csv from finished run logs."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from utils import CANONICAL_RESULTS_COLUMNS, PROJECT_ROOT

FINISHED_MARKER = "All operations completed successfully!"
RUN_LOG_PATTERN = re.compile(r"^\d{8}_\d{6}_.+\.log$")
VALID_ACTIONS_PATTERN = re.compile(r"Valid actions:\s*([0-9]+(?:\.[0-9]+)?)%")
TOTAL_STEPS_PATTERN = re.compile(r"Total steps:\s*([0-9]+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill experiments_results.csv from run logs")
    parser.add_argument("--logs-dir", default="logs", help="Directory containing per-run logs")
    parser.add_argument("--runs-dir", default="runs", help="Directory containing run artifacts")
    parser.add_argument("--output", default="experiments_results.csv", help="Backfilled CSV output path")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose warnings and summary")
    return parser.parse_args()


def maybe_relative_to_project(path_value: Any) -> str:
    if not isinstance(path_value, str) or not path_value:
        return ""
    path_obj = Path(path_value)
    if not path_obj.is_absolute():
        return path_value
    try:
        return str(path_obj.resolve().relative_to(PROJECT_ROOT.resolve()))
    except ValueError:
        return os.path.relpath(str(path_obj.resolve()), str(PROJECT_ROOT.resolve()))


def read_text(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        logging.warning("Failed reading %s: %s", path, exc)
        return None


def safe_get(data: Dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def parse_resolved_config(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists() or config_path.stat().st_size == 0:
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data if isinstance(data, dict) else {}
    except Exception as exc:  # noqa: BLE001
        logging.warning("Failed parsing YAML %s: %s", config_path, exc)
        return {}


def parse_eval_metrics(log_text: str) -> Dict[str, str]:
    valid_matches = VALID_ACTIONS_PATTERN.findall(log_text)
    steps_matches = TOTAL_STEPS_PATTERN.findall(log_text)
    return {
        "eval_valid_actions": valid_matches[-1] if valid_matches else "",
        "eval_total_steps": steps_matches[-1] if steps_matches else "",
    }


def build_row(run_id: str, config_data: Dict[str, Any], eval_data: Dict[str, str]) -> Dict[str, str]:
    row = {col: "" for col in CANONICAL_RESULTS_COLUMNS}
    row["run_id"] = run_id

    experiment_name = config_data.get("experiment_name")
    row["experiment_name"] = str(experiment_name) if experiment_name is not None else ""

    data_dir = config_data.get("data_dir")
    row["data_dir"] = maybe_relative_to_project(data_dir)

    dataset_filename = safe_get(config_data, "dataset", "filename")
    row["dataset_filename"] = str(dataset_filename) if dataset_filename is not None else ""

    train_num_aps = safe_get(config_data, "env", "train", "num_aps")
    row["train_num_aps"] = str(train_num_aps) if train_num_aps is not None else ""

    train_on_line = safe_get(config_data, "env", "train", "on_line")
    row["train_on_line"] = str(train_on_line) if train_on_line is not None else ""

    eval_num_aps = safe_get(config_data, "env", "eval", "num_aps")
    row["eval_num_aps"] = str(eval_num_aps) if eval_num_aps is not None else ""

    eval_on_line = safe_get(config_data, "env", "eval", "on_line")
    row["eval_on_line"] = str(eval_on_line) if eval_on_line is not None else ""

    hidden_layers = safe_get(config_data, "network", "hidden_layers")
    if hidden_layers is not None:
        row["hidden_layers"] = json.dumps(hidden_layers)

    dropout_prob = safe_get(config_data, "network", "dropout_prob")
    row["dropout_prob"] = str(dropout_prob) if dropout_prob is not None else ""

    learning_rate = safe_get(config_data, "training", "learning_rate")
    row["learning_rate"] = str(learning_rate) if learning_rate is not None else ""

    n_steps = safe_get(config_data, "training", "n_steps")
    row["n_steps"] = str(n_steps) if n_steps is not None else ""

    invalid_action_penalty = safe_get(config_data, "training", "invalid_action_penalty")
    row["invalid_action_penalty"] = str(invalid_action_penalty) if invalid_action_penalty is not None else ""

    reload_freq = safe_get(config_data, "training", "reload_freq")
    row["reload_freq"] = str(reload_freq) if reload_freq is not None else ""

    episodes = safe_get(config_data, "training", "episodes")
    if isinstance(episodes, (int, float)) and isinstance(n_steps, (int, float)):
        row["train_total_steps"] = str(int(episodes) * int(n_steps))

    row["eval_valid_actions"] = eval_data.get("eval_valid_actions", "")
    row["eval_total_steps"] = eval_data.get("eval_total_steps", "")

    return row


def list_run_logs(logs_dir: Path) -> List[Path]:
    if not logs_dir.exists():
        return []
    candidates = []
    for path in logs_dir.glob("*.log"):
        if path.name.startswith("run_experiments_"):
            continue
        if not RUN_LOG_PATTERN.match(path.name):
            continue
        candidates.append(path)
    return sorted(candidates)


def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s",
    )

    logs_dir = Path(args.logs_dir)
    runs_dir = Path(args.runs_dir)
    output_path = Path(args.output)

    try:
        run_logs = list_run_logs(logs_dir)
        rows: List[Dict[str, str]] = []

        for log_path in run_logs:
            log_text = read_text(log_path)
            if not log_text:
                continue
            if FINISHED_MARKER not in log_text:
                logging.warning("Skipping unfinished run log: %s", log_path)
                continue

            run_id = log_path.stem
            config_path = runs_dir / run_id / "model" / "resolved_config.yaml"
            config_data = parse_resolved_config(config_path)
            eval_data = parse_eval_metrics(log_text)

            try:
                row = build_row(run_id, config_data, eval_data)
                rows.append(row)
            except Exception as exc:  # noqa: BLE001
                logging.warning("Failed to build row for run_id=%s: %s", run_id, exc)
                continue

        rows.sort(key=lambda r: r.get("run_id", ""))

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CANONICAL_RESULTS_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

        if args.verbose:
            logging.info("Backfilled %s with %d rows", output_path, len(rows))
        return 0
    except Exception as exc:  # noqa: BLE001
        logging.error("Fatal error: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
