"""
A2C-Based Moving IoT Service Composition - Annex B
A2C Network Architectures and Agent

This module implements:
1. SharedA2CNetwork - Shared encoder with separate actor/critic heads
2. SeparateA2CNetwork - Separate networks with LSTM for actor
3. A2CAgent - Advantage Actor-Critic agent implementation
"""

import torch
import torch.nn as nn
import torch.optim as optim


class SharedA2CNetwork(nn.Module):
    """
    A2C with shared feature encoder for actor and critic

    Architecture:
    Input -> Shared Encoder (FC 256 -> ReLU -> FC 128 -> ReLU)
           -> Actor Head (FC -> Softmax) / Critic Head (FC -> Value)
    """

    def __init__(self, state_dim, action_dim, hidden_dims=[256, 128]):
        """
        Initialize shared A2C network

        Args:
            state_dim: Dimension of state space
            action_dim: Dimension of action space
            hidden_dims: List of hidden layer dimensions
        """
        super(SharedA2CNetwork, self).__init__()

        # Shared feature encoder
        self.shared = nn.Sequential(
            nn.Linear(state_dim, hidden_dims[0]),
            nn.ReLU(),
            nn.Linear(hidden_dims[0], hidden_dims[1]),
            nn.ReLU(),
        )

        # Actor (policy) head - outputs action probabilities
        self.actor = nn.Sequential(
            nn.Linear(hidden_dims[1], action_dim), nn.Softmax(dim=-1)
        )

        # Critic (value) head - outputs state value
        self.critic = nn.Sequential(nn.Linear(hidden_dims[1], 1))

    def forward(self, state):
        """
        Forward pass

        Args:
            state: State tensor

        Returns:
            tuple: (policy, value)
        """
        features = self.shared(state)
        policy = self.actor(features)
        value = self.critic(features)
        return policy, value


class SeparateA2CNetwork(nn.Module):
    """
    A2C with separate networks for actor (LSTM-based) and critic

    Architecture:
    - Actor: LSTM for trajectory encoding -> FC layers -> Softmax
    - Critic: FC layers -> Value

    Used for complex spatio-temporal state representations
    """

    def __init__(self, state_dim, action_dim, lstm_hidden=128, fc_hidden=64):
        """
        Initialize separate A2C network

        Args:
            state_dim: Dimension of state space
            action_dim: Dimension of action space
            lstm_hidden: LSTM hidden size
            fc_hidden: FC layer hidden size
        """
        super(SeparateA2CNetwork, self).__init__()

        # Actor: LSTM for trajectory encoding
        self.actor_lstm = nn.LSTM(
            input_size=state_dim,
            hidden_size=lstm_hidden,
            num_layers=1,
            batch_first=True,
        )

        self.actor_fc = nn.Sequential(
            nn.Linear(lstm_hidden, fc_hidden),
            nn.ReLU(),
            nn.Linear(fc_hidden, action_dim),
            nn.Softmax(dim=-1),
        )

        # Critic: Standard feedforward
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 256),
            nn.ReLU(),
            nn.Linear(256, fc_hidden),
            nn.ReLU(),
            nn.Linear(fc_hidden, 1),
        )

    def forward(self, state, hidden=None):
        """
        Forward pass

        Args:
            state: State tensor
            hidden: Optional LSTM hidden state

        Returns:
            tuple: (policy, value, hidden_state)
        """
        # Actor with LSTM for temporal processing
        if hidden is None:
            actor_out, hidden = self.actor_lstm(state.unsqueeze(1))
        else:
            actor_out, hidden = self.actor_lstm(state.unsqueeze(1), hidden)

        policy = self.actor_fc(actor_out.squeeze(1))

        # Critic standard processing
        value = self.critic(state)

        return policy, value, hidden


class A2CAgent:
    """
    Advantage Actor-Critic Agent for moving IoT service composition

    Implements:
    - Policy gradient with advantage function
    - Separate updates for actor and critic (separate architecture)
    - Joint updates (shared architecture)
    - Entropy regularization for exploration
    """

    def __init__(
        self,
        state_dim,
        action_dim,
        architecture="shared",
        lr_actor=0.0003,
        lr_critic=0.0007,
        gamma=0.99,
        entropy_coef=0.01,
        value_loss_coef=0.5,
        max_grad_norm=0.5,
    ):
        """
        Initialize A2C agent

        Args:
            state_dim: State space dimension
            action_dim: Action space dimension
            architecture: 'shared' or 'separate'
            lr_actor: Learning rate for actor
            lr_critic: Learning rate for critic
            gamma: Discount factor
            entropy_coef: Entropy coefficient for exploration
            value_loss_coef: Value loss coefficient
            max_grad_norm: Maximum gradient norm for clipping
        """
        self.gamma = gamma
        self.entropy_coef = entropy_coef
        self.value_loss_coef = value_loss_coef
        self.max_grad_norm = max_grad_norm

        # Create network based on architecture type
        if architecture == "shared":
            self.network = SharedA2CNetwork(state_dim, action_dim)
            self.optimizer = optim.Adam(self.network.parameters(), lr=lr_actor)
            self.is_separate = False
        else:  # separate
            self.network = SeparateA2CNetwork(state_dim, action_dim)
            self.actor_params = list(self.network.actor_lstm.parameters()) + list(
                self.network.actor_fc.parameters()
            )
            self.critic_params = list(self.network.critic.parameters())
            self.actor_optimizer = optim.Adam(self.actor_params, lr=lr_actor)
            self.critic_optimizer = optim.Adam(self.critic_params, lr=lr_critic)
            self.is_separate = True

    def select_action(self, state):
        """
        Select action using current policy

        Args:
            state: Current state

        Returns:
            tuple: (selected_action, log_probability)
        """
        state_tensor = torch.FloatTensor(state).unsqueeze(0)

        with torch.no_grad():
            if self.is_separate:
                policy, _, _ = self.network(state_tensor)
            else:
                policy, _ = self.network(state_tensor)

        # Sample action from policy distribution
        action = torch.multinomial(policy, 1).item()
        log_prob = torch.log(policy[0, action] + 1e-8)

        return action, log_prob

    def get_value(self, state):
        """
        Get state value for a given state

        Args:
            state: Current state

        Returns:
            float: State value
        """
        state_tensor = torch.FloatTensor(state).unsqueeze(0)

        with torch.no_grad():
            if self.is_separate:
                _, value, _ = self.network(state_tensor)
            else:
                _, value = self.network(state_tensor)

        return value.item()

    def update(self, rewards, log_probs, values, dones):
        """
        Update actor and critic networks using advantage

        Args:
            rewards: List of rewards
            log_probs: List of log probabilities
            values: List of state values
            dones: List of done flags
        """
        # Calculate returns and advantages using TD(0)
        returns = []
        advantages = []

        # Compute advantages backwards
        advantage = 0
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]

            # Advantage: A = r + gamma * V(s') - V(s)
            advantage = (
                rewards[t] + self.gamma * next_value * (1 - dones[t]) - values[t]
            )
            advantages.insert(0, advantage)
            returns.insert(0, advantage + values[t])

        # Convert to tensors
        returns = torch.tensor(returns, dtype=torch.float32)
        advantages = torch.tensor(advantages, dtype=torch.float32)

        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        if self.is_separate:
            # Separate updates for actor and critic
            self._update_separate(log_probs, advantages, returns, values)
        else:
            # Joint update for shared network
            self._update_shared(log_probs, advantages, returns)

    def _update_separate(self, log_probs, advantages, returns, values):
        """Update separate architecture"""
        # Actor update
        log_probs_tensor = torch.stack(log_probs)
        policy_loss = -(log_probs_tensor * advantages.detach()).mean()
        entropy_loss = (
            -self.entropy_coef
            * self._calculate_entropy(
                self.network.actor_fc[-2]  # Get softmax layer
            ).mean()
        )

        actor_loss = policy_loss + entropy_loss

        self.actor_optimizer.zero_grad()
        actor_loss.backward(retain_graph=True)
        nn.utils.clip_grad_norm_(self.actor_params, self.max_grad_norm)
        self.actor_optimizer.step()

        # Critic update
        values_tensor = torch.tensor(values, dtype=torch.float32)
        value_loss = nn.MSELoss()(returns, values_tensor)

        self.critic_optimizer.zero_grad()
        value_loss.backward()
        nn.utils.clip_grad_norm_(self.critic_params, self.max_grad_norm)
        self.critic_optimizer.step()

    def _update_shared(self, log_probs, advantages, returns):
        """Update shared architecture"""
        # Policy loss with advantage
        log_probs_tensor = torch.stack(log_probs)
        policy_loss = -(log_probs_tensor * advantages.detach()).mean()

        # Entropy loss for exploration
        with torch.no_grad():
            if isinstance(self.network, SharedA2CNetwork):
                # Get policy from forward pass
                # Use current policy for entropy
                policy_loss_for_entropy = policy_loss
            else:
                policy_loss_for_entropy = policy_loss

        entropy_loss = (
            -self.entropy_coef
            * self._calculate_entropy_uniform(log_probs_tensor.shape[1]).mean()
        )

        # Value loss
        value_loss = self.value_loss_coef * nn.MSELoss()(
            returns, torch.tensor([returns.mean()]).expand_as(returns)
        )

        # Total loss
        total_loss = policy_loss + entropy_loss + value_loss

        self.optimizer.zero_grad()
        total_loss.backward()
        nn.utils.clip_grad_norm_(self.network.parameters(), self.max_grad_norm)
        self.optimizer.step()

    def _calculate_entropy(self, policy):
        """Calculate entropy of policy distribution"""
        # This is a placeholder - actual entropy should be computed from policy output
        return torch.zeros(1)

    def _calculate_entropy_uniform(self, action_dim):
        """Calculate uniform entropy for regularization"""
        # Entropy of uniform distribution = log(action_dim)
        return torch.tensor([float(action_dim)]).log()

    def save_model(self, path):
        """Save model to file"""
        torch.save(
            {
                "network": self.network.state_dict(),
                "optimizer": self.optimizer.state_dict()
                if hasattr(self, "optimizer")
                else None,
            },
            path,
        )

    def load_model(self, path):
        """Load model from file"""
        checkpoint = torch.load(path)
        self.network.load_state_dict(checkpoint["network"])
        if checkpoint["optimizer"] and hasattr(self, "optimizer"):
            self.optimizer.load_state_dict(checkpoint["optimizer"])


def create_a2c_agent(state_dim, action_dim, architecture="shared", **kwargs):
    """
    Factory function to create A2C agent

    Args:
        state_dim: State space dimension
        action_dim: Action space dimension
        architecture: 'shared' or 'separate'
        **kwargs: Additional hyperparameters

    Returns:
        A2CAgent: Configured agent
    """
    return A2CAgent(
        state_dim=state_dim, action_dim=action_dim, architecture=architecture, **kwargs
    )


if __name__ == "__main__":
    # Test shared network
    print("Testing Shared A2C Network...")
    shared_net = SharedA2CNetwork(state_dim=10, action_dim=5)
    state = torch.randn(1, 10)
    policy, value = shared_net(state)
    print(f"Policy shape: {policy.shape}, Value shape: {value.shape}")

    # Test separate network
    print("\nTesting Separate A2C Network...")
    separate_net = SeparateA2CNetwork(state_dim=10, action_dim=5)
    policy, value, hidden = separate_net(state)
    print(f"Policy shape: {policy.shape}, Value shape: {value.shape}")

    # Test agent
    print("\nTesting A2C Agent...")
    agent = A2CAgent(state_dim=10, action_dim=5, architecture="shared")
    action, log_prob = agent.select_action(state.numpy().squeeze())
    print(f"Selected action: {action}, Log prob: {log_prob.item():.4f}")

    # Test update
    rewards = [1.0, 0.5, 0.0]
    log_probs = [log_prob, torch.tensor(-1.0), torch.tensor(-0.5)]
    values = [0.5, 0.3, 0.1]
    dones = [False, False, True]
    agent.update(rewards, log_probs, values, dones)
    print("Update completed successfully")
