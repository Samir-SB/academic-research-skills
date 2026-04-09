"""Configuration management for A2C experiment automation."""

from __future__ import annotations

import argparse
from argparse import Namespace
from pathlib import Path
from typing import Any, List, Optional, Literal

import numpy as np
import torch
import yaml
from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt


PROJECT_ROOT = Path(__file__).resolve().parent


class networkConfig(BaseModel):
    hidden_layers: List[int] = [512, 512, 512]
    dropout_prob: float = Field(0.5, ge=0.0, le=1.0)
    state_dim: Optional[int] = None
    action_dim: Optional[int] = None
    accuracy: Optional[float] = None


class TrainingConfig(BaseModel):
    learning_rate: PositiveFloat = 1e-4
    gamma: float = Field(0.9, ge=0.0, le=1.0)
    n_steps: PositiveInt = 15
    invalid_action_penalty: float = -0.1
    reload_freq: PositiveInt = 5
    episodes: PositiveInt = 5
    target_accuracy: PositiveInt = 90
    entropy_coef: float = Field(0.05, ge=0.0)
    max_grad_norm: float = 1.0


class DatasetConfig(BaseModel):
    filename: str = "df_shuffled_200.csv"


class EnvPhaseConfig(BaseModel):
    num_aps: PositiveInt = 20
    on_line: bool = True


class EnvConfig(BaseModel):
    final_nb_aps: PositiveInt = 50
    train: EnvPhaseConfig = EnvPhaseConfig()
    eval: EnvPhaseConfig = EnvPhaseConfig()


class MasterA2CConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    device: Literal["cpu", "cuda:0"] = "cuda:0" if torch.cuda.is_available() else "cpu"
    random_seed: int = 42

    resume_training: bool = False
    train: bool = True

    experiment_name: str = "A2C_N_steps"
    model_dir: Path = Path("./model")
    plot_dir: Path = Path("./plot")
    log_dir: Path = Path("./logs")
    data_dir: Path = Path("./data")
    dataset: DatasetConfig = DatasetConfig()
    env: EnvConfig = EnvConfig()

    data_test_size: float = Field(0.3, ge=0.0, le=1.0)
    data_shuffle: bool = False

    network: networkConfig = networkConfig()
    training: TrainingConfig = TrainingConfig()

    @staticmethod
    def _to_builtin_scalars(value: Any) -> Any:
        """Recursively convert NumPy scalar/object values into builtin Python types."""
        if isinstance(value, dict):
            return {k: MasterA2CConfig._to_builtin_scalars(v) for k, v in value.items()}
        if isinstance(value, list):
            return [MasterA2CConfig._to_builtin_scalars(v) for v in value]
        if isinstance(value, tuple):
            return [MasterA2CConfig._to_builtin_scalars(v) for v in value]
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, np.generic):
            return value.item()
        return value

    def setup_system(self) -> None:
        Path(self.model_dir).mkdir(parents=True, exist_ok=True)
        Path(self.plot_dir).mkdir(parents=True, exist_ok=True)
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        torch.manual_seed(self.random_seed)
        np.random.seed(self.random_seed)

    def save_resolved(self) -> None:
        resolved_config_path = self.model_dir / "resolved_config.yaml"
        resolved_data = self._to_builtin_scalars(self.model_dump(mode="python"))
        with open(resolved_config_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                resolved_data,
                f,
                sort_keys=False,
                allow_unicode=False,
            )

    # Compatibility alias used by legacy code.
    def save_resloved(self) -> None:  # pragma: no cover
        self.save_resolved()


def _resolve_path(path: Path, base: Path) -> Path:
    return path if path.is_absolute() else (base / path).resolve()


def load_config(
    config_path: str,
    run_id: Optional[str] = None,
    runs_root: str = "runs",
    logs_root: str = "logs",
) -> MasterA2CConfig:
    cfg_path = Path(config_path)
    if not cfg_path.is_absolute():
        cfg_path = (PROJECT_ROOT / cfg_path).resolve()
    if cfg_path.suffix.lower() not in {".yaml", ".yml"}:
        raise ValueError("Only YAML config files are supported (.yaml/.yml).")

    with open(cfg_path, "r", encoding="utf-8") as f:
        config_dict = yaml.safe_load(f) or {}

    config = MasterA2CConfig(**config_dict)

    runs_root_path = _resolve_path(Path(runs_root), PROJECT_ROOT)
    logs_root_path = _resolve_path(Path(logs_root), PROJECT_ROOT)

    if run_id:
        run_root = runs_root_path / run_id
        config.model_dir = run_root / "model"
        config.plot_dir = run_root / "plot"
    else:
        config.model_dir = _resolve_path(config.model_dir, PROJECT_ROOT)
        config.plot_dir = _resolve_path(config.plot_dir, PROJECT_ROOT)

    config.log_dir = logs_root_path
    config.data_dir = _resolve_path(config.data_dir, PROJECT_ROOT)

    config.setup_system()
    return config


def parser_args() -> Namespace:
    parser = argparse.ArgumentParser(description="A2C Wireless Network Training Pipeline")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/exp1.yaml",
        help="Path to YAML experiment configuration",
    )
    parser.add_argument(
        "--run-id",
        type=str,
        default=None,
        help="Optional run id for artifact output under runs/<run-id>",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parser_args()
    try:
        config = load_config(args.config, run_id=args.run_id)
        print(f"Loaded experiment: {config.experiment_name}")
        print(f"Model dir: {config.model_dir}")
        print(f"Plot dir: {config.plot_dir}")
    except Exception as e:
        print(f"Configuration Error: {e}")
