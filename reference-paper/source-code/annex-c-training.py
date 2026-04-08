"""
A2C-Based Moving IoT Service Composition - Annex C
Training Loop and Utilities

This module implements:
1. train_a2c - Main training loop
2. predict_service_trajectories - Trajectory prediction for proactive composition
3. evaluate_agent - Evaluation functions
4. Visualization utilities
"""

import torch
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import time


def predict_service_trajectories(services, horizon):
    """
    Predict future service trajectories for proactive composition

    Uses linear prediction based on current velocity:
    pos(t) = pos(0) + velocity * t

    Args:
        services: List of service dictionaries
        horizon: Number of future time steps

    Returns:
        dict: Service ID -> list of predicted positions
    """
    trajectories = {}

    for service in services:
        positions = []
        pos = service["position"]
        vel = service["velocity"]

        for t in range(horizon):
            future_pos = [pos[0] + vel[0] * t, pos[1] + vel[1] * t]
            positions.append(future_pos)

        trajectories[service["id"]] = positions

    return trajectories


def predict_service_trajectories_with_noise(services, horizon, noise_std=0.1):
    """
    Predict future service trajectories with noise for robustness

    Args:
        services: List of service dictionaries
        horizon: Number of future time steps
        noise_std: Standard deviation of noise

    Returns:
        dict: Service ID -> list of predicted positions
    """
    trajectories = {}

    for service in services:
        positions = []
        pos = service["position"]
        vel = service["velocity"]

        for t in range(horizon):
            # Add noise to prediction for robustness
            noise = np.random.normal(0, noise_std, 2)
            future_pos = [
                pos[0] + vel[0] * t + noise[0],
                pos[1] + vel[1] * t + noise[1],
            ]
            positions.append(future_pos)

        trajectories[service["id"]] = positions

    return trajectories


def extend_state_with_trajectories(state, trajectories):
    """
    Extend state representation with trajectory predictions

    Args:
        state: Current state dictionary
        trajectories: Predicted trajectories

    Returns:
        dict: Extended state
    """
    extended = state.copy()
    extended["trajectories"] = trajectories
    return extended


def calculate_total_capacity(services, device_pos, str_calc):
    """
    Calculate total capacity using STR model

    Args:
        services: List of services
        device_pos: Device position
        str_calc: STRCalculator instance

    Returns:
        float: Total capacity
    """
    total = 0
    for service in services:
        distance = str_calc.calculate_distance(service["position"], device_pos)
        capacity = str_calc.calculate_capacity(distance)
        total += capacity
    return total


def state_to_vector(state, include_trajectories=True, trajectory_horizon=10):
    """
    Convert state dictionary to feature vector for neural network

    Args:
        state: State dictionary
        include_trajectories: Whether to include trajectory features
        trajectory_horizon: Number of trajectory steps

    Returns:
        numpy.ndarray: State vector
    """
    features = []

    # Device position and velocity
    features.extend(state["device_pos"])
    features.extend(state["device_velocity"])

    # Time step (normalized)
    features.append(state["time_step"] / 1000.0)

    # Service positions (flattened)
    num_services = len(state["services"])
    for service in state["services"]:
        features.extend(service["position"])
        features.extend(service["velocity"])
        features.append(service.get("energy", 0) / 30.0)
        features.append(service.get("available_time", 0) / 500.0)

    # Trajectory features
    if include_trajectories and "trajectories" in state:
        for service_id in range(num_services):
            if service_id in state["trajectories"]:
                traj = state["trajectories"][service_id]
                # Include first and last trajectory points
                if len(traj) > 0:
                    features.extend(traj[0])  # First predicted position
                    features.extend(traj[-1])  # Last predicted position

    return np.array(features, dtype=np.float32)


def train_a2c(
    environment,
    agent,
    num_episodes=1000,
    trajectory_horizon=10,
    state_to_vector_fn=state_to_vector,
    verbose=True,
):
    """
    Train A2C agent on moving IoT service composition environment

    Args:
        environment: MovingIoTEnvironment instance
        agent: A2CAgent instance
        num_episodes: Number of training episodes
        trajectory_horizon: Trajectory prediction horizon
        state_to_vector_fn: Function to convert state to vector
        verbose: Whether to print progress

    Returns:
        tuple: (episode_rewards, success_rates, metrics)
    """
    episode_rewards = []
    success_rates = []
    convergence_metrics = defaultdict(list)

    for episode in range(num_episodes):
        state = environment.reset()
        episode_reward = 0
        done = False

        log_probs = []
        values = []
        rewards = []

        # Trajectory prediction for proactive composition
        predicted_trajectories = predict_service_trajectories(
            environment.services, trajectory_horizon
        )

        step_count = 0
        while not done:
            # Extend state with trajectory predictions
            extended_state = extend_state_with_trajectories(
                state, predicted_trajectories
            )

            # Convert to vector for neural network
            state_vector = state_to_vector_fn(extended_state)

            # Select action
            action, log_prob = agent.select_action(state_vector)

            # Step environment
            next_state, reward, done = environment.step(action)

            # Get state value for advantage calculation
            state_value = agent.get_value(state_vector)

            # Store transition
            log_probs.append(log_prob)
            values.append(state_value)
            rewards.append(reward)

            episode_reward += reward
            step_count += 1

            # Update state for next iteration
            state = next_state

            # Update trajectory predictions periodically
            if step_count % 10 == 0:
                predicted_trajectories = predict_service_trajectories(
                    environment.services, trajectory_horizon
                )

        # Update agent with collected transitions
        dones = [False] * (len(rewards) - 1) + [True]
        agent.update(rewards, log_probs, values, dones)

        episode_rewards.append(episode_reward)

        # Calculate success rate (percentage of positive rewards)
        success_rate = sum(1 for r in rewards if r > 0) / max(len(rewards), 1) * 100
        success_rates.append(success_rate)

        # Record metrics
        convergence_metrics["rewards"].append(episode_reward)
        convergence_metrics["success_rate"].append(success_rate)
        convergence_metrics["episode_length"].append(step_count)

        if verbose and episode % 100 == 0:
            recent_rewards = np.mean(episode_rewards[-100:])
            recent_success = np.mean(success_rates[-100:])
            print(
                f"Episode {episode}/{num_episodes} - "
                f"Avg Reward: {recent_rewards:.2f}, "
                f"Success Rate: {recent_success:.2f}%"
            )

    return episode_rewards, success_rates, convergence_metrics


def evaluate_agent(
    environment, agent, num_episodes=100, state_to_vector_fn=state_to_vector
):
    """
    Evaluate trained agent performance

    Args:
        environment: MovingIoTEnvironment instance
        agent: Trained A2CAgent instance
        num_episodes: Number of evaluation episodes
        state_to_vector_fn: Function to convert state to vector

    Returns:
        dict: Evaluation metrics
    """
    episode_rewards = []
    success_rates = []
    reconfiguration_counts = []

    for episode in range(num_episodes):
        state = environment.reset()
        done = False

        episode_reward = 0
        success_count = 0
        reconfiguration_count = 0
        prev_action = None

        while not done:
            # Convert state to vector
            state_vector = state_to_vector_fn(state)

            # Select action (greedy for evaluation)
            with torch.no_grad():
                action, _ = agent.select_action(state_vector)

            # Track reconfiguration
            if prev_action is not None and action != prev_action:
                reconfiguration_count += 1
            prev_action = action

            # Step environment
            next_state, reward, done = environment.step(action)

            episode_reward += reward
            if reward > 0:
                success_count += 1

            state = next_state

        episode_rewards.append(episode_reward)
        success_rate = success_count / max(1, environment.time_step) * 100
        success_rates.append(success_rate)
        reconfiguration_counts.append(reconfiguration_count)

    return {
        "mean_reward": np.mean(episode_rewards),
        "std_reward": np.std(episode_rewards),
        "mean_success_rate": np.mean(success_rates),
        "std_success_rate": np.std(success_rates),
        "mean_reconfiguration": np.mean(reconfiguration_counts),
        "std_reconfiguration": np.std(reconfiguration_counts),
    }


def plot_training_curves(episode_rewards, success_rates, save_path=None):
    """
    Plot training convergence curves

    Args:
        episode_rewards: List of episode rewards
        success_rates: List of success rates
        save_path: Optional path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Smooth curves with moving average
    window = 50
    smoothed_rewards = np.convolve(
        episode_rewards, np.ones(window) / window, mode="valid"
    )
    smoothed_success = np.convolve(
        success_rates, np.ones(window) / window, mode="valid"
    )

    # Plot rewards
    ax1.plot(episode_rewards, alpha=0.3, label="Raw")
    ax1.plot(smoothed_rewards, label=f"Smoothed ({window}-episode MA)")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Episode Reward")
    ax1.set_title("Training Rewards")
    ax1.legend()
    ax1.grid(True)

    # Plot success rate
    ax2.plot(success_rates, alpha=0.3, label="Raw")
    ax2.plot(smoothed_success, label=f"Smoothed ({window}-episode MA)")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Success Rate (%)")
    ax2.set_title("Success Rate")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Figure saved to {save_path}")

    plt.close()


def plot_comparison(results_dict, metric="success_rate", save_path=None):
    """
    Plot comparison between multiple algorithms

    Args:
        results_dict: Dict of {name: values}
        metric: Metric name to plot
        save_path: Optional path to save figure
    """
    plt.figure(figsize=(10, 6))

    for name, values in results_dict.items():
        # Smooth with moving average
        window = 20
        smoothed = np.convolve(values, np.ones(window) / window, mode="valid")
        plt.plot(smoothed, label=name)

    plt.xlabel("Episode")
    plt.ylabel(metric)
    plt.title(f"{metric} Comparison")
    plt.legend()
    plt.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    plt.close()


def run_experiment(config):
    """
    Run complete training experiment

    Args:
        config: Configuration dictionary

    Returns:
        dict: Results
    """
    from annex_a_str_environment import MovingIoTEnvironment, STRCalculator
    from annex_b_a2c_networks import A2CAgent

    # Create environment
    str_calc = STRCalculator(
        Rc=config.get("Rc", 250),
        k=config.get("k", 0.03),
        B=config.get("B", 10e6),
        SNR_max=config.get("SNR_max", 1000),
    )

    env = MovingIoTEnvironment(
        num_services=config.get("num_services", 50),
        area_size=config.get("area_size", 1000),
        str_calc=str_calc,
    )

    # Determine state and action dimensions
    state_dim = config.get("state_dim", 300)  # Based on 50 services + trajectories
    action_dim = config.get("num_services", 50) * 2 + 1  # select + replace + maintain

    # Create agent
    agent = A2CAgent(
        state_dim=state_dim,
        action_dim=action_dim,
        architecture=config.get("architecture", "shared"),
        lr_actor=config.get("lr_actor", 0.0003),
        lr_critic=config.get("lr_critic", 0.0007),
        gamma=config.get("gamma", 0.99),
    )

    # Train
    start_time = time.time()
    rewards, success_rates, metrics = train_a2c(
        env,
        agent,
        num_episodes=config.get("num_episodes", 1000),
        trajectory_horizon=config.get("trajectory_horizon", 10),
    )
    training_time = time.time() - start_time

    # Evaluate
    eval_results = evaluate_agent(env, agent, num_episodes=50)

    return {
        "training_rewards": rewards,
        "success_rates": success_rates,
        "metrics": metrics,
        "evaluation": eval_results,
        "training_time": training_time,
    }


if __name__ == "__main__":
    # Test training loop
    from annex_a_str_environment import MovingIoTEnvironment, STRCalculator
    from annex_b_a2c_networks import A2CAgent

    print("Running quick training test...")

    # Setup
    str_calc = STRCalculator(Rc=250, k=0.03)
    env = MovingIoTEnvironment(num_services=20, area_size=500)
    agent = A2CAgent(state_dim=100, action_dim=10, architecture="shared")

    # Quick training (10 episodes for test)
    rewards, success_rates, metrics = train_a2c(
        env, agent, num_episodes=10, verbose=True
    )

    print(f"\nFinal metrics:")
    print(f"  Avg reward: {np.mean(rewards):.2f}")
    print(f"  Avg success rate: {np.mean(success_rates):.2f}%")

    # Evaluate
    eval_results = evaluate_agent(env, agent, num_episodes=5)
    print(f"\nEvaluation:")
    print(f"  Mean reward: {eval_results['mean_reward']:.2f}")
    print(f"  Success rate: {eval_results['mean_success_rate']:.2f}%")
