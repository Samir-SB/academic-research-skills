"""Utility helpers for automated experiment runs."""

from __future__ import annotations

import csv
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent

CANONICAL_RESULTS_COLUMNS = [
    "run_id",
    "experiment_name",
    "data_dir",
    "dataset_filename",
    "train_num_aps",
    "train_on_line",
    "train_total_steps",
    "eval_num_aps",
    "eval_on_line",
    "eval_valid_actions",
    "eval_total_steps",
    "hidden_layers",
    "dropout_prob",
    "learning_rate",
    "n_steps",
    "invalid_action_penalty",
    "reload_freq",
]

LEGACY_RESULTS_COLUMN_MAP = {
    "run_id": "run_id",
    "experiment_name": "experiment_name",
    "data_dir": "data_dir",
    "dataset_filename": "dataset_filename",
    "num_aps": "train_num_aps",
    "train_num_aps": "train_num_aps",
    "train_on_line": "train_on_line",
    "train_total_steps": "train_total_steps",
    "eval_num_aps": "eval_num_aps",
    "eval_on_line": "eval_on_line",
    "eval_on_line_": "eval_on_line",
    "eval_valid_actions": "eval_valid_actions",
    "eval_total_steps": "eval_total_steps",
    "hidden_layers": "hidden_layers",
    "dropout_prob": "dropout_prob",
    "learning_rate": "learning_rate",
    "n_steps": "n_steps",
    "invalid_action_penalty": "invalid_action_penalty",
    "reload_freq": "reload_freq",
}


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return cleaned.strip("_") or "experiment"


def read_experiment_name(config_path: str) -> str:
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return str(data.get("experiment_name", "experiment"))


def generate_run_id(experiment_name: str, ts: Optional[datetime] = None) -> str:
    now = ts or datetime.utcnow()
    return f"{now.strftime('%Y%m%d_%H%M%S')}_{slugify(experiment_name)}"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def setup_run_logging(log_path: Path) -> None:
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler) and Path(handler.baseFilename) == log_path:
            return

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    root_logger.addHandler(file_handler)


def to_project_relative_path(path: Path, project_root: Path = PROJECT_ROOT) -> Path:
    """Return a project-relative path when possible, otherwise a stable relative path."""
    absolute_path = path.resolve()
    try:
        return absolute_path.relative_to(project_root.resolve())
    except ValueError:
        return Path(os.path.relpath(str(absolute_path), str(project_root.resolve())))


def format_duration_minutes(elapsed_seconds: float) -> str:
    """Format elapsed seconds as mm:ss.xx and decimal minutes."""
    minutes = int(elapsed_seconds // 60)
    seconds = elapsed_seconds - (minutes * 60)
    return f"{minutes:02d}:{seconds:05.2f} ({elapsed_seconds / 60.0:.4f} minutes)"


def _normalize_column_name(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return normalized.strip("_")


def _canonical_column_name(value: str) -> Optional[str]:
    normalized = _normalize_column_name(value)
    if normalized in LEGACY_RESULTS_COLUMN_MAP:
        return LEGACY_RESULTS_COLUMN_MAP[normalized]
    if normalized in CANONICAL_RESULTS_COLUMNS:
        return normalized
    return None


def _canonicalize_results_row(raw_row: Dict[str, str]) -> Dict[str, str]:
    canonical_row = {column: "" for column in CANONICAL_RESULTS_COLUMNS}
    for key, value in raw_row.items():
        canonical_key = _canonical_column_name(key)
        if canonical_key is None:
            continue
        canonical_row[canonical_key] = value
    return canonical_row


def append_experiment_result(
    result_row: Dict[str, Any],
    csv_path: Path = PROJECT_ROOT / "experiments_results.csv",
) -> None:
    """Normalize experiment results CSV schema and append one row."""
    existing_rows: List[Dict[str, str]] = []

    if csv_path.exists() and csv_path.stat().st_size > 0:
        with open(csv_path, "r", newline="", encoding="utf-8") as input_file:
            reader = csv.DictReader(input_file)
            for raw_row in reader:
                existing_rows.append(_canonicalize_results_row(raw_row))

    canonical_new_row = {column: "" for column in CANONICAL_RESULTS_COLUMNS}
    for key, value in result_row.items():
        if key not in canonical_new_row:
            continue
        canonical_new_row[key] = str(value)
    existing_rows.append(canonical_new_row)

    with open(csv_path, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=CANONICAL_RESULTS_COLUMNS)
        writer.writeheader()
        writer.writerows(existing_rows)
