# Paper 16: Detailed Solution Framework Analysis

## Paper Information
- **Title**: Elastic Composition of Crowdsourced IoT Energy Services
- **Year**: 2022
- **Algorithm**: Genetic Algorithm + Elastic Adaptation

---

## 1. Functions Used for Selection and Aggregation

### 1.1 Prosumer Availability Model

The paper models crowdsourced energy prosumers with variable availability:

$$A_p(t) = A_{base}(p) \cdot S_{status}(t) \cdot R_{reliability}(p)$$

Where:
- $A_p(t)$ = effective availability of prosumer $p$ at time $t$
- $A_{base}(p)$ = base capacity of prosumer $p$
- $S_{status}(t)$ = current status factor (0-1, based on activity)
- $R_{reliability}(p)$ = reliability rating of prosumer $p$

### 1.2 Elastic Pool Aggregation

The core innovation is treating energy services as a dynamic pool:

$$E_{pool}(t) = \sum_{p \in P_{active}} A_p(t) + \sum_{p \in P_{backup}} \beta \cdot A_p(t)$$

Where:
- $P_{active}$ = currently active prosumers in composition
- $P_{backup}$ = backup prosumer pool
- $\beta$ = backup activation threshold (0 < β < 1)
- $E_{pool}(t)$ = total elastic pool capacity at time $t$

### 1.3 Elastic Capacity Function

The elastic capacity measures composition flexibility:

$$C_{elastic}(P) = \frac{|P_{active}| + \alpha \cdot |P_{backup}|}{|P_{required}|}$$

Where:
- $\alpha$ = backup contribution factor (typically 0.5)
- $|P_{required}|$ = number of prosumers needed to meet demand
- $C_{elastic}$ = elasticity ratio (>1 indicates flexibility)

### 1.4 Selection Function (GA-based)

The genetic algorithm optimizes composition selection:

$$\text{Fitness}(S) = w_1 \cdot E_{total} + w_2 \cdot R_{composition} - w_3 \cdot C_{switch}$$

Subject to:
$$E_{total} \geq E_{required}$$
$$R_{composition} \geq R_{min}$$

Where:
- $E_{total}$ = total energy from selected prosumers
- $R_{composition}$ = composite reliability
- $C_{switch}$ = expected switching cost
- $w_1, w_2, w_3$ = weights

### 1.5 Prosumer Ranking Function

Prosumers are ranked by composite score:

$$Rank(p) = \gamma_1 \cdot A_p + \gamma_2 \cdot R_{reliability}(p) + \gamma_3 \cdot H_{history}(p)$$

Where:
- $A_p$ = availability score
- $R_{reliability}(p)$ = reliability score
- $H_{history}(p)$ = historical contribution score
- $\gamma_1, \gamma_2, \gamma_3$ = ranking weights

### 1.6 Elastic Trigger Function

Elasticity is triggered when:

$$E_{actual}(t) < (1 - \delta) \cdot E_{expected}(t)$$

Or when:
$$|P_{active}| < (1 - \epsilon) \cdot |P_{required}|$$

Where:
- $\delta$ = energy deviation threshold (e.g., 0.1)
- $\epsilon$ = prosumer count threshold (e.g., 0.2)

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Genetic Algorithm (Global Optimization)

The GA finds optimal composition configurations:

#### Population Encoding
Each chromosome represents a prosumer selection:
```
Chromosome: [0 1 0 1 1 0 0 1 0 1 ...]
            └───┘ └───┘ └───┘ └───┘
           Prosumer 1 2 3 4 ... selected
```

#### Fitness Evaluation
```
evaluate(chromosome):
    selected = get_selected_prosumers(chromosome)
    energy = sum(p.capacity for p in selected)
    reliability = compute_composite_reliability(selected)
    fitness = weighted_score(energy, reliability)
    return fitness
```

#### Selection (Exploitation)
Tournament selection:
```
select(population, tournament_size):
    candidates = random_sample(population, tournament_size)
    return best(candidates, by=fitness)
```

#### Crossover (Exploration)
Two-point crossover:
```
crossover(parent1, parent2):
    points = random.sample(range(len), 2)
    child1 = parent1[:p1] + parent2[p1:p2] + parent1[p2:]
    child2 = parent2[:p1] + parent1[p1:p2] + parent2[p2:]
    return child1, child2
```

#### Mutation (Exploration)
Bit-flip mutation:
```
mutate(chromosome, rate):
    for each gene:
        if random() < rate:
            flip bit
    return chromosome
```

### 2.2 Elastic Adaptation Algorithm

The adaptation mechanism adjusts composition dynamically:

#### Monitoring Loop
```
monitor(prosumers, composition, requirement):
    while running:
        current = measure_availability(prosumers)
        expected = compute_expected_energy(current)
        
        if (expected < requirement * 0.9) or 
           (len(active) < required * 0.8):
            trigger_elastic(composition, prosumers, requirement)
        
        sleep(interval)
```

#### Elastic Adjustment
```
trigger_elastic(composition, prosumers, requirement):
    # Exploration: Find backup prosumers
    backups = find_available_prosumers(
        prosumers,
        exclude=composition.active,
        status=available
    )
    
    # Select best backup
    if backups:
        best_backup = select_best(backups)
        composition.add(best_backup)
        
        # Update elastic metrics
        composition.elastic_capacity += 1
        composition.elastic_ratio = compute_elastic(composition)
    
    return composition
```

### 2.3 GA Parameters and Balance

| Parameter | Value | Effect |
|-----------|-------|--------|
| Population Size | 50-100 | Diversity level |
| Generations | 100-200 | Convergence |
| Crossover Rate | 0.7-0.9 | Information exchange |
| Mutation Rate | 0.01-0.05 | Novelty introduction |
| Elitism | Top 5 | Best solution retention |

### 2.4 Exploration vs Exploitation Strategy

| Phase | Strategy | Mechanism |
|-------|----------|-----------|
| GA Initial | Exploration | High mutation, random init |
| GA Convergence | Exploitation | Tournament selection |
| Elastic Trigger | Exploration | Backup prosumer search |
| Elastic Recovery | Exploitation | Immediate backup activation |

### 2.5 Pool Management Algorithm

Maintains dynamic prosumer pool:

```
maintain_pool(prosumers, active_set, backup_set):
    for p in prosumers:
        if p.availability < LOW_THRESHOLD:
            if p in active_set:
                move to backup_set
        elif p.availability > HIGH_THRESHOLD:
            if p in backup_set and len(active_set) < MAX_ACTIVE:
                move to active_set
    
    # Elastic: maintain minimum backup ratio
    if len(backup_set) / len(active_set) < MIN_RATIO:
        recruit_new_prosumers()
    
    return active_set, backup_set
```

---

## 3. Dataset Used

### 3.1 Synthetic Crowdsourced Prosumer Data

The evaluation uses synthetic datasets representing crowdsourced energy:

#### Prosumer Profiles
| Type | Capacity | Reliability | Variability |
|------|----------|-------------|-------------|
| Residential Solar | 2-5 kWh | 0.7-0.9 | High |
| Commercial Solar | 10-30 kWh | 0.85-0.95 | Medium |
| Wind Turbine | 5-15 kWh | 0.75-0.9 | High |
| Battery Storage | 5-20 kWh | 0.9-0.98 | Low |
| EV Charger | 7-22 kWh | 0.8-0.95 | Medium |

#### Scale Configurations
- Small: 20 prosumers, 50 kWh demand
- Medium: 50 prosumers, 100 kWh demand
- Large: 100+ prosumers, 200+ kWh demand

### 3.2 Temporal Variation Patterns

The dataset includes realistic temporal patterns:

```
Daily Pattern (Solar):
  Peak: 10am-4pm (high availability)
  Off-peak: 8pm-6am (low availability)
  
Daily Pattern (General):
  Morning: 6am-10am (increasing)
  Midday: 10am-2pm (peak)
  Afternoon: 2pm-6pm (decreasing)
  Evening: 6pm-10pm (moderate)
  Night: 10pm-6am (low)
```

### 3.3 Prosumer Behavior Simulation

| Behavior Type | Probability | Pattern |
|---------------|-------------|---------|
| Consistent | 40% | Regular availability |
| Intermittent | 35% | Variable, partly predictable |
| Erratic | 25% | Random, unpredictable |

### 3.4 Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Success Rate | % requests fully satisfied | >90% |
| Elasticity Index | Pool flexibility measure | >1.2 |
| Adaptation Latency | Time to adjust composition | <60s |
| Energy Utilization | % pool capacity used | >70% |

---

## 4. Complete Workflow

### 4.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Elastic Composition Engine (ECE)              │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐│
│  │    GA-based   │  │   Elastic     │  │    Pool        ││
│  │  Composition  │  │  Adaptation   │  │  Management    ││
│  │   Optimizer   │  │  Controller   │  │    Module      ││
│  └────────────────┘  └────────────────┘  └────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    Prosumer Pool (Dynamic)                  │
├─────────────────────────────────────────────────────────────┤
│   Active Set    │    Backup Set    │    Recruiting         │
│   (Composing)   │    (Available)   │    (On-demand)       │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Workflow Flowchart

```
START
  │
  ▼
┌─────────────────────┐
│ Initialize Prosumer │
│ Pool               │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Receive Energy     │
│ Request             │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Run GA Optimizer   │
│ (Find Initial      │
│ Composition)       │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Activate Selected  │
│ Prosumers          │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Monitor Pool       │
│ Availability       │
└─────────────────────┘
  │
  ▼
         ┌─────────────────────┐
         │ Elastic Trigger?    │
         │ (deviation detected)│
         └──────────┬────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
       YES                        NO
        │                        │
        ▼                        ▼
┌───────────────────┐    ┌─────────────────────┐
│ Trigger Elastic   │    │ Continue Monitoring │
│ Adaptation        │    │                     │
└───────────────────┘    └─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Explore Backup    │
│ Prosumers          │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Add Best Backup    │
│ to Composition     │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Update Pool        │
│ (Active/Backup)    │
└─────────────────────┘
        │
        ▼
    Continue
```

### 4.3 Complete Pseudocode

```python
class ElasticCompositionEngine:
    def __init__(self, config):
        self.ga_params = config.ga_params
        self.elastic_thresholds = config.elastic_thresholds
        self.pool = ProsumerPool()
        
    def initialize(self, prosumers):
        """Initialize prosumer pool"""
        for p in prosumers:
            self.pool.add(p)
            
    def compose(self, energy_requirement):
        """Main composition with GA optimization"""
        # GA optimization phase
        population = self.initialize_population(
            self.pool.all_prosumers,
            pop_size=self.ga_params.population_size
        )
        
        best_solution = None
        best_fitness = -float('inf')
        
        for gen in range(self.ga_params.generations):
            # Evaluate fitness
            for chrom in population:
                chrom.fitness = self.evaluate_fitness(
                    chrom, energy_requirement
                )
                
            # Selection
            parents = self.tournament_select(
                population,
                self.ga_params.tournament_size
            )
            
            # Crossover
            children = self.crossover(
                parents,
                self.ga_params.crossover_rate
            )
            
            # Mutation
            children = self.mutate(
                children,
                self.ga_params.mutation_rate
            )
            
            # Elitism
            elite = self.get_elite(population, n=5)
            population = elite + children
            
            # Track best
            gen_best = max(population, key=lambda c: c.fitness)
            if gen_best.fitness > best_fitness:
                best_fitness = gen_best.fitness
                best_solution = gen_best
                
        # Convert to prosumer selection
        selected = self.decode_solution(
            best_solution,
            self.pool.all_prosumers
        )
        
        return self.create_composition(selected)
    
    def evaluate_fitness(self, chromosome, requirement):
        """Calculate fitness for GA individual"""
        selected = self.decode_solution(chromosome)
        
        total_energy = sum(p.capacity for p in selected)
        reliability = self.compute_reliability(selected)
        
        # Check constraints
        if total_energy < requirement.energy:
            return -float('inf')
        if reliability < requirement.min_reliability:
            return -float('inf')
            
        # Fitness function
        w1, w2, w3 = 0.4, 0.4, 0.2
        fitness = (w1 * total_energy / requirement.energy +
                  w2 * reliability -
                  w3 * self.estimate_switching_cost(selected))
        
        return fitness
    
    def trigger_elastic(self, composition, requirement):
        """Elastic adaptation when triggered"""
        active = composition.active_prosumers
        backup = composition.backup_prosumers
        
        # Calculate deficit
        current_energy = sum(p.current_capacity for p in active)
        deficit = requirement.energy - current_energy
        
        # Exploration: Find suitable backup prosumers
        candidates = []
        for p in backup:
            if p.current_capacity > 0:
                score = self.score_prosumer(p, requirement)
                candidates.append((p, score))
        
        # Sort by score (Exploitation of best)
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Add best candidates until requirement met
        added = []
        for p, score in candidates:
            if sum(e.capacity for e in added) >= deficit:
                break
            added.append(p)
            
        # Update composition
        composition.expand(added)
        
        # Recruit more prosumers if needed
        if len(added) < deficit_needed:
            self.pool.recruit_new_prosumers(
                needed=deficit_needed - len(added)
            )
            
        return composition
    
    def monitor_and_adapt(self, composition, requirement):
        """Continuous monitoring with elastic adaptation"""
        while True:
            # Measure current state
            current_energy = composition.current_total_energy()
            active_count = len(composition.active)
            
            # Check triggers
            energy_trigger = (current_energy < 
                            requirement.energy * 
                            (1 - self.elastic_thresholds.energy_deviation))
            
            count_trigger = (active_count < 
                           requirement.min_prosumers * 
                           (1 - self.elastic_thresholds.count_deviation))
            
            if energy_trigger or count_trigger:
                composition = self.trigger_elastic(
                    composition, 
                    requirement
                )
                
            # Maintain pool
            self.pool.maintain(
                composition.active,
                composition.backup
            )
            
            sleep(self.monitoring_interval)
    
    def maintain_pool(self, active, backup):
        """Maintain dynamic pool of prosumers"""
        # Update availability for all prosumers
        for p in self.pool.all_prosumers:
            p.update_availability()
            
        # Check active prosumers
        for p in active:
            if p.availability < LOW_THRESHOLD:
                active.remove(p)
                backup.append(p)
                
        # Check backup for recovery
        recovered = [p for p in backup 
                    if p.availability > HIGH_THRESHOLD]
        
        for p in recovered:
            if len(active) < MAX_ACTIVE:
                backup.remove(p)
                active.append(p)
                
        # Maintain minimum backup ratio
        if len(backup) / len(active) < MIN_BACKUP_RATIO:
            self.pool.recruit(needed=MIN_BACKUP_RATIO * len(active) - len(backup))
```

### 4.4 Elastic vs Static Comparison

| Aspect | Static | Elastic |
|--------|--------|---------|
| Pool Management | Fixed set | Dynamic expansion/contraction |
| Adaptation | Full re-optimization | Incremental backup activation |
| Scalability | Degrades | Near-linear |
| Failure Recovery | Rebuild | Activate backup |
| Flexibility | Low | High |

### 4.5 GA-Epoch vs Elastic Runtime

The system operates at two timescales:

```
┌──────────────────────────────────────────────────────┐
│                    Time Scale                        │
├──────────────────────┬───────────────────────────────┤
│   GA Optimization    │      Runtime Adaptation       │
│   (seconds-minutes)  │      (seconds)               │
├──────────────────────┼───────────────────────────────┤
│  - Population init   │  - Availability monitoring  │
│  - Fitness eval     │  - Elastic trigger check    │
│  - Selection        │  - Backup exploration       │
│  - Crossover        │  - Pool maintenance         │
│  - Mutation         │  - Elastic adjustment       │
└──────────────────────┴───────────────────────────────┘
```

---

## 5. Summary

### Key Framework Components

| Component | Function | Innovation |
|-----------|----------|------------|
| GA Optimizer | Initial composition | Global optimal search |
| Elastic Controller | Runtime adaptation | Dynamic pool expansion |
| Pool Manager | Prosumer lifecycle | Active/backup management |
| Trigger Mechanism | Change detection | Multi-threshold detection |

### Algorithm Characteristics

- **Exploration**: GA crossover/mutation, backup prosumer search
- **Exploitation**: GA selection, best backup activation, elite preservation
- **Balance**: GA epochs vs elastic runtime adaptation

### Dataset Characteristics

- **Type**: Synthetic crowdsourced prosumer profiles
- **Scale**: 20-100+ prosumers
- **Patterns**: Temporal variation, heterogeneous reliability

---

*Analysis Date: April 2026*
*Paper Type: Original Research*