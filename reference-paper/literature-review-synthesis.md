# Literature Review Synthesis: Moving IoT Service Composition

## Overview

This document synthesizes key findings from the most relevant papers for the thesis on "A2C-Based Proactive Composition for Moving IoT Services". The focus is on papers that directly address moving IoT services, service composition with mobility, and dynamic service handover.

---

## Papers Analyzed

| Paper | Title | Year | Focus | RL Approach |
|-------|-------|------|-------|--------------|
| Paper 11 | ML in Real-Time IoT Systems | Survey | ML techniques for IoT | N/A (Survey) |
| Paper 17 | Deep RL for Composing Moving IoT Services | 2021 | Moving service composition | Q-learning with NN |
| Paper 18 | Spatially Cohesive Service Discovery and Dynamic Handover | 2017 | Service handover in MANET | Rule-based (DFS/BFS/MST) |

---

## Key Research Challenges in Moving IoT Services

### 1. Service Mobility Modeling

**Paper 17 (Neiat et al.)**:
- Models moving services as moving regions with trajectory samples
- User trajectory represented as timestamped location samples `<ti, xi, yi>`
- Valid candidate: moving service paired with user trajectory over w consecutive timesteps
- Uses trajectory overlap detection for service matching

**Paper 18 (Baek & Ko)**:
- Models spatio-cohesiveness as distance constraints between services
- Distance metric: Euclidean between coordinates
- Cohesiveness achievement: `ri(c) = max(1 - distance/l, 0)` where l is maximum allowed distance

**Paper 11 (Survey)**:
- Identifies ML techniques for trajectory prediction
- Deep learning for time-series forecasting
- Federated learning for distributed IoT

### 2. Service Composition Approaches

**Paper 17 (RL-based)**:
- **Algorithm**: Q-learning with Neural Networks (basic deep Q-learning)
- **State space**: Current user trajectory sample `<t, x, y>`
- **Action space**: Valid candidate service IDs + dummy service
- **Reward**: Based on QoS (capacity), proportional to signal strength
- **Network architecture**: 3 hidden layers × 512 neurons, ReLU, dropout 0.5

**Paper 18 (Rule-based)**:
- **Algorithm**: Spanning tree-based (DFS/BFS/MST)
- **Objective**: Maximize spatio-cohesiveness `RT(c) = Σ min(ri) / |ST ∪ {u}|`
- **Handover**: Integrated in objective function with hysteresis margin
- **At i=0**: `cSC(s0) = min(RT(c))`
- **At i>0**: `cSC(si) = min(RT(c), handover(c(si) - cSC(si-1)))`

### 3. Dynamic Service Handover

**Paper 17**:
- Uses **trajectory overlap detection** (NOT prediction)
- No explicit handover mechanism
- Agent learns to select best available service at each step
- Dummy service handles "no valid candidates" scenario

**Paper 18**:
- **Explicit handover mechanism** with hysteresis margin + threshold
- Handover decision based on spatio-cohesiveness degradation
- Objective function integrates handover cost
- Maintains service quality by switching to alternative services

---

## Comparative Analysis

| Aspect | Paper 17 | Paper 18 |
|--------|----------|----------|
| **Problem** | Compose moving IoT services | Discover + handover in MANET |
| **Algorithm** | Q-learning with NN | Rule-based (DFS/BFS/MST) |
| **State space** | User trajectory sample | Service locations + distances |
| **Action space** | Service IDs + dummy | Service selection from candidates |
| **Handover** | Implicit (via RL) | Explicit with threshold |
| **Prediction** | ❌ Not addressed | ❌ Not addressed |
| **QoS model** | Signal strength (Shannon-Hartley) | Spatio-cohesiveness |

---

## Research Gaps Identified

### 1. Trajectory Prediction Gap
- **Paper 17**: Uses trajectory overlap detection, NOT prediction
- **Paper 18**: No prediction mechanism
- **Paper 11**: Identifies ML for trajectory prediction as emerging area
- **Thesis contribution**: Proactive composition using trajectory prediction

### 2. Handover Mechanism Gap
- **Paper 17**: Implicit via RL, no explicit handover policy
- **Paper 18**: Explicit but rule-based, threshold-based
- **Thesis contribution**: A2C-based proactive handover

### 3. Scalability Gap
- **Paper 17**: Centralized RL, no distributed approach
- **Paper 18**: Centralized composition
- **Thesis contribution**: Consider edge-based deployment

### 4. RL Approach Gap
- **Paper 17**: Basic Q-learning, no advantage actor-critic
- **Thesis contribution**: A2C for better sample efficiency and continuous action spaces

---

## Methodological Insights for Thesis

### From Paper 17 (Most Relevant)
1. **State representation**: User trajectory as state - relevant for your thesis
2. **Action space design**: Include dummy service for handling unavailable services
3. **Reward design**: Based on QoS capacity, normalized to [0, 1]
4. **Network architecture**: Deep networks (512 units) work for trajectory-based state

### From Paper 18 (Handover)
1. **Spatio-cohesiveness metric**: `ri(c) = max(1 - distance/l, 0)` - adaptable
2. **Hysteresis approach**: Threshold-based handover decision
3. **Objective function integration**: Handover cost in composition objective

### From Paper 11 (ML Survey)
1. **Deep learning for prediction**: LSTM, GRU for trajectory forecasting
2. **Edge computing**: ML at edge for low-latency decisions
3. **Federated learning**: Privacy-preserving distributed ML

---

## Summary

The literature reveals:
1. **Limited work on moving IoT service composition** - Papers 17 and 18 are the most relevant
2. **No trajectory prediction** - Current approaches use overlap detection, not prediction
3. **Rule-based or basic RL** - Paper 18 uses rules, Paper 17 uses basic Q-learning
4. **Thesis opportunity**: A2C-based proactive composition with trajectory prediction and dynamic handover

---

## Next Steps

1. Continue literature review synthesis in main paper
2. Create summary table for all 18 reference papers
3. Draft literature review chapter incorporating these findings