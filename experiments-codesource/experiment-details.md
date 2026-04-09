# Experiment Code Source - Technical Documentation

This document provides a comprehensive overview of the `experiments-codesource/` directory, which implements a reinforcement learning framework for Access Point (AP) selection in wireless networks.

## Overview

The codebase implements and compares **A2C (Advantage Actor-Critic)** and **DQN (Deep Q-Network)** algorithms for selecting optimal APs in a moving IoT environment. The system is designed for experiment automation with YAML-driven configuration and structured output.

---

## Project Structure

```
experiments-codesource/
├── configs/
│   ├── exp1.yaml          # Example experiment configuration
│   └── exp2.yaml          # Second experiment variant
├── data/
│   ├── random/            # Randomly generated dataset variants
│   │   ├── df_shuffled_100.csv
│   │   └── df_shuffled_200.csv
│   └── selected/          # Curated dataset variants
│       └── df_shuffled_500.csv
├── dataset/
│   ├── illinois_data.csv  # Original Illinois dataset
│   └── overlap_data.csv  # Dataset with AP overlap
├── runs/                  # Per-run artifacts (created at runtime)
├── logs/                  # Run logs (created at runtime)
├── train.py              # Canonical training entrypoint
├── run_experiments.sh    # Background sequential experiment runner
├── config.py             # Config loading interface
├── config_mgmt.py        # Configuration management & Pydantic models
├── illinois_online.py    # Gymnasium environment for AP selection
├── claude_a2c_online.py  # A2C training implementation
├── dqn_baseline3.py       # DQN baseline using Stable Baselines3
├── helper_env.py         # Data preprocessing & state/reward computation
├── training_plots.py     # Visualization utilities
├── utils.py             # Logging & experiment result tracking
├── bruteforce.py        # Brute force baseline for comparison
├── inference_dqn.py     # DQN inference script
├── generate_drl_data.py # Data generation utilities
└── experiments_results.csv  # Aggregated experiment results
```

---

## Core Components

### 1. Configuration Management (`config_mgmt.py`)

The system uses **Pydantic** for type-safe configuration with the following structure:

| Config Class | Description |
|--------------|-------------|
| `networkConfig` | Neural network architecture (hidden_layers, dropout) |
| `TrainingConfig` | RL hyperparameters (lr, gamma, n_steps, entropy_coef) |
| `DatasetConfig` | Dataset filename |
| `EnvPhaseConfig` | Environment settings per phase (num_aps, on_line) |
| `EnvConfig` | Contains train/eval phase configs + final_nb_aps |
| `MasterA2CConfig` | Top-level config aggregating all components |

Key defaults:
- `hidden_layers`: [512, 512, 512]
- `dropout_prob`: 0.5
- `learning_rate`: 1e-4
- `gamma`: 0.9 (discount factor)
- `n_steps`: 15 (bootstrap steps)
- `target_accuracy`: 90%

### 2. Environment (`illinois_online.py`)

**APSelectionEnv** - Custom Gymnasium environment for AP selection:

- **State Space**: Relative polar coordinates (r, cosθ, sinθ) for each AP
  - Format: `[r₁, cos₁, sin₁, r₂, cos₂, sin₂, ..., rₙ, cosₙ, sinₙ]`
  - Dimension: `3 * final_nb_aps`
  
- **Action Space**: Discrete (0 to N) where N is number of APs + 1 (dummy service)

- **Reward Function**: Channel capacity based on distance
  ```
  SNR(d) = 1.0                    if d ≤ 300m
  SNR(d) = exp(-0.01 * (d - 300)) if 300m < d < 500m
  SNR(d) = 0                      if d ≥ 500m
  
  Capacity = log₂(1 + SNR)
  ```

- **Key Features**:
  - Supports both online and offline modes
  - Automatic state padding and permutation for variable AP counts
  - Invalid action penalty for selecting out-of-range APs

### 3. Data Preprocessing (`helper_env.py`)

| Function | Description |
|----------|-------------|
| `gps_to_enu()` | Convert GPS (lat/lon) to local ENU coordinates |
| `enu_to_polar()` | Convert Cartesian to ego-centric polar coordinates |
| `build_ego_polar_states()` | Vectorized state building for all rows |
| `compute_capacity()` | Shannon-capacity based reward computation |
| `reshape_data()` | Flatten consecutive rows into single state vectors |
| `fill_states_columns()` | Pad states to fixed dimension for permutation |

### 4. A2C Implementation (`claude_a2c_online.py`)

**SharedNetwork** architecture:
- Shared feature extraction layers (ReLU + Dropout)
- Separate actor head (logits) and critic head (value)

**A2CAgent**:
- N-step bootstrapping for advantage estimation
- Entropy regularization for exploration
- Gradient clipping (max_norm=1.0)
- Automatic model checkpointing

**Training Loop** (`A2CTrainer`):
- Runs configured number of episodes
- Tracks actor/critic losses, entropy, valid action percentage
- Saves best model based on total reward
- Supports model reloading at intervals

**Evaluation** (`A2CEvaluator`):
- Computes valid action percentage on test set
- Tracks action distribution
- Returns evaluation metrics dictionary

### 5. DQN Baseline (`dqn_baseline3.py`)

Uses **Stable Baselines3** with:
- Custom feature extractor (512-512-512 with dropout)
- DQN with experience replay
- Configurable hyperparameters

---

## Configuration File Format

Example `configs/exp1.yaml`:

```yaml
experiment_name: 40aps_offline
random_seed: 64
train: true
data_dir: data/selected
dataset:
  filename: df_shuffled_500.csv
env:
  final_nb_aps: 50
  train:
    num_aps: 50
    on_line: false
  eval:
    num_aps: 30 
    on_line: false
data_test_size: 0.3

network:
  hidden_layers: [512, 512, 512]
  dropout_prob: 0.5

training:
  learning_rate: 0.00005
  gamma: 0.9
  n_steps: 30
  invalid_action_penalty: -1
  reload_freq: 10
  episodes: 100
  target_accuracy: 98
  entropy_coef: 0.05
  max_grad_norm: 1.0
```

---

## Running Experiments

### Single Experiment
```bash
python train.py --config configs/exp1.yaml
```

### Multiple Experiments (Background)
```bash
./run_experiments.sh configs/exp1.yaml configs/exp2.yaml
```

### Output Structure
```
runs/<run_id>/
├── model/
│   ├── a2c_shared_net.pth
│   └── resolved_config.yaml
├── plot/
│   ├── episode_a2c.png
│   └── stacked_bar_chart.png
└── logs/
    └── <run_id>.log

experiments_results.csv  # Aggregated results across all runs
```

---

## Data Pipeline

1. **Raw Data** (`dataset/illinois_data.csv`): GPS coordinates of users and APs
2. **Preprocessing** (`helper_env.py`): Convert to polar coordinates, compute rewards
3. **Reshaping**: Group consecutive rows into state-action pairs
4. **Padding**: Extend to `final_nb_aps` dimension for consistent input size
5. **Permutation**: Randomly shuffle AP order each episode (prevents ordering bias)

---

## Key Design Decisions

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| State representation | Ego-centric polar (r, cosθ, sinθ) | Translation/rotation invariant |
| Reward function | Shannon capacity | Matches wireless communication theory |
| Network architecture | Shared layers + separate heads | Promotes feature reuse |
| Training approach | N-step returns | Reduces bias-variance tradeoff |
| Model selection | Best total reward | Optimizes overall performance |

---

## Known Issues / Tasks

From `tasks.md`:
- [x] Task 1-4: Completed (YAML config, merged plots, variable inputs, logging improvements)
- [ ] Task 5: Move permutation `p` to reset() function (in progress)

---

## Dependencies

- Python 3.x
- PyTorch
- Gymnasium
- Stable Baselines3
- NumPy, Pandas
- Matplotlib, OpenCV
- PyYAML, Pydantic