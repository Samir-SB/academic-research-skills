"""
Advantage Actor-Critic (A2C) Training Framework

This module implements a clean, production-ready A2C training pipeline for
access point selection in wireless networks. It features a shared network
architecture with separate actor and critic heads.

Key Features:
- Modular architecture with clear separation of concerns
- Comprehensive logging and metrics tracking
- Configurable hyperparameters via dataclass
- N-step bootstrapping for improved learning
- Gradient clipping and entropy regularization
- Automatic model checkpointing and evaluation
- Visualization of training progress and action distributions
"""

import os
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Tuple, List, Dict, Deque, Optional
from collections import deque, Counter
import logging

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
from sklearn.model_selection import train_test_split

# Import custom modules
from illinois_online import APSelectionEnv
from training_plots import plot_training_metrics, plot_stacked_actions
from config_mgmt import MasterA2CConfig, TrainingConfig
from utils import append_experiment_result, format_duration_minutes, to_project_relative_path

import json
from copy import deepcopy
from typing import Any

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal
from pathlib import Path


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# NEURAL NETWORK ARCHITECTURE
# =============================================================================

class SharedNetwork(nn.Module):
    """
    Shared network architecture for A2C with separate actor and critic heads.
    
    The network consists of:
    1. Shared feature extraction layers
    2. Actor head: outputs action logits (not probabilities)
    3. Critic head: outputs state value estimate
    
    This architecture promotes feature reuse and efficient learning.
    """
    
    def __init__(
        self,
        input_size: int,
        hidden_layers: List[int],
        actor_output_size: int,
        critic_output_size: int = 1,
        dropout_prob: float = 0.1
    ):
        """
        Initialize the shared network.
        
        Args:
            input_size: Dimension of input state
            hidden_layers: List of hidden layer sizes
            actor_output_size: Number of discrete actions
            critic_output_size: Dimension of value output (typically 1)
            dropout_prob: Dropout probability for regularization
        """
        super().__init__()
        
        # Build shared feature extraction layers
        layers = []
        prev_dim = input_size
        
        for layer_size in hidden_layers:
            layers.extend([
                nn.Linear(prev_dim, layer_size),
                nn.ReLU(),
                nn.Dropout(p=dropout_prob)
            ])
            prev_dim = layer_size
        
        self.shared_layers = nn.Sequential(*layers)
        
        # Actor head - outputs logits (no softmax applied here)
        self.actor_head = nn.Linear(prev_dim, actor_output_size)
        
        # Critic head - outputs state value
        self.critic_head = nn.Linear(prev_dim, critic_output_size)
        
        logger.info(
            f"Initialized SharedNetwork: input={input_size}, "
            f"hidden={hidden_layers}, output={actor_output_size}"
        )
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass through the network.
        
        Args:
            x: Input state tensor of shape (batch_size, input_size)
        
        Returns:
            Tuple of (value, logits):
            - value: State value estimate of shape (batch_size, 1)
            - logits: Action logits of shape (batch_size, num_actions)
        """
        shared_features = self.shared_layers(x)
        
        # Actor outputs logits (no softmax)
        logits = self.actor_head(shared_features)
        
        # Critic outputs value
        value = self.critic_head(shared_features)
        
        return value, logits
    
    def save(self, filepath: Path) -> None:
        """
        Save model state dict to file.
        
        Args:
            filepath: Path to save the model
        """
        torch.save(self.state_dict(), filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load(self, filepath: Path) -> None:
        """
        Load model state dict from file.
        
        Args:
            filepath: Path to load the model from
        
        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not filepath.exists():            
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        self.load_state_dict(torch.load(filepath, weights_only=True))
        self.eval()  # Set to evaluation mode
        logger.info(f"Model loaded from {filepath}")


# =============================================================================
# METRICS TRACKER
# =============================================================================

class MetricsTracker:
    """
    Tracks and manages training metrics.
    
    Maintains running statistics for losses, entropy, validation accuracy,
    and other relevant metrics during training.
    """
    
    def __init__(self):
        """Initialize empty metric lists."""
        self.actor_losses: List[float] = []
        self.critic_losses: List[float] = []
        self.entropies: List[float] = []
        self.valid_action_percentages: List[float] = []
        self.episode_rewards: List[float] = []
        self.best_rewards: List[float] = []
    
    def record_step(
        self,
        actor_loss: float,
        critic_loss: float,
        entropy: float
    ) -> None:
        """Record metrics from a training step."""
        self.actor_losses.append(actor_loss)
        self.critic_losses.append(critic_loss)
        self.entropies.append(entropy)
    
    def record_episode(
        self,
        valid_percentage: float,
        episode_reward: float
    ) -> None:
        """Record metrics from an episode."""
        self.valid_action_percentages.append(valid_percentage)
        self.episode_rewards.append(episode_reward)
    
    def get_latest_metrics(self) -> Dict[str, float]:
        """Get the most recent metrics."""
        return {
            'actor_loss': self.actor_losses[-1] if self.actor_losses else 0.0,
            'critic_loss': self.critic_losses[-1] if self.critic_losses else 0.0,
            'entropy': self.entropies[-1] if self.entropies else 0.0,
            'valid_pct': self.valid_action_percentages[-1] if self.valid_action_percentages else 0.0,
        }


# =============================================================================
# A2C AGENT
# =============================================================================

class A2CAgent:
    """
    Advantage Actor-Critic agent with n-step bootstrapping.
    
    This agent uses a shared network architecture and implements the A2C
    algorithm with entropy regularization and gradient clipping for stable
    training.
    """
    
    def __init__(self, config: MasterA2CConfig):
        """
        Initialize the A2C agent.
        
        Args:
            config: Configuration object with all hyperparameters
        """
        self.config = config
        self.device = torch.device(config.device)
        
        # Initialize network
        self.model = SharedNetwork(
            input_size=config.network.state_dim,
            hidden_layers=config.network.hidden_layers,
            actor_output_size=config.network.action_dim,
            dropout_prob=config.network.dropout_prob
        ).to(self.device)
        
        # Initialize optimizer
        self.optimizer = optim.Adam(
            self.model.parameters(),
            lr=config.training.learning_rate
        )
        
        # Transition buffer for n-step learning
        self.transitions: Deque = deque(maxlen=config.training.n_steps)
        
        # Metrics tracker
        self.metrics = MetricsTracker()
        
        # Best model tracking
        self.best_reward = float('-inf')
        
        logger.info(f"Initialized A2C agent on device: {self.device}")
        logger.info(f"Config: {config.training}")
    
    def act(self, state: np.ndarray, deterministic: bool = False) -> int:
        """
        Select an action given the current state.
        
        Args:
            state: Current environment state
            deterministic: If True, select argmax action; if False, sample
        
        Returns:
            Selected action index
        """
        state_tensor = torch.FloatTensor(state.copy()).to(self.device)
        
        with torch.no_grad():
            _, logits = self.model(state_tensor)
            
            if deterministic:
                action = torch.argmax(logits).item()
            else:
                dist = Categorical(logits=logits)
                action = dist.sample().item()
         
        
        return action
    
    def store_transition(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool
    ) -> None:
        """
        Store a transition in the buffer.
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode terminated
        """
        self.transitions.append((state, action, reward, next_state, done))
    
    def _prepare_batch(self) -> Tuple[torch.Tensor, ...]:
        """
        Convert stored transitions to tensors.
        
        Returns:
            Tuple of (states, actions, next_states, rewards, dones) as tensors
        """
        states, actions, rewards, next_states, dones = zip(*self.transitions)
        
        states_t = torch.FloatTensor(np.array(states)).to(self.device)
        actions_t = torch.LongTensor(np.array(actions)).to(self.device)
        rewards_t = torch.FloatTensor(np.array(rewards)).to(self.device)
        next_states_t = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones_t = torch.FloatTensor(np.array(dones)).to(self.device)
        
        return states_t, actions_t, next_states_t, rewards_t, dones_t
    
    def train_step(self) -> None:
        """
        Perform a single training step using stored transitions.
        
        Implements the A2C update with:
        1. Value and policy network forward passes
        2. Advantage estimation using n-step returns
        3. Actor loss with entropy regularization
        4. Critic loss (MSE of value prediction)
        5. Gradient clipping and optimization
        """
        if len(self.transitions) < self.config.training.n_steps:
            return  # Not enough transitions yet
        
        # Prepare batch
        states, actions, next_states, rewards, dones = self._prepare_batch()
        
        # Forward pass - current states
        values, logits = self.model(states)
        dist = Categorical(logits=logits)
        
        log_probs = dist.log_prob(actions)
        entropy = dist.entropy().mean()
        
        # Forward pass - next states for bootstrapping
        with torch.no_grad():
            next_values, _ = self.model(next_states)
       
        # Compute n-step returns (TD targets)
        targets = rewards + self.config.training.gamma * next_values.squeeze(-1) * (1 - dones)
        
        # Compute advantages
        advantages = targets - values.squeeze(-1)
            
        # Actor loss: policy gradient with advantage
        actor_loss = -(log_probs * advantages.detach()).mean()
        
        # Add entropy regularization to encourage exploration
        actor_loss -= self.config.training.entropy_coef * entropy
        
        # Critic loss: MSE of value prediction
        critic_loss = advantages.pow(2).mean()
        
        # Combined loss
        total_loss = actor_loss + critic_loss
        
        # Optimization step
        self.optimizer.zero_grad()
        total_loss.backward()
        
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(
            self.model.parameters(),
            max_norm=self.config.training.max_grad_norm
        )
        
        self.optimizer.step()
        
        # Record metrics
        self.metrics.record_step(
            actor_loss.item(),
            critic_loss.item(),
            entropy.item()
        )
    
    def save_model(self, suffix: str = '') -> None:
        """
        Save the current model.
        
        Args:
            suffix: Optional suffix for the filename
        """
        filename = f'a2c_shared_net{suffix}.pth'
        filepath = self.config.model_dir / filename
        self.model.save(filepath)
    
    def load_model(self, filepath: Path) -> None:
        """
        Load a saved model.
        
        Args:
            filename: Name of the model file to load
        """
        # filepath = self.config.model_dir / filename
        self.model.load(filepath)


# =============================================================================
# TRAINER
# =============================================================================

class A2CTrainer:
    """
    Handles the complete training loop for the A2C agent.
    
    Manages episodes, tracks metrics, saves checkpoints, and provides
    visualization of training progress.
    """
    
    def __init__(
        self,
        agent: A2CAgent,
        env: APSelectionEnv,
        config: TrainingConfig
    ):
        """
        Initialize the trainer.
        
        Args:
            agent: A2C agent to train
            env: Training environment
            config: Training configuration
        """
        self.agent = agent
        self.env = env
        self.cfg = config   
        self.dummy_idx = env.action_space.n - 1 
        
        logger.info("Trainer initialized")
    
    def _run_episode(self, episode_num: int) -> Tuple[float, float]:
        """
        Run a single training episode.
        
        Args:
            episode_num: Current episode number
        
        Returns:
            Tuple of (total_reward, valid_action_percentage)
        """
        state, _ = self.env.reset()
       
        done = False
        total_reward = 0.0
        valid_actions = []
        
        while not done:
            # Select action
            action = self.agent.act(state)
            
            # Execute action in environment
            next_state, reward, terminated, truncated, _ = self.env.step(action)
            done = terminated or truncated
            
            # Apply penalty for invalid actions
            if reward == 0 and action == self.dummy_idx:
                reward = self.cfg.invalid_action_penalty
                valid_actions.append(0)
            else:
                valid_actions.append(1 if reward > 0 else 0)
            
            # Store transition
            self.agent.store_transition(state, action, reward, next_state, done)
            
            # Train when buffer is full
            if len(self.agent.transitions) == self.cfg.n_steps:
                self.agent.train_step()
                self.agent.transitions.clear()
            
            state = next_state
            total_reward += reward
        
        # Calculate validation metric
        valid_percentage = np.mean(valid_actions) * 100
        
        return total_reward, valid_percentage
    
    def train(self) -> None:
        """
        Execute the complete training loop.
        
        Trains the agent for the configured number of episodes, tracks
        metrics, saves checkpoints, and generates visualizations.
        """
        logger.info("=" * 70)
        logger.info("Starting A2C Training")
        logger.info("=" * 70)
        
        reward_percentage = []        
        for episode in range(self.cfg.episodes):
            # Run episode
            total_reward, valid_percentage = self._run_episode(episode)
            
            # Record episode metrics
            self.agent.metrics.record_episode(valid_percentage, total_reward)
            
            # Save best model
            if total_reward > self.agent.best_reward:
                self.agent.best_reward = total_reward
                self.agent.save_model()
                logger.info(f"New best reward: {total_reward:.2f} - Model saved")
            
            # Calculate Reward percentage
            reward_percentage.append(round((total_reward/self.env.total_steps), 4) * 100)
            # Log progress
            logger.info(
                f"Episode {episode}/{self.cfg.episodes} | "
                f"Reward: {total_reward:.2f} | "
                f"Valid Actions: {valid_percentage:.1f}% | "
                f"Best: {self.agent.best_reward:.2f}"
            )
            
            # Plot training metrics
            plot_training_metrics(
                self.agent.metrics.actor_losses,
                self.agent.metrics.critic_losses,
                self.agent.metrics.entropies,
                episode + 1,
                self.agent.metrics.valid_action_percentages,
                reward_percentage,
                'Advantage Actor-Critic (A2C) - Shared Network',              
                self.cfg.model_dump()
            )                     
            
            if (episode + 1) % self.cfg.reload_freq == 0:
                filepath = self.agent.config.model_dir / 'a2c_shared_net.pth'
                self.agent.load_model(filepath)
                # reload only one time
                self.cfg.reload_freq = self.cfg.episodes
            
            if valid_percentage >= self.cfg.target_accuracy:
                break  
        
        logger.info("=" * 70)
        logger.info("Training Completed!")
        logger.info(f"Best reward achieved: {self.agent.best_reward:.2f}")
        logger.info("=" * 70)


# =============================================================================
# EVALUATOR
# =============================================================================

class A2CEvaluator:
    """
    Evaluates a trained A2C agent on a test environment.
    
    Provides metrics and visualizations of agent performance including
    action distributions and reward statistics.
    """
    
    def __init__(
        self,
        agent: A2CAgent,
        test_env: APSelectionEnv
    ):
        """
        Initialize the evaluator.
        
        Args:
            agent: Trained A2C agent
            test_env: Test environment
        """
        self.agent = agent
        self.test_env = test_env
        self.num_steps = test_env.total_steps
        
        logger.info(f"Evaluator initialized for {self.num_steps} steps")
    
    def evaluate(self, deterministic: bool = True) -> Dict:
        """
        Evaluate the agent on the test environment.
        
        Args:
            deterministic: If True, use deterministic (greedy) action selection
        
        Returns:
            Dictionary containing evaluation metrics
        """
        logger.info("Starting evaluation...")
        
        # Set model to evaluation mode
        self.agent.model.eval()
        
        # Reset environment
        state, _ = self.test_env.reset()
        
        # Tracking variables
        total_reward = 0.0
        valid_actions = []
        all_actions = []
        valid_action_choices = []
        
        # Run evaluation
        for step in range(self.num_steps):
            # Select action
            action = self.agent.act(state, deterministic=deterministic)
            all_actions.append(action)
            
            # Execute action
            next_state, reward, terminated, truncated, _ = self.test_env.step(action)
            done = terminated or truncated
            
            # Track valid actions
            is_valid = reward > 0
            valid_actions.append(is_valid)
            
            if is_valid:
                valid_action_choices.append(action)
            
            state = next_state
            total_reward += reward
            
            if done:
                logger.warning(f"Episode terminated early at step {step + 1}")
                break
        
        # Calculate metrics
        valid_percentage = np.mean(valid_actions) * 100
        action_distribution = Counter(all_actions)
        valid_action_distribution = Counter(valid_action_choices)
        
        # Log results
        logger.info(f"Evaluation completed:")
        logger.info(f"  Total reward: {total_reward:.2f}")
        logger.info(f"  Valid actions: {valid_percentage:.1f}%")
        logger.info(f"  Total steps: {len(all_actions)}")
        
        # Create visualizations
        # plot_stacked_actions(action_distribution, valid_action_distribution)
        
        return {
            # 'total_reward': total_reward,
            'valid_percentage': valid_percentage,
            'total_steps': len(all_actions),
            'action_distribution': action_distribution,
            'valid_action_distribution': valid_action_distribution,
            # 'num_steps': len(all_actions)
        }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_experiment(config: MasterA2CConfig, run_id: Optional[str] = None) -> Dict:
    """Run training/evaluation for a pre-loaded config and return eval results."""
    logger.info(f"Starting Experiment: {config.experiment_name}")
    logger.info(f"Training Config: {config.training}")

    # Paths   
    TEST_SIZE = config.data_test_size
    DATA_PATH = config.data_dir / config.dataset.filename
    PROJECT_ROOT = Path(__file__).resolve().parent
    
    # Load data
    df = pd.read_csv(DATA_PATH)
   
   
    # use only 10_000 rows per episode    
    steps = config.env.train.num_aps * 10_000
    df = df.iloc[:steps, :]    
    
    # split data into training and test data
    states_train, states_test = train_test_split(df, test_size = TEST_SIZE,  random_state= 2)
    
    logger.info(f"Test size: {TEST_SIZE} | Train: {len(states_train)} | Test: {len(states_test)}") 
    logger.info(f"Dataset file: {DATA_PATH.name}")
    logger.info(
        "Env config | final_nb_aps=%s | train(num_aps=%s,on_line=%s) | eval(num_aps=%s,on_line=%s)",
        config.env.final_nb_aps,
        config.env.train.num_aps,
        config.env.train.on_line,
        config.env.eval.num_aps,
        config.env.eval.on_line,
    )
    
    # Create environments
    if config.train:
        train_env = APSelectionEnv(
            states_train,
            num_aps=config.env.train.num_aps,
            on_line=config.env.train.on_line,
            final_nb_aps=config.env.final_nb_aps,
        )
    test_env = APSelectionEnv(
        states_test,
        num_aps=config.env.eval.num_aps,
        on_line=config.env.eval.on_line,
        final_nb_aps=config.env.final_nb_aps,
    )
    
    config.network.state_dim = int(test_env.observation_space.shape[0])
    config.network.action_dim = int(test_env.action_space.n)
        
    logger.info(f"State dimension: {config.network.state_dim}")
    logger.info(f"Action dimension: {config.network.action_dim}")
    
    # Initialize agent
    agent = A2CAgent(config)
    
    # Train
    if config.train:
        filepath = agent.config.model_dir / 'a2c_shared_net.pth'
        if config.resume_training:
            agent.load_model(filepath) 
            
        trainer = A2CTrainer(agent, train_env, config.training)        
        trainer.train()
        
        
        agent.load_model(filepath)
           
    else:      
        filepath = PROJECT_ROOT /'model/a2c_shared_net.pth'
        
    # Evaluate
    agent.load_model(filepath)
    
    evaluator = A2CEvaluator(agent, test_env)
    start_time = time.perf_counter()
    results = evaluator.evaluate(deterministic=False)  
    end_time = time.perf_counter()
    elapsed_seconds = end_time - start_time
    logger.info(f"Execution time: {format_duration_minutes(elapsed_seconds)}")
    if results['valid_percentage'] > config.training.target_accuracy:
        config.network.accuracy = results['valid_percentage']
        config.save_resolved()
    
    # Create visualizations
    plot_stacked_actions(results['action_distribution'], results['valid_action_distribution'])

    effective_run_id = run_id or config.model_dir.parent.name
    append_experiment_result(
        {
            "run_id": effective_run_id,
            "experiment_name": config.experiment_name,
            "data_dir": to_project_relative_path(config.data_dir),
            "dataset_filename": config.dataset.filename,
            "train_num_aps": config.env.train.num_aps,
            "train_on_line": config.env.train.on_line,
            "train_total_steps": train_env.total_steps if config.train else 0,
            "eval_num_aps": config.env.eval.num_aps,
            "eval_on_line": config.env.eval.on_line,
            "eval_valid_actions": f"{results['valid_percentage']:.4f}",
            "eval_total_steps": test_env.total_steps,
            "hidden_layers": json.dumps(config.network.hidden_layers),
            "dropout_prob": config.network.dropout_prob,
            "learning_rate": config.training.learning_rate,
            "n_steps": config.training.n_steps,
            "invalid_action_penalty": config.training.invalid_action_penalty,
            "reload_freq": config.training.reload_freq,
        }
    )
    
    logger.info("All operations completed successfully!")
    return results


def main() -> None:
    """Legacy compatibility entrypoint; forwards execution to train.py."""
    import sys
    args = sys.argv[1:]
    forward_args: List[str] = []

    if "--config" in args:
        forward_args = args
    elif "--variant" in args:
        idx = args.index("--variant")
        variant_value = args[idx + 1] if idx + 1 < len(args) else "configs/exp1.yaml"
        if variant_value.endswith(".json"):
            candidate = variant_value[:-5] + ".yaml"
            forward_args = ["--config", candidate]
        else:
            forward_args = ["--config", variant_value]
        # Keep any additional flags (for example --run-id/--help).
        extra_args = args[:idx] + args[idx + 2 :]
        forward_args.extend(extra_args)
    else:
        forward_args = ["--config", "configs/exp1.yaml", *args]

    print(
        "[DEPRECATION] Direct execution of claude_a2c_online.py is deprecated. "
        "Forwarding to train.py."
    )
    os.execvp("python3", ["python3", "train.py", *forward_args])


if __name__ == '__main__':
    main()
