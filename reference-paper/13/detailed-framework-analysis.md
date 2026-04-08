# Paper 13: Detailed Solution Framework Analysis

## Paper Information
- **Title**: Crowdsourcing Energy as a Service
- **Year**: 2016
- **Algorithm**: Crowdsourced Energy Trading + Optimization Framework

---

## 1. Functions Used for Selection and Aggregation

### 1.1 Energy Aggregation Functions

#### Sequential Energy Flow
$$E_{total} = \sum_{i=1}^{n} E_i$$

Where:
- $E_{total}$ = total energy from aggregated sources
- $E_i$ = energy from source $i$

#### Parallel Energy Sources
$$E_{combined} = \sum_{i \in S} E_i$$

Where:
- $E_{combined}$ = combined energy from parallel sources
- $S$ = set of parallel energy sources

### 1.2 Energy Trading Value Model

#### Provider Revenue Function
$$\text{Revenue}(e_i) = P_{market} \cdot E_i + \text{Incentive}_i$$

Where:
- $P_{market}$ = market price per energy unit
- $E_i$ = energy sold by provider $i$
- $\text{Incentive}_i$ = additional incentive for quality

#### Consumer Cost Function
$$\text{Cost}(S) = P_{market} \cdot E_{required} + \sum_{i \in S} P_{premium}^i$$

Where:
- $E_{required}$ = total energy required
- $P_{premium}^i$ = premium cost for service $i$

#### Quality-Adjusted Value
$$\text{Value}(e_i) = \frac{E_i \cdot \text{Quality}_i}{\text{Cost}_i}$$

Where:
$$\text{Quality}_i = w_1 \cdot \text{Reliability}_i + w_2 \cdot \text{Availability}_i + w_3 \cdot \text{Freshness}_i$$

### 1.3 Matching Score

$$\text{MatchScore}(c, p) = \frac{1}{1 + |E_{demand} - E_{supply}|} \cdot \text{Quality}(p) \cdot \text{Reputation}(p)$$

Where:
- $c$ = consumer (energy demand)
- $p$ = provider (energy supply)
- $E_{demand}$ = consumer's energy need
- $E_{supply}$ = provider's available energy
- $\text{Reputation}(p)$ = provider's historical rating

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Energy Source Discovery

#### Consumer Search (Exploration)
- Explore multiple energy providers
- Consider geographic distribution
- Factor in temporal availability

#### Provider Ranking (Exploitation)
- Rank providers by MatchScore
- Filter by price constraints
- Select highest value providers

### 2.2 Matching Algorithm

#### Greedy Matching
```
1. Sort consumers by urgency (energy need deadline)
2. For each consumer:
   a. Find available providers within budget
   b. Rank by MatchScore
   c. Select best matching provider
   d. Reserve energy allocation
   e. Update provider remaining capacity
```

#### Optimal Matching (Hungarian Algorithm)
If multiple consumers and providers:
- Build cost matrix: cost[i][j] = Cost(consumer_i, provider_j)
- Apply Hungarian algorithm for optimal assignment
- Minimize total cost while satisfying all demands

### 2.3 Dynamic Pricing Mechanism

#### Price Adjustment (Exploration)
$$P_{dynamic} = P_{base} \cdot (1 + \text{demand\_factor} \cdot \frac{D - S}{S})$$

Where:
- $D$ = total demand
- $S$ = total supply
- $\text{demand\_factor}$ = sensitivity parameter

### 2.4 Exploration-Exploitation Balance

| Mechanism | Exploration | Exploitation |
|-----------|-------------|--------------|
| Provider Discovery | Explore new crowd sources | Use high-reputation providers |
| Matching | Consider multiple consumers | Best MatchScore selection |
| Pricing | Adjust to market conditions | Fixed premium for quality |
| Allocation | Explore alternatives | Optimal assignment |

---

## 3. Dataset Used

### 3.1 Crowdsourced Energy Trading Platform

#### Provider Registry
Each provider has:
- **Provider ID**: Unique identifier
- **Energy Profile**:
  - Available energy (Wh)
  - Energy type (solar, battery, kinetic, etc.)
  - Generation rate
- **Quality Metrics**:
  - Reliability rating
  - Availability percentage
  - Freshness (time since last update)
- **Reputation Score**: Historical performance

#### Consumer Requests
- Energy demand (Wh)
- Budget limit
- Quality requirements
- Time constraints

#### Dataset Characteristics
| Parameter | Value |
|-----------|-------|
| Providers | 100-500 (crowd) |
| Consumers | 20-100 per cycle |
| Energy per Provider | 1-20 Wh |
| Quality Attributes | 3-4 per provider |
| Trading Cycles | Continuous |

### 3.2 Evaluation Scenarios

| Scenario | Providers | Demand | Purpose |
|----------|-----------|--------|---------|
| Low Demand | 100 | 50 Wh | Baseline |
| Medium Demand | 200 | 200 Wh | Standard test |
| High Demand | 500 | 500 Wh | Stress test |
| Real-time | 300 | Variable | Dynamic trading |

---

## 4. Complete Workflow

### 4.1 Phase 1: Preprocessing

```
┌─────────────────────────────────────────────────────────────┐
│            CROWD ENERGY TRADING PLATFORM SETUP              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Initialize provider registry                           │
│     - Collect provider profiles                            │
│     - Record historical reputation                         │
│     - Set energy availability windows                      │
│                                                              │
│  2. Set market parameters                                  │
│     - Base price P_base                                    │
│     - Demand factor sensitivity                            │
│     - Premium tiers                                        │
│                                                              │
│  3. Compute provider metrics                               │
│     - Quality scores                                       │
│     - MatchScore parameters                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 2: Energy Trading Cycle

```
┌─────────────────────────────────────────────────────────────┐
│              ENERGY TRADING EXECUTION CYCLE                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ TRADING CYCLE (repeat for each period)               │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │ 1. COLLECT CONSUMER REQUESTS                        │   │
│  │    - Energy demand E_required                       │   │
│  │    - Budget limit                                    │   │
│  │    - Quality requirements                            │   │
│  │                                                      │   │
│  │ 2. UPDATE PROVIDER AVAILABILITY                     │   │
│  │    - Check current energy levels                    │
│  │    - Remove depleted providers                      │   │
│  │    - Add newly available sources                    │   │
│  │                                                      │   │
│  │ 3. DYNAMIC PRICING                                  │   │
│  │    - Compute demand/supply ratio                    │   │
│  │    - Adjust P_base to P_dynamic                    │   │
│  │                                                      │   │
│  │ 4. MATCHING ALGORITHM                               │   │
│  │    - For each consumer:                             │   │
│  │    - Compute MatchScore for each provider          │   │
│  │    - Apply greedy or Hungarian matching            │   │
│  │                                                      │   │
│  │ 5. ENERGY ALLOCATION                                │   │
│  │    - Reserve matched energy                         │   │
│  │    - Update provider remaining capacity            │   │
│  │    - Record transaction                              │   │
│  │                                                      │   │
│  │ 6. REPUTATION UPDATE                                │   │
│  │    - After energy delivery:                         │   │
│  │    - Consumer rates provider                        │   │
│  │    - Update reputation score                        │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Phase 3: Continuous Optimization

```
┌─────────────────────────────────────────────────────────────┐
│              CONTINUOUS TRADING OPTIMIZATION                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  After each trading cycle:                                   │
│                                                              │
│  1. Analyze matching efficiency                             │
│  2. Identify unmet demand                                   │
│  3. Adjust provider discovery for next cycle               │
│  4. Update pricing strategy                                  │
│  5. Optimize allocation algorithm                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Complete Flowchart

```
                          ┌─────────────────────┐
                          │  Platform Init       │
                          │  - Provider Registry │
                          │  - Market Params    │
                          └──────────┬──────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │     TRADING CYCLE             │
                     │                               │
                     │  ┌─────────────┐              │
                     │  │ Collect     │              │
                     │  │ Requests    │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Update      │              │
                     │  │ Providers   │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Dynamic     │              │
                     │  │ Pricing     │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Matching    │              │
                     │  │ Algorithm   │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Energy      │              │
                     │  │ Allocation  │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Reputation  │              │
                     │  │ Update      │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     └─────────┼─────────────────────┘
                               │
                               ▼
                     ┌───────────────────────┐
                     │  Continue Next Cycle? │
                     └───────────┬───────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                |
               YES               │               NO
                ▼                │                ▼
     ┌──────────────────┐       │    ┌──────────────────────┐
     │ Continue         │       │    │ Return Results       │
     │ Optimization     │       │    └──────────────────────┘
     └──────────────────┘       │
                                 │
                                 └──────────────────────────┘
                                             (back to loop)
```

### 4.5 Pseudocode

```
ALGORITHM: Crowdsourcing Energy as a Service

INPUT:
  - Provider registry P = {p1, ..., pn}
  - Consumer requests C = {c1, ..., cm}
  - Market parameters
  - Matching strategy (greedy or optimal)

OUTPUT:
  - Energy allocation matches A = {(c_i, p_j, E)}

1. Initialize market:
   P_base = initial_price
   demand_factor = sensitivity

2. For each trading cycle t:
   
   a. // Collect and validate requests
      For each consumer c in C:
          Validate: E_required, Budget, Quality_req
   
   b. // Update provider availability
      For each provider p in P:
          Update available_energy(p)
          Remove if available_energy < min_threshold
   
   c. // Dynamic pricing
      D = total_demand(C)
      S = total_supply(P)
      P_dynamic = P_base * (1 + demand_factor * (D-S)/S)
   
   d. // Matching
      If matching_strategy == "greedy":
         For each consumer c sorted by urgency:
             Candidates = {p in P | p.energy >= c.demand AND p.cost <= c.budget}
             Sort Candidates by MatchScore(c, p)
             Select best p, allocate min(c.demand, p.energy)
      Else:  // Hungarian algorithm
         Build cost matrix
         Apply Hungarian algorithm
         Extract optimal assignments
   
   e. // Energy allocation
      For each match (c, p):
          Allocate E = min(c.demand, p.available_energy)
          Record transaction: A.add((c, p, E))
          p.available_energy -= E
          c.demand -= E
   
   f. // After energy delivery:
      For each provider p:
          rating = consumer_rate(p)
          p.reputation = update(p.reputation, rating)

3. Return allocation A with total cost and revenue

END ALGORITHM
```

---

## 5. Summary

| Component | Details |
|-----------|---------|
| **Selection Function** | MatchScore = (1/(1+|E_demand-E_supply|)) · Quality · Reputation |
| **Aggregation Functions** | Sequential sum, Parallel sum |
| **Revenue Model** | Revenue = P_market · E + Incentive |
| **Cost Model** | Cost = P_market · E_required + Premium |
| **Matching** | Greedy or Hungarian algorithm |
| **Pricing** | Dynamic: P_base · (1 + demand_factor·(D-S)/S) |
| **Novel Contribution** | Crowdsourced energy trading platform |
| **Exploration** | Provider discovery, dynamic pricing |
| **Exploitation** | High MatchScore selection, reputation-based |
| **Dataset** | Crowdsourced (100-500 providers), 20-100 consumers per cycle |
| **Workflow** | Platform Init → Trading Cycle → Continuous Optimization |

---

*This document provides detailed analysis of Paper 13's solution framework.*