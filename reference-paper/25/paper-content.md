# Paper 25: Large-Scale Service Composition Using Deep RL

## Basic Information
- **Title**: A Deep Reinforcement Learning Approach for Large-Scale Service Composition
- **Authors**: Ahmed Moustafa, Takayuki Ito
- **Year**: 2018
- **Venue**: PRIMA 2018 (Principles and Practice of Multi-Agent Systems)
- **Algorithm**: Deep Q-Network (DQN) for large-scale composition

---

## Abstract

This paper addresses the challenge of service composition in large-scale, dynamic service-oriented environments. Traditional composition approaches fail to handle the high scalability, complexity, and dynamicity of modern IoT and web service ecosystems. The proposed approach uses deep reinforcement learning to adaptively compose services in dynamic environments with large numbers of services.

---

## Problem Definition

### Challenges in Large-Scale Composition
1. **Scalability**: Thousands of services with similar functions
2. **Dynamicity**: QoS changes over time
3. **Complexity**: Multiple composition workflows
4. **Adaptability**: Need for online adaptation

### Objective
- Find optimal composition that maximizes QoS
- Adapt to environment changes
- Handle partially observable states

---

## Proposed Approach

### Deep RL Framework

**State Representation**
- Current workflow position
- Available service candidates
- QoS history

**Action Space**
- Select concrete service for each abstract service
- Sequential decision making

**Reward Function**
- End-to-end QoS of composition
- Penalty for constraint violations

### Network Architecture
- **Model**: DQN with experience replay
- **Feature Extraction**: Service attributes as input
- **Output**: Q-values for each action

### Handling Dynamicity
- Continuous retraining
- Epsilon-greedy exploration
- Target network for stability

---

## Experimental Evaluation

### Setup
- Large service repository (thousands of services)
- Various workflow structures
- Dynamic QoS changes

### Baselines
- Genetic Algorithm
- Particle Swarm Optimization
- Random selection

### Results
- Outperforms GA/PSO in dynamic scenarios
- Faster adaptation to QoS changes
- Better scalability

---

## Relevance to Thesis

### What's Missing
- Not moving IoT services (static)
- Uses DQN, not A2C
- No trajectory prediction
- No handover mechanism

### What Can Be Used
- Large-scale composition framework
- Dynamic QoS handling approach
- Network architecture reference

---

## References

1. Moustafa, A., & Ito, T. (2018). A Deep Reinforcement Learning Approach for Large-Scale Service Composition. *PRIMA 2018*.