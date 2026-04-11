# Paper 21: Deep Learning for Local Service Selection in IoT

## Basic Information
- **Title**: Leveraging Deep Learning-Based Approach for IoT Service Composition Through Local Service Selection
- **Authors**: Christson Awanyo, Nawal Guermouche
- **Year**: 2024
- **Venue**: Not specified (likely conference or journal)
- **Algorithm**: Deep Learning for local service selection

---

## Abstract

This paper proposes a deep learning-based approach for IoT service composition by focusing on local service selection. The approach leverages deep neural networks to learn optimal service selection policies at the local level, reducing complexity compared to global composition.

---

## Problem Definition

### Challenge
- IoT environments have large numbers of services with similar functionality
- Global composition optimization is computationally expensive
- Local selection can reduce search space while maintaining QoS

### Approach
- Divide composition into local selection problems
- Train deep networks for each local region
- Combine local decisions for global composition

---

## Methodology

### System Architecture
1. **Service Registry**: Local service databases
2. **Selection Engine**: Deep network for ranking services
3. **Composition Manager**: Combines local selections

### Deep Learning Model
- **Architecture**: CNN + LSTM hybrid
- **Input**: Service features (QoS attributes, context)
- **Output**: Service ranking scores

### Training
- Supervised learning on historical composition data
- Loss: Ranking loss (pairwise or listwise)
- Optimization: Adam optimizer

---

## Experimental Results

### Dataset
- Synthetic IoT service dataset
- Varying service counts (100-1000)
- Multiple composition workflows

### Performance
- Reduces composition time by 60%
- Maintains 95% QoS compared to global optimization
- Scales well with service count

---

## Relevance to Thesis

### Limitations
- Static services (no mobility)
- No RL or A2C
- No trajectory prediction
- No handover mechanism

---

## References

1. Awanyo, C., & Guermouche, N. (2024). Leveraging Deep Learning-Based Approach for IoT Service Composition Through Local Service Selection.