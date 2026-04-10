# Paper Comparison: A2C vs Double DQN (Paper 17)

## Executive Summary

| Aspect | Paper 17 (Double DQN) | Your Paper (A2C) | Improvement |
|--------|----------------------|-----------------|------------|
| **Algorithm** | Double DQN | Advantage Actor-Critic | — |
| **Method Type** | Value-based | Policy + Value (Actor-Critic) | — |
| **Proactive** | No (reactive) | Yes (trajectory prediction) | New capability |
| **Network Architecture** | Single (target + online) | Shared + Separate | More options |
| **Trajectory Encoding** | No | LSTM (Separate) | New feature |
| **Convergence Analysis** | No | Yes (Theorems 1-2) | New theoretical grounding |

---

## Problem Formalization

| Component | Paper 17 | Your Paper |
|-----------|----------|----------|
| **MDP Framework** | ✓ | ✓ Preserved |
| **State Space** | Service positions, device position, velocity | Same + Predicted trajectories |
| **Action Space** | Service selection | Same |
| **STR Model** | Distance → STR → Capacity | Same (preserved) |
| **Reward Function** | Capacity-based | Extended with stability |
| **Spatio-Temporal Validity** | Defined | Same |

---

## Key Differences

### 1. Algorithm: Double DQN → A2C

| Double DQN (Paper 17) | A2C (Your Paper) |
|----------------------|-----------------|
| Value-based learning | Policy-based + Value-based |
| Q-value approximation | Advantage function: A(s,a) = Q(s,a) - V(s) |
| Overestimation bias prone | Reduced overestimation |
| ε-greedy exploration | Entropy regularization |
| Single network architecture | Shared + Separate networks |
| Reactive decision-making | Proactive via trajectory prediction |

### 2. Network Architecture

| Paper 17 | Your Paper |
|-----------|----------|
| Single: Target Q-network + Online Q-network | Shared: Common encoder + Actor/Critic heads |
| — | Separate: LSTM actor + Feedforward critic |
| No trajectory encoding | LSTM for trajectory-aware policy |

### 3. Proactive Composition

| Paper 17 | Your Paper |
|-----------|----------|
| Reactive (current positions only) | Proactive (predicted trajectories) |
| No trajectory prediction | Linear velocity-based prediction |
| — | Planning horizon H=10 steps |

### 4. Theoretical Analysis

| Paper 17 | Your Paper |
|-----------|----------|
| No formal analysis | Theorem 1: Convergence rate O(ε̃⁻²) |
| — | Theorem 2: Sample complexity |
| — | Corollary 1: Scalability O(n²) |
| — | Corollary 2: Convergence time |

---

## Datasets (Same)

| Dataset | Paper 17 | Your Paper |
|---------|----------|----------|
| **Indoor (ATC Osaka)** | ✓ 185,554 trajectories, 1.7B samples | Same |
| **Illinois** | ✓ 207 trajectories, 357K samples | Same |
| **Real GPS (Illinois)** | ✗ | ✓ Added (42,480 samples) |

---

## Results Comparison

### Success Rate

| Scenario | Paper 17 (Double DQN) | A2C Shared | A2C Separate |
|----------|---------------------|------------|--------------|
| Pedestrian 2 km/h | 92.4% | 94.1% | 95.2% |
| Pedestrian 10 km/h | 71.8% | 82.3% | 85.7% |
| Vehicle 80 km/h | 54.3% | 67.2% | 73.5% |

**Improvement**: 19.2% absolute at 80 km/h (35% relative)

### Re-composition Frequency

| Metric | Paper 17 | Your Paper |
|--------|----------|----------|
| Double DQN | 124.3/hr | — |
| A2C Separate | — | 69.2/hr |
| **Reduction** | — | **44%** |

### Adaptation Speed

| Metric | Paper 17 | Your Paper |
|--------|----------|----------|
| Mean | 4.7s | 2.3s |
| **Improvement** | — | **51%** |

---

## STR Model (Preserved)

| Component | Paper 17 | Your Paper |
|-----------|----------|----------|
| Distance | $d_{ij} = \sqrt{(x_i-x_j)^2 + (y_i-y_j)^2}$ | Same |
| STR | $1$ if $d \leq R_c$, else $e^{-k(d-R_c)}$ | Same |
| Capacity | $B \cdot \log_2(1 + STR \cdot SNR_{max})$ | Same |
| Reward | Capacity-based | Same + penalties |

**Parameters**: Rc=200-300m, k=0.01-0.05, B=10MHz, SNRmax=1000

---

## What Your Paper Adds

1. **A2C Algorithm**: Policy gradient + value-based for stable learning
2. **Architecture Comparison**: Shared vs Separate networks
3. **Proactive Composition**: Trajectory prediction
4. **Theoretical Analysis**: Convergence proofs and sample complexity
5. **Real GPS Validation**: Illinois dataset (92.3% valid action selection)
6. **Stability**: Entropy regularization reduces re-composition
7. **Production Implementation**: YAML automation, Gymnasium compliance

---

## What Paper 17 Has That Your Paper Needs to Reference

| Paper 17 Feature | Your Paper Status |
|-----------------|----------------|
| Parallel Flock-Based Ground Truth | Not implemented |
| MapReduce Spatio-Temporal | Not implemented |
| Ablation on ground truth comparison | Missing |

---

## Summary

| Metric | Paper 17 | Your Paper | Delta |
|--------|----------|----------|-------|
| Success Rate (80 km/h) | 54.3% | 73.5% | +19.2% |
| Re-composition | 124.3/hr | 69.2/hr | -44% |
| Adaptation | 4.7s | 2.3s | -51% |
| Proactive | No | Yes | ✓ New |
| Theoretical | No | Yes | ✓ New |
| Implementation | Basic | Production | ✓ Improved |

**Your paper successfully adapts Double DQN to A2C while preserving the core STR-based selection from Paper 17. Key improvements in high-mobility scenarios and proactive composition capability.**

---

*Generated: April 2026*