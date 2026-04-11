# Peer Review Analysis: Paper 16 - Elastic Composition of Crowdsourced IoT Energy Services

## 1. Executive Summary

This paper (Lakhdari et al., arXiv 2020) introduces the concept of elastic composition for crowdsourced IoT energy services that handles service fluctuation and consumer flexibility. The key contribution is a multi-objective optimization framework that considers both reliability and time extension to select optimal service compositions.

**Paper Details:**
- Title: Elastic Composition of Crowdsourced IoT Energy Services
- Authors: Abdallah Lakhdari, Athman Bouguettaya, Sajib Mistry, Azadeh Ghari Neiat, Basem Suleiman
- Venue: arXiv preprint (arXiv:2011.06771)
- Date: November 2020

---

## 2. Problem Context

### 2.1 Problem Definition
In crowdsourced IoT energy environments, services may fluctuate (fail due to device usage) and consumers have flexible charging time preferences. The paper proposes elastic composition that can extend query duration beyond initial deadline when services fail.

### 2.2 Key Concepts
1. **Soft deadline (Dls)**: Initial query duration
2. **Hard deadline (Dlh)**: Maximum waiting time for consumer
3. **Fluctuation**: Services may fail due to excessive device usage by owners
4. **Elasticity**: Composition can extend beyond soft deadline up to hard deadline

### 2.3 Key Assumptions
1. Consumer location is fixed after launching query
2. Services are on-demand, can be decomposed and consumed partially
3. Energy usage patterns exhibit regularity
4. Reliability can be estimated from usage behavior and provision history

---

## 3. Methodology

### 3.1 Service Model
```
CES = <Eid, Eownerid, F, Q>
where Q = <l, St, Et, DEC, I, Tsr, Reli>
```

### 3.2 Reliability Model
- **Energy Usage Behavior (EUBi)**: Parameter (0-1) based on device usage patterns
  - Suspend: α=1 (not using device)
  - Casual: α=0.75 (light usage)
  - Regular: α=0.50 (predictable usage)
- **Provision History (PBi)**: Ratio of successful provisions to total
- **Reliability**: Reli = EUBi × PBi

### 3.3 Elastic Composition Framework
1. **Temporal chunking**: Divide query duration at service start/end times
2. **Reliability assessment**: Calculate aggregate reliability for compositions
3. **Time extension estimation**: Estimate additional time needed if services fail
4. **Pareto front optimization**: Find optimal trade-offs between reliability and extension
5. **Utility function**: u(Compi) = we × TEC(Compi) + wr × Rel(Compi)

### 3.4 Key Formulas
- **Total Energy Capacity**: TEC(Compj) = Σ DEC(psi)
- **Aggregate Reliability**: AgR(Compj) = (1/m) × Σ (DEC(psi)/TEC × du(psi)/du) × Rel(psi)
- **Time Extension**: ExtQ(Compj) = RemRE(Compj) / (E(I) × E(Tsr))

### 3.5 Evaluation
- **Datasets**: Yelp (spatio-temporal) + QLD Smartgrid (energy) + Carat (reliability/entropy)
- **Comparison**: Brute-force, Heuristic, Temporal knapsack, Greedy
- **Metrics**: CPU time, Pareto front cardinality, Extension estimation error

---

## 4. Key Findings

### 4.1 Strengths
1. **Novel concept**: First to propose elastic composition with soft/hard deadlines
2. **Reliability modeling**: Integrates usage behavior and provision history
3. **Multi-objective optimization**: Pareto front approach for reliability vs. time trade-off
4. **User preferences**: Supports risk-taker, risk-averse, and risk-neutral strategies
5. **Heuristic efficiency**: Significantly reduces search space while maintaining quality

### 4.2 Weaknesses
1. **No mobility handling**: Still confined to microcells, providers assumed stationary
2. **No trajectory prediction**: Uses historical patterns, not ML-based prediction
3. **Post-hoc handling**: Extends time after failure, not proactive service migration
4. **Consumer stationary**: Assumes consumer stays within microcell after query launch

---

## 5. Research Gaps

### 5.1 Mobility Gaps (Relevant to Thesis)
- **Microcell scope**: Limited to confined areas
- **No provider mobility**: Assumes stationary providers during service provision
- **No handover**: Cannot proactively migrate services when provider leaves
- **Consumer mobility**: Assumes fixed location after query launch

### 5.2 Algorithm Gaps
- **Heuristic optimality**: No guarantee of global optimal solution
- **Failure handling**: Reactive (extends time) rather than proactive (preemptive migration)
- **No RL**: Still heuristic-based, not learned from experience

### 5.3 Scope Gaps
- **Energy services only**: Does not generalize to other IoT service types
- **Single reception mode**: Assumes one provider at a time
- **Limited prediction**: Uses historical reliability, not predictive models

---

## 6. Comparison with Thesis Focus

| Aspect | Paper 16 | Your Thesis |
|--------|----------|-------------|
| **Moving services** | ❌ Microcell only | ✅ Large-scale trajectory |
| **Prediction** | Historical reliability | ✅ Trajectory prediction |
| **Failure handling** | Time extension (reactive) | ✅ Proactive handover |
| **RL approach** | ❌ Heuristic-based | ✅ A2C learning |
| **Scope** | Confined area (energy) | Open area (general IoT) |

**Relevance to Thesis**: Low - The reliability modeling is interesting, but the approach is reactive (extending time after failure) rather than proactive (service migration). The microcell scope differs significantly from your thesis.

---

## 7. Evolution Across Papers 13-16

| Aspect | Paper 13 | Paper 14 | Paper 15 | Paper 16 |
|--------|----------|----------|----------|----------|
| **Year** | 2018 | 2020 | 2021 | 2020 |
| **Key innovation** | Temporal composition | Fluid/intermittent | Proactive requests | Elastic/deadlines |
| **Mobility** | Fixed | Micro-mobility | Routine-based | Fluctuation handling |
| **Failure** | No handling | Substitution | Pre-planning | Time extension |
| **RL** | No | No | No | No |
| **Scope** | Confined | Confined | Confined | Confined |

---

## 8. Summary Table

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Novelty | High | Elastic composition concept |
| Technical Quality | Medium | Solid heuristics, multi-objective optimization |
| Evaluation | Medium | Real datasets, comprehensive experiments |
| Practicality | Medium | Confined area, no real hardware |
| Relevance to Thesis | Low | Reactive failure handling, microcell scope |

**Recommendation**: The reliability modeling and multi-objective optimization approach are methodologically interesting. However, the paper does not address moving services or proactive handover mechanisms needed for your thesis. Useful as background on reliability estimation but not directly applicable.