# Paper 23: Large-Scale Adaptive Service Composition with Deep RL

## Basic Information
- **Title**: Large-Scale and Adaptive Service Composition Based on Deep Reinforcement Learning
- **Authors**: Hongbing Wang, Mingzhu Gu, Qi Yu, Yong Tao, Jiajie Li, Huanhuan Fei, Jia Yan
- **Year**: 2019
- **Venue**: Knowledge-Based Systems (Elsevier)
- **Algorithm**: Adaptive Deep Q-learning and RNN Composition Network (ADQRCN)

---

## Abstract

This paper addresses large-scale and adaptive service composition in dynamic environments. The authors propose ADQRCN, which combines deep Q-learning with recurrent neural networks to handle partially observable service environments.

---

## Problem Definition

### Challenges
1. **Large-scale**: Thousands of candidate services
2. **Dynamic**: QoS changes over time
3. **Partially Observable**: Can't observe full environment state

### Objective
- Adaptive composition in dynamic environments
- Handle large service repositories
- Learn from historical composition data

---

## Proposed Approach: ADQRCN

### Architecture

**1. Deep Q-Network**
- Function approximation for Q-values
- Handles large action spaces

**2. Recurrent Neural Network (RNN)**
- Models temporal dependencies
- Handles partially observable states
- Uses LSTM/GRU cells

**3. Composition Network**
- Sequential service selection
- Considers workflow structure

### State Representation
- Current workflow position
- Available service candidates
- Historical QoS (as sequence)
- Partially observable information

### Action Space
- Select service for each workflow step

### Reward
- End-to-end composition QoS
- Adaptation bonus for dynamic changes

---

## Key Innovations

### 1. POMDP Modeling
- Partially Observable Markov Decision Process
- More realistic than full observability

### 2. RNN for State Estimation
- Infer hidden environment states
- Better decision making

### 3. Adaptive Learning Rate
- Adjust based on environment dynamics

---

## Experimental Results

### Setup
- QWS dataset (2,507 web services)
- Simulated dynamic QoS changes
- Various workflow sizes

### Performance
- 30% better than static methods
- Adapts to QoS changes
- Scales to large service pools

---

## Relevance to Thesis

### Limitations for Thesis
- Not moving IoT services
- Uses DQN, not A2C
- No trajectory prediction
- No proactive handover

### Useful Insights
- POMDP modeling for service composition
- RNN for temporal learning
- Adaptive mechanisms

---

## References

1. Wang, H., Gu, M., Yu, Q., Tao, Y., Li, J., Fei, H., & Yan, J. (2019). Large-scale and adaptive service composition based on deep reinforcement learning. *Knowledge-Based Systems*.