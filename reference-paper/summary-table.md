# Reference Papers Summary Table

## Overview
This table summarizes all 18 reference papers analyzed for the PhD thesis on "A2C-Based Proactive Composition for Moving IoT Services".

---

## Papers 01-10: General IoT Service Composition

| # | Title | Authors | Year | Focus | Relevance |
|---|-------|---------|------|-------|-----------|
| 01 | [To be analyzed] | - | - | - | - |
| 02 | [To be analyzed] | - | - | - | - |
| 03 | [To be analyzed] | - | - | - | - |
| 04 | [To be analyzed] | - | - | - | - |
| 05 | [To be analyzed] | - | - | - | - |
| 06 | [To be analyzed] | - | - | - | - |
| 07 | [To be analyzed] | - | - | - | - |
| 08 | [To be analyzed] | - | - | - | - |
| 09 | [To be analyzed] | - | - | - | - |
| 10 | [To be analyzed] | - | - | - | - |

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
| 13 | Crowdsourcing Energy as a Service | Lakhdari et al. | 2018 | Temporal composition of energy services | Fractional knapsack | Confined area |
| 14 | Fluid Composition of Intermittent IoT Energy Services | Lakhdari & Bouguettaya | 2020 | Handle service disconnections | 0/1 knapsack + heuristic | Confined area |
| 15 | Proactive Composition of Mobile IoT Energy Services | Lakhdari & Bouguettaya | 2021 | Proactive service/request generation | Graph-based planning | Confined area |
| 16 | Elastic Composition of Crowdsourced IoT Energy Services | Lakhdari et al. | 2020 | Handle service fluctuation | Multi-objective optimization | Confined area |

**Key Limitations of Papers 13-16:**
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
| **Algorithm** | Q-learning with Neural Networks (basic deep Q-learning) |
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

## Comparative Summary

### By Focus Area

| Category | Papers | Key Limitation |
|----------|--------|----------------|
| **General IoT** | 01-10 | Need analysis |
| **ML for IoT** | 11 | Survey, no specific solution |
| **Energy crowdsourcing** | 13-16 | Confined area, heuristic-based |
| **Moving services** | 17-18 | Paper 17: basic Q-learning; Paper 18: rule-based |

### By Algorithm Type

| Algorithm | Papers | Limitations |
|-----------|--------|-------------|
| **Heuristic** | 13-16, 18 | No learning, rule-based |
| **Basic Q-learning** | 17 | No target network, no advantage |
| **Survey** | 11 | No implementation |

---

## Key Research Gaps for Thesis

1. **No A2C**: All RL approaches use basic Q-learning
2. **No trajectory prediction**: Use overlap detection, not prediction
3. **No proactive handover**: Reactive only
4. **Confined area limitation**: Papers 13-16 limited to microcells

---

## Statistics

- **Total papers**: 18
- **Analyzed**: 11, 13-18 (7 papers)
- **To analyze**: 01-10, 12 (11 papers)
- **Most relevant**: 17, 18 (moving IoT services)
- **RL approaches**: 1 (Paper 17 - basic Q-learning)
- **Handover mechanisms**: 2 (Paper 17 implicit, Paper 18 explicit)

---

*Last updated: April 2026*
*Thesis: A2C-Based Proactive Composition for Moving IoT Services*