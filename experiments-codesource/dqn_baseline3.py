import argparse

import gymnasium as gym
import pandas as pd
from sklearn.model_selection import train_test_split
import gymnasium as gym
import torch as th
import torch.nn as nn
from stable_baselines3 import DQN
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

from config_mgmt import load_config
from illinois_online import APSelectionEnv

class CustomDropoutNetwork(BaseFeaturesExtractor):
    """
    Custom feature extractor implementing a [512, 512, 512] 
    architecture with 0.5 Dropout between layers.
    """
    def __init__(self, observation_space: gym.Space, features_dim: int = 512):
        super().__init__(observation_space, features_dim)
        
        # Extract input dimension from a standard 1D continuous state space
        input_dim = observation_space.shape[0]
        
        # Define the custom [512, 512, 512] network with Dropout
        self.network = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            
            nn.Linear(512, features_dim),
            nn.ReLU(),
            nn.Dropout(p=0.2)
        )

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.network(observations)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train/evaluate DQN baseline from YAML config")
    parser.add_argument("--config", default="configs/exp1.yaml", help="Path to YAML config")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    data_path = config.data_dir / config.dataset.filename

    df = pd.read_csv(data_path)

    # split data into training and test data
    states_train, states_test = train_test_split(df, test_size=config.data_test_size, random_state=2)

    
    env_train = APSelectionEnv(
        states_train,
        num_aps=config.env.train.num_aps,
        on_line=config.env.train.on_line,
        final_nb_aps=config.env.final_nb_aps,
    )

    # 2. Inject Custom Network via policy_kwargs
    policy_kwargs = dict(
        features_extractor_class=CustomDropoutNetwork,
        features_extractor_kwargs=dict(features_dim=512),
        net_arch=[] # Essential: Keep empty to prevent SB3 from adding redundant hidden layers
    )

    # 3. Initialize DQN with Stability Best Practices
    model = DQN(
        "MlpPolicy",
        env_train,
        policy_kwargs=policy_kwargs,
        learning_rate=5e-5,          # Lowered LR for stability with deep/dropout networks
        buffer_size=100000,
        learning_starts=5000,        # Ensure sufficient warm-up
        batch_size=64,              # Larger batches help smooth out dropout variance
        gamma=0.9,
        target_update_interval=1000, # Slower target updates for stability
        exploration_fraction=0.2,    # Extended exploration phase
        verbose=1
    )

    # 4. Train Model
    model.learn(total_timesteps=500_000)

    # Save the model
    model.save("dqn_model_50_sb3")

    # ======================================================================================

    env_test = APSelectionEnv(
        states_test,
        num_aps=config.env.eval.num_aps,
        on_line=config.env.eval.on_line,
        final_nb_aps=config.env.final_nb_aps,
    )

    # 2. Wrap it with Monitor
    env_test = Monitor(env_test)

    # Load your model (if not already in memory)
    model = DQN.load("dqn_model_50_sb3") 

    # Evaluate the agent
    mean_reward, std_reward = evaluate_policy(model, env_test, n_eval_episodes=1)

    print(f"Mean reward: {mean_reward} +/- {std_reward}")
    print(f"persentage reward: {100*(mean_reward/env_test.total_steps):.2f}")


if __name__ == "__main__":
    main()
