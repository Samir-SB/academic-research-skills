# Peer Review Analysis: Paper 15 - Proactive Composition of Mobile IoT Energy Services

## 1. Executive Summary

This paper (Lakhdari & Bouguettaya, arXiv 2021) extends the previous work on crowdsourced energy services by proposing a proactive composition framework that leverages mobility patterns and energy usage behavior to automatically generate energy services and requests ahead of time. The key contribution is a framework that anticipates energy requirements and plans when, where, and how much energy to request based on user's daily routine.

**Paper Details:**
- Title: Proactive Composition of Mobile IoT Energy Services
- Authors: Abdallah Lakhdari, Athman Bouguettaya
- Venue: arXiv preprint (arXiv:2107.12519)
- Date: July 2021

---

## 2. Problem Context

### 2.1 Problem Definition
In dynamic crowdsourced IoT energy environments, energy supply and demand are often mismatched in both space and time. The paper proposes proactively defining when, where, and how much energy to request based on user's mobility patterns and energy usage behavior.

### 2.2 Key Insight
Human mobility is highly predictable due to daily routine regularity. By leveraging this predictability, energy requests can be generated proactively rather than reactively when battery reaches threshold.

### 2.3 Key Assumptions
1. Consumer stays within one microcell after launching request
2. Mobility patterns follow daily routine regularity
3. Energy usage behavior exhibits regularity correlated with daily activities
4. Users have flexible and non-flexible activities in their routine

---

## 3. Methodology

### 3.1 Proactive Energy Service Model
```
PES = <S, P, F, Q, M, U>
where:
- S: service ID
- P: provider ID
- Q: QoS tuple <l, r, st, et, DEC, I, Tsr, Reli>
- M: mobility patterns of provider
- U: energy usage behavior of provider
```

### 3.2 Proactive Energy Request Model
```
Rq = <t, l, RE, CI, du>
where:
- t: timestamp when request launched
- l: consumer location (assumed stationary within microcell)
- RE: required energy amount
- CI: maximum intensity
- du: charging period
```

### 3.3 Mobility Patterns
- Represented as probabilistic time series
- Mi(ti, loci, θi): likelihood of user i being at location loci at time ti
- Derived from historical records using statistical methods

### 3.4 Energy Usage Behavior
- Ui(ti, SoCi): battery state of charge temporal sequence
- Used to predict future energy requirements

### 3.5 Consumer Flexibility Model
```
Fxi = <Ai, Chi, Sri>
- Ai: availability distribution for visited microcells
- Chi: binary - whether microcell can be changed
- Sri: binary - whether stay time is flexible
```

### 3.6 Proactive Composition Algorithm
1. Define mobility plan for each provider
2. Generate proactive services based on provider's daily routine
3. Create mobility graph (nodes = microcells, edges = movement)
4. Estimate energy availability at each microcell
5. Define proactive requests based on consumer's energy needs
6. Consumer selects microcells to visit based on energy availability
7. Perform spatio-temporal composition for each request

### 3.7 Evaluation
- **Datasets**: Yelp (spatio-temporal) + QLD Smartgrid (energy)
- **Comparison**: Proactive vs Spatio-temporal vs Brute-force composition
- **Metrics**: Successful request ratio, received energy amount

---

## 4. Key Findings

### 4.1 Strengths
1. **Proactive approach**: Anticipates energy needs before they arise
2. **Mobility prediction**: Leverages predictable human mobility patterns
3. **Flexibility modeling**: Distinguishes flexible vs non-flexible activities
4. **Supply-demand balancing**: Adjusts requests based on energy availability
5. **Multi-microcell planning**: Plans energy requests across multiple locations

### 4.2 Weaknesses
1. **Predefined routine**: Assumes users follow consistent daily routine
2. **Microcell scope**: Still limited to confined areas
3. **No real prediction**: Uses historical patterns, not ML-based prediction
4. **Consumer stationary**: Assumes consumer stays within microcell after request
5. **No handover**: Does not address service migration during consumption

---

## 5. Research Gaps

### 5.1 Mobility Gaps (Relevant to Thesis)
- **Microcell limitation**: Still confined to small indoor areas
- **Routine assumption**: Requires consistent daily patterns
- **No trajectory prediction**: Uses statistical patterns, not predictive models
- **Consumer mobility**: Assumes stationary consumer

### 5.2 Algorithm Gaps
- **Graph-based planning**: Mobility graph is simplistic
- **No RL approach**: Still heuristic-based, not learned
- **Static patterns**: Cannot adapt to changing routines

### 5.3 Scope Gaps
- **Energy services only**: Focuses on energy, not general IoT services
- **Single provider per device**: Assumes one device per provider
- **No real-time adaptation**: Cannot adjust plan mid-execution

---

## 6. Comparison with Thesis Focus

| Aspect | Paper 15 | Your Thesis |
|--------|----------|-------------|
| **Moving services** | ⚠️ Microcell mobility | ✅ Large-scale trajectory |
| **Prediction** | Historical patterns | ✅ Trajectory prediction |
| **Proactive** | ✅ Yes | ✅ Yes (A2C-based) |
| **Handover** | ❌ Not addressed | ✅ Service migration |
| **RL approach** | ❌ Heuristic-based | ✅ A2C learning |

**Relevance to Thesis**: Medium-High - The proactive concept is aligned with your thesis, but the scope (microcells, energy services, heuristic-based) differs significantly. The mobility pattern modeling provides inspiration but lacks predictive ML components.

---

## 7. Evolution Across Papers 13-15

| Aspect | Paper 13 | Paper 14 | Paper 15 |
|--------|----------|----------|----------|
| **Year** | 2018 | 2020 | 2021 |
| **Service type** | Static | Intermittent | Proactive |
| **Mobility** | Fixed | Micro-mobility | Routine-based prediction |
| **Algorithm** | Fractional knapsack | 0/1 knapsack + heuristic | Graph-based planning |
| **Key innovation** | Temporal composition | Substitution mechanism | Proactive requests |
| **Scope** | Confined area | Confined area | Confined area |

---

## 8. Summary Table

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Novelty | High | Proactive composition concept |
| Technical Quality | Medium | Graph-based, lacks formal analysis |
| Evaluation | Medium | Synthetic data, promising results |
| Practicality | Medium | Routine assumption limits applicability |
| Relevance to Thesis | Medium-High | Proactive concept aligns with thesis |

**Recommendation**: The proactive composition concept is relevant to your thesis. However, the paper lacks trajectory prediction using ML/RL, and the microcell scope differs from your open geographic area focus. Useful as background on proactive service/request modeling.