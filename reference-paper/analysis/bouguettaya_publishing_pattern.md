# Publishing Pattern Analysis: Bouguettaya's Research & IoT Service Composition Literature

## Executive Summary

This analysis examines the recurring publishing pattern in IoT service composition research, focusing on Athman Bouguettaya's work (Papers 13-17) and validating the pattern through broader academic literature.

---

## 1. Observed Pattern: "Algorithm or Reward Function Change"

### 1.1 Bouguettaya Papers 13-17: The "Add One Feature" Pattern

| Paper | Title | Problem Formulation | Algorithm | Key Addition | Reference |
|-------|-------|---------------------|-----------|--------------|-----------|
| **13** | Crowdsourcing Energy as a Service | Fractional Knapsack | Greedy/Knapsack | Static temporal composition | [E1] |
| **14** | Fluid Composition of Intermittent IoT Energy | ILP + Bin-packing | Constraint satisfaction | **+ Intermittency modeling + adaptation** | [E2] |
| **15** | Proactive Composition of Mobile IoT Energy | Trajectory-based | Trajectory prediction | **+ Mobility + handoff** | [E3] |
| **16** | Elastic Composition of Crowdsourced IoT Energy | Elastic optimization | Genetic Algorithms | **+ Elastic pool + GA** | [E4] |
| **17** | Moving IoT Services (Neiat 2021) | MDP/DRL | Double DQN | **+ Deep RL + trajectory prediction** | [1]

### 1.2 The Pattern: Same Domain, One Change Per Paper

```
Paper 13: Static composition → Fractional Knapsack
     ↓
Paper 14: + Intermittency + Adaptation → ILP/Bin-packing  
     ↓
Paper 15: + Mobility + Trajectory → Proactive composition
     ↓
Paper 16: + Elasticity + GA → Genetic optimization
     ↓
Paper 17: + Deep RL → Double DQN
```

Each paper:
- Stays in the **same domain** (energy service composition)
- Changes **ONE component** (problem formulation, algorithm, or added feature)
- Claims **improvement** over previous work

---

## 2. Detailed Analysis of Papers 13-16

### Paper 13: Crowdsourcing Energy as a Service (Energy-aaS-1)
- **Problem**: Static energy service composition from wearables
- **Algorithm**: Fractional Knapsack
- **QoS Model**: 2D (TSR, DEC)
- **Innovation**: Temporal fractional composition
- **Reference**: [E1]

### Paper 14: Fluid Composition of Intermittent IoT Energy Services (Energy-aaS-2)
- **Problem**: Intermittent energy sources (solar, wind, battery)
- **Algorithm**: ILP + Bin-packing + Adaptation
- **QoS Model**: 6-dimensional (Stability, Reliability, Power Quality, Response Time, Cost, Distance)
- **NEW**: Intermittency stochastic model, adaptation triggers, confidence scoring
- **Reference**: [E2]

### Paper 15: Proactive Composition of Mobile IoT Energy Services (Energy-aaS-3)
- **Problem**: Mobile IoT devices (moving during operation)
- **NEW**: Trajectory prediction, handoff management, proactive pre-configuration
- **Reference**: [E3]

### Paper 16: Elastic Composition of Crowdsourced IoT Energy Services (Energy-aaS-4)
- **Problem**: Crowdsourced energy with uncertainty
- **Algorithm**: Genetic Algorithms + Real-time adaptation
- **NEW**: Elastic pool management, dynamic capacity scaling
- **Reference**: [E4]

### Paper 17: Moving IoT Services (Neiat 2021)
- **Problem**: Moving services (not energy-specific)
- **Algorithm**: Double DQN + Trajectory prediction
- **NEW**: Deep RL formulation, STR model

---

## 3. Academic Literature Validation

### From Web Search Results:

**A) Same Pattern Across All IoT Service Composition Literature:**

| Period | Algorithm | Notes |
|--------|-----------|-------|
| 2015-2017 | GA, PSO, ACO | Early optimization |
| 2018-2020 | ABC, WOA, SFLA | Swarm intelligence |
| 2020-2022 | DQN, Double DQN | First RL (Neiat 2021) |
| 2022-2024 | A2C, PPO, TD3 | Actor-critic |
| 2024-2025 | Hybrid (FPA-TS, DDAPSO) | Combining algorithms |

**B) NP-hard Problem Formulation:**
- "QoS-aware service composition is an NP-hard multi-objective optimization problem" - Yu & Lin 2007
- "Equivalent to Multidimensional Multiple Choice Knapsack Problem (MMKP)"
- Same formulation used across 15+ years of papers

**C) Algorithm Change Pattern:**
- GA → PSO → ACO → ABC → WOA → SFLA → NSGA-II → Hybrid
- Each paper: "We improve upon Y using Z"
- Same problem, different solution approach

---

## 4. Pattern Analysis

### 4.1 Algorithm Evolution

```
Original Problem → Algorithm A → Algorithm B → Algorithm C → ...
        ↓              ↓             ↓            ↓
    Static       Genetic       Intelligent   Hybrid
    Composition  Composition   Composition   Composition
```

### 4.2 Feature Addition Pattern (Bouguettaya Papers)

```
Base (Paper 13)
    ├── + Intermittency → Paper 14
    │       └── + Mobility → Paper 15
    │               └── + Elasticity → Paper 16
    │                       └── + Deep RL → Paper 17
```

### 4.3 Problem Formulation Evolution

```
TSP → Knapsack → MMKP → ILP → MDP → POMDP → Multi-objective
```

---

## 5. True Contribution Requirements

### 5.1 What's Different in Your Research (A2C)?

1. **Problem Formulation**: MDP instead of static optimization
2. **Learning Paradigm**: Actor-Critic instead of value-based or deterministic
3. **State Representation**: Polar coordinates instead of trajectory prediction
4. **Architecture**: Shared vs Separate networks

### 5.2 Why This Pattern Exists

- Easy to publish in conferences/journals
- Provides clear "contribution"
- Easy to compare results
- Doesn't require changing fundamental assumptions

### 5.3 What Could Be Done Differently

- Focus on **new problem formulation**
- Change **fundamental assumptions** (e.g., service discovery vs service selection)
- Use **different real-world data**
- Change **state/action representation**

---

## 6. Conclusion

### Confirmed Pattern (Bouguettaya Papers 13-17):

| Paper | Main Change | Contribution |
|-------|-------------|--------------|
| 13 | Fractional Knapsack | Temporal composition |
| 14 | + Adaptation | Intermittency handling |
| 15 | + Mobility | Trajectory prediction |
| 16 | + GA | Elastic optimization |
| 17 | + DQN | Deep RL |

### The Problem:

- Same core problem domain (energy/service composition)
- Same type of contribution (algorithm + one new feature)
- No fundamental innovation in problem formulation

### What Distinguishes Your Work:

- **A2C** instead of DQN (Neiat 2021)
- **Polar coordinates** instead of trajectory prediction
- **Stable Baselines3** instead of custom implementation
- **Pedestrian data only** (not vehicles)

---

## 7. Drone-as-a-Service (DaaS) Papers - Same Pattern Confirmed!

The user identified the same pattern in the Drone-as-a-Service papers by Bouguettaya's group:

| Paper | Year | Algorithm | Key Addition | Reference |
|-------|------|-----------|--------------|-----------|
| DaaS-1: Composing DaaS for Delivery | 2019 | 3D R-tree + Dijkstra/Heuristic | Basic drone composition | Shahzaad et al., ICWS 2019 [D1] |
| DaaS-2: Constraint-Aware DaaS | 2019 | Multi-armed Bandit + Skyline | Recharging constraints | Shahzaad et al., ICSOC 2019 [D2] |
| DaaS-3: Swarm-based DaaS | 2020 | Modified A* | Swarm behavior (sequential/parallel) | Alkouz et al., arXiv 2020 [D3] |
| DaaS-4: Game-theoretic DaaS | 2020 | Game Theory | Multi-agent negotiation | Shahzaad et al., ICWS 2020 [D4] |
| DaaS-5: Top-k Dynamic DaaS | 2021 | Top-k algorithm | Probabilistic wait/recharge times | Shahzaad et al., arXiv 2021 [D5] |
| DaaS-6: DaaS Under Uncertainty | 2021 | PDR (Predictive) + Spatiotemporal | Uncertainty-aware scheduling | Hamdi et al., IEEE TSC 2021 [D6] |
| DaaS-7: Multi-Package Delivery | 2022 | Graph-based Heuristic | Multi-package SOA | Shahzaad & Bouguettaya, arXiv 2022 [D7] |

### The Pattern in DaaS Papers:

```
DaaS-1: Basic composition → Dijkstra + Heuristic
     ↓
DaaS-2: + Recharging constraints → Multi-armed Bandit + Skyline
     ↓
DaaS-3: + Swarm behavior → Modified A*
     ↓
DaaS-4: + Multi-agent → Game Theory
     ↓
DaaS-5: + Top-k ranking → Probabilistic composition
     ↓
DaaS-6: + Uncertainty → Predictive DQN-style
     ↓
DaaS-7: + Multi-package → Graph-based SOA
```

**Exactly the same pattern!** Each paper:
- Stays in **same domain** (drone delivery services)
- Changes **ONE component** (problem formulation, algorithm, or added feature)
- Claims **improvement** over previous work

---

## 8. Summary: Algorithm Change Pattern in IoT Service Composition

### Cross-Validation: All Bouguettaya Papers Follow Same Pattern

| Domain | Papers | Algorithm Evolution |
|--------|--------|---------------------|
| Energy Services | 13-16 | Knapsack → ILP → Trajectory → GA |
| Moving IoT | 17 | Trajectory → Double DQN |
| Drone Services | DaaS 1-7 | Dijkstra → MAB → A* → Game Theory → Top-k → Predictive → Graph |

### Conclusion

The "algorithm change" pattern is **industry-wide** in IoT service composition research:
1. Same NP-hard problem formulation
2. Apply different optimization/ML algorithm
3. Claim improvement
4. Publish in top venues

Your A2C work follows this same pattern but with:
- **A2C** (Actor-Critic) instead of DQN (Value-based)
- **Polar coordinates** (r, cosθ, sinθ) for state representation
- **Pedestrian datasets** (ATC indoor, Illinois outdoor) instead of synthetic
- **Stable Baselines3** framework

---

## 9. Energy-as-a-Service (EaaS) Papers - Full Pattern

The Energy-as-a-Service papers by Bouguettaya's group follow the exact same pattern:

| Paper | Year | Algorithm | Key Addition | Reference |
|-------|------|-----------|--------------|-----------|
| EaaS-1: Crowdsourcing Energy as a Service | 2018 | Fractional Knapsack | Basic crowdsourced energy | [E1] |
| EaaS-2: Composing Energy Services in Crowdsourced IoT | 2020 | Optimization | Full composition framework | [E2] |
| EaaS-3: Fluid Composition of Intermittent Energy | 2020 | ILP + Bin-packing | Intermittency handling | [E3] |
| EaaS-4: Elastic Composition of Crowdsourced Energy | 2020 | GA + Elastic pool | Elastic capacity scaling | [E4] |
| EaaS-5: Proactive Composition of Mobile Energy | 2021 | Trajectory prediction | Mobility + handoff | [E5] |
| EaaS-6: Fairness-aware Crowdsourcing Energy | 2021 | Fairness optimization | Multi-request fairness | [E6] |
| EaaS-7: Incentive-based Selection and Composition | 2022 | Game Theory + Incentive | Provider incentives | [E7] |
| EaaS-8: QoE Optimization in IoT Energy Services | 2022 | QoE metric | Quality of Experience | [E8] |
| EaaS-9: Service-based Wireless Energy Crowdsourcing | 2022 | Service-based | Ecosystem framework | [E9] |

### The Pattern in EaaS Papers:

```
EaaS-1: Basic crowdsourcing → Fractional Knapsack
     ↓
EaaS-2: + Composition framework → Optimization
     ↓
EaaS-3: + Intermittency → ILP + Bin-packing
     ↓
EaaS-4: + Elasticity → GA + Elastic pool
     ↓
EaaS-5: + Mobility → Trajectory prediction
     ↓
EaaS-6: + Fairness → Multi-request optimization
     ↓
EaaS-7: + Incentives → Game Theory
     ↓
EaaS-8: + QoE → Quality of Experience
     ↓
EaaS-9: + Ecosystem → Service-based framework
```

**Same exact pattern!** Each paper stays in the same domain (energy service composition) and changes ONE component.

---

## References

### Drone-as-a-Service (DaaS) Papers

[D1] B. Shahzaad, A. Bouguettaya, S. Mistry, and A. Ghari Neiat, "Composing drone-as-a-service (DaaS) for delivery," in Proc. IEEE ICWS, 2019, pp. 28-32.

[D2] B. Shahzaad, A. Bouguettaya, S. Mistry, and A. Ghari Neiat, "Constraint-aware drone-as-a-service composition," in Proc. IEEE ICSOC, 2019, pp. 369-382.

[D3] B. Alkouz, A. Bouguettaya, and S. Mistry, "Swarm-based Drone-as-a-Service (SDaaS) for delivery," arXiv:2005.06952, 2020.

[D4] B. Shahzaad, A. Bouguettaya, and S. Mistry, "A game-theoretic drone-as-a-service composition for delivery," in Proc. IEEE ICWS, 2020, pp. 449-453.

[D5] B. Shahzaad and A. Bouguettaya, "Top-k dynamic service composition in skyway networks," arXiv:2111.09153, 2021.

[D6] A. Hamdi, F. D. Salim, D. Y. Kim, A. Ghari Neiat, and A. Bouguettaya, "Drone-as-a-service composition under uncertainty," IEEE Trans. Services Computing, vol. 15, no. 6, pp. 3202-3215, 2021.

[D7] B. Shahzaad and A. Bouguettaya, "Service-oriented architecture for drone-based multi-package delivery," arXiv:2206.04544, 2022.

### Energy-as-a-Service (EaaS) Papers

[E1] A. Lakhdari, A. Bouguettaya, and A. Ghari Neiat, "Crowdsourcing energy as a service," in Proc. IEEE ICSOC, 2018, pp. 342-351.

[E2] A. Lakhdari, A. Bouguettaya, S. Mistry, and A. Ghari Neiat, "Composing energy services in a crowdsourced IoT environment," IEEE Trans. Services Computing, vol. 14, no. 4, pp. 1154-1167, 2020.

[E3] A. Lakhdari, A. Bouguettaya, S. Mistry, and A. Ghari Neiat, "Fluid composition of intermittent IoT energy services," in Proc. IEEE SCC, 2020, pp. 329-336.

[E4] A. Lakhdari, A. Bouguettaya, S. Mistry, A. Ghari Neiat, and B. Suleiman, "Elastic composition of crowdsourced IoT energy services," in Proc. IEEE EAI Mobiquitous, 2020.

[E5] A. Lakhdari and A. Bouguettaya, "Proactive composition of mobile IoT energy services," in Proc. IEEE ICWS, 2021, pp. 192-197.

[E6] A. Lakhdari and A. Bouguettaya, "Fairness-aware crowdsourcing of IoT energy services," in Proc. IEEE ICSOC, 2021, pp. 351-367.

[E7] A. Abusafia, A. Bouguettaya, and S. Mistry, "Incentive-based selection and composition of IoT energy services," in Proc. IEEE ICWS, 2022.

[E8] A. Abusafia, A. Lakhdari, and A. Bouguettaya, "Quality of experience optimization in IoT energy services," in Proc. IEEE ICWS, 2022, pp. 91-96.

[E9] A. Abusafia, A. Lakhdari, and A. Bouguettaya, "Service-based wireless energy crowdsourcing," in Proc. IEEE ICSOC, 2022.