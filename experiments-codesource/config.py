"""Shared config loading interface for experiment entrypoints."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple, Optional

from config_mgmt import MasterA2CConfig, load_config
from utils import generate_run_id, read_experiment_name


def load_experiment_config(config_path: str, run_id: Optional[str] = None) -> Tuple[MasterA2CConfig, str]:
    cfg_path = Path(config_path)
    if not cfg_path.is_absolute():
        cfg_path = (Path(__file__).resolve().parent / cfg_path).resolve()

    exp_name = read_experiment_name(str(cfg_path))
    resolved_run_id = run_id or generate_run_id(exp_name)
    config = load_config(str(cfg_path), run_id=resolved_run_id)
    return config, resolved_run_id
