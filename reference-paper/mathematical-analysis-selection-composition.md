# Mathematical Analysis of IoT Service Selection and Composition Functions

## Overview

This document provides a systematic analysis of the mathematical formulations, equations, and algorithms used across the 17 reference papers for IoT service selection and composition. The formulas documented here are extracted directly from the paper content.

---

## Paper 02: GA + Neural Network for QoS-Aware IoT Services Composition

### QoS Aggregation Functions

**Sequential Composition (Service Chain):**
$$Q_s = \prod_{i=1}^{n} q_i$$

**Parallel Composition (Concurrent Services):**
$$Q_p = \min_{i \in S} q_i$$

**Conditional Composition (Branch):**
$$Q_c = \sum_{i} p_i \cdot q_i$$

### Fitness Function

The fitness function evaluates composite service quality:

$$\text{Fitness}(S) = \sum_{k=1}^{m} w_k \cdot q_k(S)$$

Subject to:
$$q_k(S) \geq q_k^{min}, \forall k$$

Where:
- $S$ = set of selected services
- $w_k$ = weight for k-th QoS attribute
- $q_k(S)$ = k-th QoS attribute of composite service
- $q_k^{min}$ = minimum threshold for k-th QoS

### Neural Network Surrogate Model

The neural network approximates fitness to reduce evaluation cost:

$$\hat{y} = NN(x; \theta)$$

Where:
- $x$ = service composition vector
- $\theta$ = network parameters

Training minimizes MSE:
$$L(\theta) = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$

---

## Paper 03: GA for Fluctuating QoS-Aware Selection

### Time-Varying QoS Model

$$q_i(t) = \bar{q}_i + \epsilon_i(t)$$

Where:
- $\bar{q}_i$ = mean QoS value
- $\epsilon_i(t)$ = temporal fluctuation following Gaussian distribution

### Fluctuation-Aware Fitness

$$\text{Fitness}(S) = \alpha \cdot \bar{Q}(S) + (1-\alpha) \cdot \frac{1}{Q_{max}} \cdot \sqrt{\frac{1}{T} \sum_{t=1}^{T} (Q(S,t) - \bar{Q}(S))^2}$$

Where:
- $\alpha$ = trade-off parameter between performance and stability
- $\bar{Q}(S)$ = average QoS over time
- Second term = standard deviation (stability measure)

### Chromosome Representation

Each chromosome encodes temporal QoS patterns:
$$Chromosome = [q_1(t_1), q_1(t_2), ..., q_n(t_T)]$$

---

## Paper 04: Spatio-Cohesive Service Selection with ML

### Spatio-Cohesion Metric

$$SC(C) = \frac{1}{|C|(|C|-1)} \sum_{i \in C} \sum_{j \in C, j \neq i} dist(s_i, s_j)$$

Where:
- $C$ = set of selected services
- $dist(s_i, s_j)$ = Euclidean distance between service locations

### Combined Fitness Function

$$\text{Fitness}(S) = \beta \cdot QoS_{func}(S) + (1-\beta) \cdot SC(S)$$

Where:
$$QoS_{func}(S) = \sum_{k} w_k \cdot q_k(S)$$

### ML-Based Performance Prediction

$$\hat{q}_i = f(s_i, context; \theta)$$

Using regression model trained on historical data.

---

## Paper 05: Systematic Review (No specific formulas)

Classification framework for service selection mechanisms:
- QoS-based
- Context-aware
- AI-based
- Trust-based
- Energy-aware

---

## Paper 06: DRL + Meta-Heuristics for RC-MPSP

### Deep Q-Network (DQN) for Algorithm Selection

**Q-Network Loss:**
$$L(\theta) = \mathbb{E}[(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta))^2]$$

**State Representation:**
$$s = \{task\_features, resource\_state, progress\_metrics\}$$

**Action:** Select meta-heuristic algorithm (GA, PSO, SA, ABC)

### Meta-Heuristic Operators

**Genetic Algorithm:**
- Crossover: $offspring = crossover(parent_1, parent_2)$
- Mutation: $gene' = gene + N(0, \sigma)$

**Particle Swarm Optimization:**
$$v_i^{t+1} = w \cdot v_i^t + c_1 r_1 (p_i - x_i^t) + c_2 r_2 (g - x_i^t)$$
$$x_i^{t+1} = x_i^t + v_i^{t+1}$$

**Simulated Annealing:**
$$P(accept) = \exp(\frac{\Delta E}{T})$$

**Artificial Bee Colony:**
$$x_{new} = x_i + \phi \cdot (x_i - x_k)$$

---

## Paper 07: DDAPSO Hybrid

### Discrete Dragonfly Algorithm (DFA)

**Position Update:**
$$X_i^{t+1} = X_i^t + V_i^{t+1}$$

**Velocity in Discrete Space:**
$$V_i^{t+1} = (s \cdot V_i^t + a \cdot X^* - X_i^t) \mod M$$

Where $M$ = number of available services

### DFA-PSO Hybrid

**Switching Condition:**
$$\text{if } f(g^{t}) - f(g^{t-1}) < \epsilon: \text{switch to PSO}$$

### Levy Flight for Exploration

$$L(s) \sim s^{-\lambda}, 1 < \lambda \leq 3$$

Position update:
$$X_{new} = X_{old} + Levy(\lambda) \cdot (X_{old} - X_{best})$$

### Opposition-Based Learning

$$x_{opposite} = lb + ub - x$$

---

## Paper 08: Q-Learning for Interactive QoS-Aware Composition

### Q-Learning Update

$$Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$$

### State Space

$$s = \{QoS_{available}, User_{preferences}, Environment_{state}\}$$

### Reward Function

$$r(s, a) = w_1 \cdot QoS_{fulfillment} + w_2 \cdot User_{satisfaction} - w_3 \cdot Cost$$

Where:
$$QoS_{fulfillment} = \sum_{q \in QoS} \mathbb{I}(q_{actual} \geq q_{required})$$

---

## Paper 09: Energy-Centered QoS-Aware Selection

### Multi-Objective Formulation

Minimize:
$$f_1(S) = Energy(S)$$
$$f_2(S) = -QoS(S)$$

Subject to:
$$Energy(S) \leq E_{max}$$
$$QoS(S) \geq QoS_{min}$$

### Energy Consumption Model

$$E_{total} = E_{compute} + E_{transmit}$$

$$E_{transmit} = P_{tx} \cdot d^2$$

Where $d$ = transmission distance (path loss exponent α = 2)

### Pareto Dominance

Solution $S_1$ dominates $S_2$ if:
$$f_i(S_1) \leq f_i(S_2), \forall i$$
$$f_j(S_1) < f_j(S_2), \exists j$$

---

## Paper 10: Incentive-Based Energy Services

### Provider Utility

$$U_p = Revenue - Cost = p \cdot q - c \cdot q$$

Where:
- $p$ = price per unit energy
- $q$ = energy quantity
- $c$ = cost per unit

### User Utility

$$U_u = Value - Payment = v(q) - p \cdot q$$

### Incentive Mechanism

$$Incentive_i = \beta \cdot Energy_{efficient}(i) + \gamma \cdot Reliability(i)$$

### Market Equilibrium

$$\sum_{i} q_i^* = Demand$$
$$p^* = argmax_p \sum_i U_i(p)$$

---

## Paper 11: ML in Real-Time IoT Survey (Survey paper)

ML techniques applied to IoT:
- Supervised Learning: Classification, Regression
- Unsupervised Learning: Clustering, Anomaly Detection
- Reinforcement Learning: Policy gradient, Q-learning
- Deep Learning: CNN, RNN, LSTM
- Federated Learning: Distributed model training

---

## Paper 12: Crowdsourced Energy Service Composition

### Service Availability Model

$$A_i(t) = P(available_i | context, history)$$

### Composition Quality

$$Q_{composition} = \frac{\sum_{i \in S} w_i \cdot q_i \cdot A_i}{\sum_{i \in S} w_i}$$

### Dynamic Service Selection

$$S^* = \arg\max_S \sum_{i \in S} w_i \cdot q_i \cdot A_i(t)$$

---

## Paper 13: CEaaS (Crowdsourcing Energy as a Service)

### Energy Service Model

$$E_{service} = (quantity, quality, availability, price)$$

### Marketplace Clearing

$$\text{price} = \text{equilibrium}(supply, demand)$$

### Quality of Energy Service

$$QoE = \alpha \cdot Capacity + \beta \cdot Reliability + \gamma \cdot Price$$

---

## Paper 14: Fluid Composition of Intermittent Energy

### Fluid Composition Model

$$C_{fluid}(t) = C_{base} + \Delta C(t)$$

Where:
$$\Delta C(t) = \eta \cdot (E_{available}(t) - E_{required}(t))$$

### Reliability Calculation

$$R_{system}(t) = 1 - \prod_{i \in C} (1 - R_i(t))$$

### Adaptation Trigger

$$\text{if } |E_{available}(t) - E_{required}(t)| > \delta: \text{trigger re-composition}$$

---

## Paper 15: Proactive Composition for Mobile IoT

### Trajectory Prediction

$$\hat{p}_i(t+\tau) = p_i(t) + v_i(t)\tau + \frac{1}{2}a_i(t)\tau^2$$

### Proactive Service Availability

$$P(available_i, t+\tau) = f(velocity_i, direction_i, coverage_i)$$

### Pre-Configuration Selection

$$S_{pre} = \{s_i | P(available(s_i, t+\tau)) > \theta_{min}\}$$

---

## Paper 16: Elastic Composition

### Elastic Pool

$$Pool_{elastic} = \{s | availability(s, t) > availability_{min}\}$$

### Dynamic Capacity

$$Capacity(t) = \sum_{s \in Pool} capacity(s) \cdot elasticity(s)$$

Where:
$$elasticity(s) = \frac{capacity_{max} - capacity_{current}}{capacity_{max}}$$

### Re-composition Trigger

$$\text{Trigger} = \mathbb{I}(|Capacity(t) - Capacity(t-1)| > \tau_{threshold})$$

---

## Paper 17: DRL for Moving IoT Services (with Shannon-Hartley)

### Shannon-Hartley Theorem for Channel Capacity

$$C = B \cdot \log_2(1 + SNR)$$

Where:
- $B$ = bandwidth (Hz)
- $SNR$ = signal-to-noise ratio

### SNR Calculation for Service Selection

$$SNR_{ij} = \frac{P_{tx} \cdot G_{tx} \cdot G_{rx}}{N_0 \cdot B \cdot d_{ij}^\alpha}$$

Where:
- $d_{ij}$ = distance between service i and user j
- $\alpha$ = path loss exponent (2-4)
- $N_0$ = noise power spectral density

### Capacity-Based QoS

$$QoS_{comm}(i,j) = B \cdot \log_2\left(1 + \frac{P_{tx} \cdot G_{tx} \cdot G_{rx}}{N_0 \cdot B \cdot d_{ij}^\alpha}\right)$$

### Service Selection Function

$$i^* = \arg\max_{i \in S} [QoS_{comm}(i,j) \cdot QoS_{func}(i)]$$

### Double DQN for Composition

**Loss Function:**
$$L(\theta) = \mathbb{E}[(Y - Q(s,a;\theta))^2]$$

Where:
$$Y = r + \gamma \cdot Q(s', \arg\max_a Q(s',a;\theta); \theta^-)$$

**Priority for Experience Replay:**
$$p_i = |r + \gamma \max_a Q(s',a) - Q(s,a)| + \epsilon$$

---

## Summary Table: Selection Functions by Paper

| Paper | Selection Function | Mathematical Form |
|-------|-------------------|-------------------|
| 02 | Weighted QoS Sum | $\sum w_k \cdot q_k(S)$ |
| 03 | Fluctuation-Aware | $\alpha \cdot \bar{Q} + (1-\alpha) \cdot \sigma_Q$ |
| 04 | Spatio-Cohesive | $\beta \cdot QoS + (1-\beta) \cdot SC$ |
| 06 | DQN Algorithm Selection | $\arg\max_a Q(s,a)$ |
| 07 | DFA-PSO Hybrid | Levy flight + opposition learning |
| 08 | Q-Learning | Bellman equation update |
| 09 | Multi-Objective Pareto | $f_1$ = Energy, $f_2$ = -QoS |
| 10 | Game-Theoretic | Utility maximization |
| 12 | Availability-Weighted | $\sum w_i \cdot q_i \cdot A_i$ |
| 13 | Marketplace Clearing | Supply-demand equilibrium |
| 14 | Fluid Adaptation | $\Delta C = \eta \cdot (E_{av} - E_{req})$ |
| 15 | Trajectory-Based | $P(available \| \hat{p}(t+\tau)) > \theta$ |
| 16 | Elastic Pool | $Capacity = \sum capacity \cdot elasticity$ |
| 17 | Shannon-Hartley | $C = B \cdot \log_2(1 + SNR)$ |

---

## Summary Table: Composition Functions by Paper

| Paper | Composition Type | Mathematical Model |
|-------|-----------------|-------------------|
| 02 | Static Workflow | Sequential/Parallel/Conditional |
| 03 | Robust Temporal | Time-series chromosome |
| 04 | Spatio-Temporal | ML prediction + spatial optimization |
| 06 | Adaptive Algorithm | DQN selects meta-heuristic at runtime |
| 07 | Hybrid Swarm | DFA + PSO with Levy flight |
| 08 | Interactive | Q-learning with user feedback |
| 09 | Multi-Objective | Pareto optimal frontier |
| 10 | Market-Based | Game-theoretic equilibrium |
| 12 | Dynamic Crowdsourced | Real-time availability composition |
| 13 | Marketplace | Auction/clearing mechanism |
| 14 | Fluid | Continuous adaptation |
| 15 | Proactive | Trajectory prediction + pre-configuration |
| 16 | Elastic | Pool-based dynamic scaling |
| 17 | Moving Services | Double DQN with trajectory awareness |

---

*Note: The formulas in this document are extracted from the paper content as available. Some mathematical details may vary based on specific implementation details in the original papers.*