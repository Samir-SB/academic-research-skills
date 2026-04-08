# Paper 09: Detailed Solution Framework Analysis

## Paper Information
- **Title**: Energy-Centered and QoS-Aware Services Selection for Internet of Things
- **Year**: 2018
- **Algorithm**: Energy-Aware Multi-Criteria Decision Making (EA-MCDM)

---

## 1. Functions Used for Selection and Aggregation

### 1.1 QoS Aggregation Functions

#### Sequential Composition (Service Chain)
$$Q_s = \prod_{i=1}^{n} q_i$$

Where:
- $Q_s$ = composite QoS for sequential composition
- $q_i$ = QoS attribute of service $i$

#### Parallel Composition (Concurrent Execution)
$$Q_p = \min_{i \in S} q_i$$

Where:
- $Q_p$ = composite QoS for parallel composition

#### Conditional Composition (Branch)
$$Q_c = \sum_{j} p_j \cdot q_j$$

Where:
- $p_j$ = probability of branch $j$

### 1.2 Energy Consumption Model

The core innovation: energy-aware service selection:

$$E(s_i) = E_{proc} + E_{trans} + E_{comm}$$

Where:
- $E_{proc}$ = processing energy consumption
- $E_{trans}$ = transmission energy consumption
- $E_{comm}$ = communication energy consumption

#### Detailed Energy Components
$$E_{proc}(s_i) = P_{proc} \cdot t_{proc}(s_i)$$

$$E_{trans}(s_i) = P_{tx} \cdot d(s_i, u) \cdot rate$$

$$E_{comm}(s_i) = P_{rx} \cdot t_{comm}(s_i)$$

Where:
- $P_{proc}$ = processing power
- $t_{proc}$ = processing time
- $P_{tx}$ = transmit power
- $d(s_i, u)$ = distance between service and user
- $P_{rx}$ = receive power

### 1.3 Combined Energy-QoS Fitness Function

$$\text{Score}(s_i) = \lambda_E \cdot \text{EnergyScore}(s_i) + \lambda_Q \cdot \text{QoSScore}(s_i)$$

Where:
- $\lambda_E + \lambda_Q = 1$
- $\lambda_E$ = energy weight (typically 0.5-0.7 for energy-critical applications)

#### Energy Score (normalized)
$$\text{EnergyScore}(s_i) = 1 - \frac{E(s_i) - E_{min}}{E_{max} - E_{min}}$$

Where:
- $E_{min}$ = minimum energy in candidate set
- $E_{max}$ = maximum energy in candidate set

#### QoS Score (normalized)
$$\text{QoSScore}(s_i) = \sum_{k=1}^{m} w_k \cdot \frac{q_k(s_i) - q_k^{min}}{q_k^{max} - q_k^{min}}$$

Where:
- $w_k$ = weight for k-th QoS attribute
- $q_k^{min}, q_k^{max}$ = min/max for normalization

### 1.4 TOPSIS-Based Ranking

The paper uses TOPSIS (Technique for Order Preference by Similarity to Ideal Solution):

**Ideal Solution:**
- $q_k^{ideal} = q_k^{max}$ for benefit attributes
- $q_k^{ideal} = q_k^{min}$ for cost attributes

**Distance Metrics:**
$$d_i^+ = \sqrt{\sum_{k=1}^{m} w_k (q_k(s_i) - q_k^{ideal})^2}$$

$$d_i^- = \sqrt{\sum_{k=1}^{m} w_k (q_k(s_i) - q_k^{worst})^2}$$

**Final Score:**
$$\text{RelativeCloseness}_i = \frac{d_i^-}{d_i^+ + d_i^-}$$

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Energy-Aware Service Discovery

The approach doesn't use evolutionary algorithms but uses intelligent search:

#### Service Filtering (Exploitation)
1. Filter services by energy constraint: $E(s_i) \leq E_{threshold}$
2. Sort by energy consumption
3. Keep top N candidates

#### Multi-Criteria Ranking (Exploitation)
- Apply TOPSIS with combined energy-QoS criteria
- Rank services by relative closeness

#### Adaptive Weight Adjustment
```
If battery_level > 80%:
    λ_E = 0.3, λ_Q = 0.7  // QoS priority
Else if battery_level > 50%:
    λ_E = 0.5, λ_Q = 0.5  // Balanced
Else if battery_level > 20%:
    λ_E = 0.7, λ_Q = 0.3  // Energy priority
Else:
    λ_E = 0.9, λ_Q = 0.1  // Energy critical
```

### 2.2 Exploration Mechanisms

#### Service Discovery with Energy Budget
- Explore alternative services within energy budget
- Trade-off: potentially better QoS vs energy savings

#### Dynamic Re-selection (Exploration)
- Monitor energy consumption during execution
- If energy drops below threshold, explore alternative services
- Select new service with better energy profile

### 2.3 Exploration-Exploitation Balance

| Mechanism | Exploration | Exploitation |
|-----------|-------------|--------------|
| Initial Selection | Filter by energy budget | TOPSIS ranking |
| Adaptive Weights | Adjust based on battery | Prioritize energy/QoS |
| Dynamic Re-selection | Explore alternatives | Use learned good services |
| Service Caching | Discover new services | Reuse proven services |

---

## 3. Dataset Used

### 3.1 Synthetic IoT Service Registry

#### Service Registry Structure
Each service has:
- **Service ID**: Unique identifier
- **Functionality**: Service type/category
- **Location**: (latitude, longitude)
- **Energy Profile**:
  - Processing energy
  - Transmission energy
  - Communication energy
- **QoS Attributes**:
  - Response time
  - Cost
  - Reliability

#### Dataset Characteristics
| Parameter | Value |
|-----------|-------|
| Number of Services | 30-100 |
| Service Categories | 5-8 functional categories |
| Energy Range | 0.1-5.0 Wh |
| QoS Attributes | 3-4 per service |

### 3.2 Device Profiles
- Different IoT device types with varying energy budgets
- Battery levels: 10%-100%

### 3.3 Evaluation Scenarios

| Scenario | Services | Battery Level | Purpose |
|----------|----------|---------------|---------|
| High Battery | 50 | >80% | QoS optimization |
| Medium Battery | 50 | 50% | Balanced |
| Low Battery | 50 | <20% | Energy priority |
| Dynamic | 100 | Varying | Re-selection test |

---

## 4. Complete Workflow

### 4.1 Phase 1: Preprocessing

```
┌─────────────────────────────────────────────────────────────┐
│               ENERGY-AWARE SERVICE PREPROCESSING             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Generate synthetic IoT service registry                 │
│     - Service categories                                    │
│     - Energy profiles (E_proc, E_trans, E_comm)             │
│     - QoS attributes                                        │
│                                                              │
│  2. Compute energy for each service                         │
│     - E(s_i) = E_proc + E_trans + E_comm                   │
│                                                              │
│  3. Normalize metrics                                       │
│     - Normalize energy (0-1, lower is better)               │
│     - Normalize QoS (0-1, higher is better)                │
│                                                              │
│  4. Set adaptive weights                                    │
│     - λ_E, λ_Q based on current battery level              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 2: Energy-Aware Selection

```
┌─────────────────────────────────────────────────────────────┐
│            ENERGY-CENTERED SERVICE SELECTION                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SERVICE SELECTION LOOP                               │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │ 1. GET CANDIDATE SERVICES                           │   │
│  │    - For current task, get matching services        │   │
│  │    - Filter by functional requirements              │   │
│  │                                                      │   │
│  │ 2. ENERGY FILTERING                                 │   │
│  │    - Remove services exceeding energy budget        │   │
│  │    - E(s_i) ≤ E_threshold                           │   │
│  │                                                      │   │
│  │ 3. ADAPTIVE WEIGHT CALCULATION                      │   │
│  │    - Check current battery level                    │   │
│  │    - Set λ_E, λ_Q accordingly                        │   │
│  │                                                      │   │
│  │ 4. TOPSIS RANKING                                    │   │
│  │    - Compute weighted normalized matrix             │   │
│  │    - Find ideal and worst solutions                 │   │
│  │    - Calculate distances d+, d-                     │   │
│  │    - Compute relative closeness                     │   │
│  │                                                      │   │
│  │ 5. SELECT BEST SERVICE                              │   │
│  │    - Select service with highest closeness          │   │
│  │    - Add to composition                              │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Phase 3: Dynamic Re-selection

```
┌─────────────────────────────────────────────────────────────┐
│               DYNAMIC ENERGY-AWARE RE-SELECTION              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  During execution:                                          │
│                                                              │
│  1. Monitor energy consumption                              │
│  2. If remaining_energy < threshold:                        │
│     a. Explore alternative services                        │
│     b. Filter by new energy constraint                     │
│     c. Re-rank using TOPSIS                                │
│     d. Switch to more energy-efficient service             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Complete Flowchart

```
                          ┌─────────────────────┐
                          │  Preprocessing       │
                          │  - Service Registry  │
                          │  - Energy Compute    │
                          │  - Normalization     │
                          └──────────┬──────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │     SELECTION LOOP            │
                     │                               │
                     │  ┌─────────────┐              │
                     │  │ Get         │              │
                     │  │ Candidates  │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Energy      │              │
                     │  │ Filter      │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Adaptive    │              │
                     │  │ Weights     │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ TOPSIS      │              │
                     │  │ Ranking     │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Select      │              │
                     │  │ Best        │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     └─────────┼─────────────────────┘
                               │
                               ▼
                     ┌───────────────────────┐
                     │  Workflow Complete?  │
                     └───────────┬───────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
               YES               │               NO
                ▼                │                ▼
     ┌──────────────────┐       │    ┌──────────────────────┐
     │ Execute &        │       │    │ Continue Selection    │
     │ Monitor Energy   │       │    └──────────────────────┘
     └────────┬─────────┘       │
              │                │
              ▼                │
     ┌──────────────────┐       │
     │ Energy Low?      │       │
     │ Re-select?       │       │
     └────────┬─────────┘       │
              │                │
              └────────────────┘
                  (back to loop)
```

### 4.5 Pseudocode

```
ALGORITHM: Energy-Centered QoS-Aware Service Selection

INPUT:
  - Service registry R = {s1, ..., sn}
  - Workflow tasks T = {t1, ..., tk}
  - QoS weights W = {w1, ..., wm}
  - Energy budget E_threshold

OUTPUT:
  - Energy-efficient service composition S*

// Phase 1: Preprocessing
1. For each service s_i in registry:
      Compute E(s_i) = E_proc + E_trans + E_comm

2. Normalize metrics:
      Energy_norm(s_i) = (E(s_i) - E_min) / (E_max - E_min)
      QoS_norm(s_i, k) = (q_k(s_i) - q_k^min) / (q_k^max - q_k^min)

// Phase 2: Selection
3. For each task t in workflow:
   
   a. Get candidate services C for task t
   
   b. Filter by energy constraint:
         C_filtered = {s ∈ C | E(s) ≤ E_threshold}
   
   c. Determine adaptive weights:
         battery = get_battery_level()
         λ_E = f(battery)  // Higher for lower battery
         λ_Q = 1 - λ_E
   
   d. Compute combined score for each s in C_filtered:
         EnergyScore = 1 - Energy_norm(s)
         QoSScore = Σ w_k · QoS_norm(s, k)
         Score(s) = λ_E · EnergyScore + λ_Q · QoSScore
   
   e. OR use TOPSIS:
         // Weighted normalized matrix
         // Ideal/worst solutions
         // Distance calculation
         // Relative closeness
         Score(s) = RelativeCloseness(s)
   
   f. Select service with highest Score:
         s* = argmax_{s∈C_filtered} Score(s)
         Add s* to composition

// Phase 3: Dynamic Re-selection (Optional)
4. During execution:
   If remaining_energy < re_selection_threshold:
      Explore alternative services
      Re-apply selection with stricter energy constraint
      Potentially switch to more efficient service

5. Return composition S*

END ALGORITHM
```

---

## 5. Summary

| Component | Details |
|-----------|---------|
| **Selection Function** | Combined score: λ_E·EnergyScore + λ_Q·QoSScore |
| **Aggregation Functions** | Sequential (∏), Parallel (min), Conditional (Σp·q) |
| **Energy Model** | E = E_proc + E_trans + E_comm |
| **Ranking Method** | TOPSIS with energy-QoS criteria |
| **Adaptation** | Dynamic λ_E based on battery level |
| **Exploration** | Service discovery within energy budget, dynamic re-selection |
| **Exploitation** | TOPSIS ranking, energy filtering |
| **Novel Contribution** | Energy-centered selection with adaptive weights |
| **Dataset** | Synthetic IoT (30-100 services) with energy profiles |
| **Workflow** | Preprocessing → Energy-Aware Selection → Dynamic Re-selection |

---

*This document provides detailed analysis of Paper 09's solution framework.*