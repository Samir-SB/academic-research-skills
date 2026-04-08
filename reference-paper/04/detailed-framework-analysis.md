# Paper 04: Detailed Solution Framework Analysis

## Paper Information
- **Title**: Spatio-Cohesive Service Selection Using Machine Learning in Dynamic IoT Environments
- **Year**: 2020
- **Algorithm**: Hybrid ML-GA (K-NN + ANN + GA)

---

## 1. Functions Used for Selection and Aggregation

### 1.1 QoS Aggregation Functions

The paper aggregates QoS attributes for composite services:

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

### 1.2 Spatio-Cohesive Fitness Function

The core innovation: fitness combines QoS with spatial cohesion:

$$\text{Fitness}(S) = w_1 \cdot \text{QoS}(S) + w_2 \cdot \text{SC}(S)$$

Where:
- $w_1 + w_2 = 1$ = weight parameters
- $\text{QoS}(S)$ = aggregated QoS score
- $\text{SC}(S)$ = spatial cohesion score

#### Spatio-Cohesive Score Components

$$\text{SC}(S) = \alpha \cdot D_{\text{dev}} + \beta \cdot D_{\text{disp}} + \gamma \cdot D_{\text{dens}}$$

Where:
- $D_{\text{dev}}$ = Spatial deviation (distance from user location)
- $D_{\text{disp}}$ = Spatial dispersion (spread of selected services)
- $D_{\text{dens}}$ = Spatial density (concentration of services)
- $\alpha + \beta + \gamma = 1$

#### Individual Spatial Metrics

**Spatial Deviation:**
$$D_{\text{dev}}(S) = \frac{1}{|S|} \sum_{i \in S} \text{dist}(u, s_i)$$

Where:
- $u$ = user/IoT device location
- $s_i$ = location of service $i$
- Lower deviation = better spatial proximity

**Spatial Dispersion:**
$$D_{\text{disp}}(S) = \sqrt{\frac{1}{|S|} \sum_{i \in S} (\text{dist}(s_i, \bar{s}))^2}$$

Where:
- $\bar{s}$ = centroid of selected services
- Lower dispersion = more clustered services

**Spatial Density:**
$$D_{\text{dens}}(S) = \frac{|S|}{\text{Area}(S)}$$

Where:
- $\text{Area}(S)$ = minimum bounding area covering all services
- Higher density = more compact service cluster

### 1.3 QoS Score Function

$$\text{QoS}(S) = \sum_{k=1}^{m} w_k \cdot q_k(S)$$

Subject to constraints:
$$q_k(S) \geq q_k^{\text{min}}, \forall k$$

Where:
- $m$ = number of QoS attributes
- $w_k$ = weight for k-th attribute
- $q_k(S)$ = aggregated k-th QoS attribute
- $q_k^{\text{min}}$ = minimum threshold

### 1.4 K-NN Service Discovery

The K-Nearest Neighbors finds similar services for replacement:

$$\text{Similarity}(s_i, s_j) = \frac{\sum_{k=1}^{m} w_k \cdot \text{sim}_k(q_i^k, q_j^k)}{\sum_{k=1}^{m} w_k}$$

Where:
- $\text{sim}_k$ = similarity for attribute $k$ (using normalized difference)
- K nearest services: $\{s_1', ..., s_K'\}$ with highest similarity

### 1.5 ANN QoS Prediction

Neural network predicts QoS for unknown service combinations:

$$\hat{q}_k = ANN_k(s_1, ..., s_n; \theta_k)$$

Where:
- Input: service feature vector
- Output: predicted QoS attribute $k$
- $\theta_k$ = network parameters for attribute $k$

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Hybrid ML-GA Framework

#### Machine Learning Components (Exploitation)
1. **K-NN for Service Discovery**
   - Find K most similar services to any service
   - Used during mutation for intelligent service replacement
   - Exploration: discover diverse alternatives
   - Exploitation: find high-quality similar services

2. **ANN for QoS Prediction**
   - Train on historical service compositions
   - Predict QoS for new combinations
   - Reduces computational cost vs simulation
   - Exploitation: guide search toward high-QoS regions

#### Genetic Algorithm (Main Optimizer)
The GA handles exploration and exploitation:

**Population Initialization**
- Generate initial population of service selections
- Each chromosome: list of service IDs for composition
- Population size: 50-100 individuals

**Selection Operator (Exploitation)**
Tournament selection:
1. Select k individuals randomly
2. Choose best as parent based on fitness
3. Tournament size: 3-5

**Crossover Operator (Exploration)**
Single-point crossover:
```
Parent1: [S1, S2, S3 | S4, S5]
Parent2: [A1, A2, A3 | A4, A5]
Offspring: [S1, S2, S3, A4, A5]
```

**Mutation Operator (Exploration)**
K-NN guided mutation:
1. For each gene, with probability $P_m$:
2. Find K nearest services using K-NN
3. Replace with one of top 2-3 similar services
4. Mutation rate: 0.03-0.08

**Elitism (Exploitation)**
- Preserve top 2-5 individuals to next generation
- Ensures best solutions preserved

### 2.2 Exploration-Exploitation Balance

| Component | Exploration | Exploitation |
|-----------|-------------|--------------|
| K-NN | Find diverse alternatives | Select similar high-quality |
| ANN | - | Predict QoS, guide search |
| GA Crossover | Combine service combinations | - |
| GA Mutation | Introduce new services via K-NN | Replace with similar services |
| Selection | - | Tournament selection |
| Elitism | - | Preserve best solutions |

### 2.3 Adaptive Strategy

| Phase | K-NN Usage | ANN Usage | GA Parameters |
|-------|------------|-----------|---------------|
| Early | More exploration (larger K) | Training phase | Higher mutation |
| Middle | Balanced | Active prediction | Balanced |
| Late | More exploitation (smaller K) | Prediction refinement | Lower mutation |

---

## 3. Dataset Used

### 3.1 Synthetic IoT Service Registry with Spatial Attributes

#### Service Registry Structure
Each service has:
- **Service ID**: Unique identifier
- **Functionality**: Service type/category
- **Location**: (latitude, longitude) coordinates
- **QoS Attributes**:
  - Response time (ms)
  - Cost ($)
  - Reliability (0-1)
  - Availability (0-1)

#### Dataset Characteristics
| Parameter | Value |
|-----------|-------|
| Number of Services | 50-150 |
| Service Categories | 5-10 functional categories |
| Geographic Area | 100 km × 100 km |
| Spatial Distribution | Random, clustered, grid |
| QoS Attributes | 4-6 per service |

### 3.2 User/Request Characteristics
- User locations: randomly distributed in service area
- Composition requests: workflow patterns with spatial requirements

### 3.3 Evaluation Scenarios

| Scenario | Services | Spatial Pattern | Purpose |
|----------|----------|-----------------|---------|
| Sparse | 50 | Random distribution | Baseline |
| Dense | 100 | Clustered | High density test |
| Mixed | 75 | Grid + random | Complex topology |
| Dynamic | 100 | Time-varying | Adaptation test |

---

## 4. Complete Workflow

### 4.1 Phase 1: Preprocessing - ML Model Training

```
┌─────────────────────────────────────────────────────────────┐
│               MACHINE LEARNING MODEL TRAINING                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Generate synthetic IoT service registry                  │
│     - Service categories and types                          │
│     - Assign QoS values                                     │
│     - Assign geographic locations                           │
│                                                              │
│  2. Build K-NN Service Similarity Model                    │
│     - Feature vector: QoS attributes                        │
│     - Similarity metric: weighted Euclidean                │
│     - Precompute similarity matrix                         │
│                                                              │
│  3. Train ANN QoS Prediction Model                        │
│     - Input: service feature vectors                       │
│     - Output: QoS attribute predictions                    │
│     - Training: backpropagation with MSE loss              │
│     - Validation on held-out compositions                  │
│                                                              │
│  4. Initialize GA parameters                               │
│     - Population size, generations                          │
│     - Crossover probability                                 │
│     - Mutation probability                                  │
│     - w1, w2 weights                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 2: Hybrid GA Optimization

```
┌─────────────────────────────────────────────────────────────┐
│              ML-ENHANCED GA OPTIMIZATION                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ GENERATION LOOP (repeat until convergence)          │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │ 1. EVALUATE FITNESS (ML-Accelerated)                │   │
│  │    - For each individual:                           │   │
│  │    - ANN prediction: QoS(S)                         │   │
│  │    - Compute spatial metrics: D_dev, D_disp, D_dens│   │
│  │    - Calculate SC(S) = α·D_dev + β·D_disp + γ·D_dens│   │
│  │    - Fitness = w1·QoS + w2·SC                      │   │
│  │                                                      │   │
│  │ 2. SELECTION (Tournament)                           │   │
│  │    - Select parents based on fitness                │   │
│  │                                                      │   │
│  │ 3. CROSSOVER                                        │   │
│  │    - Single-point crossover                         │   │
│  │    - Probability = 0.7-0.9                         │   │
│  │                                                      │   │
│  │ 4. K-NN GUIDED MUTATION                            │   │
│  │    - For each gene with probability pm:            │   │
│  │    - Find K nearest services via K-NN              │   │
│  │    - Replace with similar service                  │   │
│  │                                                      │   │
│  │ 5. ELITISM                                          │   │
│  │    - Preserve top individuals                       │   │
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
│  2. Decode chromosome to service list                       │
│  3. Compute final QoS via ANN or simulation                │
│  4. Verify QoS constraints satisfied                        │
│  5. Extract spatial cohesion metrics                        │
│  6. If valid → return optimal spatio-cohesive selection    │
│  7. If invalid → apply repair or discard                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Complete Algorithm Flowchart

```
                          ┌─────────────────────┐
                          │  Preprocessing      │
                          │  - Service Registry │
                          │  - K-NN Training    │
                          │  - ANN Training      │
                          │  - GA Init           │
                          └──────────┬──────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │     GENERATION LOOP          │
                     │                               │
                     │  ┌─────────────┐              │
                     │  │ Evaluate    │              │
                     │  │ Fitness     │              │
                     │  │ w1·QoS+w2·SC│              │
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
                     │  │ K-NN        │              │
                     │  │ Mutation    │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Elitism     │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     └─────────┼─────────────────────┘
                               │
                               ▼
                     ┌───────────────────────┐
                     │  Convergence Check    │
                     │  - Max generations    │
                     │  - Fitness plateau    │
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
     │ Spatio-Coherent  │        │    │ Generation           │
     │ Solution         │        │    └──────────────────────┘
     └──────────────────┘        │
                                 │
                                 └──────────────────────────┘
                                             (back to loop)
```

### 4.5 Pseudocode

```
ALGORITHM: Spatio-Coherent ML-GA for IoT Service Selection

INPUT:
  - Service registry R = {s1, s2, ..., sn}
  - User location u
  - QoS weights W = {w1, ..., wm}
  - Spatial weights α, β, γ
  - Fitness weights w1, w2
  - GA parameters: pop_size, generations, pc, pm, K

OUTPUT:
  - Optimal spatio-cohesive service selection S*

// Phase 1: Preprocessing
1. Build K-NN model:
   For each service si:
      Compute similarity to all other services
   Store nearest K neighbors for each service

2. Train ANN QoS predictors:
   Generate training compositions
   Compute actual QoS via simulation
   Train ANN_k for each QoS attribute k

// Phase 2: GA Optimization
3. Initialize population P with random service selections
4. For gen = 1 to generations:
   
   a. For each individual in P:
         // QoS via ANN
         QoS = ANN.predict(composition)
         
         // Spatial metrics
         D_dev = mean_distance_to_user(user_loc, services)
         D_disp = spatial_dispersion(services)
         D_dens = spatial_density(services)
         SC = α·D_dev + β·D_disp + γ·D_dens
         
         // Fitness
         Fitness = w1·QoS + w2·SC
   
   b. Create new population P':
         - Elitism: copy best individuals
         - While |P'| < pop_size:
             * Select parents via tournament
             * Apply crossover (prob = pc)
             * Apply K-NN mutation (prob = pm)
             * Add offspring to P'
   
   c. P = P'
   
   d. If convergence: break

// Phase 3: Solution Extraction
5. Select best individual from final P
6. Verify constraints satisfied
7. Return S* with QoS and spatial metrics

END ALGORITHM
```

---

## 5. Summary

| Component | Details |
|-----------|---------|
| **Selection Function** | Fitness = w1·QoS + w2·SC, w1+w2=1 |
| **Aggregation Functions** | Sequential (∏), Parallel (min), Conditional (Σp·q) |
| **QoS Attributes** | Response time, cost, reliability, availability |
| **Spatial Metrics** | Deviation, dispersion, density |
| **ML Components** | K-NN (similarity), ANN (QoS prediction) |
| **Exploration** | Crossover, K-NN mutation (pm=0.03-0.08) |
| **Exploitation** | Tournament selection, ANN prediction, Elitism |
| **Novel Contribution** | Spatio-cohesive selection combining QoS + spatial metrics |
| **Dataset** | Synthetic IoT (50-150 services) with location attributes |
| **Workflow** | ML Training → GA Optimization → Solution Extraction |

---

*This document provides detailed analysis of Paper 04's solution framework.*