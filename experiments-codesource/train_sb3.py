#!/usr/bin/env python3
"""Stable Baselines3 training entrypoint for A2C experiments."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import logging

import numpy as np
import pandas as pd
from stable_baselines3 import A2C, DQN
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import plot_results

from illinois_online import APSelectionEnv
from config import load_experiment_config
from utils import ensure_dir, setup_run_logging, to_project_relative_path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run SB3 A2C/DQN experiment from YAML config"
    )
    parser.add_argument("--config", required=True, help="YAML config path")
    parser.add_argument("--run-id", default=None, help="Optional run id")
    parser.add_argument(
        "--algo", default="A2C", choices=["A2C", "DQN"], help="RL algorithm"
    )
    return parser.parse_args()


def create_env(config, data_path: str, num_aps: int = 5, is_online: bool = False):
    """Create and wrap the environment for SB3."""
    df = pd.read_csv(data_path)
    env = APSelectionEnv(df, num_aps=num_aps, on_line=is_online)
    env = Monitor(env)
    return env


def run_experiment(config, run_id: str = None, algo: str = "A2C") -> None:
    """Run RL experiment using Stable Baselines3."""

    # Load data
    data_path = config.get("data_path", "data/illinois_dataset.csv")
    num_aps = config.get("num_aps", 5)
    is_online = config.get("is_online", False)

    logger.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)

    # Create environment
    env = create_env(config, data_path, num_aps, is_online)

    # Get hyperparameters from config
    total_timesteps = config.get("total_timesteps", 100000)
    learning_rate = config.get("learning_rate", 7e-4)
    gamma = config.get("gamma", 0.99)
    ent_coef = config.get("ent_coef", 0.01)
    vf_coef = config.get("vf_coef", 0.5)
    max_grad_norm = config.get("max_grad_norm", 0.5)
    n_steps = config.get("n_steps", 5)

    # Create model directory
    model_dir = config.get("model_dir", Path("models"))
    ensure_dir(model_dir)

    # Initialize model based on algorithm choice
    if algo == "A2C":
        model = A2C(
            policy="MlpPolicy",
            env=env,
            learning_rate=learning_rate,
            n_steps=n_steps,
            gamma=gamma,
            ent_coef=ent_coef,
            vf_coef=vf_coef,
            max_grad_norm=max_grad_norm,
            verbose=1,
            tensorboard_log=model_dir / "tb_logs",
        )
    elif algo == "DQN":
        buffer_size = config.get("buffer_size", 100000)
        learning_starts = config.get("learning_starts", 1000)
        target_update_interval = config.get("target_update_interval", 500)
        model = DQN(
            policy="MlpPolicy",
            env=env,
            learning_rate=learning_rate,
            gamma=gamma,
            verbose=1,
            buffer_size=buffer_size,
            learning_starts=learning_starts,
            target_update_interval=target_update_interval,
            tensorboard_log=model_dir / "tb_logs",
        )
    else:
        raise ValueError(f"Unknown algorithm: {algo}")

    logger.info(f"Training {algo} for {total_timesteps} timesteps")

    # Callbacks
    checkpoint_callback = CheckpointCallback(
        save_freq=10000, save_path=model_dir, name_prefix=f"{algo}_checkpoint"
    )

    # Train
    model.learn(
        total_timesteps=total_timesteps, callback=checkpoint_callback, progress_bar=True
    )

    # Save final model
    final_model_path = model_dir / f"{algo}_final"
    model.save(final_model_path)
    logger.info(f"Model saved to {final_model_path}")

    # Evaluate
    logger.info("Running evaluation...")
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
    logger.info(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")

    # Log results
    results = {
        "run_id": run_id,
        "algorithm": algo,
        "total_timesteps": total_timesteps,
        "mean_reward": mean_reward,
        "std_reward": std_reward,
    }

    from utils import append_experiment_result

    append_experiment_result(results, config.get("results_file", "results.csv"))

    return model, env, results


def main() -> int:
    args = parse_args()
    config, run_id = load_experiment_config(args.config, args.run_id)

    run_root = config.model_dir.parent
    ensure_dir(run_root)
    ensure_dir(config.log_dir)
    setup_run_logging(config.log_dir / f"{run_id}.log")
    config.save_resolved()

    os.chdir(run_root)

    run_experiment(config, run_id=run_id, algo=args.algo)

    print(f"run_id={run_id}")
    print(f"run_dir={to_project_relative_path(run_root)}")
    print(f"log_file={to_project_relative_path(config.log_dir / f'{run_id}.log')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
