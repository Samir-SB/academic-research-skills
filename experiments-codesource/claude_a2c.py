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
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Tuple, List, Dict, Optional, Deque
from collections import deque, Counter
import logging

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical

# Import custom modules
from illinois_env import APSelectionEnv
from training_plots import plot_training_metrics, create_bar_chart
from helper_plot import plot_stacked_actions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class A2CConfig:
    """Configuration for A2C training with all hyperparameters."""
    
    # Network architecture
    state_dim: int
    action_dim: int
    hidden_layers: List[int]
    dropout_prob: float = 0.5
    
    # Training parameters
    learning_rate: float = 1e-4
    gamma: float = 0.9  # Discount factor
    n_steps: int = 15  # N-step bootstrapping
    
    # Regularization
    entropy_coef: float = 0.05  # Entropy regularization coefficient
    max_grad_norm: float = 1.0  # Gradient clipping threshold
    
    # Training loop
    num_episodes: int = 50
    
    # Penalties
    invalid_action_penalty: float = -1.0
    
    # Device
    device: str = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    
    # Paths
    model_dir: Path = Path('./model')
    
    # Random seed
    random_seed: int = 42
    
    def __post_init__(self):
        """Ensure model directory exists."""
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Set random seeds for reproducibility
        torch.manual_seed(self.random_seed)
        np.random.seed(self.random_seed)
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary for logging."""
        config_dict = asdict(self)
        config_dict['model_dir'] = str(config_dict['model_dir'])
        return config_dict


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
    
    def __init__(self, config: A2CConfig):
        """
        Initialize the A2C agent.
        
        Args:
            config: Configuration object with all hyperparameters
        """
        self.config = config
        self.device = torch.device(config.device)
        
        # Initialize network
        self.model = SharedNetwork(
            input_size=config.state_dim,
            hidden_layers=config.hidden_layers,
            actor_output_size=config.action_dim,
            dropout_prob=config.dropout_prob
        ).to(self.device)
        
        # Initialize optimizer
        self.optimizer = optim.Adam(
            self.model.parameters(),
            lr=config.learning_rate
        )
        
        # Transition buffer for n-step learning
        self.transitions: Deque = deque(maxlen=config.n_steps)
        
        # Metrics tracker
        self.metrics = MetricsTracker()
        
        # Best model tracking
        self.best_reward = float('-inf')
        
        logger.info(f"Initialized A2C agent on device: {self.device}")
        logger.info(f"Config: {config.to_dict()}")
    
    def act(self, state: np.ndarray, deterministic: bool = False) -> int:
        """
        Select an action given the current state.
        
        Args:
            state: Current environment state
            deterministic: If True, select argmax action; if False, sample
        
        Returns:
            Selected action index
        """
        state_tensor = torch.FloatTensor(state).to(self.device)
        
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
        if len(self.transitions) < self.config.n_steps:
            return  # Not enough transitions yet
        
        # Prepare batch
        states, actions, next_states, rewards, dones = self._prepare_batch()
        
        # Forward pass - current states
        values, logits = self.model(states)
        dist = Categorical(logits=logits)
        
        log_probs = dist.log_prob(actions)
        entropy = dist.entropy().mean()
        
        # Forward pass - next states for bootstrapping
        # with torch.no_grad():
        next_values, _ = self.model(next_states)
        
        # Compute n-step returns (TD targets)
        targets = rewards + self.config.gamma * next_values.squeeze(-1) * (1 - dones)
        
        # Compute advantages
        advantages = targets - values.squeeze(-1)
        
        # Actor loss: policy gradient with advantage
        actor_loss = -(log_probs * advantages.detach()).mean()
        
        # Add entropy regularization to encourage exploration
        actor_loss -= self.config.entropy_coef * entropy
        
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
            max_norm=self.config.max_grad_norm
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
    
    def load_model(self, filename: str = 'a2c_shared_net.pth') -> None:
        """
        Load a saved model.
        
        Args:
            filename: Name of the model file to load
        """
        filepath = self.config.model_dir / filename
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
        config: A2CConfig
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
        self.config = config
        self.n_actions = env.action_space.n
        
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
            if reward == 0 and action == self.n_actions - 1:
                reward = self.config.invalid_action_penalty
                valid_actions.append(0)
            else:
                valid_actions.append(1 if reward > 0 else 0)
            
            # Store transition
            self.agent.store_transition(state, action, reward, next_state, done)
            
            # Train when buffer is full
            if len(self.agent.transitions) == self.config.n_steps:
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
        
        # for episode in range(1, self.config.num_episodes + 1):
        episode = 0
        while episode < self.config.num_episodes:
            # Run episode
            total_reward, valid_percentage = self._run_episode(episode)
            
            # Record episode metrics
            self.agent.metrics.record_episode(valid_percentage, total_reward)
            
            # Save best model
            if total_reward > self.agent.best_reward:
                self.agent.best_reward = total_reward
                self.agent.save_model()
                logger.info(f"New best reward: {total_reward:.2f} - Model saved")
            
            if episode // 5 == 0:
                self.agent.load_model('a2c_shared_net.pth')
            
            # Log progress
            logger.info(
                f"Episode {episode}/{self.config.num_episodes} | "
                f"Reward: {total_reward:.2f} | "
                f"Valid Actions: {valid_percentage:.1f}% | "
                f"Best: {self.agent.best_reward:.2f}"
            )
            
            # Plot training metrics
            plot_training_metrics(
                self.agent.metrics.actor_losses,
                self.agent.metrics.critic_losses,
                self.agent.metrics.entropies,
                episode,
                self.agent.metrics.valid_action_percentages,
                self.agent.metrics.best_rewards,
                'Advantage Actor-Critic (A2C) - Shared Network',
                self.config.to_dict()
            )
            
            if valid_percentage < 50:
                self.config.num_episodes += 1
            else:
                self.config.num_episodes = episode
            
            episode += 1
        
        # Save final model
        self.agent.save_model('_final')       
        
        
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
        test_env: APSelectionEnv,
        num_steps: int
    ):
        """
        Initialize the evaluator.
        
        Args:
            agent: Trained A2C agent
            test_env: Test environment
            num_steps: Number of steps to evaluate
        """
        self.agent = agent
        self.test_env = test_env
        self.num_steps = num_steps
        
        logger.info(f"Evaluator initialized for {num_steps} steps")
    
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
        
        # # Create visualizations
        # plot_stacked_actions(action_distribution, valid_action_distribution)
        
        return {
            # 'total_reward': total_reward,
            'valid_percentage': valid_percentage,
            'action_distribution': action_distribution,
            'valid_action_distribution': valid_action_distribution,
            # 'num_steps': len(all_actions)
        }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def load_data(
    states_path: Path,
    rewards_path: Path,
    train_split: float = 2/3
) -> Tuple[pd.DataFrame, pd.DataFrame, int]:
    """
    Load and split data into train and test sets.
    
    Args:
        states_path: Path to states CSV file
        rewards_path: Path to rewards CSV file
        train_split: Fraction of data to use for training
    
    Returns:
        Tuple of (states_df, rewards_df, split_index)
    """
    logger.info("Loading data...")
    
    states_df = pd.read_csv(states_path)
    rewards_df = pd.read_csv(rewards_path)
    
    split_idx = int(len(states_df) * train_split)
    
    logger.info(f"Loaded {len(states_df)} samples")
    logger.info(f"Train: {split_idx} | Test: {len(states_df) - split_idx}")
    
    return states_df, rewards_df, split_idx


def main():
    """Main execution function."""
    
    # Paths
    DATA_DIR = Path('data/25_aug')
    STATES_PATH = DATA_DIR / 'states.csv'
    REWARDS_PATH = DATA_DIR / 'rewards.csv'
    
    # Load data
    states_df, rewards_df, split_idx = load_data(STATES_PATH, REWARDS_PATH, train_split=0.25)
    
    # Create environments
    train_env = APSelectionEnv(
        states_df.iloc[:split_idx, :],
        rewards_df.iloc[:split_idx, :]
    )
    
    test_env = APSelectionEnv(
        states_df.iloc[split_idx:, :],
        rewards_df.iloc[split_idx:, :]
    )
    
    # Configuration
    config = A2CConfig(
        state_dim=train_env.observation_space.shape[0],
        action_dim=train_env.action_space.n,
        hidden_layers=[512, 512],
        n_steps=60,
        learning_rate=1e-4,
        gamma=0.9,
        dropout_prob=0.5,
        num_episodes=5
    )
    
    logger.info(f"State dimension: {config.state_dim}")
    logger.info(f"Action dimension: {config.action_dim}")
    
    # Initialize agent
    agent = A2CAgent(config)
    
    # Train    
    trainer = A2CTrainer(agent, train_env, config)
    num_test_steps = len(states_df) - split_idx
    
    trainer.train()

    # Evaluate
    agent.load_model('a2c_shared_net.pth')

    evaluator = A2CEvaluator(agent, test_env, num_test_steps)
    results = evaluator.evaluate(deterministic=False)       
                
    # Create visualizations
    plot_stacked_actions(results['action_distribution'], results['valid_action_distribution'])
    logger.info("All operations completed successfully!")

if __name__ == '__main__':
    main()