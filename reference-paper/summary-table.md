# Reference Papers Summary Table

## Overview
This table summarizes all 25 reference papers analyzed for the PhD thesis on "A2C-Based Proactive Composition for Moving IoT Services".

---

## Papers 01-10: General IoT Service Composition

| # | Title | Authors | Year | Focus | Algorithm | Relevance |
|---|-------|---------|------|-------|-----------|-----------|
| 01 | Service Composition in Dynamic Environments: A Systematic Review | Various | 2021 | Systematic review (147 studies, 2006-2020) | Survey | Medium - Literature overview |
| 02 | GA + NN for QoS-aware IoT Services Composition | Various | 2022 | QoS optimization with surrogate model | GA + Neural Network | Medium - GA baseline |
| 03 | GA for Fluctuating QoS-Aware Selection | Various | 2022 | Temporal QoS variations | Genetic Algorithm | Medium - GA variation |
| 04 | Spatio-Cohesive Service Selection using ML | Various | 2021 | Spatial proximity + ML prediction | Machine Learning | Medium - Spatial context |
| 05 | IoT Service Selection Mechanisms: Systematic Study | Various | 2020 | Systematic review (114 studies, 2010-2019) | Survey | Medium - Literature overview |

---

## Paper 11: ML in Real-Time IoT Systems

| Attribute | Value |
|-----------|-------|
| **Title** | Machine Learning in Real-Time Internet of Things (IoT) Systems: A Survey |
| **Type** | Survey Paper |
| **Focus** | ML techniques for real-time IoT decision-making |
| **Key Techniques** | Supervised/unsupervised learning, RL, deep learning, federated learning |
| **Application Domains** | Smart cities, healthcare, industrial IoT, transportation |
| **Relevance** | Provides ML background for trajectory prediction |

---

## Papers 12-16: Energy Crowdsourcing (Bouguettaya Group)

| # | Title | Authors | Year | Focus | Algorithm | Scope |
|---|-------|---------|------|-------|-----------|-------|
| 12 | Composing Energy Services in Crowdsourced IoT | Various | 2018 | Crowdsourced energy services | Crowdsourcing Model | Confined area |
| 13 | Crowdsourcing Energy as a Service | Lakhdari et al. | 2018 | Temporal composition of energy services | Fractional knapsack | Confined area |
| 14 | Fluid Composition of Intermittent IoT Energy Services | Lakhdari & Bouguettaya | 2020 | Handle service disconnections | 0/1 knapsack + heuristic | Confined area |
| 15 | Proactive Composition of Mobile IoT Energy Services | Lakhdari & Bouguettaya | 2021 | Proactive service/request generation | Graph-based planning | Confined area |
| 16 | Elastic Composition of Crowdsourced IoT Energy Services | Lakhdari et al. | 2020 | Handle service fluctuation | Multi-objective optimization | Confined area |

**Key Limitations of Papers 12-16:**
- All confined to microcells (coffee shops, food courts)
- No trajectory prediction - uses historical patterns
- No RL approaches - heuristic-based only
- No explicit handover mechanisms

---

## Papers 17-18: Moving IoT Services (Most Relevant to Thesis)

### Paper 17: Deep RL for Composing Moving IoT Services

| Attribute | Value |
|-----------|-------|
| **Title** | A Deep Reinforcement Learning Approach for Composing Moving IoT Services |
| **Authors** | Neiat et al. |
| **Year** | 2021 |
| **Venue** | IEEE Transactions on Services Computing |
| **Problem** | Compose moving IoT services for continuous QoS |
| **Algorithm** | Q-learning with Neural Networks (basic deep Q-learning, NOT DQN or Double DQN) |
| **State Space** | User trajectory sample `<t, x, y>` |
| **Action Space** | Valid candidate service IDs + dummy service |
| **Reward** | Based on QoS capacity (signal strength) |
| **Network** | 3 hidden layers × 512 neurons, ReLU, dropout 0.5 |
| **Hyper-parameters** | γ=0.9, lr=0.001, ε-greedy (decay 0.995) |
| **Handover** | Implicit via RL (trajectory overlap detection) |
| **Relevance** | HIGH - Addresses moving services with RL |

### Paper 18: Spatially Cohesive Service Discovery and Dynamic Handover

| Attribute | Value |
|-----------|-------|
| **Title** | Spatially Cohesive Service Discovery and Dynamic Service Handover for Distributed IoT Environments |
| **Authors** | Baek & Ko |
| **Year** | 2017 |
| **Venue** | IEEE ICWS |
| **Problem** | Service discovery and handover in MANET |
| **Algorithm** | Rule-based (DFS/BFS/MST spanning trees) |
| **Spatio-cohesiveness** | `ri(c) = max(1 - distance/l, 0)` |
| **Objective** | `RT(c) = Σ min(ri) / |ST ∪ {u}|` |
| **Handover** | Explicit with hysteresis margin + threshold |
| **Relevance** | HIGH - Addresses handover mechanism |

---

## Papers 20-25: Additional DRL Approaches

| # | Title | Authors | Year | Focus | Algorithm | Scope |
|---|-------|---------|------|-------|-----------|-------|
| 20 | PPDRL: Pretraining-and-Policy Based DRL | Yi et al. | 2022 | QoS-aware composition | DQN + Pretraining + Policy Scoring | Static services |
| 21 | Deep Learning for Local Service Selection | Awanyo & Guermouche | 2024 | Local service selection | CNN + LSTM | Static services |
| 22 | PD3QND: Deep RL with Noise & Double Dueling | Chen et al. | 2023 | Dynamic QoS | DQN + Noise + PER + Double Dueling | Dynamic services |
| 23 | ADQRCN: Adaptive DQN + RNN | Wang et al. | 2019 | Large-scale, partially observable | DQN + RNN | Large-scale |
| 24 | ML Survey: 147 Papers (2018-2023) | Lu et al. | 2024 | Systematic survey | Survey (Q-learning, DQN, A3C, A2C) | All domains |
| 25 | Large-Scale DRL | Moustafa & Ito | 2018 | Large-scale composition | DQN | Large-scale |

### Key Findings from Paper 24 (Survey of 147 papers)
- **Q-learning**: 12 papers
- **DQN**: 8 papers
- **Actor-Critic**: 3 papers
- **A3C**: 2 papers (only A3C, NO A2C found)
- **PPO**: 1 paper
- **Moving IoT services**: Only 3 papers
- **A2C specifically**: 0 papers

### Paper 22 (PD3QND) vs A2C
- PD3QND uses DQN variants (Noise, PER, Double Dueling)
- Still value-based, not actor-critic
- No trajectory prediction
- No proactive handover
- No moving IoT services

---

## Additional Papers (06-10)

| # | Title | Authors | Year | Focus | Algorithm | Relevance |
|---|-------|---------|------|-------|-----------|-----------|
| 06 | DRL + Meta-Heuristics for RC-MPSP | Various | 2021 | Resource-constrained scheduling | DQN + GA/PSO/SA/ABC | Low - Scheduling, not IoT |
| 07 | DDAPSO: Hybrid DFA + PSO | Various | 2021 | Large-scale service selection | Discrete Dragonfly + PSO | Medium - Meta-heuristic baseline |
| 08 | RL for Interactive QoS-aware Composition | Various | 2020 | Adaptive composition with user feedback | Q-learning | Medium - RL for composition |
| 09 | Energy-Centered QoS-Aware Selection | Various | 2021 | Energy efficiency + QoS | Multi-objective optimization | Medium - Energy-aware |
| 10 | Incentive-Based IoT Energy Services | Various | 2020 | Market-based service selection | Game-theoretic | Low - Energy marketplace |

---

## Comparative Summary

### By Focus Area

| Category | Papers | Key Limitation |
|----------|--------|----------------|
| **General IoT** | 01-10 | Diverse approaches, not moving services |
| **ML for IoT** | 11 | Survey, no specific solution |
| **Energy crowdsourcing** | 12-16 | Confined area, heuristic-based |
| **Moving services** | 17-18 | Paper 17: basic Q-learning; Paper 18: rule-based |

### By Algorithm Type

| Algorithm | Papers | Limitations |
|-----------|--------|-------------|
| **Survey/Review** | 01, 05, 11, 24 | No implementation |
| **Genetic Algorithm** | 02, 03 | No learning, static optimization |
| **Machine Learning** | 04, 21 | Prediction only, no RL |
| **DQN** | 06, 20, 22, 23, 25 | Value-based, no actor-critic |
| **DQN + RNN** | 23 | POMDP but still value-based |
| **Meta-heuristic Hybrid** | 07, 09 | No learning |
| **Q-learning** | 08, 17 | Basic Q-learning, no A2C |
| **Rule-based** | 18 | No learning |
| **Crowdsourcing** | 12-16 | Confined areas, no mobility |
| **A3C** | 24 (mentioned) | Only 2 papers, none for moving IoT |

---

## Key Research Gaps for Thesis

1. **No A2C**: All RL approaches use basic Q-learning (Papers 08, 17)
2. **No trajectory prediction**: Use overlap detection, not prediction (Paper 17)
3. **No proactive handover**: Reactive only (Papers 17, 18)
4. **Confined area limitation**: Papers 12-16 limited to microcells
5. **Limited RL in IoT**: Only 2 papers (08, 17) use RL for service composition

---

## Statistics

- **Total papers**: 25
- **Analyzed**: 01-25 (all 25 papers)
- **Most relevant**: 17, 18, 22, 24 (moving IoT services, handover, survey)
- **RL approaches**: 8+ (Q-learning, DQN, DQN+RNN, A3C)
- **A2C/A3C approaches**: 2 (A3C: papers 24 survey mentions 2, NO A2C found)
- **Survey papers**: 4 (01, 05, 11, 24)
- **Handover mechanisms**: 2 (Paper 17 implicit, Paper 18 explicit)

---

## Key Research Gaps (Validated by Papers 20-25)

1. **No A2C**: Survey (Paper 24) confirms 0 papers use A2C for IoT service composition
2. **No trajectory prediction**: All DRL papers use current state, not future trajectory
3. **No proactive handover**: Reactive only in all papers
4. **Value-based only**: All use DQN variants, no actor-critic for moving services
5. **Moving services**: Only 3 papers (17, 18, 24 mentions) address mobile IoT services

---

*Last updated: April 2026*
*Thesis: A2C-Based Proactive Composition for Moving IoT Services*