# Peer Review Analysis: PPDRL - Pretraining-and-Policy Based Deep RL for QoS-Aware Service Composition

## Overview

This paper addresses the challenge of QoS-aware service composition in large-scale service ecosystems. Unlike traditional optimization approaches, PPDRL combines supervised pretraining with deep reinforcement learning to achieve faster convergence and better solution quality. The key innovation is using genetic algorithm solutions to pretrain the Q-network before RL fine-tuning.

## Research Questions Answered

### 1. What specific problem does this paper address?

The paper addresses four key challenges in QoS-aware service composition:

1. **NP-hard optimization**: The search space grows exponentially with service count, making exhaustive search impractical.

2. **Dynamic QoS**: Service quality attributes change over time, requiring adaptive composition strategies.

3. **Large-scale services**: The QWS dataset contains 2,507 web services across 233 categories, creating a massive selection space.

4. **Exploitation vs Exploration tradeoff**: Balancing optimal solution search with learning efficiency.

### 2. What is the motivation scenario?

The paper uses real-world web service composition from the QWS dataset. Users submit composition workflows (sequences of abstract services), and the system must select concrete service implementations that maximize end-to-end QoS. This is motivated by practical scenarios like:
- Building composite applications from cloud services
- Selecting API implementations in service-oriented architectures
- Optimizing IoT service chains for performance

### 3. How does the paper model the service composition problem?

**Workflow Model**:
- Abstract services represent functional requirements
- Concrete services are candidate implementations with QoS attributes
- Composition forms a directed acyclic graph of service selections

**State Representation**:
```
State = (service_attributes, workflow_position)
```
- Service attributes: Response time, availability, throughput, success rate
- Workflow position: Current position in composition workflow

**Action Space**:
- Discrete: Select one concrete service for each abstract service
- Cardinality equals number of available candidates per workflow step

**Reward Function**:
```
R = Σ w_i × QoS_i(composition)
```
- Weighted sum of normalized QoS attributes
- Weights can represent user preferences

### 4. What is the two-phase PPDRL approach?

**Phase 1: Pretraining (MLE)**
- Generate training data using Genetic Algorithm solutions
- Train Q-network with supervised learning (maximum likelihood)
- Learns good initial policy from "expert" GA solutions
- Output: Pretrained Q-network with reasonable initial weights

**Phase 2: Policy Scoring with DQN**
- Fine-tune using deep Q-learning with experience replay
- Policy scoring mechanism: Evaluate and rank composite service candidates
- Adaptive exploitation-exploration balance
- Uses target network for stability

### 5. What network architecture is used?

**Q-Network Structure**:
- Input: Service feature vector (QoS attributes)
- Hidden layers: Fully connected (128 → 64 → 32 neurons)
- Output: Q-value for each possible action (service selection)
- Activation: ReLU
- Regularization: Dropout (not specified, implied)

**Hyperparameters**:
| Parameter | Value |
|-----------|-------|
| Learning rate | 0.001 |
| Discount factor (γ) | 0.9 |
| Replay buffer | 10,000 |
| Batch size | 32 |
| Exploration steps | 10,000 |
| Target update frequency | 1,000 steps |

### 6. How does it handle dynamic QoS changes?

The paper acknowledges dynamic QoS but doesn't fully address it:
- Pretraining provides initial policy robustness
- DQN's experience replay helps adapt to changes
- No explicit mechanism for rapid QoS fluctuation

### 7. What are the experimental results?

**Dataset**: QWS (Quality Web Service) dataset - 2,507 real web services

**Composition Problems**: 60 randomly generated workflows of various sizes

**Performance Comparison**:
| Algorithm | Avg Fitness | Convergence (iterations) |
|-----------|-------------|-------------------------|
| GA | 0.72 | 500 |
| PSO | 0.68 | 400 |
| Q-Learning | 0.58 | 600 |
| DQN | 0.65 | 300 |
| PRETON (pretrain only) | 0.70 | 200 |
| **PPDRL** | **0.78** | **150** |

**Key Findings**:
1. PPDRL converges 3-4x faster than GA/PSO
2. Pretraining reduces training time significantly
3. Policy scoring improves exploration efficiency
4. Outperforms all baselines in solution quality

### 8. How does PPDRL compare to baselines?

**Strengths over baselines**:
- Faster convergence than pure DQN (150 vs 300 iterations)
- Better solution quality than GA (0.78 vs 0.72)
- More stable than Q-learning (tabular methods fail at scale)

**Weaknesses compared to thesis approach**:
- Static service model - doesn't handle service mobility
- Value-based (DQN) not actor-critic (A2C)
- No trajectory prediction or future state modeling
- No proactive handover mechanism for moving services
- Purely reactive - selects based on current state only

## Strengths of This Paper

1. **Novel pretraining approach**: Using GA solutions for supervised pretraining is innovative and effective.

2. **Practical evaluation**: Uses real-world QWS dataset with 2,507 services.

3. **Comprehensive baselines**: Compares against GA, PSO, Q-learning, DQN, and pretraining-only variants.

4. **Clear framework**: Two-phase approach is well-defined and reproducible.

5. **Good convergence**: Achieves 3-4x faster convergence than state-of-the-art meta-heuristics.

## Weaknesses and Limitations

1. **Static services only**: Doesn't address moving IoT services where location changes over time.

2. **Value-based RL**: Uses DQN (value-based), not A2C (actor-critic). Cannot learn stochastic policies.

3. **No trajectory prediction**: Doesn't model or predict future service positions.

4. **No handover mechanism**: No explicit mechanism for service continuity when QoS degrades.

5. **Reactive only**: Makes decisions based on current state, not proactive based on predicted future.

6. **Single-agent**: No coordination or competition with other agents.

7. **Fixed QoS model**: Assumes QoS changes slowly enough for adaptation; doesn't handle rapid fluctuations.

## Relevance to Thesis

### What's Missing (Critical Gaps)
- **NOT moving IoT services**: Static web services only
- **NOT A2C**: Uses DQN (value-based), not actor-critic
- **NO trajectory prediction**: No mobility modeling
- **NO proactive handover**: Reactive composition only

### What Can Be Used as Baseline
- DRL architecture for comparison (DQN baseline)
- Pretraining strategy concept (transfer learning)
- QoS optimization framework and reward design
- Experimental methodology and evaluation metrics

## Questions for Further Investigation

1. How does the pretraining approach generalize to new composition workflows?
2. Can the policy scoring mechanism handle partially observable states?
3. What happens when QoS changes dramatically between training and deployment?
4. How does the approach scale to thousands of concurrent users?

## Comparison with Paper 17 (Moving IoT Services)

| Aspect | Paper 17 (Neiat) | Paper 20 (PPDRL) |
|--------|------------------|------------------|
| **Services** | Moving IoT | Static web |
| **Algorithm** | Basic deep Q-learning | DQN with pretraining |
| **State** | User trajectory sample | Service attributes |
| **Handover** | Implicit (RL-based) | None |
| **Prediction** | Trajectory overlap | None |
| **Adaptation** | Online learning | DQN adaptation |

**Key insight**: Paper 17 addresses moving services but uses basic Q-learning; Paper 20 uses advanced DQN but for static services. Neither combines moving services with advanced RL like A2C.

---

*Analysis Date: April 2026*
*Thesis: A2C-Based Proactive Composition for Moving IoT Services*