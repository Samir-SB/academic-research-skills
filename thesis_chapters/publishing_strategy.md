# Publishing Strategy: Converting Thesis Work into Two Publications

## Following the Bouguettaya Publishing Pattern

```
Current Thesis: A2C-based Proactive Composition for Moving IoT Services
         ↓
Paper 1 (Conference): Add ONE new feature + algorithm improvement
Paper 2 (Journal): Add DIFFERENT feature + expanded experiments
```

---

## Proposed Strategy

### Paper 1: Conference (IEEE ICWS/SCC 2026)

**Proposed Title:**
"A2C-Based Moving IoT Service Composition with Polar Coordinate State Representation"

**Focus:**
- Add **polar coordinate representation** (r, cosθ, sinθ) as the new feature
- Compare with DQN/Double DQN (Neiat 2021)
- Single dataset (ATC indoor)

**Changes from Original Thesis:**

| Component | Thesis Work | Conference Version |
|-----------|-------------|-------------------|
| State representation | Polar coordinates | Polar coordinates (main focus) |
| Algorithm | A2C | A2C vs DQN comparison |
| Dataset | ATC + Illinois | ATC only |
| Network architecture | Shared + Separate | Shared only |
| Results | Full comparison | Simplified |

**Target Length:** 8-10 pages

---

### Paper 2: Journal (IEEE TSC)

**Proposed Title:**
"Actor-Critic Reinforcement Learning for Proactive Moving IoT Service Composition"

**Focus:**
- Add **adaptive network architecture** comparison (shared vs separate)
- Add **real pedestrian datasets** evaluation (ATC indoor + Illinois outdoor)
- Add **detailed learning convergence analysis**

**Changes from Original Thesis:**

| Component | Thesis Work | Journal Version |
|-----------|-------------|-----------------|
| State representation | Polar coordinates | Polar coordinates + ablation study |
| Algorithm | A2C | A2C + architecture analysis |
| Dataset | ATC + Illinois | Both (full evaluation) |
| Network architecture | Shared + Separate | Both (detailed comparison) |
| Results | Basic | Full statistical analysis |

**New Additions for Journal:**
1. Shared vs Separate network comparison
2. Convergence rate analysis
3. Detailed sensitivity analysis
4. Pedestrian vs Vehicle mobility pattern comparison

**Target Length:** 15-20 pages

---

## Paper 1 Outline (Conference)

### Section 1: Introduction (1 page)
- Problem: Moving IoT service composition challenge
- Gap: DQN overestimation bias, trajectory prediction overhead
- Contribution: A2C + polar coordinates

### Section 2: Background (1 page)
- Moving IoT services (cite Paper 17 / Neiat 2021)
- STR model (cite Neiat 2021)
- A2C basics (cite Mnih 2016)

### Section 3: Framework (2 pages)
- State: Polar coordinates (r, cosθ, sinθ)
- Action: Service selection (discrete)
- Reward: STR-based capacity

### Section 4: Implementation (1 page)
- Gymnasium environment
- Stable Baselines3 A2C

### Section 5: Experiments (2 pages)
- Dataset: ATC indoor
- Metrics: Success rate, avg reward
- Baselines: Random, DQN

### Section 6: Results (1.5 pages)
- Comparison table/figures
- Key findings

### Section 7: Conclusion (0.5 page)

---

## Paper 2 Outline (Journal)

### Section 1: Introduction (2 pages)
- Full problem statement
- Literature review summary
- Research questions

### Section 2: Background and Related Work (3 pages)
- Service composition fundamentals
- Moving IoT services
- RL for service composition
- Publishing pattern analysis (optional - demonstrates originality)

### Section 3: System Model and Problem Formulation (2 pages)
- Spatio-temporal service model
- MDP formulation
- STR-based reward function

### Section 4: A2C-Based Framework (3 pages)
- **State representation** (polar coordinates - detailed derivation)
- **Network architecture** (shared vs separate - design choices)
- Action space and reward design

### Section 5: Experimental Setup (2 pages)
- **Datasets: ATC + Illinois** (both evaluated)
- Environment configuration
- Comparison methods

### Section 6: Results and Analysis (4 pages)
- A2C vs baselines (DQN, Random)
- Shared vs Separate network comparison
- Convergence analysis
- Parameter sensitivity

### Section 7: Discussion (2 pages)
- Implications for moving IoT service composition
- Limitations
- Comparison with prior work (Paper 17 / Neiat 2021)

### Section 8: Conclusion (1 page)

---

## Timeline

| Phase | Task | Duration |
|-------|------|----------|
| 1 | Extract conference paper from thesis | 1 week |
| 2 | Review and revise | 3 days |
| 3 | Submit to conference | - |
| 4 | Expand for journal paper | 2 weeks |
| 5 | Add experiments | 1 week |
| 6 | Final review | 1 week |
| 7 | Submit to journal | - |

---

## Key Notes

1. **Avoid Self-Plagiarism**: Use different phrasing, reorganize content
2. **Citations**: Properly cite both papers (original thesis and prior work)
3. **Novelty**: Each paper must present a distinct contribution
4. **Formatting**: Follow target venue guidelines (IEEE formatting)

---

## Target Venues

**Conferences:**
- IEEE ICWS 2026 (International Conference on Web Services)
- IEEE SCC 2026 (Services Computing Conference)

**Journals:**
- IEEE Transactions on Services Computing (Recommended)
- Future Generation Computer Systems
- Journal of Network and Computer Applications

---

## Differentiation Strategy

### Conference Paper Contribution:
- Novel state representation (polar coordinates vs trajectory prediction)
- First application of A2C to this specific problem

### Journal Paper Contribution:
- Network architecture analysis (shared vs separate)
- Comprehensive evaluation on real datasets
- Detailed convergence and sensitivity analysis

### Comparison with Neiat 2021 (Paper 17):

| Aspect | Paper 17 | Conference | Journal |
|--------|----------|------------|---------|
| Algorithm | Double DQN | A2C | A2C |
| State | Trajectory prediction | Polar coords | Polar coords |
| Dataset | Synthetic | ATC | ATC + Illinois |
| Architecture | Single | Shared | Both compared |

---

## Next Steps

1. Identify target conference deadline
2. Start drafting conference paper
3. Identify target journal
4. Plan additional experiments for journal