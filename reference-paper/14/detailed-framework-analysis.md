# Paper 14: Detailed Solution Framework Analysis

## Paper Information
- **Title**: Fluid Composition of Intermittent IoT Energy Services
- **Year**: 2022
- **Algorithm**: Fluid Composition Algorithm with Real-Time Adaptation

---

## 1. Functions Used for Selection and Aggregation

### 1.1 Intermittent Energy Availability Model

The paper models energy availability from intermittent sources as a time-varying function:

$$A_i(t) = \bar{A}_i \cdot f_{intermittent}(t; \theta_i)$$

Where:
- $A_i(t)$ = available energy from service $i$ at time $t$
- $\bar{A}_i$ = average energy capacity of service $i$
- $f_{intermittent}$ = intermittent pattern function (solar/wind profiles)
- $\theta_i$ = parameters defining variability characteristics

#### Solar Energy Pattern
$$f_{solar}(t) = \sin\left(\frac{\pi(t - t_{sunrise})}{t_{daylight}}\right) \cdot (1 - \alpha \cdot C_{cloud})$$

Where:
- $t_{sunrise}$ = sunrise time
- $t_{daylight}$ = daylight duration
- $C_{cloud}$ = cloud cover factor (0-1)
- $\alpha$ = cloud impact coefficient

#### Wind Energy Pattern
$$f_{wind}(t) = \beta_0 + \beta_1 \sin(\omega t) + \gamma \cdot W_{gust}(t)$$

Where:
- $\beta_0, \beta_1$ = baseline and oscillation coefficients
- $\omega$ = wind pattern frequency
- $W_{gust}(t)$ = stochastic gust component

### 1.2 Energy Aggregation Function

For combining multiple energy services in a composition:

$$E_{total}(t) = \sum_{i=1}^{n} A_i(t) \cdot x_i$$

Subject to:
$$\sum_{i=1}^{n} x_i = k$$
$$x_i \in \{0, 1\}$$

Where:
- $E_{total}(t)$ = total aggregated energy at time $t$
- $x_i$ = binary decision variable (1 if service $i$ selected)
- $k$ = number of services in composition

### 1.3 Reliability Function

The reliability of composition given intermittent services:

$$R(S, t) = P\left(E_{total}(t) \geq E_{required}(t)\right)$$

Where:
- $R(S, t)$ = reliability of composition $S$ at time $t$
- $E_{required}(t)$ = energy required by IoT application
- Probability computed from historical availability patterns

### 1.4 Selection Function (Fluid Composition)

The fluid composition algorithm selects services based on:

$$Score(S) = w_1 \cdot E_{avg} + w_2 \cdot R_{avg} - w_3 \cdot C_{switch}$$

Where:
- $E_{avg}$ = average energy provision
- $R_{avg}$ = average reliability
- $C_{switch}$ = expected service switching cost
- $w_1, w_2, w_3$ = weights (∑w = 1)

### 1.5 Adaptation Trigger Function

Re-composition is triggered when:

$$\Delta E(t) = \left|E_{total}(t) - E_{required}(t)\right| > \tau$$

Or when:
$$R(S, t) < R_{threshold}$$

Where:
- $\tau$ = energy deviation threshold
- $R_{threshold}$ = minimum acceptable reliability

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Fluid Composition Algorithm

The fluid composition approach uses a dynamic service pool rather than fixed compositions:

#### Initialization Phase
1. Register available energy services
2. Build availability profile database
3. Initialize service pool

#### Composition Phase (Exploitation)
1. Rank services by reliability and capacity
2. Select top-k services that meet energy requirements
3. Compute composite availability distribution

#### Adaptation Phase (Exploration)
When triggered, explore alternative compositions:
1. Evaluate service replacements
2. Test backup service combinations
3. Select best adapted composition

### 2.2 Real-Time Adaptation Mechanism

The adaptation algorithm handles intermittent fluctuations:

#### Monitoring Loop
```
while application running:
    measure current energy availability
    compute expected energy for horizon (t, t+Δ)
    if deviation > threshold OR reliability < min:
        trigger re-composition
    wait adaptive_interval
```

#### Re-Composition Algorithm
```
recompose(current_composition, available_services):
    candidates = generate_replacements(current_composition)
    for each candidate:
        compute reliability = simulate(candidate)
        compute energy = aggregate(candidate)
    select best candidate by Score()
    return new composition
```

### 2.3 Exploration vs Exploitation Balance

| Mechanism | Type | Description |
|-----------|------|-------------|
| Initial composition | Exploitation | Select highest reliability services |
| Deviation threshold | Exploration | Allow flexible adaptation trigger |
| Backup pool | Exploration | Maintain alternative services |
| Gradual transition | Exploitation | Smooth service switching |

### 2.4 Service Pool Management

The fluid approach maintains a dynamic pool:

```
maintain_pool(available_services):
    active = services meeting reliability threshold
    backup = services below threshold but improving
    removed = services with prolonged low availability
    
    for service in backup:
        if availability recovers:
            move to active
    
    for service in active:
        if availability drops:
            move to backup (or remove if prolonged)
    
    return active + backup
```

---

## 3. Dataset Used

### 3.1 Synthetic IoT Energy Service Data

The evaluation uses synthetic datasets representing:

#### Service Profiles
- **Solar Services**: 50 services with varying capacity (1-10 kWh)
- **Wind Services**: 30 services with capacity (2-8 kWh)
- **Hybrid Services**: 20 services combining solar+wind

#### Intermittency Parameters
| Service Type | Variability | Peak Hours | Recovery Time |
|--------------|-------------|------------|---------------|
| Solar | High | 10am-4pm | 1-2 hours |
| Wind | Medium-High | Variable | 15-30 min |
| Hybrid | Low-Medium | Composite | Variable |

#### Environmental Patterns
- Cloud cover: 0-80% (seasonal variation)
- Wind speed: 2-15 m/s
- Temperature: -10°C to 40°C

### 3.2 Workload Patterns

#### Energy Demand Profiles
- Continuous: 24/7 operation
- Periodic: Daily cycles
- Burst: Event-driven peaks

#### Scale Configurations
- Small: 10 services, 5 kWh demand
- Medium: 50 services, 20 kWh demand
- Large: 100 services, 50 kWh demand

### 3.3 Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Service Availability | % time energy requirement met | >95% |
| Energy Utilization | % of available energy used | >80% |
| Adaptation Frequency | Re-composition events per hour | <2 |
| Transition Latency | Time to switch services | <30s |

---

## 4. Complete Workflow

### 4.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Fluid Composition Engine              │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Availability│  │   Composition│  │    Adaptation│  │
│  │   Monitor    │  │    Planner   │  │   Controller │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│              Energy Service Pool (Dynamic)               │
├─────────────────────────────────────────────────────────┤
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │
│  │Solar 1 │ │Solar 2 │ │Wind 1  │ │Wind 2  │ ...       │
│  └────────┘ └────────┘ └────────┘ └────────┘           │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Workflow Flowchart

```
START
  │
  ▼
┌─────────────────────┐
│ Initialize Services │
│   & Build Pool      │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Monitor Energy      │
│  Availability       │
└─────────────────────┘
  │
  ▼
         ┌─────────────────────┐
         │ Deviation > Threshold│
         │ OR Reliability < Min │
         └──────────┬────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
      YES                        NO
        │                        │
        ▼                        ▼
┌───────────────────┐    ┌─────────────────────┐
│ Trigger Re-      │    │   Continue          │
│ Composition       │    │   Monitoring        │
└───────────────────┘    └─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Generate Candidate  │
│ Compositions        │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Evaluate Candidates │
│ (Reliability, Energy)│
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Select Best         │
│ Composition         │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Execute Service     │
│ Switch              │
└─────────────────────┘
        │
        ▼
    Continue
```

### 4.3 Complete Pseudocode

```python
class FluidCompositionEngine:
    def __init__(self, config):
        self.pool = ServicePool()
        self.threshold = config.energy_threshold
        self.reliability_min = config.min_reliability
        self.monitoring_interval = config.interval
        
    def initialize(self, services):
        """Initialize service pool"""
        for service in services:
            self.pool.add(service)
            service.availability_profile = self.compute_profile(service)
            
    def run(self, energy_requirement):
        """Main composition loop"""
        current_composition = self.initial_compose(energy_requirement)
        
        while True:
            availability = self.pool.measure_current()
            expected = self.predict_energy(availability, horizon)
            
            deviation = abs(expected - energy_requirement)
            
            if deviation > self.threshold:
                current_composition = self.recompose(
                    current_composition, 
                    energy_requirement
                )
            
            time.sleep(self.monitoring_interval)
            
    def initial_compose(self, requirement):
        """Create initial composition (Exploitation)"""
        candidates = self.pool.get_reliable_services()
        scored = [(s, self.score_service(s, requirement)) 
                  for s in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        
        selected = []
        total_energy = 0
        for service, score in scored:
            if total_energy >= requirement:
                break
            selected.append(service)
            total_energy += service.capacity
            
        return selected
    
    def recompose(self, current, requirement):
        """Adapt to changes (Exploration)"""
        candidates = self.pool.get_available_services()
        
        best_composition = current
        best_score = self.evaluate_composition(current, requirement)
        
        for size in range(1, len(candidates)+1):
            for combo in combinations(candidates, size):
                score = self.evaluate_composition(combo, requirement)
                if score > best_score:
                    best_composition = combo
                    best_score = score
                    
        return best_composition
    
    def evaluate_composition(self, composition, requirement):
        """Compute composition fitness"""
        energy = sum(s.current_capacity for s in composition)
        reliability = self.compute_reliability(composition)
        
        w1, w2 = 0.6, 0.4  # weights
        score = w1 * (energy / requirement) + w2 * reliability
        
        return score
    
    def compute_reliability(self, composition):
        """Calculate reliability probability"""
        samples = 1000
        successes = 0
        
        for _ in range(samples):
            total = sum(s.sample_availability() for s in composition)
            if total >= self.requirement:
                successes += 1
                
        return successes / samples
```

### 4.4 Key Innovation: Fluid Pool Management

The key difference from static composition:

| Aspect | Static | Fluid |
|--------|--------|-------|
| Service Set | Fixed at composition time | Dynamic pool |
| Adaptation | Re-composition from scratch | Pool-based replacement |
| Recovery | Full re-optimization | Activate backup services |
| Efficiency | Lower under variability | Higher with pool flexibility |

### 4.5 Adaptation Threshold Tuning

The system adapts threshold based on:

```
if adaptation_frequency > HIGH:
    increase threshold (reduce sensitivity)
elif adaptation_frequency < LOW:
    decrease threshold (increase sensitivity)
else:
    maintain current threshold
```

This self-tuning balances responsiveness vs. stability.

---

## 5. Summary

### Key Framework Components

| Component | Function | Innovation |
|-----------|----------|------------|
| Energy Model | Time-varying availability | Intermittency patterns |
| Selection | Fluid pool-based | Dynamic service activation |
| Aggregation | Energy summing | Probabilistic reliability |
| Adaptation | Event-triggered | Threshold-based re-composition |

### Algorithm Characteristics

- **Exploration**: Backup pool maintenance, candidate exploration during re-composition
- **Exploitation**: Initial composition from highest-reliability services
- **Balance**: Self-tuning threshold adapts to environment variability

### Dataset Characteristics

- **Type**: Synthetic intermittent energy patterns
- **Scale**: 10-100 services
- **Patterns**: Solar, wind, hybrid with realistic variability

---

*Analysis Date: April 2026*
*Paper Type: Original Research*