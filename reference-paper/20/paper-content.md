# Paper 20: PPDRL - Pretraining and Policy-Based Deep RL for QoS-Aware Service Composition

## Basic Information
- **Title**: PPDRL: A Pretraining-and-Policy Based Deep Reinforcement Learning Approach for QoS-aware Service Composition
- **Authors**: Kan Yi, Jin Yang, Shuangling Wang, Xiao Ren
- **Year**: 2022
- **Venue**: Security and Communication Networks (Wiley)
- **Algorithm**: Deep Q-Network (DQN) with Pretraining + Policy Scoring

---

## Problem Definition

Service composition combines atomic services to meet complex user requirements. The QoS-aware service composition problem involves selecting optimal concrete services for each abstract service in a composition workflow to maximize end-to-end QoS.

### Challenges
1. **NP-hard optimization**: Exponential search space
2. **Dynamic QoS**: Service QoS changes over time
3. **Large-scale services**: QWS dataset has 2,507 web services across 233 categories
4. **Exploitation vs Exploration**: Balancing optimal solution search with learning efficiency

---

## Proposed Approach: PPDRL-SC

### Two-Phase Framework

**Phase 1: Pretraining with Maximum Likelihood Estimation (MLE)**
- Learn a good initial policy through supervised learning
- Training data: Solutions from genetic algorithm
- Objective: Maximize likelihood of good solutions
- Output: Pretrained Q-network

**Phase 2: Policy Scoring with Deep Q-Learning**
- Fine-tune using DQN with experience replay
- Policy scoring mechanism: Evaluate and rank composite service candidates
- Adaptive exploitation-exploration balance

### State Representation
```
State = (service_attributes, workflow_position)
```
- Service attributes: Response time, availability, throughput, etc.
- Workflow position: Current position in composition workflow

### Action Space
```
Action = Select concrete service for current abstract service
```
- Discrete actions: One per concrete service candidate

### Reward Function
```
R = Σ w_i × QoS_i(composition)
```
- Weighted sum of QoS attributes
- Weights may represent user preferences

### Network Architecture
- Input: Service feature vector
- Hidden: Fully connected layers (128-64-32 neurons)
- Output: Q-value per action

### Hyperparameters
| Parameter | Value |
|-----------|-------|
| Learning rate | 0.001 |
| Discount factor (γ) | 0.9 |
| Replay buffer | 10,000 |
| Batch size | 32 |
| Exploration steps | 10,000 |
| Target update frequency | 1,000 |

---

## Experimental Setup

### Dataset
- **QWS Dataset**: 2,507 real web services in 233 categories
- 60 randomly generated composition problems
- Various sizes and structures

### Baselines
1. Genetic Algorithm (GA)
2. Particle Swarm Optimization (PSO)
3. Q-Learning (tabular)
4. Deep Q-Network (DQN)
5. PRETON (pretraining only)

### Metrics
- Fitness value (QoS optimization)
- Convergence speed
- Solution quality

---

## Results

### Performance Comparison
| Algorithm | Avg Fitness | Convergence (iterations) |
|-----------|-------------|-------------------------|
| GA | 0.72 | 500 |
| PSO | 0.68 | 400 |
| Q-Learning | 0.58 | 600 |
| DQN | 0.65 | 300 |
| PRETON | 0.70 | 200 |
| **PPDRL** | **0.78** | **150** |

### Key Findings
1. PPDRL converges 3-4x faster than GA/PSO
2. Pretraining significantly reduces training time
3. Policy scoring improves exploration efficiency
4. Outperforms all baselines in solution quality

---

## Relevance to Thesis

### What's Missing (Gap Analysis)
- **NOT moving IoT services**: Focus on static web services
- **NOT A2C**: Uses DQN (value-based), not actor-critic
- **NO trajectory prediction**: No mobility modeling
- **NO handover mechanism**: Reactive composition only

### What Can Be Used
- DRL architecture as baseline for comparison
- Pretraining strategy (transfer learning concept)
- QoS optimization framework
- Reward function design

---

## Limitations

1. Static service model - doesn't address service mobility
2. Single-agent approach - no coordination
3. Fixed QoS model - doesn't handle rapid changes
4. No proactive decision-making - purely reactive

---

## References

1. Yi, K., Yang, J., Wang, S., & Ren, X. (2022). PPDRL: A Pretraining-and-Policy Based Deep Reinforcement Learning Approach for QoS-aware Service Composition. *Security and Communication Networks*.