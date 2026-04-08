# Paper 07: Detailed Solution Framework Analysis

## Paper Information
- **Title**: DDAPSO: Hybrid Discrete Dragonfly Algorithm and Particle Swarm Algorithm to Service Selection and Composition for the Internet of Things Applications
- **Year**: 2020
- **Algorithm**: DDAPSO (Discrete Dragonfly Algorithm + Particle Swarm Optimization Hybrid)

---

## 1. Functions Used for Selection and Aggregation

### 1.1 QoS Aggregation Functions

Standard QoS aggregation for composition patterns:

#### Sequential Composition (Service Chain)
$$Q_s = \prod_{i=1}^{n} q_i$$

Where:
- $Q_s$ = composite QoS for sequential composition
- $q_i$ = QoS attribute of service $i$

#### Parallel Composition (Concurrent Execution)
$$Q_p = \min_{i \in S} q_i$$

Where:
- $Q_p$ = composite QoS for parallel composition
- $\min$ selects worst-case among parallel services

#### Conditional Composition (Branch)
$$Q_c = \sum_{j} p_j \cdot q_j$$

Where:
- $p_j$ = probability of branch $j$
- $q_j$ = QoS for branch $j$

### 1.2 Fitness Function

$$\text{Fitness}(S) = \sum_{k=1}^{m} w_k \cdot q_k(S)$$

Subject to:
$$q_k(S) \geq q_k^{\text{min}}, \forall k \in \{1, ..., m\}$$

Where:
- $S$ = selected service composition
- $m$ = number of QoS attributes
- $w_k$ = weight for k-th attribute (∑w_k = 1)
- $q_k(S)$ = aggregated QoS attribute
- $q_k^{\text{min}}$ = minimum threshold

### 1.3 Discrete Transfer Function

To adapt continuous PSO to discrete service selection, binary transfer function:

$$T(v_i^d) = \frac{1}{1 + e^{-v_i^d}}$$

Then:
$$x_i^d = \begin{cases} 1 & \text{if } rand() < T(v_i^d) \\ 0 & \text{otherwise} \end{cases}$$

Where:
- $v_i^d$ = velocity of particle $i$ in dimension $d$
- $x_i^d$ = binary position (service selected/not selected)
- $rand()$ = uniform random [0,1]

### 1.4 Dragonfly Position Update (DA Component)

$$X_{i}^{t+1} = X_i^t + V_i^{t+1}$$

Where $V_i^{t+1}$ combines:
- Separation: $S_i = -\sum_{j} X_i - X_j$
- Alignment: $A_i = \frac{1}{N} \sum_{j} V_j$
- Cohesion: $C_i = \frac{1}{N} \sum_{j} X_j - X_i$
- Food attraction: $F_i = X_f - X_i$
- Enemy avoidance: $E_i = X_e + X_i$

$$V^{t+1} = (w \cdot V^t + s \cdot S_i + a \cdot A_i + c \cdot C_i + f \cdot F_i + e \cdot E_i)$$

Where $w$, $s$, $a$, $c$, $f$, $e$ are weighting parameters.

---

## 2. Algorithms Used for Exploration and Exploration

### 2.1 Hybrid DDAPSO Algorithm

Combines discrete PSO and Dragonfly Algorithm:

#### Population Initialization
- Generate binary particles representing service selections
- Each particle: binary vector of length = number of services in workflow
- Population size: 30-50 particles

#### PSO Component (Exploitation)
**Velocity Update:**
$$v_i^{t+1} = w \cdot v_i^t + c_1 r_1 (p_i^* - x_i^t) + c_2 r_2 (g^* - x_i^t)$$

**Position Update (Binary):**
- Apply transfer function to convert to binary

#### Dragonfly Component (Exploration)
- Use DA when particles converge prematurely
- Apply separation/alignment/cohesion/food/enemy behaviors
- Better global exploration than PSO alone

#### Switching Strategy
```
if (iteration % switch_cycle == 0):
    if (diversity < threshold):
        Switch to DA for exploration
    else:
        Continue PSO
```

### 2.2 Exploration-Exploitation Balance

| Component | Exploration | Exploitation |
|-----------|-------------|--------------|
| PSO Velocity | Random component (r1, r2) | Personal/best position attraction |
| Dragonfly | Separation, enemy avoidance | Food attraction, cohesion |
| Transfer Function | Random threshold | Sigmoid probability |
| Switching | DA mode when diversity low | PSO mode when diverse |

### 2.3 Algorithm Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| w (inertia) | 0.4-0.9 | Balance exploration/exploitation |
| c1 (cognitive) | 1.5-2.0 | Personal best influence |
| c2 (social) | 1.5-2.0 | Global best influence |
| Switch threshold | 0.3 | When to switch to DA |
| pc | 0.7-0.9 | Crossover probability |
| pm | 0.02-0.08 | Mutation probability |

---

## 3. Dataset Used

### 3.1 Synthetic IoT Service Registry

#### Service Registry Structure
Each service has:
- **Service ID**: Unique identifier
- **Functionality**: Service type/category
- **QoS Attributes**:
  - Response time
  - Cost
  - Reliability
  - Availability
  - Throughput

#### Dataset Characteristics
| Parameter | Value |
|-----------|-------|
| Number of Services | 50-200 |
| Service Categories | 5-10 functional categories |
| QoS Attributes | 5-6 per service |
| Workflow Tasks | 5-10 tasks |

### 3.2 Workflow Patterns
- Linear chains
- Parallel branches
- Mixed workflows with loops

### 3.3 Evaluation Scenarios

| Scenario | Services | Workflow Complexity | Purpose |
|----------|----------|---------------------|---------|
| Small | 50 | Simple chain | Baseline |
| Medium | 100 | Chain + parallel | Standard |
| Large | 150-200 | Complex workflow | Scalability test |

---

## 4. Complete Workflow

### 4.1 Phase 1: Preprocessing

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA PREPARATION                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Generate synthetic IoT service registry                  │
│     - Service categories and types                          │
│     - Assign QoS values                                     │
│                                                              │
│  2. Define workflow structure                               │
│     - Task sequence                                         │
│     - Parallel branches                                     │
│     - QoS requirements per task                             │
│                                                              │
│  3. Initialize algorithm parameters                         │
│     - Population size: 30-50                               │
│     - w, c1, c2 for PSO                                    │
│     - Switch threshold                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 2: DDAPSO Optimization

```
┌─────────────────────────────────────────────────────────────┐
│                DDAPSO OPTIMIZATION LOOP                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ITERATION LOOP (repeat until convergence)           │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │ 1. EVALUATE FITNESS                                 │   │
│  │    - For each particle:                             │   │
│  │    - Decode binary to service selection             │   │
│  │    - Compute aggregated QoS                         │   │
│  │    - Apply fitness function                         │   │
│  │                                                      │   │
│  │ 2. UPDATE PERSONAL BEST (p_i*)                      │   │
│  │    - If fitness > fitness(p_i*): p_i* = x_i        │   │
│  │                                                      │   │
│  │ 3. UPDATE GLOBAL BEST (g*)                          │   │
│  │    - If fitness > fitness(g*): g* = best_particle  │   │
│  │                                                      │   │
│  │ 4. SWITCHING DECISION                               │   │
│  │    - Check diversity                                │   │
│  │    - Choose PSO or DA mode                          │   │
│  │                                                      │   │
│  │ 5. UPDATE VELOCITY & POSITION                       │   │
│  │    - If PSO mode: PSO velocity + binary transfer   │   │
│  │    - If DA mode: Dragonfly position update         │   │
│  │                                                      │   │
│  │ 6. APPLY MUTATION (optional)                        │   │
│  │    - With probability pm                            │   │
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
│  1. Select best particle from population                   │
│  2. Decode binary vector to service list                    │
│  3. Verify QoS constraints satisfied                         │
│  4. Return optimal composition S*                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Complete Flowchart

```
                          ┌─────────────────────┐
                          │  Initialize          │
                          │  - Population        │
                          │  - Parameters        │
                          └──────────┬──────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │     ITERATION LOOP            │
                     │                               │
                     │  ┌─────────────┐              │
                     │  │ Evaluate    │              │
                     │  │ Fitness     │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Update      │              │
                     │  │ p_i*, g*    │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Check       │              │
                     │  │ Diversity   │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Switch      │              │
                     │  │ PSO/DA      │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Update      │              │
                     │  │ Velocity    │              │
                     │  │ Position    │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     └─────────┼─────────────────────┘
                               │
                               ▼
                     ┌───────────────────────┐
                     │  Convergence Check    │
                     │  - Max iterations     │
                     │  - Fitness plateau    │
                     └───────────┬───────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
               YES               │               NO
                │                │                │
                ▼                │                ▼
     ┌──────────────────┐        │    ┌──────────────────────┐
     │ Return Best     │        │    │ Continue Iteration   │
     │ Solution        │        │    └──────────────────────┘
     └──────────────────┘        │
                                 │
                                 └──────────────────────────┘
                                             (back to loop)
```

### 4.5 Pseudocode

```
ALGORITHM: DDAPSO for IoT Service Selection

INPUT:
  - Service registry R = {s1, ..., sn}
  - Workflow tasks T = {t1, ..., tk}
  - QoS weights W = {w1, ..., wm}
  - Parameters: pop_size, w, c1, c2, threshold

OUTPUT:
  - Optimal service composition S*

// Phase 1: Initialization
1. Initialize population P with binary particles
2. Evaluate initial fitness for all particles
3. Set p_i* = initial positions, g* = best particle

// Phase 2: Optimization
4. For iter = 1 to max_iter:
   
   a. For each particle i:
         Compute fitness using QoS aggregation
   
   b. Update p_i* if better fitness found
   
   c. Update g* if better fitness found
   
   d. Compute population diversity:
         diversity = mean(hamming_distance(x_i, x_j))
   
   e. If diversity < threshold:
         // Use Dragonfly Algorithm (exploration)
         For each particle:
            Compute S, A, C, F, E
            Update position using DA formula
      Else:
         // Use PSO (exploitation)
         For each particle:
            Update velocity: v = w*v + c1*r1*(p_i*-x) + c2*r2*(g*-x)
            Apply binary transfer function to get new position
   
   f. If convergence: break

// Phase 3: Solution Extraction
5. Return best particle as S*

END ALGORITHM
```

---

## 5. Summary

| Component | Details |
|-----------|---------|
| **Selection Function** | Fitness(S) = Σ w_k · q_k(S) |
| **Aggregation Functions** | Sequential (∏), Parallel (min), Conditional (Σp·q) |
| **PSO Component** | Velocity update + binary transfer function |
| **DA Component** | Separation, alignment, cohesion, food, enemy |
| **Exploration** | DA mode, random velocity, mutation |
| **Exploitation** | PSO personal/global best attraction |
| **Novel Contribution** | Hybrid DDAPSO with adaptive PSO/DA switching |
| **Dataset** | Synthetic IoT (50-200 services), 5-10 workflow tasks |
| **Workflow** | Preprocessing → DDAPSO Loop → Solution Extraction |

---

*This document provides detailed analysis of Paper 07's solution framework.*