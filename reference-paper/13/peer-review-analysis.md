# Peer Review Analysis: Crowdsourcing Energy as a Service

## Paper: Crowdsourcing Energy as a Service

---

## 1. Executive Summary

This paper proposes a novel framework for crowdsourcing energy services from IoT devices that introduce a new crowdsourced
energy as a service, where distributed energy resources are dynamically composed and delivered using wireless power transfer energy-related quality model considering spatiotemporal aspects evaluated based on the transmission success rate. The temporal composition algorithm leverages fractional knapsack optimization to select optimal combinations of energy services within user-specified time constraints. The approach is evaluated using Yelp check-in data augmented with synthetic QoS parameters.


---

## 2. Key Findings

### 2.1 Problem Context
- **Problem**: Energy scarcity for mobile IoT devices in public spaces
- **Solution Space**: Crowdsourcing energy from nearby wearable IoT devices
- **Challenge**: Spatiotemporal availability and wireless transfer efficiency
- **Significance**: Enables energy sharing without infrastructure dependency

### 2.2 Proposed Approach
- **Service Model**: Crowdsourced Energy as a Service (EaaS)
- **QoS Model**: Transmission success rate, deliverable energy capacity, temporal attributes
- **Composition**: Fractional knapsack-based temporal composition
- **Indexing**: 3D R-tree for spatiotemporal service discovery

### 2.3 Technical Contributions
1. **Service Model**: Formal definition of crowdsourced energy service with QoS attributes
2. **Quality Model**: Novel energy-specific QoS metrics (TSR, DEC)
3. **Temporal Composition**: Fractional knapsack algorithm for optimal service selection
4. **Spatiotemporal Indexing**: 3D R-tree for efficient service discovery

### 2.4 Evaluation Methodology
- **Dataset**: Yelp check-in data (coffee shops)
- **Synthetic Parameters**: DEC, intensity, TSR randomly generated
- **Comparison**: Temporal composition vs. greedy selection
- **Results**: Necessity of temporal composition for high-energy requirements

### 2.5 Related Work Categories
- **IoT Services**: Resource-constrained device services
- **Energy Transfer**: Wireless power transfer technologies
- **Service Composition**: QoS-aware composition
- **Crowdsourcing**: Crowd-based sensing and resource sharing

---

## 3. Research Gaps

### 3.1 Mobility Gaps
- **Moving Consumers**: Assumes consumer stays fixed after query launch
- **Moving Providers**: Assumes providers are fixed in space
- **Real Mobility**: No handling of dynamic provider/consumer movement
- **Location Prediction**: No trajectory-based service prediction

### 3.2 Scalability Gaps
- **Large-Scale**: Limited discussion of city-wide deployment
- **Concurrent Queries**: No mention of handling multiple simultaneous queries
- **Distributed Index**: Centralized 3D R-tree limitation
- **Real-Time Updates**: Static availability assumption

### 3.3 Wireless Transfer Gaps
- **Multi-Hop**: Single-hop transfer only
- **Interference**: No consideration of multiple simultaneous transfers
- **Directional Charging**: Single consumer assumption
- **Energy Efficiency**: No optimization for transfer efficiency vs. time trade-off

### 3.4 Temporal Modeling Gaps
- **Prediction**: No availability prediction for future time periods
- **Uncertainty**: Deterministic assumption contradicts real-world variability
- **Partial Information**: No handling of incomplete QoS information
- **Historical Data**: No learning from past service patterns

### 3.5 Composition Algorithm Gaps
- **Global Optimal**: Fractional knapsack is greedy, not globally optimal
- **NP-Hard**: Real composition may be NP-hard with multiple constraints
- **Constraint Types**: Only time and energy constraints considered
- **Re-composition**: No dynamic re-composition when services become unavailable

### 3.6 Evaluation Gaps
- **Synthetic Data**: Real QoS values not from actual wearable devices
- **No Real Hardware**: No wireless power transfer validation
- **Single Location**: Coffee shop scenario only
- **No User Studies**: Actual user behavior not studied
- **No Benchmark Comparison**: Only greedy baseline

### 3.7 Economic Gaps
- **Pricing Model**: No cost or pricing mechanism
- **Incentive Design**: No incentive for providers to share energy
- **Market Equilibrium**: No market-based dynamics
- **Fairness**: No fairness in energy allocation

### 3.8 Security Gaps
- **Privacy**: Location and energy usage privacy not addressed
- **Authentication**: No provider/consumer authentication
- **Energy Theft**: No fraud detection
- **DoS Attacks**: Vulnerable to malicious service providers

---

## 4. Peer Review Questions and Responses

### Q1: How does the framework handle provider mobility when services are offered by moving wearables?

**Response**: The paper explicitly assumes service providers are **fixed in space** and can transfer energy wirelessly inside a micro-region (e.g., coffeeshop). This is a significant limitation for real-world deployment where both providers and consumers may be mobile. The approach cannot handle moving providers, which limits applicability to static scenarios like waiting areas.

---

### Q2: What is the computational complexity of the 3D R-tree indexing for large-scale deployments?

**Response**: The paper does not discuss complexity analysis. While R-tree provides O(log n) typical query time, the 3D R-tree may suffer from:
- Increased node splits with time dimension
- Overlap in temporal dimension
- No discussion of update operations when services join/leave

---

### Q3: How does the fractional knapsack guarantee optimal composition compared to integer approaches?

**Response**: The fractional knapsack provides **locally optimal** solution per time slot via greedy selection, but is **not globally optimal**. The algorithm selects highest DEC service for each time slot independently, which may not yield the maximum total energy. The greedy approach is polynomial but sacrifices global optimality.

---

### Q4: How are the QoS parameters (TSR, DEC) actually measured or estimated in practice?

**Response**: The paper generates these **synthetically** with random values. No real measurement methodology is provided. TSR depends on:
- Transmission gain Gt (antenna characteristics)
- Distance D (dynamic based on consumer position)
- Path-loss coefficient θ (environment-dependent)

In practice, these would require real-time measurement or estimation, which is not addressed.

---

### Q5: What happens when a selected service becomes unavailable during the composition period?

**Response**: The paper assumes **deterministic availability** - services are available as scheduled. There is no:
- Re-composition mechanism
- Backup service selection
- Failure recovery

This is unrealistic for crowdsourced services where providers may leave or exhaust energy.

---

### Q6: How does the approach handle multiple consumers requesting energy simultaneously?

**Response**: The paper does not address **concurrent queries**. The algorithm assumes a single consumer query at a time. Real deployment would need:
- Resource allocation among multiple consumers
- Priority mechanisms
- Fairness guarantees
- Competition for limited energy services

---

### Q7: What incentive mechanisms encourage wearable owners to share their energy?

**Response**: **Not addressed**. The paper focuses purely on technical composition without any economic or incentive model. In practice, users need:
- Financial compensation
- Reputation systems
- Energy credits
- Gamification elements

---

### Q8: How does the framework ensure energy transfer safety for both provider and consumer?

**Response**: Not discussed. Wireless power transfer involves:
- Thermal effects on devices
- Electromagnetic exposure
- Device compatibility (3-5V assumption)
- Battery protection

No safety constraints or validation are included.

---

### Q9: What is the practical range of wireless energy transfer considered in the model?

**Response**: The TSR formula includes parameter **β (short distance energy transmission parameter)**, but no specific values are provided. The paper assumes "short range distance is required for successful wireless delivery" but does not quantify this. Practical wireless power transfer typically operates within 1-3 meters.

---

### Q10: How does the approach compare against existing wireless power transfer standards (Qi, etc.)?

**Response**: Not compared. The paper treats wireless power transfer abstractly without:
- Standard compliance
- Interoperability with existing protocols
- Hardware implementation constraints

---

### Q11: What are the energy overhead calculations for the wireless transfer itself?

**Response**: Not explicitly calculated. The DEC formula accounts for TSR losses, but:
- No energy consumed by the transfer process itself
- No power consumption of the wearable during transfer
- No battery degradation modeling

---

### Q12: How does the time slot division handle edge cases with many overlapping services?

**Response**: The algorithm creates time slots at every service start/end time. With **n services**, this creates **O(n) time slots**. However:
- No complexity analysis provided
- No handling of numerical precision issues
- No optimization for dense service periods

---

### Q13: What validation exists for the usage pattern parameter (α) values?

**Response**: Based on Carroll et al. [3] but:
- α = 1 (Suspend), 0.75 (Casual), 0.50 (Regular) are assumptions
- No empirical validation for wearable devices specifically
- No adaptation mechanism for individual users

---

### Q14: How does the framework handle heterogeneous device types with different voltages?

**Response**: Paper assumes **all devices operate between 3-5V** and are "compatible in term of voltage." This:
- Simplifies real-world heterogeneity
- Ignores different charging standards
- No negotiation or adaptation for mismatched devices

---

### Q15: What happens when the required energy cannot be fully satisfied?

**Response**: The paper states: "Crowdsourcer returns a set of available services which provides the **maximum available amount** of energy within the query duration." This is a **partial fulfillment** scenario with no user notification or alternative suggestions.

---

### Q16: How are false or malicious service announcements detected?

**Response**: Not addressed. The framework trusts:
- Announced energy capacity (EC)
- Announced end time (aet)
- QoS parameters

No verification or reputation system exists.

---

### Q17: What is the expected latency from query to energy delivery initiation?

**Response**: Not measured or discussed. The composition algorithm has computational overhead that would add latency, critical for urgent charging needs.

---

### Q18: How does the framework handle service discovery in areas with no nearby energy services?

**Response**: Implicitly returns empty set. No:
- Service discovery expansion
- Provider recruitment
- Alternative recommendations

---

### Q19: What happens when a provider's actual end time differs from announced?

**Response**: The formula **et = st + α(EC - Thr)/I** recalculates real end time. If calculated et < announced aet, use estimated. Otherwise, use announced. This provides some flexibility but assumes predictable consumption.

---

### Q20: How does the evaluation scale to realistic IoT deployments with thousands of services?

**Response**: No scalability analysis. Yelp dataset provides check-in data but:
- Limited to coffee shop locations
- No actual IoT device simulation
- No performance metrics (time, memory)

---

### Q21: What are the assumptions about energy measurement accuracy?

**Response**: Assumes precise measurement of:
- Current intensity I
- Energy capacity EC
- Battery threshold Thr

In practice, IoT devices have limited battery sensing accuracy.

---

### Q22: How does the approach handle different energy unit preferences (Wh, mAh, etc.)?

**Response**: Uses **mAh** (milliAmpere hour) for DEC. No conversion or normalization discussed. Different devices may report energy in different units.

---

### Q23: What is the theoretical basis for the fractional knapsack application?

**Response**: Based on classic fractional knapsack [6] but adapted:
- Time slots as "capacity"
- DEC as "value"
- Service fractions as "items"

Theoretical justification for this mapping not thoroughly explored.

---

### Q24: How are partial services from the same provider handled differently?

**Response**: Treats each mini-service independently. No:
- Provider grouping
- Multi-service coordination
- Priority for single-provider solutions

---

### Q25: What parameters are needed to replicate the experiments?

**Response**: Insufficient replication details:
- Specific Yelp dataset version
- Random seed for synthetic parameters
- Exact scenario configurations
- Implementation details

---

### Q26: How does the approach compare to cloud/edge charging alternatives?

**Response**: Not compared. The approach is evaluated in isolation against greedy selection only. No comparison to:
- Traditional charging stations
- Mobile charging services
- Battery swap options

---

### Q27: What is the energy overhead of the composition algorithm itself?

**Response**: Not calculated. The computational energy cost of running the algorithm is ignored, which may be significant for resource-constrained devices.

---

### Q28: How do user preferences for service selection get incorporated beyond energy amount?

**Response**: Mentioned but not implemented: "According to a consumer's preferences (shortest duration, earliest start, or maximum energy)." No implementation details or evaluation.

---

### Q29: What happens when the wireless transfer is interrupted mid-session?

**Response**: Not addressed. No:
- Interruption detection
- Service re-selection
- Partial energy credit

---

### Q30: How does the framework support different query durations (short vs. long)?

**Response**: The evaluation defines scenarios for short/long durations (Tables 1-4), showing different composition strategies. However, no adaptive algorithm for duration types.

---

## 5. Strengths

1. **Novel Problem**: First work to formulate crowdsourced energy as a service composition problem
2. **Mathematical Rigor**: Well-defined QoS model with concrete formulas
3. **Algorithmic Innovation**: Fractional knapsack adaptation for temporal composition
4. **Spatiotemporal Indexing**: 3D R-tree provides efficient discovery framework
5. **Practical Scenario**: Coffee shop use case is realistic and relatable

---

## 6. Weaknesses

1. **Static Assumption**: Providers and consumers assumed fixed in space
2. **No Mobility Handling**: Cannot handle real-world movement
3. **Single Query**: No concurrent query handling
4. **Synthetic Evaluation**: No real hardware validation
5. **No Incentive**: Economic aspects completely ignored
6. **Limited Baselines**: Only greedy comparison
7. **No Re-composition**: No dynamic adaptation to failures

---

## 7. Overall Assessment

| Criterion | Rating | Comments |
|-----------|--------|----------|
| **Novelty** | High | First to frame energy as crowdsourced service |
| **Technical Quality** | Medium | Solid algorithm but limited validation |
| **Evaluation** | Low | Synthetic data, single baseline |
| **Practicality** | Low | Static assumptions limit real deployment |
| **Completeness** | Medium | Missing mobility, economics, security |

**Recommendation**: The paper provides a valuable conceptual framework and algorithmic foundation for crowdsourced energy services. However, significant extensions are needed for practical deployment, particularly in handling mobility, concurrent users, and real-world validation. The work serves as a strong starting point for the research direction but requires substantial follow-up for real-world impact.