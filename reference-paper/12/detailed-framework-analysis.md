# Paper 12: Detailed Solution Framework Analysis

## Paper Information
- **Title**: Composing Energy Services in a Crowdsourced IoT Environment
- **Year**: 2017
- **Algorithm**: Crowdsourced Energy Service Composition (CESC) with Optimization

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

### 1.2 Crowdsourced Energy Service Model

#### Energy Service Utility
$$\text{Utility}(e_i) = \alpha \cdot E_{available} + \beta \cdot \text{Reliability}_i + \gamma \cdot \text{Availability}_i$$

Where:
- $E_{available}$ = available energy from crowdsourced source
- $\text{Reliability}_i$ = historical reliability
- $\text{Availability}_i$ = temporal availability
- $\alpha + \beta + \gamma = 1$

#### Cost Function
$$\text{Cost}(e_i) = C_{base} + C_{energy} \cdot E_{used} + C_{latency} \cdot L_i$$

Where:
- $C_{base}$ = base service cost
- $C_{energy}$ = cost per energy unit
- $E_{used}$ = energy consumed
- $C_{latency}$ = latency cost
- $L_i$ = service latency

### 1.3 Service Selection Score

$$\text{Score}(s_i) = \frac{\text{Utility}(s_i)}{\text{Cost}(s_i)} \cdot \text{QoSFactor}$$

Where:
$$\text{QoSFactor} = \prod_{k} w_k \cdot q_k(s_i)$$

### 1.4 Composition Energy Balance

$$E_{total} = \sum_{i \in S} E_i \geq E_{required}$$

Subject to:
$$Cost_{total} = \sum_{i \in S} Cost(e_i) \leq Budget$$

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Crowdsourced Service Discovery

#### Energy Source Discovery (Exploration)
- Explore available crowdsourced energy sources
- Consider geographic proximity
- Factor in availability windows

#### Quality Filtering (Exploitation)
- Remove sources below reliability threshold
- Filter by availability matches workflow timing
- Rank by utility/cost ratio

### 2.2 Composition Algorithm

#### Greedy Selection with Energy Constraint
```
1. Sort candidate services by Score descending
2. Select highest Score service
3. Check energy constraint: E_total >= E_required
4. Check cost constraint: Cost_total <= Budget
5. If constraints satisfied: add to composition
6. Repeat until all tasks filled
```

#### Dynamic Reallocation (Exploration)
- During execution, if energy source becomes unavailable
- Re-explore alternative sources
- Re-optimize composition dynamically

### 2.3 Exploration-Exploitation Balance

| Mechanism | Exploration | Exploitation |
|-----------|-------------|--------------|
| Service Discovery | Find new crowdsourced sources | Filter high utility sources |
| Selection | Consider alternatives | Best Score selection |
| Reallocation | Explore alternatives when source fails | Use cached good sources |
| Energy Balancing | Search for sufficient energy | Minimize cost |

### 2.4 Algorithm Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| α (energy weight) | 0.3-0.5 | Energy availability emphasis |
| β (reliability) | 0.2-0.4 | Reliability consideration |
| γ (availability) | 0.2-0.3 | Temporal availability |
| Reliability threshold | 0.7-0.9 | Minimum reliability filter |

---

## 3. Dataset Used

### 3.1 Crowdsourced IoT Energy Service Registry

#### Service Registry Structure
Each service has:
- **Service ID**: Unique identifier
- **Provider ID**: Crowd energy provider
- **Energy Profile**:
  - Available energy (Wh)
  - Energy type (solar, battery, kinetic)
- **QoS Attributes**:
  - Reliability
  - Availability (time windows)
  - Cost
  - Latency

#### Dataset Characteristics
| Parameter | Value |
|-----------|-------|
| Number of Energy Services | 50-150 |
| Providers | 20-50 (crowd) |
| Energy Range | 0.5-10 Wh per service |
| QoS Attributes | 4 per service |
| Availability Windows | 1-24 hours |

### 3.2 Evaluation Scenarios

| Scenario | Sources | Energy Demand | Purpose |
|----------|---------|---------------|---------|
| Low Demand | 50 | 5 Wh | Baseline |
| Medium Demand | 100 | 20 Wh | Standard |
| High Demand | 150 | 50 Wh | Stress test |
| Dynamic | 100 | Variable | Reallocation test |

---

## 4. Complete Workflow

### 4.1 Phase 1: Preprocessing

```
┌─────────────────────────────────────────────────────────────┐
│            CROWDSOURCED SERVICE PREPROCESSING                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Generate crowdsourced energy service registry           │
│     - Provider pool (diverse sources)                      │
│     - Energy profiles and availability                     │
│     - Historical reliability data                         │
│                                                              │
│  2. Compute service metrics                                │
│     - Utility values                                       │
│     - Cost values                                          │
│     - Normalized QoS                                       │
│                                                              │
│  3. Set constraints                                        │
│     - Total energy required                                │
│     - Budget limit                                         │
│     - Reliability threshold                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 2: Energy-Aware Composition

```
┌─────────────────────────────────────────────────────────────┐
│          CROWDSOURCED ENERGY SERVICE COMPOSITION             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ COMPOSITION LOOP (for each workflow task)            │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │ 1. DISCOVER ENERGY SOURCES                          │   │
│  │    - Explore available crowdsourced sources         │   │
│  │    - Filter by availability windows                 │   │
│  │                                                      │   │
│  │ 2. COMPUTE SCORES                                   │   │
│  │    - For each source:                               │   │
│  │    - Utility = α·E + β·Rel + γ·Avail                │   │
│  │    - Cost = C_base + C_energy·E + C_latency·L      │   │
│  │    - Score = (Utility/Cost) · QoSFactor             │   │
│  │                                                      │   │
│  │ 3. FILTER BY CONSTRAINTS                            │   │
│  │    - Energy: E_total >= E_required                 │   │
│  │    - Cost: Cost_total <= Budget                    │   │
│  │    - Reliability >= threshold                      │   │
│  │                                                      │   │
│  │ 4. GREEDY SELECTION                                 │   │
│  │    - Sort by Score descending                      │   │
│  │    - Select highest Score until constraints met    │   │
│  │                                                      │   │
│  │ 5. ADD TO COMPOSITION                               │   │
│  │    - Update E_total, Cost_total                     │   │
│  │    - Verify constraints still satisfied             │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Phase 3: Dynamic Adaptation

```
┌─────────────────────────────────────────────────────────────┐
│               DYNAMIC ENERGY RE-ALLOCATION                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  During execution:                                          │
│                                                              │
│  1. Monitor energy sources                                  │
│  2. If source becomes unavailable:                         │
│     a. Explore alternatives                                │
│     b. Check if energy constraint still met                 │
│     c. If not, find replacement source                     │
│     d. Reallocate energy                                   │
│  3. If cost exceeds budget:                                │
│     a. Find lower-cost alternatives                       │
│     b. Re-optimize composition                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Complete Flowchart

```
                          ┌─────────────────────┐
                          │  Preprocessing       │
                          │  - Registry         │
                          │  - Metrics          │
                          │  - Constraints      │
                          └──────────┬──────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │     COMPOSITION LOOP          │
                     │                               │
                     │  ┌─────────────┐              │
                     │  │ Discover   │              │
                     │  │ Sources    │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Compute    │              │
                     │  │ Scores     │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Filter      │              │
                     │  │ Constraints │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Greedy     │              │
                     │  │ Selection  │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     └─────────┼─────────────────────┘
                               │
                               ▼
                     ┌───────────────────────┐
                     │  All Tasks Complete?  │
                     └───────────┬───────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
               YES               │               NO
                ▼                │                ▼
     ┌──────────────────┐       │    ┌──────────────────────┐
     │ Dynamic         │       │    │ Continue Composition  │
     │ Monitoring       │       │    └──────────────────────┘
     └────────┬─────────┘       │
              │                │
              ▼                │
     ┌──────────────────┐       │
     │ Source Fail?     │       │
     │ Budget Exceeded? │       │
     └────────┬─────────┘       │
              │                │
              └────────────────┘
                  (back to loop or return)
```

### 4.5 Pseudocode

```
ALGORITHM: Crowdsourced Energy Service Composition

INPUT:
  - Energy service registry R = {e1, ..., en}
  - Workflow tasks T = {t1, ..., tk}
  - Energy requirement E_required
  - Budget limit
  - Weights α, β, γ

OUTPUT:
  - Optimal energy service composition S*

// Phase 1: Preprocessing
1. For each service e_i:
      Compute Utility(e_i) = α·E + β·Rel + γ·Avail
      Compute Cost(e_i) = C_base + C_energy·E + C_latency·L

2. Set constraints:
      E_total_required = E_required
      Cost_max = Budget

// Phase 2: Composition
3. S* = {}  // Empty composition
4. E_accumulated = 0
5. Cost_accumulated = 0

6. For each task t in workflow:
   
   a. Get candidate energy sources C for task t
   
   b. For each source e in C:
         Score(e) = (Utility(e) / Cost(e)) · QoSFactor(e)
   
   c. Sort C by Score descending
   
   d. For each e in sorted C:
         If (E_accumulated + E(e) <= E_required + tolerance) AND
            (Cost_accumulated + Cost(e) <= Budget):
            Add e to S*
            E_accumulated += E(e)
            Cost_accumulated += Cost(e)
            Break
   
   e. If no service added: return failure

// Phase 3: Dynamic Adaptation
7. During execution:
   For each source e in S*:
      If e becomes unavailable:
         Find replacement e' from registry
         If found and constraints satisfied:
            Replace e with e' in S*
         Else:
            Report failure

8. Return S*

END ALGORITHM
```

---

## 5. Summary

| Component | Details |
|-----------|---------|
| **Selection Function** | Score = (Utility/Cost) · QoSFactor |
| **Aggregation Functions** | Sequential (∏), Parallel (min), Conditional (Σp·q) |
| **Utility Model** | Utility = α·E + β·Reliability + γ·Availability |
| **Cost Model** | Cost = C_base + C_energy·E + C_latency·L |
| **Constraints** | Energy requirement, Budget limit, Reliability threshold |
| **Exploration** | Discover new crowdsourced sources, dynamic reallocation |
| **Exploitation** | Greedy selection by Score, constraint filtering |
| **Novel Contribution** | Crowdsourced energy service composition |
| **Dataset** | Crowdsourced IoT (50-150 services), 20-50 providers |
| **Workflow** | Preprocessing → Composition Loop → Dynamic Adaptation |

---

*This document provides detailed analysis of Paper 12's solution framework.*