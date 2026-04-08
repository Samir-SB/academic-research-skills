# Mathematical Analysis of IoT Service Selection and Composition Functions

## Executive Summary

This document provides a systematic analysis of the mathematical formulations, equations, and algorithms used across the 17 reference papers for IoT service selection and composition. Each paper employs distinct mathematical approaches ranging from evolutionary computation fitness functions to deep reinforcement learning loss functions.

---

## Part I: Selection Functions Mathematics

### Paper 02: GA-NN Hybrid for QoS-Aware Composition

#### 1.1 QoS Aggregation Functions

For service composition, QoS attributes are aggregated based on composition patterns:

**Sequential Composition (Chain):**
$$Q_{sequential} = \prod_{i=1}^{n} q_i$$

Where $q_i$ represents the QoS attribute (reliability, availability) of service $s_i$ in the chain.

**Parallel Composition (And):**
$$Q_{parallel} = \min_{i \in S} q_i$$

For parallel services, the minimum QoS determines the composite quality.

**Conditional Composition (Xor):**
$$Q_{conditional} = \sum_{i} p_i \cdot q_i$$

Where $p_i$ is the probability of selecting branch $i$.

#### 1.2 Fitness Function

$$f(x) = w_1 \cdot QoS_{response} + w_2 \cdot QoS_{reliability} + w_3 \cdot QoS_{availability} + w_4 \cdot QoS_{cost} - \lambda \cdot penalty(x)$$

Where:
- $w_i$ are weighted coefficients summing to 1
- $penalty(x)$ handles constraint violations
- $\lambda$ is penalty coefficient

#### 1.3 Neural Network Surrogate

The NN approximates the fitness function:
$$\hat{f}(x) = \sigma(W_2 \cdot \sigma(W_1 \cdot x + b_1) + b_2)$$

Where:
- $W_1, W_2$ are weight matrices
- $\sigma$ is activation function (ReLU or sigmoid)
- $b_1, b_2$ are bias vectors

**Training Loss:**
$$L = \frac{1}{N} \sum_{i=1}^{N} (f(x_i) - \hat{f}(x_i))^2$$

---

### Paper 03: GA for Fluctuating QoS

#### 1.4 Time-Series QoS Model

$$q_i(t) = \bar{q}_i + \epsilon_i(t)$$

Where:
- $\bar{q}_i$ is mean QoS value
- $\epsilon_i(t)$ is temporal fluctuation following $N(0, \sigma_i^2)$

#### 1.5 Fluctuation-Aware Fitness

$$f_{fluct}(x) = \alpha \cdot \bar{Q}_{avg} + (1-\alpha) \cdot Q_{stability}$$

Where:
$$\bar{Q}_{avg} = \frac{1}{T} \sum_{t=1}^{T} Q(x, t)$$
$$Q_{stability} = \frac{1}{Q_{max}} \cdot \frac{1}{T} \sum_{t=1}^{T} |Q(x,t) - \bar{Q}_{avg}|$$

- $\alpha \in [0,1]$ balances average performance vs stability
- $Q_{max}$ is maximum possible QoS

#### 1.6 Temporal Chromosome Encoding

Each chromosome encodes time-series QoS:
$$chromosome = [q_1(t_1), q_1(t_2), ..., q_n(t_T)]$$

---

### Paper 04: ML-Based Spatio-Cohesive Selection

#### 1.7 Spatio-Cohesion Metric

$$SC(x) = \frac{1}{|C|^2} \sum_{i \in C} \sum_{j \in C} d(i, j)$$

Where:
- $C$ is the set of selected services
- $d(i,j)$ is spatial distance between services $i$ and $j$

#### 1.8 Combined Fitness Function

$$f(x) = \beta \cdot QoS_{functional} + (1-\beta) \cdot SC(x) \cdot E_{factor}$$

Where:
- $E_{factor}$ is energy consumption factor
- $\beta$ balances functionality vs spatial cohesion

#### 1.9 ML Prediction Model

For service performance prediction:
$$\hat{q}_i = M_\theta(s_i, context)$$

Trained using MSE loss:
$$L_{ML} = \frac{1}{N} \sum_{i=1}^{N} (q_i - \hat{q}_i)^2$$

---

### Paper 06: DRL + Meta-Heuristics

#### 1.10 DQN Loss Function

$$L(\theta) = \mathbb{E}[(r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta))^2]$$

Where:
- $\theta$ are current network parameters
- $\theta^-$ are target network parameters
- $\gamma$ is discount factor
- $r$ is reward

#### 1.11 Meta-Heuristic Selection Policy

$$P(a = h | s) = \frac{\exp(\phi(s, h)/\tau)}{\sum_{h' \in H} \exp(\phi(s, h')/\tau)}$$

Where:
- $h$ is meta-heuristic type (GA, PSO, SA, ABC)
- $\phi(s,h)$ is learned feature function
- $\tau$ is temperature parameter

#### 1.12 Reward Function for Scheduling

$$r(s, a) = r_{makespan} + r_{resource} + r_{feasibility}$$

Where:
$$r_{makespan} = -\lambda_1 \cdot (makespan - makespan_{best})$$
$$r_{resource} = -\lambda_2 \cdot resource_{violation}$$

---

### Paper 07: DDAPSO Hybrid

#### 1.13 Discrete DFA Position Update

For discrete service selection:
$$X_{i}^{t+1} = X_i^t + V_i^{t+1}$$

Where velocity is discretized:
$$V_i^{t+1} = \text{round}(s \cdot V_i^t + a \cdot X^* - X_i^t)$$

#### 1.14 DFA-PSO Hybrid Switching

$$\text{switch} = \begin{cases} \text{DFA} & \text{if } iter < T_{switch} \cdot \rho \\ \text{PSO} & \text{otherwise} \end{cases}$$

Where $\rho \in [0,1]$ is adaptation factor based on exploration progress.

#### 1.15 Levy Flight for Exploration

$$Levy(\lambda) = \frac{\Gamma(1+\lambda) \sin(\pi\lambda/2)}{\Gamma((1+\lambda)/2) \lambda 2^{(\lambda-1)/2}} \cdot \frac{1}{s^{1+\lambda}}$$

Position update with Levy:
$$X_{new} = X_{old} + \text{Levy}(\lambda) \cdot (X_{old} - X_{best})$$

#### 1.16 Opposition-Based Initialization

$$x_{opposite} = lb + ub - x$$

Initial population includes both $x$ and $x_{opposite}$ for better coverage.

---

### Paper 08: Q-Learning for Composition

#### 1.17 Q-Learning Bellman Equation

$$Q(s, a) \leftarrow Q(s, a) + \alpha \cdot [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$$

Where:
- $\alpha$ is learning rate
- $\gamma$ is discount factor
- $s$ is state, $a$ is action

#### 1.18 State Representation

$$s = \{QoS_{available}, User_{preferences}, Environment_{state}\}$$

#### 1.19 Reward Function

$$r(s, a) = r_{QoS} + r_{satisfaction} + r_{efficiency}$$

Where:
$$r_{QoS} = \sum_{q \in QoS} w_q \cdot (q_{actual} - q_{threshold})$$
$$r_{satisfaction} = \text{Feedback}_{user}$$
$$r_{efficiency} = -c \cdot Cost$$

---

### Paper 09: Energy-Centered Multi-Objective

#### 1.20 Multi-Objective Fitness

$$\vec{f}(x) = (f_1(x), f_2(x))$$

Where:
$$f_1(x) = Energy(x) = \sum_{i \in S} e_i(x)$$
$$f_2(x) = QoS(x) = \sum_{j} w_j \cdot q_j(x)$$

#### 1.21 Pareto Dominance

Solution $x_1$ dominates $x_2$ ($x_1 \succ x_2$) if:
$$\forall i: f_i(x_1) \leq f_i(x_2) \land \exists j: f_j(x_1) < f_j(x_2)$$

#### 1.22 Energy Consumption Model

$$E_{total} = E_{computation} + E_{communication}$$

$$E_{computation} = P_{cpu} \cdot t_{exec}$$
$$E_{communication} = P_{tx} \cdot d^2 + P_{rx} \cdot d^2$$

Where $d$ is transmission distance.

---

### Paper 10: Game-Theoretic Incentives

#### 1.23 Provider Utility Function

$$U_p(s_p) = \pi(s_p) - c_p(s_p)$$

Where:
- $\pi(s_p)$ is payment received
- $c_p(s_p)$ is cost of providing service

#### 1.24 User Utility Function

$$U_u(s) = v(s) - \pi(s)$$

Where $v(s)$ is value derived from service composition.

#### 1.25 Incentive Mechanism

$$I(s_p) = \beta \cdot Energy_{saved}(s_p) + \gamma \cdot QoS_{provided}(s_p)$$

Where $I(s_p)$ is incentive payment to provider.

#### 1.26 Market Equilibrium

At equilibrium:
$$\sum_{p} x_p^* = D$$
$$U_p(x_p^*) \geq U_p(x_p) \quad \forall p, x_p$$

---

## Part II: Composition Functions Mathematics

### Paper 06: Adaptive Algorithm Selection

#### 2.1 Composition as Sequential Decision

The composition problem is formulated as MDP:
- **State Space**: Current partial composition, available services
- **Action Space**: Add service to composition, terminate
- **Transition**: Deterministic based on service addition
- **Reward**: QoS improvement, cost efficiency

#### 2.2 Meta-Heuristic Integration

Each meta-heuristic optimizes composition:

**Genetic Algorithm:**
$$P_{crossover} = 0.8, P_{mutation} = 0.05$$
$$x_{new} = x_{parent1} \oplus x_{parent2}$$

**Particle Swarm:**
$$v_i^{t+1} = w \cdot v_i^t + c_1 r_1 (p_i - x_i^t) + c_2 r_2 (g - x_i^t)$$
$$x_i^{t+1} = x_i^t + v_i^{t+1}$$

**Simulated Annealing:**
$$P(accept) = \exp(\frac{\Delta E}{T})$$

**Artificial Bee Colony:**
$$x_{new} = x_i + \phi \cdot (x_i - x_k)$$

---

### Paper 08: Interactive RL Composition

#### 2.3 Composition Policy

$$\pi(a|s) = \text{argmax}_{a} Q(s, a; \theta)$$

#### 2.4 User Preference Learning

$$Q(s, a) = Q_{base}(s, a) + \lambda \cdot Preference_{user}$$

Where preference is updated:
$$Preference_{new} = Preference_{old} + \eta \cdot (feedback - Preference_{old})$$

---

### Paper 14: Fluid Composition

#### 2.5 Fluid Adaptation Function

$$C_{new}(t) = C_{old}(t) + \Delta C(t)$$

Where:
$$\Delta C(t) = \alpha \cdot (E_{available}(t) - E_{required}(t)) \cdot \mathbb{I}(|E_{available} - E_{required}| > \delta)$$

- $\alpha$ is adaptation rate
- $\delta$ is threshold for triggering adaptation

#### 2.6 Reliability Assurance

$$R_{composite}(t) = 1 - \prod_{i \in C(t)} (1 - R_i(t))$$

---

### Paper 15: Proactive Composition

#### 2.7 Trajectory Prediction

$$\hat{p}_{i}(t+\Delta t) = p_i(t) + v_i(t) \cdot \Delta t + \frac{1}{2} a_i(t) \cdot \Delta t^2$$

#### 2.8 Proactive Service Setup

$$S_{preconfig} = \{s_i | P(available(s_i, t+\tau)) > \theta\}$$

Where $\tau$ is time until device reaches service location.

---

### Paper 16: Elastic Composition

#### 2.9 Elastic Pool Management

$$Pool_{elastic} = \{s | availability(s, t) > availability_{min}\}$$

#### 2.10 Capacity Scaling

$$Capacity(t) = \sum_{s \in Pool_{elastic}} capacity(s) \cdot elasticity(s)$$

Where $elasticity(s) \in [0,1]$ represents service flexibility.

#### 2.11 Re-composition Trigger

$$trigger = \begin{cases} 1 & \text{if } |Capacity(t) - Capacity(t-1)| > \tau \\ 0 & \text{otherwise} \end{cases}$$

---

### Paper 17: Double DQN for Moving Services

#### 2.12 Double DQN Loss

$$L(\theta) = \mathbb{E}[(Y - Q(s, a; \theta))^2]$$

Where:
$$Y = r + \gamma \cdot Q(s', \text{argmax}_{a'} Q(s', a'; \theta); \theta^-)$$

#### 2.13 Prioritized Experience Replay

Priority for replay:
$$p_i = |r + \gamma \max_a Q(s', a) - Q(s, a)|^\omega + \epsilon$$

Sampling probability:
$$P(i) = \frac{p_i^\alpha}{\sum_j p_j^\alpha}$$

#### 2.14 Trajectory-Aware State

$$s_{traj} = \{p_i, v_i, a_i, QoS_i, \hat{p}_i(t+\tau)\}$$

---

## Part III: Comparative Mathematical Analysis

### 3.1 Optimization Paradigms

| Paper | Optimization Type | Mathematical Approach |
|-------|-------------------|------------------------|
| 02 | Evolutionary | GA fitness with NN surrogate |
| 03 | Evolutionary | Time-series GA with stability |
| 04 | Evolutionary + ML | GA with ML prediction |
| 06 | RL + Meta-heuristic | DQN loss with algorithm selection |
| 07 | Swarm Intelligence | DFA-PSO hybrid with Levy |
| 08 | Reinforcement Learning | Q-learning Bellman |
| 09 | Multi-Objective | Pareto dominance |
| 10 | Game Theory | Utility equilibrium |
| 14-17 | Adaptive | Dynamic update functions |

### 3.2 Common Mathematical Patterns

**QoS Aggregation:**
- Multiplicative for parallel (min operation)
- Additive for weighted sums
- Probabilistic for conditional

**Fitness Functions:**
- Weighted sum: $f = \sum w_i \cdot q_i$
- Penalty method: $f = f_{obj} - \lambda \cdot penalty$
- Pareto ranking for multi-objective

**Adaptation Mechanisms:**
- Threshold-triggered: $\mathbb{I}(value > threshold)$
- Gradient-based: $x_{new} = x_{old} + \alpha \cdot \nabla f$
- RL update: $Q \leftarrow Q + \alpha \cdot (r + \gamma \max Q' - Q)$

### 3.3 Complexity Analysis

| Algorithm | Time Complexity | Space Complexity |
|-----------|------------------|-------------------|
| GA | $O(g \cdot pop \cdot n)$ | $O(pop \cdot n)$ |
| PSO | $O(g \cdot n)$ | $O(pop)$ |
| Q-Learning | $O(|S| \cdot |A|)$ | $O(|S| \cdot |A|)$ |
| DQN | $O(iter \cdot batch)$ | $O(|params|)$ |
| DDAPSO | $O(g \cdot pop \cdot n)$ | $O(pop \cdot n)$ |

Where: $g$ = generations, $pop$ = population size, $n$ = number of services, $|S|$ = state space, $|A|$ = action space.

---

## Part IV: Mathematical Gaps and Limitations

### 4.1 Identified Gaps

1. **Convergence Guarantees**: Most papers lack formal convergence proofs
2. **Optimality Bounds**: No theoretical bounds on solution quality
3. **Complexity Analysis**: Limited computational complexity analysis
4. **Uncertainty Quantification**: Few papers model prediction uncertainty

### 4.2 Mathematical Assumptions

- QoS values assumed independent (often violated)
- Linear aggregation (non-linear interactions ignored)
- Stationary environments (dynamic changes may invalidate)
- Perfect service information (incomplete information not modeled)

### 4.3 Areas for Mathematical Enhancement

1. **Stochastic Optimization**: Model service failures, QoS variations
2. **Robust Optimization**: Handle worst-case scenarios
3. **Distributed Optimization**: Multi-agent formulations
4. **Formal Verification**: Model checking for composition correctness

---

## Part V: Summary Table

| Paper | Selection Function | Composition Function | Key Mathematical Tool |
|-------|-------------------|---------------------|---------------------|
| 02 | $f_{fitness}(x) = \sum w_i q_i$ | QoS aggregation chain | GA + NN surrogate |
| 03 | $f_{fluct}(x) = \alpha \bar{Q} + (1-\alpha)Q_{stab}$ | Time-series validation | Modified GA |
| 04 | $f(x) = \beta \cdot QoS + (1-\beta) \cdot SC$ | Spatial optimization | GA + ML |
| 06 | $L_{DQN} = (Y - Q)^2$ | Meta-heuristic switching | DQN + GA/PSO/SA/ABC |
| 07 | $X_{new} = X + V_{levy}$ | Swarm optimization | DFA + PSO + Levy |
| 08 | $Q(s,a) \leftarrow Q + \alpha[r + \gamma \max Q' - Q]$ | Sequential decisions | Q-learning |
| 09 | $x_1 \succ x_2 \iff \forall i f_i(x_1) \leq f_i(x_2)$ | Pareto optimization | Multi-objective GA |
| 10 | $U_p = \pi - c$, $U_u = v - \pi$ | Market equilibrium | Game theory |
| 14 | $C_{new} = C + \alpha \Delta E \cdot \mathbb{I}(\Delta E > \delta)$ | Fluid adaptation | Dynamic update |
| 15 | $\hat{p}(t+\tau) = p + v\tau + \frac{1}{2}a\tau^2$ | Proactive planning | Trajectory prediction |
| 16 | $Capacity(t) = \sum capacity \cdot elasticity$ | Elastic pool | GA + adaptation |
| 17 | $L = (r + \gamma Q(s', \max Q') - Q)^2$ | Trajectory-aware MDP | Double DQN |

---

## Conclusion

The mathematical foundations across the 17 papers demonstrate a progression from classical optimization (genetic algorithms, particle swarm) to learning-based approaches (Q-learning, deep RL) and hybrid methods. Key mathematical patterns include:

1. **Fitness functions** using weighted QoS aggregation with penalty terms
2. **RL formulations** using Bellman equations for state-action value updates
3. **Multi-objective optimization** using Pareto dominance relations
4. **Adaptation mechanisms** using threshold-triggered dynamic updates
5. **Prediction models** using trajectory estimation and ML approximations

Significant mathematical gaps remain in convergence theory, optimality bounds, and uncertainty quantification, presenting opportunities for future research.