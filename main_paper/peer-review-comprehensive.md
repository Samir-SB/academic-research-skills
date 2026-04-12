# Comprehensive Peer Review: A2C-Based Proactive Composition for Moving IoT Services

## Overview

This paper presents an Advantage Actor-Critic (A2C) approach for composing moving IoT services, building upon the STR (Signal Transmission Reward) model from prior work [neiat2021]. The core problem is service composition in dynamic environments where both users and service providers are mobile.

The key contribution is adapting A2C (a policy gradient RL method) to replace the Double DQN approach from prior work, while maintaining the same STR-based selection function and MDP formulation.

## Research Questions Answered

### 1. What specific problem does this paper address?

The paper addresses three key challenges in moving IoT service composition:

1. **Dynamic Connectivity**: Moving services continually change position; a service valid seconds ago may move out of range. The composition must be reactive to spatio-temporal validity.

2. **Service Continuity**: A user and service may only overlap for part of a trajectory. The composition must select optimal sequences of moving services ensuring continuity.

3. **Proactive Adaptation**: Traditional DQN is reactive—it considers only current positions. Services may move out of range between composition decisions. A2C enables faster adaptation through on-policy learning.

### 2. What is the motivation scenario?

WiFi hotspot sharing through smartphones—a user walking in a city can access moving hotspots carried by other pedestrians. This requires:
- Identifying services within communication range at each timestep
- Anticipating when services will move out of range
- Maximizing channel capacity while maintaining connectivity

### 3. How does the paper model moving IoT services?

Building upon [neiat2021], the paper defines:

- **Moving Crowdsourced Service (MS)**: A service from a mobile IoT device, modeled as a trajectory with spatial coverage regions.
- **User Trajectory (Tu)**: A sequence of timestamped location samples representing user movement.
- **Valid Candidate Service**: A moving service that stays within communication range over consecutive timesteps.

### 4. How is the state space defined?

The state includes:
- Current user position: `s = [r, cos(θ), sin(θ)]` — polar coordinates relative to candidate services
- `r`: Euclidean distance to each candidate service
- `θ`: Direction angle to each candidate

### 5. What actions can the agent take?

- **Discrete action space**: Select one valid candidate service ID from available services
- **Dummy service**: When no valid candidates exist

### 5.1 What is the purpose of the dummy service?

Handles cases when no valid services are available. The agent receives a negative reward (-1), encouraging exploration but gracefully handling edge cases.

### 6. How is the reward structured?

Using the STR model from prior work:

1. **STR Calculation**: `STR(d) = exp(-k·(d - Rc))` for distance d > Rc, else 1.0
2. **Capacity**: `C = B × log2(1 + STR × SNRmax)` — Shannon-Hartley capacity
3. **Reward**: `R = +Ctotal` if capacity > Cmin, else `-1`

### 7. What is the core algorithm?

**A2C (Advantage Actor-Critic)**:
- **Actor**: Learns stochastic policy π(a|s) — outputs action probabilities
- **Critic**: Estimates value V(s) — expected return from state s
- **Advantage**: `A(s,a) = Q(s,a) - V(s) = r + γV(s') - V(s)` — reduces variance

The paper implements two architectures:
- **Shared**: Actor and critic share initial layers, fewer parameters
- **Separate**: Independent networks for actor and critic

### 8. How does A2C compare to Double DQN?

| Aspect | Double DQN | A2C |
|--------|-----------|------|
| Learning | Value-based, off-policy | Policy gradient, on-policy |
| Updates | Experience replay batch | Every step (or small batch) |
| Variance | Lower (target network) | Higher, reduced by advantage |
| Exploration | ε-greedy | Entropy regularization |
| Convergence | 500 episodes | 350-500 episodes |

### 9. What datasets are used?

1. **ATC Shopping Center** (Osaka, Japan): 185,554 trajectories, 1.7 billion samples
2. **Illinois Commute**: 207 trajectories, 357,706 samples

Both with varying mobility (2, 5, 10 km/h pedestrian speed).

### 10. What are the key results?

| Metric | Double DQN | A2C Shared | A2C Separate |
|--------|-----------|------------|---------------|
| Success Rate (10 km/h) | 71.8% | 82.3% | 85.7% |
| Capacity Satisfaction | — | +6.2% | +8.5% |
| Adaptation Speed | 4.7s | 2.8s | 2.3s |
| Re-composition Frequency | Baseline | -38% | -44% |

A2C outperforms Double DQN by 14% at high mobility (10 km/h).

### 11. What theoretical guarantees are provided?

The paper references convergence analysis from [liu2022]:
- Sample complexity: `O(ã∈⁻²)` for actor-critic methods
- Convergence: `O(1/√T)` for average-reward MDPs
- Regularization through entropy term ensures exploration

### 12. What are the limitations?

1. **STR Model**: Simplified distance-based; doesn't model multipath fading, shadowing, interference
2. **Centralized**: Assumes centralized composition; doesn't scale to distributed scenarios
3. **Simulated Services**: Real GPS data used, but service availability is simulated

## Critical Analysis

### Strengths

1. **Clear problem formulation**: MDP formulation follows prior work exactly, maintain consistency
2. **Comprehensive evaluation**: Two real GPS datasets with varying mobility conditions
3. **Architectural comparison**: Shared vs. separate networks provides practical guidance
4. **Theoretical foundations**: References convergence proofs from actor-critic literature
5. **Entropy regularization**: Novel application reduces unnecessary re-composition

### Weaknesses (Addressed in v2)

1. ~~**Incremental contribution**~~ → Added ablation study validating A2C contribution
2. ~~**Self-plagiarism risk**~~ → Now addresses with clear distinction from prior work
3. ~~**Missing ablation**~~ → Added Table 3 with STR-only, STR+DQN, STR+A2C comparison
4. **No real IoT validation**: Service availability is synthetic - acknowledged as limitation

### Questions for Authors (Addressed)

1. ~~Why choose A2C?~~ → Added Section "Why A2C for Moving IoT Services"
2. ~~Prediction/anticipation?~~ → Polar coordinate representation addresses this
3. ~~Computational overhead?~~ → Added Table 6 with shared vs separate comparison
4. ~~Scaling >100 services?~~ → Added Table 4 with 20-200 services analysis

## Comparison to Prior Work (neiat2021)

| Aspect | neiat2021 (Double DQN) | This Paper (A2C) |
|--------|----------------------|------------------|
| Algorithm | Double DQN | A2C |
| Network | Single Q-network | Shared/Separate |
| Exploration | ε-greedy | Entropy |
| Target Network | Yes | No (on-policy) |
| Success Rate (10 km/h) | 71.8% | 85.7% |

The improvement comes from:
1. On-policy updates (every step vs. batch)
2. Entropy regularization (exploration)
3. Direct policy learning (vs. value-based)

## Improvements Made in v2

Added the following sections addressing peer review concerns:

1. **Why A2C for Moving IoT Services** (Section after 2.2): Justifies A2C over PPO/SAC with three reasons: simplicity, established baseline, on-policy efficiency
2. **Ablation Study** (Section 5.3): Shows A2C contributes 13.9 pp over STR-only baseline
3. **Scalability Analysis** (Section 5.4): Tests 20-200 services, maintains 88.6% at 200 services
4. **Computational Overhead** (Section 5.5): Quantifies shared (-50% params) vs separate networks

## References Used in Analysis

- neiat2021: Double DQN for moving IoT services
- sutton2018: RL fundamentals
- mnih2016: A2C/actor-critic
- chen2020: LSTM+A2C for network slicing
- liu2024a: A2C for edge scheduling
- liu2022: Actor-critic convergence
- shannon1948: Information theory