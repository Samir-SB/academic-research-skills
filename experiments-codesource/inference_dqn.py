import logging
import argparse
from typing import Dict

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import matplotlib.pyplot as plt
from collections import deque, Counter
import time
from sklearn.model_selection import train_test_split
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

from config_mgmt import load_config
from illinois_online import APSelectionEnv
from training_plots import plot_stacked_actions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------
class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, dropout_prob=0):
        super(QNetwork, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 512),
            nn.ReLU(),
            nn.Dropout(p=dropout_prob),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(p=dropout_prob),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(p=dropout_prob),
            nn.Linear(512, action_dim)  
            )

    def forward(self, x):
        return self.fc(x)

def evaluate(eval_env: DummyVecEnv, q_net: DQN) -> Dict:
    """
    Evaluate the agent on the environment and return action statistics.
    """
    logger.info("Starting evaluation...")

    state = eval_env.reset()
    total_reward = 0.0
    valid_count = 0
    step_count = 0
    action_distribution = Counter()
    valid_action_distribution = Counter()
    total_steps = eval_env.get_attr("total_steps")[0]

    for step in range(total_steps):
        action, _ = q_net.predict(state, deterministic=True)
        action = int(action[0])
        action_distribution[action] += 1

        next_state, reward, done, _ = eval_env.step(np.array([action]))
        state = next_state
        reward_value = float(reward[0])
        total_reward += reward_value
        step_count += 1

        if reward_value > 0:
            valid_count += 1
            valid_action_distribution[action] += 1

        if bool(done[0]):
            logger.warning(f"Episode terminated early at step {step + 1}")
            break

    valid_percentage = (valid_count / step_count * 100) if step_count else 0.0

    logger.info("Evaluation completed:")
    logger.info(f"  Total reward: {total_reward:.2f}")
    logger.info(f"  Valid actions: {valid_percentage:.1f}%")
    logger.info(f"  Total steps: {step_count}")

    return {
        'valid_percentage': valid_percentage,
        'action_distribution': action_distribution,
        'valid_action_distribution': valid_action_distribution,
    }
    
# ----------------------------- Main Processing -----------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run DQN inference from YAML config")
    parser.add_argument("--config", default="configs/exp1.yaml", help="Path to YAML config")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    data_path = config.data_dir / config.dataset.filename

    df = pd.read_csv(data_path)
    states_train, _ = train_test_split(df, test_size=config.data_test_size, random_state=2)

    seed = 2
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    final_nb_aps = config.env.final_nb_aps
    env = DummyVecEnv([
        lambda: APSelectionEnv(
            states_train,
            num_aps=config.env.eval.num_aps,
            on_line=config.env.eval.on_line,
            final_nb_aps=final_nb_aps,
        )
    ])

    q_net = DQN.load("dqn_model_50_sb3", env)
    start_time = time.perf_counter()
    results = evaluate(env, q_net)
    end_time = time.perf_counter()

    logger.info(f"Execution time: {end_time - start_time:.6f} seconds")
    plot_stacked_actions(results['action_distribution'], results['valid_action_distribution'])
    logger.info("All operations completed successfully!")
