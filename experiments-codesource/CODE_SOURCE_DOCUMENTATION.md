# Code Source Documentation

This document explains the implementation in the `experiments-codesource/` folder, which contains a complete deep reinforcement learning pipeline for service/access point selection in IoT environments.

---

## Overview

The code implements an **Advantage Actor-Critic (A2C)** agent for selecting optimal access points (services) based on location and signal quality. It processes real GPS trajectory data and trains a neural network to make service selection decisions.

The system uses a **YAML-driven experiment automation** workflow with run-based artifact management.

```
YAML Config → train.py → A2C Training → Evaluation → Runs Artifacts
```

---

## File Structure

```
experiments-codesource/
├── train.py                    # Canonical training entrypoint
├── config.py                   # Config loading interface
├── config_mgmt.py              # Pydantic configuration models
├── utils.py                    # Logging, metrics, utilities
├── claude_a2c_online.py        # A2C implementation (SharedNetwork, Agent, Trainer)
├── illinois_online.py          # Gymnasium environment (APSelectionEnv)
├── helper_env.py               # Data preprocessing (GPS→ENU→Polar)
├── training_plots.py           # Training visualization
├── dqn_baseline3.py            # DQN baseline implementation
├── configs/                    # YAML experiment configurations
│   ├── exp1.yaml
│   └── exp2.yaml
├── runs/                       # Run artifacts (created at runtime)
├── logs/                       # Log files (created at runtime)
└── data/                       # Dataset directory
    ├── selected/
    └── random/
```

---

## 1. Configuration System (config_mgmt.py, config.py)

### Purpose
YAML-driven experiment configuration with Pydantic validation.

### Configuration Models

```python
# config_mgmt.py - Pydantic Models
from config_mgmt import MasterA2CConfig, load_config

# Load from YAML
config = load_config("configs/exp1.yaml", run_id="my_run_001")

# Or use config.py wrapper
from config import load_experiment_config
config, run_id = load_experiment_config("configs/exp1.yaml")
```

### Key Configuration Classes

| Class | Description |
|-------|-------------|
| `MasterA2CConfig` | Root config with device, random_seed, directories |
| `networkConfig` | Neural network architecture (hidden_layers, dropout) |
| `TrainingConfig` | Training hyperparameters (lr, gamma, n_steps, entropy_coef) |
| `EnvConfig` | Environment settings (num_aps, on_line mode) |
| `DatasetConfig` | Dataset filename |

### Example YAML Config (configs/exp1.yaml)

```yaml
experiment_name: a2c_experiment
random_seed: 42
train: true

data_dir: data/selected
dataset:
  filename: df_shuffled_200.csv

env:
  final_nb_aps: 50
  train:
    num_aps: 20
    on_line: true
  eval:
    num_aps: 20
    on_line: true

network:
  hidden_layers: [512, 512, 512]
  dropout_prob: 0.5

training:
  learning_rate: 0.00005
  gamma: 0.9
  n_steps: 60
  episodes: 50
  entropy_coef: 0.05
  max_grad_norm: 1.0
  target_accuracy: 95
```

---

## 2. Data Preprocessing (helper_env.py)

### Purpose
Converts raw GPS trajectory data into DRL-ready state and reward matrices.

### Key Classes and Functions

#### STRCalculator
```python
from helper_env import STRCalculator

calc = STRCalculator(
    confident_radius=300,  # meters - full signal threshold
    decay_factor=0.01,     # SNR exponential decay
    max_signal_range=500   # meters - zero signal threshold
)
```

| Function | Description |
|----------|-------------|
| `gps_to_enu()` | Convert GPS (lat, lon) to East-North-Up local coords |
| `enu_to_polar()` | Convert Cartesian to ego-centric polar (r, θ) |
| `compute_capacity()` | Shannon-Hartley capacity: C = log₂(1 + SNR) |
| `compute_rewards()` | Calculate capacity rewards from distance matrix |
| `get_reshaped_states()` | Group N APs per observation |

### SNR Model

```
SNR(d) = 1.0                          if d ≤ Rc
SNR(d) = exp(-k × (d - Rc))           if Rc < d < max_range
SNR(d) = 0.0                           if d ≥ max_range
```

Default: Rc = 300m, k = 0.01, max_range = 500m

---

## 3. Environment (illinois_online.py)

### Purpose
Implements the OpenAI Gymnasium interface for service selection.

### Class: `APSelectionEnv`

```python
from illinois_online import APSelectionEnv

env = APSelectionEnv(
    states_df,      # DataFrame with state vectors
    rewards_df,     # DataFrame with capacity rewards
    num_aps=25,     # Number of access points
    on_line=True    # Online vs offline mode
)
```

#### Key Properties

| Property | Description |
|----------|-------------|
| `num_aps` | Number of access points |
| `total_steps` | Number of samples |
| `action_space` | Discrete(num_aps + 1) - includes dummy action |
| `observation_space` | Box(features) - ego-centric polar state |

#### State Format

```
[r1, cos1, sin1, r2, cos2, sin2, ..., rN, cosN, sinN]
```

- Ego-centric polar: distance (r), direction (cos, sin) relative to user
- For 25 APs: 75 features (25 × 3)

#### Methods

```python
state, info = env.reset()
next_state, reward, terminated, truncated, info = env.step(action)
```

---

## 4. A2C Training (claude_a2c_online.py)

### Purpose
Implements the Advantage Actor-Critic algorithm for training the service selection agent.

### Network Architecture (`SharedNetwork`)

```
Input (state_dim)
    │
    ▼
Shared Encoder
├── Linear(state_dim → hidden[0]) → ReLU → Dropout
├── Linear(hidden[0] → hidden[1]) → ReLU → Dropout
...
    │
    ▼
┌─────────────┬─────────────┐
│ Actor Head  │ Critic Head │
│ Linear→logits│ Linear→value │
└─────────────┴─────────────┘
   Policy π       Value V(s)
```

### Key Classes

| Class | Description |
|-------|-------------|
| `SharedNetwork` | Shared feature encoder with separate actor/critic heads |
| `A2CAgent` | Advantage Actor-Critic agent with n-step returns |
| `A2CTrainer` | Training loop with advantage updates |
| `A2CEvaluator` | Evaluation with valid action percentage |

### Training Step

```python
# 1. Forward pass
values, logits = model(states)
dist = Categorical(logits=logits)

# 2. Compute n-step returns
targets = rewards + gamma ** n_steps * next_values * (1 - dones)

# 3. Compute advantage
advantages = targets - values

# 4. Actor loss (policy gradient + entropy)
actor_loss = -(log_probs * advantages.detach()).mean()
actor_loss -= entropy_coef * entropy

# 5. Critic loss (value prediction)
critic_loss = advantages.pow(2).mean()

# 6. Combined loss + gradient clipping
total_loss = actor_loss + critic_loss
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

---

## 5. Execution Workflow (train.py)

### Run Single Experiment

```bash
python train.py --config configs/exp1.yaml
```

Optional run ID:
```bash
python train.py --config configs/exp1.yaml --run-id my_run_001
```

### Run Multiple Experiments (Background)

```bash
./run_experiments.sh configs/exp1.yaml configs/exp2.yaml
```

### Output Structure

```
runs/<run_id>/
├── model/
│   ├── a2c_shared_net.pth       # Best model checkpoint
│   └── resolved_config.yaml     # Resolved configuration
├── plot/
│   ├── episode_a2c.png          # Training metrics plot
│   └── stacked_bar_chart.png    # Action distribution
└── logs/
    └── <run_id>.log             # Execution logs

logs/<run_id>.log                # Run log
experiments_results.csv          # Aggregated results
```

---

## 6. DQN Baseline (dqn_baseline3.py)

Implements DQN baseline using Stable Baselines3 for comparison with A2C.

```bash
python dqn_baseline3.py --config configs/exp1.yaml
```

---

## 7. Visualization (training_plots.py)

### Training Metrics Plot

```python
from training_plots import plot_training_metrics

plot_training_metrics(
    actor_losses, critic_losses, entropies,
    episode, valid_percentages, best_rewards,
    title, config_dict
)
```

Generates:
- Valid action percentage over episodes
- Actor loss curve
- Entropy loss curve
- Critic loss curve

### Action Distribution Plot

```python
from training_plots import plot_stacked_actions

plot_stacked_actions(total_actions, valid_actions)
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     RAW DATA                                     │
├─────────────────────────────────────────────────────────────────┤
│ dataset/illinois_data.csv                                        │
│ [id, timestamp, latitude, longitude, trajectory_id]             │
├─────────────────────────────────────────────────────────────────┤
│ dataset/overlap_data.csv                                         │
│ [id, s_id, nb_overlap, nb_overlap_500]                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      helper_env.py                              │
├─────────────────────────────────────────────────────────────────┤
│ 1. load_data() - Load CSV files                                 │
│ 2. gps_to_enu() - GPS to local coordinates                      │
│ 3. compute_distance_matrix() - Distance between all pairs      │
│ 4. STRCalculator.compute_rewards() - STR → Capacity              │
│ 5. get_reshaped_states() - Group N APs per observation          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PROCESSED DATA                                 │
├─────────────────────────────────────────────────────────────────┤
│ data/selected/df_shuffled_*.csv                                  │
│ [r1,cos1,sin1,...,rN,cosN,sinN, capacity_AP0,...,capacity_APN] │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 illinois_online.py                               │
├─────────────────────────────────────────────────────────────────┤
│ APSelectionEnv(states_df, rewards_df, num_aps)                  │
│ • step(action) → reward from capacity                           │
│ • reset() → state from preprocessed data                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              claude_a2c_online.py                                │
├─────────────────────────────────────────────────────────────────┤
│ SharedNetwork → A2CAgent → A2CTrainer → A2CEvaluator             │
│                                                                  │
│ Training Loop:                                                   │
│ for episode in episodes:                                        │
│   for step in episode:                                          │
│     action = agent.act(state)                                   │
│     next_state, reward = env.step(action)                      │
│     agent.store_transition(s,a,r,s',done)                       │
│     if len(transitions) == n_steps:                             │
│       agent.train_step()                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT ARTIFACTS                             │
├─────────────────────────────────────────────────────────────────┤
│ runs/<run_id>/model/a2c_shared_net.pth                          │
│ runs/<run_id>/plot/*.png                                        │
│ experiments_results.csv                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hyperparameters Summary

| Parameter | Default | Description |
|-----------|---------|-------------|
| learning_rate | 5e-5 | Adam optimizer learning rate |
| gamma | 0.9 | Discount factor for future rewards |
| n_steps | 60 | N-step bootstrapping window |
| entropy_coef | 0.05 | Entropy regularization weight |
| max_grad_norm | 1.0 | Gradient clipping threshold |
| dropout_prob | 0.5 | Dropout rate in shared layers |
| episodes | 50 | Training episodes |
| target_accuracy | 95 | Early stopping threshold (%) |

---

## Key Formulas

### SNR (Signal-to-Noise Ratio) - STR Model
```
SNR(d) = 1.0                          if d ≤ Rc (300m)
SNR(d) = exp(-k × (d - Rc))           if Rc < d < max_range
SNR(d) = 0.0                          if d ≥ max_range (500m)
```

### Channel Capacity (Shannon-Hartley)
```
C = log₂(1 + SNR)  [bits/second/Hz]
```

### A2C Advantage
```
A(s,a) = Q(s,a) - V(s) = r + γⁿV(s') - V(s)
```

### Actor Loss
```
L_actor = -E[log π(a|s) × A(s,a)] - λ × H(π)
```
Where H(π) is entropy for exploration.

### Critic Loss
```
L_critic = E[A(s,a)²]
```

---

## Legacy Scripts

The following legacy scripts are deprecated but still present:

| File | Status | Description |
|------|--------|-------------|
| `claude_a2c.py` | Deprecated | Old A2C implementation - use `train.py` |
| `illinois_env.py` | Deprecated | Old environment - use `illinois_online.py` |
| `helper_plot.py` | Deprecated | Old plotting - use `training_plots.py` |

---

*Document generated: April 2026*
*Updated to reflect YAML-driven experiment automation system*