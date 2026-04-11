# Paper 22: PD3QND - Deep RL for QoS-Aware IoT Service Composition

## Basic Information
- **Title**: Deep Reinforcement Learning for QoS-Aware IoT Service Composition: The PD3QND Approach
- **Authors**: Yi Chen, Lianglun Cheng, Tao Wang
- **Year**: 2023
- **Venue**: IEEE 14th International Conference on Software Engineering and Service Science (ICSESS)
- **Algorithm**: DQN with Noise Networks, Prioritized Experience Replay, Double Dueling, Demonstration Learning

---

## Abstract

This paper addresses dynamic QoS-aware IoT service composition in manufacturing environments. The authors propose PD3QND, which combines multiple DQN enhancements to handle dynamic environments with changing QoS values.

---

## Problem Definition

### Challenge
- IoT services have dynamically changing QoS
- Traditional heuristics struggle to adapt
- Need for robust, adaptive composition

### Objective
- Maximize end-to-end QoS
- Adapt to QoS changes
- Avoid cold start problem

---

## PD3QND Components

### 1. Noise Networks
- Add noise to network weights for exploration
- Alternative to epsilon-greedy
- More stable exploration

### 2. Prioritized Experience Replay
- Prioritize important experiences
- Use SumTree for efficient sampling
- Better learning from rare events

### 3. Double Dueling Architecture
- Separate value and advantage functions
- More accurate Q-value estimation
- Reduces overestimation

### 4. Demonstration Learning
- Pre-train on expert solutions
- Faster initial learning
- Avoids poor initial policies

---

## Algorithm Details

### State Space
- Service candidate features
- Workflow state
- Historical QoS

### Action Space
- Service selection decisions

### Reward
- Composite service QoS
- Penalty for constraint violation

### Hyperparameters
| Parameter | Value |
|-----------|-------|
| Learning rate | 0.0003 |
| Discount factor | 0.99 |
| Batch size | 64 |
| Replay buffer | 100,000 |
| Noise decay | 0.999 |

---

## Experimental Results

### Setup
- Manufacturing IoT dataset
- Dynamic QoS simulation
- 50 composition problems

### Performance
- 23% faster convergence than DQN
- 15% better solution quality
- Robust to QoS fluctuations
- No cold start with demonstration learning

---

## Relevance to Thesis

### What's Missing
- Static services (not moving)
- Uses DQN, not A2C
- No trajectory prediction
- No handover mechanism

### What Can Be Used
- Multi-component DQN architecture
- Demonstration learning for pre-training
- Prioritized replay for efficiency

---

## References

1. Chen, Y., Cheng, L., & Wang, T. (2023). Deep Reinforcement Learning for QoS-Aware IoT Service Composition: The PD3QND Approach. *IEEE ICSESS 2023*.