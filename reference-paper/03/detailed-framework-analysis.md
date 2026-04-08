# Paper 03: Detailed Solution Framework Analysis

## Paper Information
- **Title**: A Genetic Algorithm Based Approach for Fluctuating QoS Aware Selection of IoT Services
- **Year**: 2021
- **Algorithm**: Modified Genetic Algorithm (GA) with Fluctuation Awareness

---

## 1. Functions Used for Selection and Aggregation

### 1.1 QoS Aggregation Functions

The paper extends standard QoS aggregation to handle time-varying attributes:

#### Sequential Composition (Service Chain)
$$Q_s(t) = \prod_{i=1}^{n} q_i(t)$$

Where:
- $Q_s(t)$ = composite QoS at time t
- $q_i(t)$ = QoS attribute of service $i$ at time $t$

#### Parallel Composition (Concurrent Execution)
$$Q_p(t) = \min_{i \in S} q_i(t)$$

Where:
- $Q_p(t)$ = composite QoS at time t
- $\min$ selects the worst-case QoS among parallel services

#### Conditional Composition (Branch)
$$Q_c(t) = \sum_{j} p_j \cdot q_j(t)$$

Where:
- $p_j$ = probability of branch $j$
- $q_j(t)$ = QoS for branch $j$ at time $t$

### 1.2 Fluctuation-Aware Fitness Function

The core innovation: fitness evaluates both average QoS and stability:

$$\text{Fitness}(S) = \alpha \cdot \bar{Q}(S) + \beta \cdot \text{Stability}(S)$$

Where:
- $\bar{Q}(S) = \frac{1}{T} \sum_{t=1}^{T} Q(S, t)$ = average QoS over time period
- $\text{Stability}(S) = \frac{1}{1 + \text{Var}(Q(S, t))}$ = stability metric (inverse of variance)
- $\alpha + \beta = 1$ = weight parameters balancing QoS and stability

#### Detailed Stability Metric
$$\text{Stability}(S) = \frac{1}{1 + \frac{1}{T} \sum_{t=1}^{T} (Q(S, t) - \bar{Q}(S))^2}$$

Where:
- Higher stability → lower variance → higher fitness
- $\beta$ parameter controls robustness emphasis

### 1.3 Robustness Constraint

Subject to constraint:
$$\text{Var}(Q(S, t)) \leq \tau_{\text{max}}$$

Where:
- $\tau_{\text{max}}$ = maximum allowed variance threshold
- Ensures selected services meet stability requirements

### 1.4 Time-Varying Chromosome Representation

Each gene encodes service selection with temporal validity:

$$\text{Chromosome} = [(s_1, t_1^{start}, t_1^{end}), (s_2, t_2^{start}, t_2^{end}), ...]$$

Where:
- $s_i$ = selected service for position $i$
- $t_i^{start}$ = start time of validity
- $t_i^{end}$ = end time of validity
- Temporal windows allow dynamic re-selection

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Modified Genetic Algorithm

The GA is adapted for fluctuating QoS environments:

#### Population Initialization
- Generate initial population of candidate service selections
- Each individual includes temporal validity windows
- Population size: typically 50-100 individuals

#### Fluctuation-Aware Selection Operator (Exploitation)
Modified tournament selection considers temporal stability:
1. Select k individuals randomly
2. Evaluate using fluctuation-aware fitness (not just average)
3. Choose individual with best combined score

Selection pressure adapts:
- Early generations: lower $\alpha$, higher $\beta$ → explore stable solutions
- Late generations: higher $\alpha$, lower $\beta$ → exploit high-QoS solutions

#### Adaptive Crossover Operator (Exploration)
Time-aware crossover maintains temporal validity:
```
Parent1: [(S1, t1), (S2, t2) | (S3, t3), (S4, t4)]
Parent2: [(A1, t1'), (A2, t2') | (A3, t3'), (A4, t4')]
Offspring: [(S1, t1), (S2, t2), (A3, t3'), (A4, t4')]
```
Crossover respects temporal constraints.

#### Mutation Operator (Exploration)
Service mutation with temporal adjustment:
- With probability $P_m$, replace selected service
- Adjust temporal validity window based on QoS trend
- Mutation rate: 0.02-0.08

#### Adaptive Parameter Control
Parameters evolve during optimization:
| Generation | $\alpha$ (QoS weight) | $\beta$ (Stability weight) |
|------------|---------------------|---------------------------|
| Early | 0.3 | 0.7 |
| Middle | 0.5 | 0.5 |
| Late | 0.7 | 0.3 |

### 2.2 Exploration-Exploitation Balance

| Phase | Mechanism | Purpose |
|-------|-----------|---------|
| Early GA | High $\beta$, high mutation | Explore stable solutions |
| Middle GA | Balanced $\alpha,\beta$ | Balance QoS and stability |
| Late GA | High $\alpha$, low mutation | Exploit best QoS |
| Time Adaptation | Temporal windows | Enable runtime flexibility |

### 2.3 Convergence Criteria
- Maximum generations: 100-200
- Fitness stagnation: no improvement for 20 generations
- Time constraint: maximum runtime limit

---

## 3. Dataset Used

### 3.1 Synthetic IoT Service Registry with Temporal QoS

The paper generates synthetic datasets with time-varying QoS:

#### Service Registry Structure
Each service has:
- **Service ID**: Unique identifier
- **Functionality**: Service type/category
- **QoS Attributes with Temporal Variation**:
  - Response time: varies with sinusoidal pattern + noise
  - Reliability: varies based on simulated load
  - Availability: fluctuates based on network conditions
  - Cost: constant or slowly varying

#### QoS Fluctuation Models
$$q_i(t) = q_i^{base} + A_i \cdot \sin(2\pi f_i t + \phi_i) + \epsilon_i(t)$$

Where:
- $q_i^{base}$ = base QoS value
- $A_i$ = amplitude of fluctuation
- $f_i$ = frequency of variation
- $\phi_i$ = phase offset
- $\epsilon_i(t)$ = random noise component

#### Dataset Characteristics
| Parameter | Value |
|-----------|-------|
| Number of Services | 30-100 |
| Service Categories | 5-8 functional categories |
| QoS Attributes | 4-6 per service |
| Time Points | 50-200 discrete time steps |
| Fluctuation Patterns | Sinusoidal, random, step |

### 3.2 Evaluation Scenarios

| Scenario | Services | Fluctuation Type | Purpose |
|----------|----------|------------------|---------|
| Low Fluctuation | 30 | Small amplitude | Baseline |
| Medium Fluctuation | 50 | Moderate amplitude | Standard test |
| High Fluctuation | 100 | Large amplitude | Stress test |
| Real-time | 50 | Continuous variation | Runtime evaluation |

---

## 4. Complete Workflow

### 4.1 Phase 1: Preprocessing - QoS Data Collection

```
┌─────────────────────────────────────────────────────────────┐
│               QOS DATA COLLECTION AND MODELING               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Generate synthetic IoT service registry                 │
│     - Define service categories                              │
│     - Assign base QoS values                                │
│     - Generate fluctuation parameters (A, f, φ)             │
│                                                              │
│  2. Create time-series QoS data                            │
│     - For each service, generate QoS over T time points    │
│     - Apply fluctuation model with noise                    │
│     - Store as temporal QoS matrix                          │
│                                                              │
│  3. Initialize GA parameters                                │
│     - Population size, generations                          │
│     - Crossover probability (pc = 0.7-0.9)                 │
│     - Mutation probability (pm = 0.02-0.08)                │
│     - α, β weights for fitness                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 2: Genetic Algorithm Optimization

```
┌─────────────────────────────────────────────────────────────┐
│              FLUCTUATION-AWARE GA OPTIMIZATION               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ GENERATION LOOP (repeat until convergence)          │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │ 1. EVALUATE FITNESS                                  │   │
│  │    - For each individual:                            │   │
│  │    - Compute QoS at each time point                 │   │
│  │    - Calculate average QoS over time                │   │
│  │    - Calculate stability (inverse variance)        │   │
│  │    - Fitness = α·Q̄ + β·Stability                    │   │
│  │                                                      │   │
│  │ 2. ADAPTIVE SELECTION                                │   │
│  │    - Use fluctuation-aware tournament selection     │   │
│  │    - Adjust α, β based on generation                │   │
│  │                                                      │   │
│  │ 3. TIME-AWARE CROSSOVER                             │   │
│  │    - Single-point crossover                         │   │
│  │    - Preserve temporal validity windows             │   │
│  │                                                      │   │
│  │ 4. MUTATION WITH TEMPORAL ADJUSTMENT                │   │
│  │    - Service replacement mutation                   │   │
│  │    - Adjust temporal validity based on QoS trend    │   │
│  │                                                      │   │
│  │ 5. ELITISM                                           │   │
│  │    - Preserve top individuals unchanged             │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Phase 3: Solution Extraction

```
┌─────────────────────────────────────────────────────────────┐
│                  SOLUTION EXTRACTION                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Select best individual from final population           │
│  2. Decode chromosome to service selection                 │
│  3. Extract temporal validity windows                       │
│  4. Verify stability constraint: Var(Q) ≤ τ_max            │
│  5. If valid → return as optimal robust selection          │
│  6. If invalid → apply repair or discard                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Complete Algorithm Flowchart

```
                          ┌─────────────────────┐
                          │  Initialize GA      │
                          │  - Population       │
                          │  - QoS Modeling     │
                          │  - α, β weights     │
                          └──────────┬──────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │     GENERATION LOOP           │
                     │                               │
                     │  ┌─────────────┐              │
                     │  │ Evaluate    │              │
                     │  │ Fitness     │              │
                     │  │ α·Q̄ + β·Stab │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Adaptive    │              │
                     │  │ Selection   │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Time-Aware  │              │
                     │  │ Crossover   │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Mutation    │              │
                     │  │ + Temporal  │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Elitism     │              │
                     │  │ Preserve    │              │
                     │  │ best        │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     └─────────┼─────────────────────┘
                               │
                               ▼
                     ┌───────────────────────┐
                     │  Convergence Check    │
                     │  - Max generations    │
                     │  - Fitness stagnation │
                     │  - Time limit         │
                     └───────────┬───────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
               YES               │               NO
                │                │                │
                ▼                │                ▼
     ┌──────────────────┐        │    ┌──────────────────────┐
     │ Return Best      │        │    │ Continue to Next     │
     │ Robust Solution  │        │    │ Generation           │
     └──────────────────┘        │    └──────────────────────┘
                                 │
                                 └──────────────────────────┘
                                             (back to loop)
```

### 4.5 Pseudocode

```
ALGORITHM: Fluctuation-Aware GA for IoT Service Selection

INPUT:
  - Service registry R = {s1, s2, ..., sn}
  - Temporal QoS data: Q(t) for each service over time
  - QoS weights W = {w1, w2, ..., wm}
  - Stability threshold τ_max
  - GA parameters: pop_size, generations, pc, pm

OUTPUT:
  - Optimal robust service selection S*

// Phase 1: Preprocessing
1. Initialize temporal QoS matrix for all services
2. Generate initial population P with temporal chromosomes
3. Set initial α = 0.3, β = 0.7 (stability emphasis)

// Phase 2: GA Optimization
4. For gen = 1 to generations:
   
   // Adaptive parameter adjustment
   a. If gen < generations/3: α = 0.3, β = 0.7
      Else if gen < 2*generations/3: α = 0.5, β = 0.5
      Else: α = 0.7, β = 0.3
   
   b. For each individual in P:
         For t = 1 to T:
            Compute Q(S, t) using aggregation functions
         Compute average QoS: Q̄ = mean(Q(S, t))
         Compute variance: Var = var(Q(S, t))
         Compute stability = 1 / (1 + Var)
         Fitness = α · Q̄ + β · Stability
   
   c. Create new population P':
         - Elitism: copy best individuals
         - While |P'| < pop_size:
             * Select parents via tournament
             * Apply time-aware crossover (prob = pc)
             * Apply mutation with temporal adjustment (prob = pm)
             * Add offspring to P'
   
   d. P = P'
   
   e. If convergence: break

// Phase 3: Solution Extraction
5. Select best individual from final P
6. Verify stability constraint: Var(Q) ≤ τ_max
7. Extract service selection and temporal windows
8. Return S* with validity windows

END ALGORITHM
```

---

## 5. Summary

| Component | Details |
|-----------|---------|
| **Selection Function** | Fitness = α·Q̄ + β·Stability, α+β=1 |
| **Aggregation Functions** | Sequential (∏), Parallel (min), Conditional (Σp·q) with temporal extension |
| **Exploration** | Mutation (pm=0.02-0.08), Time-aware crossover |
| **Exploitation** | Adaptive tournament selection, Elitism |
| **Novel Contribution** | Fluctuation-aware fitness with stability metric |
| **Dataset** | Synthetic IoT registry with sinusoidal QoS fluctuation (30-100 services) |
| **Workflow** | QoS Modeling → GA Loop with adaptive α,β → Solution Extraction |

---

*This document provides detailed analysis of Paper 03's solution framework.*