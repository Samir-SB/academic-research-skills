# Code Source Documentation

This document explains the implementation in the `experiments-codesource/` folder, which contains a complete deep reinforcement learning pipeline for service/access point selection in IoT environments.

---

## Overview

The code implements an **Advantage Actor-Critic (A2C)** agent for selecting optimal access points (services) based on location and signal quality. It processes real GPS trajectory data and trains a neural network to make service selection decisions.

```
GPS Trajectories → Data Processing → State/ Reward → A2C Training → Evaluation
```

---

## File Structure

```
experiments-codesource/
├── claude_aug.py          # Data preprocessing pipeline
├── illinois_env.py        # Gymnasium environment
├── claude_a2c.py          # A2C training framework
├── training_plots.py     # Training visualization
├── helper_plot.py        # Action distribution plots
├── data/                 # Dataset folder
│   ├── combined_illinois_data.csv   # Raw GPS data
│   ├── overlap_data.csv             # User-AP overlap info
│   ├── states.csv                   # Processed states
│   ├── rewards.csv                 # Capacity rewards
│   └── 25_aug/                      # Processed dataset (25 APs)
```

---

## 1. Data Preprocessing (claude_aug.py)

### Purpose
Converts raw GPS trajectory data into DRL-ready state and reward matrices.

### Key Classes and Functions

#### Configuration (`Config` class)
```python
EARTH_RADIUS_METERS = 6378137.0
REFERENCE_DISTANCE = 300.0      # meters - full signal threshold
DECAY_RATE = 0.05               # SNR exponential decay
MAX_SIGNAL_RANGE = 500.0        # meters - zero signal threshold
MAX_RANGE = 500.0               # state representation max
```

#### Coordinate Transformations

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `gps_to_enu()` | lat, lon (pedestrian + goal) | (x, y) meters | GPS → East-North-Up local coords |
| `enu_to_polar()` | x, y | (r, θ) | Cartesian → Polar |
| `compute_ego_polar()` | GPS + heading | (r, cos, sin) | Ego-centric state representation |

#### Signal Quality Functions

| Function | Formula | Description |
|----------|---------|-------------|
| `compute_snr()` | SNR = 1.0 if d ≤ 300m<br>SNR = exp(-0.05 × (d-300)) if 300m < d < 500m<br>SNR = 0.0 if d ≥ 500m | Distance → SNR |
| `compute_capacity()` | C = log₂(1 + SNR) | Shannon-Hartley capacity |
| `compute_haversine()` | Great-circle distance | GPS → meters |

#### Main Pipeline (`DRLDataProcessor`)

```python
processor = DRLDataProcessor(
    input_dir=Path('data'),
    output_dir=Path('data'),
    num_samples=200,           # User-AP pairs to sample
    num_access_points=25,     # APs per observation
    random_seed=64
)
processor.run()
```

**Pipeline Steps:**
1. Load and merge trajectory data with overlap info
2. Sample unique user-AP pairs
3. Build state representations [r, cos, sin] per AP
4. Compute capacity rewards
5. Save to states.csv and rewards.csv

---

## 2. Environment (illinois_env.py)

### Purpose
Implements the OpenAI Gymnasium interface for service selection.

### Class: `APSelectionEnv`

```python
env = APSelectionEnv(states_df, rewards_df)
```

#### Key Properties

| Property | Description |
|----------|-------------|
| `num_aps` | Number of access points (columns in rewards) |
| `total_steps` | Number of samples (rows in states) |
| `action_space` | Discrete(25) - selection of one AP |
| `observation_space` | Box((num_aps-1)×3) - 72 features |

#### State Format
```
[r1, cos1, sin1, r2, cos2, sin2, ..., r24, cos24, sin24]
```
- Excludes the 25th AP (reference point)
- Each AP has 3 features: distance, cos(angle), sin(angle)
- Distances clipped at 500m max

#### Reward Format
```
capacity[step, action]  # Pre-calculated capacity for that AP at that step
```

#### Methods

```python
# Reset environment
state, info = env.reset()

# Take action (select AP by index)
next_state, reward, terminated, truncated, info = env.step(action)

# Render (optional)
env.render()
```

---

## 3. A2C Training (claude_a2c.py)

### Purpose
Implements the Advantage Actor-Critic algorithm for training the service selection agent.

### Configuration (`A2CConfig`)

```python
config = A2CConfig(
    state_dim=72,              # Observation size
    action_dim=25,             # Number of APs
    hidden_layers=[512, 512], # Network architecture
    learning_rate=1e-4,
    gamma=0.9,                # Discount factor
    n_steps=60,                # N-step bootstrapping
    entropy_coef=0.05,        # Exploration bonus
    dropout_prob=0.5,
    num_episodes=5,
    device='cuda:0' if available else 'cpu'
)
```

### Network Architecture (`SharedNetwork`)

```
Input (state_dim: 72)
    │
    ▼
Shared Encoder
├── Linear(72 → 512) → ReLU → Dropout(0.5)
├── Linear(512 → 512) → ReLU → Dropout(0.5)
    │
    ▼
┌─────────────┬─────────────┐
│ Actor Head  │ Critic Head │
│ Linear(512→25)│ Linear(512→1)│
│   logits    │    value    │
└─────────────┴─────────────┘
```

### Agent (`A2CAgent`)

```python
agent = A2CAgent(config)
action = agent.act(state)              # Select action
agent.store_transition(s, a, r, s', done)  # Store experience
agent.train_step()                     # Update networks
```

**Training Step:**
```python
# 1. Forward pass
values, logits = model(states)
dist = Categorical(logits=logits)

# 2. Compute n-step returns
targets = rewards + gamma * next_values * (1 - dones)

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

### Trainer (`A2CTrainer`)

```python
trainer = A2CTrainer(agent, env, config)
trainer.train()  # Runs num_episodes
```

### Evaluator (`A2CEvaluator`)

```python
evaluator = A2CEvaluator(agent, test_env, num_steps)
results = evaluator.evaluate(deterministic=True)
# Returns: valid_percentage, action_distribution
```

---

## 4. Visualization (training_plots.py, helper_plot.py)

### training_plots.py

```python
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

### helper_plot.py

```python
plot_stacked_actions(total_actions, valid_actions)
```

Generates stacked bar chart showing:
- Valid actions (green)
- Invalid actions (red)

---

## 5. Main Execution (claude_a2c.py - main())

```python
def main():
    # 1. Load data
    states_df, rewards_df, split_idx = load_data(
        STATES_PATH, REWARDS_PATH, train_split=0.25
    )
    
    # 2. Create environments
    train_env = APSelectionEnv(states_df.iloc[:split_idx], rewards_df.iloc[:split_idx])
    test_env = APSelectionEnv(states_df.iloc[split_idx:], rewards_df.iloc[split_idx:])
    
    # 3. Configure A2C
    config = A2CConfig(
        state_dim=train_env.observation_space.shape[0],
        action_dim=train_env.action_space.n,
        hidden_layers=[512, 512],
        n_steps=60,
        learning_rate=1e-4,
        gamma=0.9,
        num_episodes=5
    )
    
    # 4. Train
    agent = A2CAgent(config)
    trainer = A2CTrainer(agent, train_env, config)
    trainer.train()
    
    # 5. Evaluate
    agent.load_model('a2c_shared_net.pth')
    evaluator = A2CEvaluator(agent, test_env, num_test_steps)
    results = evaluator.evaluate(deterministic=False)
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAW DATA                                 │
├─────────────────────────────────────────────────────────────────┤
│ combined_illinois_data.csv                                      │
│ [id, timestamp, latitude, longitude]                            │
├─────────────────────────────────────────────────────────────────┤
│ overlap_data.csv                                                │
│ [id, s_id, nb_overlap, nb_overlap_500]                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   claude_aug.py                                 │
├─────────────────────────────────────────────────────────────────┤
│ 1. filter_by_timestamp() - Merge by timestamp                  │
│ 2. gps_to_enu() - GPS to local coordinates                      │
│ 3. compute_ego_polar() - Ego-centric polar [r, cos, sin]       │
│ 4. compute_haversine() - Distance in meters                    │
│ 5. compute_snr() - SNR from distance                           │
│ 6. compute_capacity() - Shannon capacity                       │
│ 7. reshape_data() - Group N APs per observation                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESSED DATA                               │
├─────────────────────────────────────────────────────────────────┤
│ states.csv (42,480 × 75)     │ rewards.csv (42,480 × 25)       │
│ [r1,cos1,sin1,...,r24,...]  │ [capacity_AP0, ..., capacity_AP24]│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                illinois_env.py                                  │
├─────────────────────────────────────────────────────────────────┤
│ APSelectionEnv(states_df, rewards_df)                           │
│ • step(action) → reward from rewards_df                         │
│ • _get_obs() → state from states_df                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   claude_a2c.py                                 │
├─────────────────────────────────────────────────────────────────┤
│ SharedNetwork → A2CAgent → A2CTrainer → A2CEvaluator           │
│                                                                  │
│ Training Loop:                                                   │
│ for episode in episodes:                                        │
│   for step in episode:                                          │
│     action = agent.act(state)                                   │
│     next_state, reward = env.step(action)                       │
│     agent.store_transition(s,a,r,s',done)                       │
│     if len(transitions) == n_steps:                             │
│       agent.train_step()                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hyperparameters Summary

| Parameter | Value | Description |
|-----------|-------|-------------|
| learning_rate | 1e-4 | Adam optimizer learning rate |
| gamma | 0.9 | Discount factor for future rewards |
| n_steps | 60 | N-step bootstrapping window |
| entropy_coef | 0.05 | Entropy regularization weight |
| max_grad_norm | 1.0 | Gradient clipping threshold |
| dropout_prob | 0.5 | Dropout rate in shared layers |
| num_episodes | 5 | Training episodes |

---

## Key Formulas

### SNR (Signal-to-Noise Ratio)
```
SNR(d) = 1.0                          if d ≤ 300m
SNR(d) = exp(-0.05 × (d - 300))      if 300m < d < 500m
SNR(d) = 0.0                          if d ≥ 500m
```

### Channel Capacity (Shannon-Hartley)
```
C = log₂(1 + SNR)  [bits/second/Hz]
```

### A2C Advantage
```
A(s,a) = Q(s,a) - V(s) = r + γV(s') - V(s)
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

## Output Files

After training:
- `model/a2c_shared_net.pth` - Trained model weights
- `plot/episode_a2c.png` - Training metrics visualization
- `stacked_bar_chart.png` - Action distribution

---

*Document generated: April 2026*