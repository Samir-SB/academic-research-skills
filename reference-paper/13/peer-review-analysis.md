# Peer Review Analysis: Paper 13 - Crowdsourcing Energy as a Service

## 1. Executive Summary

This paper (Lakhdari et al., ICSOC 2018) proposes a novel framework for crowdsourcing energy services from IoT devices (wearables) via wireless power transfer. The key contributions include a formal Crowdsourced Energy as a Service (EaaS) model, QoS attributes (Transmission Success Rate TSR, Deliverable Energy Capacity DEC), a temporal composition algorithm based on fractional knapsack, and 3D R-tree spatiotemporal indexing. The approach is evaluated using Yelp check-in data augmented with synthetic QoS parameters.

**Paper Details:**
- Title: Crowdsourcing Energy as a Service
- Authors: Abdallah Lakhdari, Athman Bouguettaya, Azadeh Ghari Neiat
- Venue: ICSOC 2018 (International Conference on Service Oriented Computing)
- DOI: https://doi.org/10.1007/978-3-030-03596-9_24

---

## 2. Problem Context

### 2.1 Problem Definition
The paper addresses energy scarcity for mobile IoT devices in public spaces. Users with depleted batteries can crowdsource energy from nearby wearable IoT devices through wireless power transfer.

### 2.2 Key Assumptions
1. Service providers (wearables) are fixed in space within a micro-region (e.g., coffeeshop)
2. Consumers stay fixed after launching a query
3. Deterministic service availability and QoS values are known a priori
4. All devices operate at 3-5V and are voltage-compatible

---

## 3. Methodology

### 3.1 Service Model
```
ES = <Eid, Eownerid, F, Q>
where Q = <Intensity, TSR, DEC, Location, StartTime, EndTime>
```

### 3.2 QoS Attributes
- **Intensity**: Current transferred (assumed constant)
- **TSR (Transmission Success Rate)**: Ratio of received to transmitted energy
  - Formula: TSR = (Gt × γ × λ^θ) / (Lp × 4π(D + β)^θ)
- **DEC (Deliverable Energy Capacity)**: DEC = α(EC - Thr) × TSR
  - α = usage pattern (1=Suspend, 0.75=Casual, 0.50=Regular)
- **End time**: et = st + α(EC - Thr)/I

### 3.3 Composition Algorithm
- **Indexing**: 3D R-tree for spatiotemporal service discovery
- **Selection**: Filter by location (within range r) and time (within query duration)
- **Composition**: Fractional knapsack - divide query duration into time slots, select highest DEC mini-service per slot
- **Output**: Ordered set of energy services/components

### 3.4 Evaluation
- Dataset: Yelp check-in data (coffee shops)
- Synthetic QoS: DEC, intensity, TSR randomly generated
- Scenarios: 16 scenarios (short/long duration × low/high energy × short/long services)
- Baseline: Greedy selection (max DEC)

---

## 4. Key Findings

### 4.1 Strengths
1. **Novel problem formulation**: First to frame crowdsourced energy as a service composition problem
2. **Rigorous mathematical model**: Well-defined QoS formulas with physical basis
3. **Algorithmic innovation**: Fractional knapsack adaptation for temporal composition
4. **Efficient indexing**: 3D R-tree provides spatiotemporal discovery framework
5. **Practical scenario**: Coffee shop use case is realistic

### 4.2 Weaknesses
1. **Static assumption**: Providers and consumers assumed fixed in space - no mobility handling
2. **Single query**: No concurrent query handling
3. **Synthetic evaluation**: No real hardware validation for wireless power transfer
4. **No incentives**: Economic aspects completely ignored
5. **Limited baselines**: Only greedy comparison
6. **No re-composition**: No dynamic adaptation when services become unavailable

---

## 5. Research Gaps

### 5.1 Mobility Gaps (Critical for Thesis)
- Moving consumers: Assumes consumer stays fixed after query launch
- Moving providers: Assumes providers are fixed in space
- No trajectory-based service prediction
- Cannot handle real-world movement

### 5.2 Scalability Gaps
- Limited discussion of city-wide deployment
- No concurrent query handling
- Centralized 3D R-tree limitation
- Static availability assumption

### 5.3 Algorithm Gaps
- Fractional knapsack is greedy, not globally optimal
- No re-composition mechanism for failures
- Only time and energy constraints considered

### 5.4 Validation Gaps
- Synthetic QoS parameters (not measured)
- No real wireless power transfer validation
- Single location (coffee shops)
- No benchmark comparisons beyond greedy

---

## 6. Comparison with Thesis Focus

| Aspect | Paper 13 | Your Thesis |
|--------|----------|-------------|
| **Moving services** | ❌ Fixed providers | ✅ Moving IoT services |
| **Mobility handling** | ❌ Not addressed | ✅ Proactive composition |
| **Handover** | ❌ Not addressed | ✅ Service migration |
| **RL approach** | ❌ Fractional knapsack | ✅ A2C-based |
| **Prediction** | ❌ Deterministic | ✅ Trajectory prediction |

**Relevance to Thesis**: Low - This paper assumes static services. However, it provides background on service composition methods and QoS modeling for energy services.

---

## 7. Questions for Further Investigation

1. How would the composition algorithm handle providers that move during the query duration?
2. What is the computational complexity of the 3D R-tree for large-scale deployments?
3. How do the TSR parameters (Gt, γ, λ, β, θ) map to real hardware?
4. What happens when a selected service becomes unavailable mid-composition?

---

## 8. Summary Table

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Novelty | High | First to frame energy as crowdsourced service |
| Technical Quality | Medium | Solid algorithm but limited validation |
| Evaluation | Low | Synthetic data, single baseline |
| Practicality | Low | Static assumptions limit real deployment |
| Relevance to Thesis | Low | Fixed services, no mobility |

**Recommendation**: Useful as background on service composition methods, but does not directly address moving IoT services or handover mechanisms needed for your thesis.