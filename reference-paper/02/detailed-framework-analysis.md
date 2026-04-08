# Paper 02: Detailed Solution Framework Analysis

## Paper Information
- **Title**: An approach based on genetic algorithms and neural networks for QoS-aware IoT services composition
- **Year**: 2022
- **Algorithm**: Genetic Algorithm + Neural Network (Hybrid)

---

## 1. Functions Used for Selection and Aggregation

### 1.1 QoS Aggregation Functions

The paper uses mathematical models to aggregate QoS attributes for different composition patterns:

#### Sequential Composition (Service Chain)
When services are executed in sequence (output of one is input to next):
$$Q_s = \prod_{i=1}^{n} q_i$$

Where:
- $Q_s$ = composite QoS for sequential composition
- $q_i$ = QoS attribute (e.g., reliability, availability) of service $i$
- The product represents multiplicative aggregation

#### Parallel Composition (Concurrent Execution)
When services are executed in parallel (all must complete):
$$Q_p = \min_{i \in S} q_i$$

Where:
- $Q_p$ = composite QoS for parallel composition
- $\min$ selects the worst-case QoS among all parallel services

#### Conditional Composition (Branch)
When composition has alternative paths:
$$Q_c = \sum_{i} p_i \cdot q_i$$

Where:
- $Q_c$ = composite QoS for conditional composition
- $p_i$ = probability of selecting branch $i$
- $q_i$ = QoS attribute for that branch

### 1.2 Fitness Function for Selection

The primary selection function evaluates composite service quality:

$$\text{Fitness}(S) = \sum_{k=1}^{m} w_k \cdot q_k(S)$$

Subject to constraint:
$$q_k(S) \geq q_k^{min}, \forall k \in \{1, 2, ..., m\}$$

Where:
- $S$ = set of selected services forming the composition
- $m$ = number of QoS attributes considered
- $w_k$ = weight for k-th QoS attribute (∑w_k = 1)
- $q_k(S)$ = k-th aggregated QoS attribute of composite service
- $q_k^{min}$ = minimum threshold for k-th QoS attribute

### 1.3 Neural Network Surrogate Function

To reduce computational cost of fitness evaluation, a neural network approximates the fitness function:

$$\hat{y} = NN(x; \theta)$$

Where:
- $x$ = service composition vector (binary encoding of selected services)
- $\theta$ = network parameters (weights and biases)
- $\hat{y}$ = predicted fitness value

#### Network Architecture
- **Input Layer**: Service composition vector (one neuron per available service)
- **Hidden Layers**: Fully connected layers with activation functions
- **Output Layer**: Single neuron for fitness prediction

### 1.4 Training Loss Function

The neural network is trained using Mean Squared Error loss:

$$L(\theta) = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

Where:
- $N$ = number of training samples
- $y_i$ = actual fitness (computed via simulation)
- $\hat{y}_i$ = predicted fitness from NN

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Genetic Algorithm (GA) - Main Optimization

The GA handles exploration and exploitation through evolutionary operators:

#### Population Initialization
- Generate initial population of candidate solutions (service compositions)
- Each individual represents a valid service combination
- Population size: typically 50-100 individuals

#### Selection Operator (Exploitation)
Uses tournament selection:
1. Randomly select k individuals from population
2. Choose the best individual to be parent
3. Repeat to select both parents

Tournament selection balances exploration/exploitation:
- Larger tournaments → stronger selection pressure → exploitation
- Smaller tournaments → weaker selection → exploration

#### Crossover Operator (Exploration)
Single-point crossover:
```
Parent1: [S1, S2, S3 | S4, S5, S6]
Parent2: [A1, A2, A3 | A4, A5, A6]
Offspring: [S1, S2, S3, A4, A5, A6]
```
Crossover combines good service combinations from parents.

#### Mutation Operator (Exploration)
Random bit-flip mutation:
- With probability $P_m$, flip each service selection bit
- Prevents premature convergence by introducing new combinations

Mutation rate typically: 0.01-0.05

#### Elitism (Exploitation)
- Preserve top N best individuals unchanged to next generation
- Ensures best solutions are not lost

### 2.2 Neural Network - Surrogate Model

The NN serves as a computational shortcut:

#### Training Phase (Offline)
1. Generate sample compositions
2. Compute actual fitness via simulation
3. Train NN to predict fitness from composition

#### Evaluation Phase (Online)
1. For new GA individuals, use NN to predict fitness
2. Only run full simulation for promising candidates
3. Reduces overall computational cost

### 2.3 Exploration-Exploitation Balance

| Phase | Mechanism | Purpose |
|-------|-----------|---------|
| Early GA | High mutation, large tournament | Explore diverse solutions |
| Late GA | Low mutation, small tournament | Exploit best found solutions |
| NN Training | MSE loss minimization | Learn fitness landscape |
| Hybrid | NN approximation + GA search | Balance cost and quality |

---

## 3. Dataset Used

### 3.1 Synthetic IoT Service Registry

The paper uses synthetic datasets generated to simulate real IoT environments:

#### Service Registry Structure
Each service has:
- **Service ID**: Unique identifier
- **Functionality**: Service type/category
- **QoS Attributes**:
  - Response time (ms)
  - Reliability (0-1)
  - Availability (0-1)
  - Cost ($)
  - Throughput (requests/sec)
  - Latency (ms)

#### Dataset Characteristics
- **Number of Services**: 50-200 services
- **Service Categories**: 5-10 functional categories
- **QoS Distribution**: Random within realistic ranges
- **Composition Requests**: Multiple workflow patterns

### 3.2 Evaluation Scenarios

| Scenario | Services | Workflow Type | Purpose |
|----------|----------|---------------|---------|
| Small | 20-50 | Simple chain | Baseline |
| Medium | 50-100 | Chain + parallel | Standard test |
| Large | 100-200 | Complex workflow | Scalability |

---

## 4. Complete Workflow

### 4.1 Phase 1: Preprocessing

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA PREPARATION                          │
├─────────────────────────────────────────────────────────────┤
│  1. Generate synthetic IoT service registry                 │
│     - Define service categories                              │
│     - Assign QoS values (random within ranges)              │
│     - Store as service database                              │
│                                                              │
│  2. Create training dataset for NN                          │
│     - Generate random compositions                           │
│     - Compute actual fitness via QoS aggregation            │
│     - Store (composition, fitness) pairs                    │
│                                                              │
│  3. Train Neural Network                                    │
│     - Input: composition vectors                             │
│     - Output: predicted fitness                              │
│     - Minimize MSE loss                                      │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 2: Genetic Algorithm Optimization

```
┌─────────────────────────────────────────────────────────────┐
│                    GA OPTIMIZATION LOOP                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ GENERATION LOOP (repeat until convergence)          │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                     │   │
│  │ 1. EVALUATE FITNESS                                 │   │
│  │    - For each individual in population:             │   │
│  │    - Use NN to predict fitness (fast)               │   │
│  │    - For top candidates, verify with simulation     │   │
│  │                                                     │   │
│  │ 2. SELECTION (Tournament)                           │   │
│  │    - Select parents for reproduction                │   │
│  │    - Tournament size = 3-5                          │   │
│  │                                                     │   │
│  │ 3. CROSSOVER                                        │   │
│  │    - Single-point crossover                         │   │
│  │    - Probability = 0.7-0.9                          │   │
│  │                                                     │   │
│  │ 4. MUTATION                                         │   │
│  │    - Bit-flip mutation                              │   │
│  │    - Probability = 0.01-0.05                        │   │
│  │                                                     │   │
│  │ 5. ELITISM                                          │   │
│  │    - Preserve top 2-5 individuals                   │   │
│  │    - Copy to next generation unchanged              │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Phase 3: Solution Extraction

```
┌─────────────────────────────────────────────────────────────┐
│                  SOLUTION EXTRACTION                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Select best individual from final population           │
│  2. Decode chromosome to service list                       │
│  3. Verify QoS constraints satisfied                        │
│  4. If valid → return as optimal composition               │
│  5. If invalid → apply repair mechanism or discard         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Complete Algorithm Flowchart

```
                          ┌─────────────────────┐
                          │  Initialize GA      │
                          │  - Population       │
                          │  - NN Training      │
                          └──────────┬──────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │     GENERATION LOOP           │
                     │                               │
                     │  ┌─────────────┐              │
                     │  │ Evaluate    │              │
                     │  │ Fitness     │              │
                     │  │ (NN + Sim)  │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Selection   │              │
                     │  │ Tournament  │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Crossover   │              │
                     │  │ Single-point│              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Mutation    │              │
                     │  │ Bit-flip    │              │
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
                     │  - Time limit         │
                     │  - Quality threshold  │
                     └───────────┬───────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
               YES               │               NO
                │                │                │
                ▼                │                ▼
     ┌──────────────────┐        │    ┌──────────────────────┐
     │ Return Best     │        │    │ Continue to Next     │
     │ Solution        │        │    │ Generation           │
     └──────────────────┘        │    └──────────────────────┘
                                 │
                                 └──────────────────────────┘
                                             (back to loop)
```

### 4.5 Pseudocode

```
ALGORITHM: GA-NN for IoT Service Composition

INPUT:
  - Service registry R = {s1, s2, ..., sn}
  - QoS weights W = {w1, w2, ..., wm}
  - Constraints C = {c1, c2, ..., ck}
  - GA parameters: pop_size, generations, pc, pm

OUTPUT:
  - Optimal service composition S*

// Phase 1: Preprocessing
1. Generate training data D = {(x, y)}
   For each random composition x:
      y = compute_fitness(x, R, W, C)
   
2. Train NN on D:
   theta = train_NN(D)

// Phase 2: GA Optimization
3. Initialize population P with random compositions
4. For gen = 1 to generations:
   
   a. For each individual in P:
         fitness = NN.predict(individual, theta)
         if top_candidate: verify with simulation
   
   b. Create new population P':
         - Elitism: copy best individuals to P'
         - While |P'| < pop_size:
             * Select parents via tournament
             * Apply crossover (prob = pc)
             * Apply mutation (prob = pm)
             * Add offspring to P'
   
   c. P = P'
   
   d. If convergence: break

// Phase 3: Solution Extraction
5. Select best individual from final P
6. Verify constraints satisfied
7. Return composition S*

END ALGORITHM
```

---

## 5. Summary

| Component | Details |
|-----------|---------|
| **Selection Function** | Weighted sum: Fitness(S) = Σ w_k · q_k(S) |
| **Aggregation Functions** | Sequential (∏), Parallel (min), Conditional (Σp·q) |
| **Exploration** | Mutation (bit-flip, pm=0.01-0.05), Crossover (single-point, pc=0.7-0.9) |
| **Exploitation** | Tournament selection, Elitism |
| **Surrogate** | Neural Network (feedforward, trained via MSE) |
| **Dataset** | Synthetic IoT service registry (50-200 services) |
| **Workflow** | Preprocessing → GA Loop → Solution Extraction |

---

*This document provides detailed analysis of Paper 02's solution framework.*