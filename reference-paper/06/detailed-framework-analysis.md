# Paper 06: Detailed Solution Framework Analysis

## Paper Information
- **Title**: A deep reinforcement learning based multiple meta-heuristic methods approach for resource constrained multi-project scheduling problem
- **Year**: 2021
- **Algorithm**: Deep Q-Network (DQN) + Multiple Meta-Heuristics (GA, PSO, SA, ABC)

---

## 1. Functions Used for Selection and Aggregation

### 1.1 Problem Formulation

The resource-constrained multi-project scheduling problem (RC-MPSP):

**Objective Function (Makespan Minimization):**
$$\text{Minimize } T = \max_{p \in P} \left( \sum_{i \in V_p} d_i \right)$$

Where:
- $T$ = makespan (total project completion time)
- $P$ = set of projects
- $V_p$ = set of activities in project $p$
- $d_i$ = duration of activity $i$

**Resource Constraint:**
$$\sum_{i \in A_t} r_{i,k} \leq R_k, \forall t, \forall k$$

Where:
- $A_t$ = set of activities executing at time $t$
- $r_{i,k}$ = resource $k$ required by activity $i$
- $R_k$ = available resource $k$

### 1.2 Fitness Function for Meta-Heuristics

Each meta-heuristic uses a common fitness function:

$$\text{Fitness}(S) = w_1 \cdot T(S) + w_2 \cdot \text{ResourceViol}(S) + w_3 \cdot \text{Penalty}(S)$$

Where:
- $T(S)$ = makespan of schedule $S$
- $\text{ResourceViol}(S)$ = resource violation count
- $\text{Penalty}(S)$ = penalty for constraint violations
- $w_1 + w_2 + w_3 = 1$

### 1.3 DQN State Representation

The DQN evaluates state to select appropriate meta-heuristic:

$$s_t = \left[ \text{progress}, \text{diversity}, \text{quality}, \text{time}, \text{memory} \right]$$

Where:
- $\text{progress}$ = improvement rate over recent generations
- $\text{diversity}$ = population diversity metric
- $\text{quality}$ = current best fitness
- $\text{elapsed}$ = time/spans since start
- $\text{memory}$ = recent algorithm performance history

### 1.4 Q-Value Function

DQN computes Q-value for meta-heuristic selection:

$$Q(s_t, a) = \mathbb{E}[R_t + \gamma \max_{a'} Q(s_{t+1}, a') | s_t, a]$$

Where:
- $s_t$ = current state
- $a$ = action (meta-heuristic selection)
- $R_t$ = reward for using algorithm $a$ at state $s_t$
- $\gamma$ = discount factor (0.9-0.99)
- $a'$ = next action

### 1.5 Reward Function

$$R_t = \Delta \text{Fitness} + \lambda \cdot \text{DiversityBonus}$$

Where:
- $\Delta \text{Fitness}$ = improvement in best fitness
- $\text{DiversityBonus}$ = reward for maintaining population diversity
- $\lambda$ = diversity weight (0.1-0.3)

### 1.6 Scheduling Sequence Aggregation

For activity sequencing:
$$S_{\text{order}} = \text{TopologicalSort}(V, E) + \text{PriorityHeuristic}(V)$$

Where:
- $V$ = activities, $E$ = precedence constraints
- Priority heuristic determines order among feasible activities

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 DQN for Algorithm Selection (Meta-Level)

The DQN decides which meta-heuristic to apply:

**Architecture:**
- Input layer: state features (5 dimensions)
- Hidden layers: fully connected (64-128 neurons)
- Output layer: Q-values for each meta-heuristic (4 actions)

**Training:**
- Pre-training phase: collect (s, a, r, s') transitions
- Experience replay: random mini-batches from memory
- Loss function: MSE between predicted and target Q-values

$$L(\theta) = \mathbb{E}[(y - Q(s, a; \theta))^2]$$

Where:
$$y = r + \gamma \max_{a'} Q(s', a'; \theta^-)$$

### 2.2 Meta-Heuristic Pool (Solution-Level)

Four meta-heuristics available:

#### 2.2.1 Genetic Algorithm (GA)

**Selection (Exploitation):**
- Tournament selection (size 3-5)
- Roulette wheel selection

**Crossover (Exploration):**
- Single-point crossover
- Two-point crossover
- Probability: 0.7-0.9

**Mutation (Exploration):**
- Swap mutation
- Insert mutation
- Probability: 0.02-0.08

#### 2.2.2 Particle Swarm Optimization (PSO)

**Velocity Update (Exploration):**
$$v_i^{t+1} = w \cdot v_i^t + c_1 r_1 (p_i^* - x_i^t) + c_2 r_2 (g^* - x_i^t)$$

Where:
- $w$ = inertia weight (0.4-0.9)
- $c_1$ = cognitive coefficient (1.5-2.0)
- $c_2$ = social coefficient (1.5-2.0)
- $p_i^*$ = personal best
- $g^*$ = global best

**Position Update (Exploitation):**
$$x_i^{t+1} = x_i^t + v_i^{t+1}$$

#### 2.2.3 Simulated Annealing (SA)

**Temperature Schedule:**
$$T_t = T_0 \cdot \alpha^t$$

Where:
- $T_0$ = initial temperature
- $\alpha$ = cooling rate (0.95-0.99)

**Acceptance Probability (Exploration):**
$$P(\text{accept}) = \begin{cases} 1 & \text{if } \Delta E < 0 \\ e^{-\Delta E/T} & \text{otherwise} \end{cases}$$

Where:
- $\Delta E$ = fitness difference

#### 2.2.4 Artificial Bee Colony (ABC)

**Employed Bees (Exploitation):**
$$x_i^{new} = x_i + \phi_{ij}(x_i - x_k)$$

Where:
- $k$ = random neighbor
- $\phi_{ij}$ = random value [-1, 1]

**Onlooker Bees (Exploitation):**
- Select solutions based on fitness-probability
- Apply modification

**Scout Bees (Exploration):**
- Abandon solutions not improved for limit cycles
- Generate new random solutions

### 2.3 Exploration-Exploitation Balance

| Component | Exploration | Exploitation |
|-----------|-------------|--------------|
| DQN | Explore algorithm performance | Select best-performing algorithm |
| GA Crossover | Combine solutions | - |
| GA Mutation | Introduce new solutions | - |
| PSO | Velocity exploration | Position exploitation |
| SA | Accept worse solutions | Accept better solutions |
| ABC Scout | Random search | - |

### 2.4 Adaptive Switching Strategy

```
If progress_rate < threshold:
    Switch to exploration-heavy (SA, ABC)
Else if diversity < threshold:
    Switch to diversity-maintaining (PSO)
Else:
    Continue current algorithm
```

---

## 3. Dataset Used

### 3.1 RC-MPSP Benchmark Instances

Standard benchmark problems for multi-project scheduling:

#### Dataset Characteristics

| Parameter | Value |
|-----------|-------|
| Projects | 2-5 projects |
| Activities per Project | 10-30 activities |
| Resources | 2-5 resource types |
| Resource Capacity | 5-15 units per resource |
| Precedence Constraints | Random DAG |

#### Activity Properties
- Duration: uniform random (1-10 time units)
- Resource requirements: random per resource type
- Precedence: random partial order

### 3.2 Evaluation Scenarios

| Scenario | Projects | Activities | Resources | Purpose |
|----------|----------|-----------|-----------|---------|
| Small | 2 | 10-15 | 2-3 | Baseline |
| Medium | 3 | 20-25 | 3-4 | Standard test |
| Large | 5 | 25-30 | 4-5 | Stress test |
| Complex | 3 | 30 | 5 | High complexity |

### 3.3 Performance Metrics
- Makespan (completion time)
- Resource utilization
- Constraint satisfaction rate
- Convergence time

---

## 4. Complete Workflow

### 4.1 Phase 1: Preprocessing - DQN Training

```
┌─────────────────────────────────────────────────────────────┐
│               DQN TRAINING FOR ALGORITHM SELECTION           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Generate benchmark RC-MPSP instances                    │
│                                                              │
│  2. Pre-train DQN:                                          │
│     - For each instance:                                    │
│       - Run each meta-heuristic for fixed spans             │
│       - Record (state, action, reward, next_state)         │
│       - Store in experience replay buffer                   │
│                                                              │
│  3. Train DQN:                                             │
│     - Sample mini-batches from buffer                       │
│     - Update Q-network via gradient descent                │
│     - Target network updated periodically                  │
│                                                              │
│  4. Set meta-heuristic parameters                          │
│     - GA: pop_size=50, pc=0.8, pm=0.05                     │
│     - PSO: w=0.7, c1=1.5, c2=1.5                           │
│     - SA: T0=100, α=0.97                                    │
│     - ABC: limit=20, colony_size=50                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 2: Hybrid DQN-Meta-Heuristic Optimization

```
┌─────────────────────────────────────────────────────────────┐
│           DQN-GUIDED META-HEURISTIC OPTIMIZATION             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ OPTIMIZATION LOOP (repeat until convergence)         │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │ 1. EXTRACT STATE                                   │   │
│  │    - Compute progress, diversity, quality           │   │
│  │    - Form state vector s_t                          │   │
│  │                                                      │   │
│  │ 2. DQN ACTION SELECTION                             │   │
│  │    - Input s_t to DQN                               │   │
│  │    - Select a_t = argmax Q(s_t, a)                 │   │
│  │    - Apply selected meta-heuristic                 │   │
│  │                                                      │   │
│  │ 3. META-HEURISTIC EXECUTION                        │   │
│  │    - Run selected algorithm (GA/PSO/SA/ABC)        │   │
│  │    - For fixed iterations or until improvement      │   │
│  │                                                      │   │
│  │ 4. COMPUTE REWARD                                  │   │
│  │    - Measure fitness improvement                    │   │
│  │    - Calculate diversity bonus                      │   │
│  │    - r_t = ΔFitness + λ·DiversityBonus            │   │
│  │                                                      │   │
│  │ 5. UPDATE DQN                                      │   │
│  │    - Store (s_t, a_t, r_t, s_{t+1}) in buffer      │   │
│  │    - Periodically update Q-network                  │   │
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
│  1. Extract best schedule from population                   │
│  2. Validate resource constraints satisfied                 │
│  3. Compute final makespan                                   │
│  4. If constraints violated → apply repair                 │
│  5. Return optimal schedule S*                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Complete Algorithm Flowchart

```
                          ┌─────────────────────┐
                          │  Initialize          │
                          │  - DQN Network       │
                          │  - Meta-heuristics   │
                          │  - Replay Buffer     │
                          └──────────┬──────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │     OPTIMIZATION LOOP          │
                     │                               │
                     │  ┌─────────────┐              │
                     │  │ Extract     │              │
                     │  │ State s_t   │              │
                     │  │ (progress,  │              │
                     │  │ diversity,  │              │
                     │  │ quality)    │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ DQN Action  │              │
                     │  │ Selection   │              │
                     │  │ a_t = argmax│              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Execute     │              │
                     │  │ Meta-heuristic│           │
                     │  │ (GA/PSO/SA/ABC)            │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Compute     │              │
                     │  │ Reward r_t  │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Update DQN  │              │
                     │  │ (s,a,r,s')  │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     └─────────┼─────────────────────┘
                               │
                               ▼
                     ┌───────────────────────┐
                     │  Convergence Check    │
                     │  - Max iterations     │
                     │  - Fitness plateau     │
                     │  - Time limit          │
                     └───────────┬───────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
               YES               │               NO
                │                │                │
                ▼                │                ▼
     ┌──────────────────┐        │    ┌──────────────────────┐
     │ Return Best     │        │    │ Continue Optimization │
     │ Schedule        │        │    │ Loop                  │
     └──────────────────┘        │    └──────────────────────┘
                                 │
                                 └──────────────────────────┘
                                             (back to loop)
```

### 4.5 Pseudocode

```
ALGORITHM: DQN-Based Multi-Meta-Heuristic for RC-MPSP

INPUT:
  - Multi-project instance: activities, resources, precedence
  - DQN parameters: γ, learning_rate, buffer_size
  - Meta-heuristic parameters

OUTPUT:
  - Optimal schedule S*

// Phase 1: Pre-training
1. Initialize DQN: Q(s, a; θ), target network Q(s, a; θ-)
2. Initialize replay buffer D
3. Pre-train:
   For each benchmark instance:
      For each meta-heuristic a ∈ {GA, PSO, SA, ABC}:
         Run a for fixed iterations
         Record transitions (s, a, r, s')
         Add to D
   Train DQN on D via gradient descent

// Phase 2: Optimization
4. Initialize population with valid schedules
5. For t = 1 to max_iterations:
   
   a. Extract state s_t:
         progress = improvement_rate(recent)
         diversity = population_diversity()
         quality = best_fitness()
         time = elapsed / max_time
         memory = algorithm_history()
   
   b. DQN selects action:
         a_t = argmax_a Q(s_t, a; θ)
   
   c. Execute meta-heuristic a_t:
         Run selected algorithm for span iterations
         Update population
   
   d. Compute reward:
         r_t = (best_fitness_old - best_fitness_new) 
               + λ·diversity_improvement
   
   e. Store transition:
         D.push(s_t, a_t, r_t, s_{t+1})
   
   f. Update DQN (periodically):
         Sample mini-batch from D
         y = r + γ·max_{a'} Q(s', a'; θ-)
         θ = θ - α·∇_θ(y - Q(s, a; θ))^2
   
   g. If convergence: break

// Phase 3: Solution Extraction
6. Return best schedule from final population

END ALGORITHM
```

---

## 5. Summary

| Component | Details |
|-----------|---------|
| **Selection Function** | DQN selects meta-heuristic based on state Q(s,a) |
| **Fitness Function** | Fitness = w₁·Makespan + w₂·ResourceViol + w₃·Penalty |
| **DQN State** | [progress, diversity, quality, time, memory] |
| **Meta-Heuristics** | GA (crossover/mutation), PSO (velocity), SA (temperature), ABC (bee roles) |
| **Exploration** | SA accepting worse, ABC scout, GA mutation, PSO velocity |
| **Exploitation** | GA selection, PSO personal/global best, ABC employed bees |
| **Novel Contribution** | DQN dynamically selects best meta-heuristic based on search state |
| **Dataset** | RC-MPSP benchmarks (2-5 projects, 10-30 activities, 2-5 resources) |
| **Workflow** | DQN Pre-training → DQN-Guided Meta-heuristic Loop → Solution Extraction |

---

*This document provides detailed analysis of Paper 06's solution framework.*