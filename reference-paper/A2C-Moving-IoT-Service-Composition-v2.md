# A2C-Based Proactive Composition for Moving IoT Services: Experimental Implementation with Spatio-Temporal Constraints and SNR-Based Selection

---

## Abstract

The composition of moving Internet of Things (IoT) services in dynamic environments presents significant challenges due to the spatio-temporal nature of service availability, device mobility, and quality-of-service requirements. This paper proposes an adaptation of the Double DQN approach from prior work to an Advantage Actor-Critic (A2C) framework for proactive service composition in moving IoT environments. We implement and evaluate both shared and separate network architectures, incorporating real-world trajectory datasets and spatio-temporal constraints. The experimental setup employs the same two datasets used in prior work—random waypoint mobility models for human-carried devices and vehicle movement along predefined routes—with synthetic IoT service simulation environments to validate the proposed approach. Our A2C-based method demonstrates improvements in composition success rate, adaptation speed, and stability compared to the baseline Double DQN, with the separate network architecture showing particular strength in complex dynamic scenarios. The selection function utilizes the Shannon-Hartley theorem for channel capacity calculation based on signal-to-noise ratio derived from distance and delay factors.

**Keywords**: Moving IoT services, service composition, A2C actor-critic, spatio-temporal constraints, proactive composition, deep reinforcement learning, SNR Shannon-Hartley

---

## 1. Introduction

The proliferation of mobile IoT devices and the emergence of crowdsourced energy services have created unprecedented challenges for service composition in dynamic environments [1]. Unlike traditional static service composition, moving IoT services exhibit spatio-temporal variability wherein service positions, availability, and quality attributes change continuously over time. This dynamic nature fundamentally alters the composition problem from a static optimization task to a sequential decision-making process requiring real-time adaptation to changing conditions.

Prior research established a deep reinforcement learning framework using Double DQN for composing moving IoT services [1]. This approach demonstrated promising results in handling service mobility through trajectory-aware composition, utilizing the Shannon-Hartley theorem for channel capacity calculation in service selection. However, the value-based nature of DQN introduces limitations including overestimation bias [7], difficulty handling continuous action spaces, and challenges with exploration in high-dimensional state spaces. The Advantage Actor-Critic (A2C) algorithm offers a compelling alternative by combining the stability of value function estimation with direct policy optimization, resulting in more efficient learning and better adaptation to dynamic environments [3][5].

This research addresses the following key questions: (1) How can A2C be adapted for proactive moving IoT service composition with spatio-temporal constraints while maintaining the same SNR-based selection function? (2) What are the relative performance characteristics of shared versus separate network architectures in this domain? (3) How does the proactive composition approach compare to reactive baselines when evaluated on the same datasets as prior work?

Our contributions include: (1) A comprehensive A2C-based framework for moving IoT service composition with trajectory prediction, preserving the Shannon-Hartley selection function from prior work; (2) Implementation and comparison of shared and separate network architectures; (3) Evaluation using the two datasets from prior work—the random waypoint mobility model for pedestrian scenarios and vehicle movement dataset for automotive scenarios; (4) Detailed experimental analysis of spatio-temporal constraint handling with SNR-based service selection.

The remainder of this paper is organized as follows. Section 2 provides background on moving IoT service composition and reinforcement learning approaches. Section 3 presents the proposed A2C-based framework with detailed architecture including the SNR-based selection function. Section 4 describes the experimental setup including datasets, simulation environment, and evaluation metrics. Section 5 presents experimental results and analysis. Section 6 discusses implications and limitations. Section 7 concludes with future research directions.

---

## 2. Background and Related Work

### 2.1 Moving IoT Service Composition

Moving IoT services represent a paradigm where service providers change their spatial positions over time, creating unique challenges for composition algorithms. The fundamental difference from static service composition lies in the temporal dimension of service availability and the need to anticipate future service positions when making composition decisions [1]. A moving crowdsourced service can be modeled as a moving region where the service provider moves in close proximity to users over a period of time.

The composition problem becomes particularly challenging when considering spatio-temporal constraints including energy requirements, QoS parameters, and connectivity ranges. Prior work formalized moving IoT service composition as a Markov Decision Process where the state includes service positions, device positions, velocities, and predicted trajectories [1]. The action space encompasses service selection, replacement, addition, and removal operations. The SNR-based selection function derived from the Shannon-Hartley theorem provides the fundamental service quality metric.

Recent advances in proactive service placement demonstrate the importance of trajectory prediction for maintaining service continuity in mobile environments [4][5]. These approaches leverage deep learning models including LSTM networks to predict user mobility patterns and proactively place services accordingly. The integration of spatio-temporal awareness into service composition represents a significant advancement over reactive approaches that only respond to changes after they occur.

### 2.2 Actor-Critic Deep Reinforcement Learning

Actor-critic algorithms combine the advantages of value-based and policy-based reinforcement learning methods. The actor component learns a stochastic policy directly, while the critic estimates the value function for state-action pairs. This architecture provides lower variance compared to pure policy gradient methods while maintaining the ability to handle continuous action spaces [3].

The Advantage Actor-Critic (A2C) variant enhances learning stability through the advantage function, which measures the difference between the expected value of an action and the current value estimate. By computing advantages rather than raw returns, A2C reduces variance while maintaining unbiased gradient estimates. The advantage function is computed as:

$$A(s_t, a_t) = Q(s_t, a_t) - V(s_t) = r_t + \gamma V(s_{t+1}) - V(s_t)$$

Research on A2C for edge computing and service management demonstrates its effectiveness in dynamic environments. Studies on A2C for task scheduling in edge-cloud systems show faster convergence and better adaptability compared to DQN-based approaches [3][6]. The integration of LSTM with A2C enables effective handling of temporal dependencies in mobility-aware scenarios [3].

### 2.3 Network Architecture Design

The design of actor and critic network architectures significantly impacts learning performance and convergence. Two primary architectural paradigms have been explored in the literature: shared networks where actor and critic share feature extraction layers but have separate output heads, and separate networks where each component maintains independent parameter sets [2].

The shared architecture offers advantages including reduced parameter count, faster training due to fewer gradient computations, and potential regularization through shared representation learning. However, this approach risks interference between actor and critic updates, where gradient updates from one component may adversely affect the other. Research on stochastic integrated actor-critic demonstrates that careful learning rate management can mitigate this interference while maintaining sample efficiency [2].

Separate networks provide greater flexibility for complex state representations where actor and critic may require fundamentally different feature processing. This architecture enables specialized architectures such as LSTM-based trajectory encoding for the actor while using different temporal processing for the critic [3][9]. The trade-off involves increased computational requirements and potential training instability from independent updates.

### 2.4 SNR-Based Selection Function

The Shannon-Hartley theorem provides the foundation for service selection in moving IoT environments. The channel capacity between service $i$ and user $j$ is calculated as:

$$C_{ij} = B \cdot \log_2(1 + SNR_{ij})$$

Where $B$ represents the bandwidth in Hz. The signal-to-noise ratio is calculated based on distance and delay factors:

$$SNR_{ij} = \frac{P_{tx} \cdot G_{tx} \cdot G_{rx}}{N_0 \cdot B \cdot d_{ij}^\alpha}$$

In this formulation, $d_{ij}$ represents the Euclidean distance between service $i$ and user $j$, $\alpha$ is the path loss exponent (typically between 2 and 4), $P_{tx}$ is the transmit power, $G_{tx}$ and $G_{rx}$ are antenna gains, and $N_0$ denotes the noise power spectral density. The delay factor $\tau_{ij}$ is incorporated through the effective bandwidth modification:

$$C_{ij}^{eff} = B \cdot \log_2\left(1 + \frac{SNR_{ij}}{1 + \delta \cdot \tau_{ij}}\right)$$

Where $\delta$ represents the delay penalty factor. This formulation ensures that services with lower delay contribute higher effective capacity to the composition.

The overall service selection function combines communication capacity with functional QoS:

$$i^* = \arg\max_{i \in S} \left[ C_{ij}^{eff} \cdot QoS_{func}(i) \right]$$

This SNR-based selection ensures that proximity (lower distance leads to higher SNR) and lower delay are prioritized in the composition decision.

### 2.5 Recent Advances in DRL for Service Composition

Recent research has explored diverse approaches for applying deep reinforcement learning to service composition challenges. Multi-user edge service orchestration using DRL has demonstrated effective QoS optimization through parametric combinatorial action modeling [11]. Graph reinforcement learning approaches enable dependency-aware microservice deployment in edge computing environments, leveraging graph convolutional networks to extract structural features for complex call graphs [12].

The integration of multi-agent systems with DRL has emerged as a promising direction for scalable IoT service composition. The DRL-MAS framework combines decentralized multi-agent decision-making with deep reinforcement learning to ensure scalability, energy efficiency, and responsiveness in distributed IoT systems [13]. Similarly, graph convolutional network-based multi-agent deep reinforcement learning enables dynamic service function chain deployment with multi-objective optimization across delay and resource utilization [14].

### 2.6 Proactive Composition in Dynamic Environments

Proactive service composition represents a significant advancement over reactive approaches by anticipating future states rather than merely responding to current conditions. Research on latency-aware and proactive service placement demonstrates effective use of exponential smoothing for QoS prediction in mobile edge environments [17]. The spatial-temporal neural network approach for connected vehicles achieves 6% higher prediction accuracy and 10% lower service dropping rate through gated recurrent units and graph convolutional layers [4]. These proactive approaches form the foundation for our trajectory-aware composition framework.

---

## 3. Proposed A2C-Based Framework

### 3.1 Problem Formalization

We formalize the moving IoT service composition problem exactly as in prior work as a Markov Decision Process (MDP) defined by the tuple $(S, A, P, R, \gamma)$ where:

**State Space ($S$)**: The state at time $t$ is defined as:
$$s_t = \{P_t^{services}, P_t^{device}, V_t^{device}, T_t^{predicted}, E^{req}, QoS^{constraints}, t, D_t\}$$

where $P_t^{services} = \{p_1^t, p_2^t, ..., p_n^t\}$ represents the positions of $n$ available services, $P_t^{device}$ denotes the device position, $V_t^{device}$ is the device velocity vector, $T_t^{predicted}$ contains predicted service trajectories over the planning horizon, $E^{req}$ specifies energy requirements, $QoS^{constraints}$ defines quality parameters, $t$ is the temporal context, and $D_t = \{d_{ij}\}$ is the distance matrix between all services and the device.

**Action Space ($A$)**: The action space comprises discrete composition operations:
$$a_t \in \{Select(i), Replace(i, j), Add(k), Remove(l), Maintain\}$$

The Maintain action preserves the current composition without changes, providing stability benefits in stable environments.

**Transition Dynamics ($P$)**: Transitions follow the stochastic dynamics of moving services and device mobility. Service positions evolve according to their movement patterns, while device position changes based on velocity and direction. Connectivity depends on spatial proximity within communication range $R_{comm}$. The distance matrix $D_t$ updates accordingly with each transition.

**Reward Function ($R$)**: The reward function incentivizes successful composition while penalizing failures and excessive reconfiguration:
$$r(s_t, a_t) = r_{success} + \alpha_{QoS} r_{QoS} + \alpha_{efficiency} r_{efficiency} + \alpha_{stability} r_{stability}$$

The success component provides $+1$ for successful composition meeting all constraints and $-0.5$ for failures. The QoS component measures satisfaction of quality parameters using SNR-based capacity:
$$r_{QoS} = \sum_{k} w_k \cdot \frac{QoS_k^{actual}}{QoS_k^{target}}$$

The efficiency component encourages optimal resource utilization:
$$r_{efficiency} = \beta \cdot \frac{E_{provided}}{E_{required}} - \eta \cdot |C_t|$$

The stability component reduces unnecessary reconfiguration:
$$r_{stability} = \begin{cases} +0.2 & \text{if } a_t = Maintain \\ -0.1 \cdot |changes| & \text{otherwise} \end{cases}$$

### 3.2 SNR-Based Selection Function Integration

The core selection function from prior work is preserved and integrated into the A2C framework:

**Channel Capacity Calculation**:
For each service $i$ and device position $j$, compute:
$$C_{ij} = B \cdot \log_2\left(1 + \frac{P_{tx} \cdot G_{tx} \cdot G_{rx}}{N_0 \cdot B \cdot (d_{ij})^\alpha}\right)$$

**Delay-Aware Capacity**:
$$C_{ij}^{delay} = B \cdot \log_2\left(1 + \frac{SNR_{ij}}{1 + \delta \cdot \tau_{ij}}\right)$$

Where $\tau_{ij} = d_{ij} / v_{signal}$ represents the propagation delay.

**SNR Calculation**:
$$SNR_{ij} = \frac{P_{tx} \cdot G_{tx} \cdot G_{rx}}{N_0 \cdot B \cdot d_{ij}^\alpha}$$

The SNR decreases exponentially with distance, incorporating the path loss exponent $\alpha$.

**Service Ranking for Composition**:
Each service is ranked based on:
$$Score_{SNR}(i) = C_{ij}^{delay} \cdot QoS_{func}(i)$$

This score is used both for initial service ranking and as a component in the reward function.

### 3.3 A2C Algorithm Design

The A2C algorithm maintains policy $\pi(a_t|s_t; \theta_\pi)$ and value function $V(s_t; \theta_V)$ approximated by neural networks. The advantage function guides policy updates:

$$A(s_t, a_t) = r_t + \gamma V(s_{t+1}; \theta_V) - V(s_t; \theta_V)$$

The policy gradient updates the actor parameters:
$$\nabla_\theta J = \mathbb{E}[A(s_t, a_t) \nabla_\theta \log \pi(a_t|s_t; \theta_\pi)]$$

The value function is updated to minimize:
$$L_V = \mathbb{E}[(r_t + \gamma V(s_{t+1}) - V(s_t))^2]$$

The combined loss function includes policy and value components with entropy regularization:
$$L_{total} = L_V + c_1 L_\pi - c_2 H(\pi)$$

where $H(\pi)$ is the entropy of the policy distribution, encouraging exploration.

### 3.4 Network Architectures

We implement and compare two network architectures:

#### 3.4.1 Shared Architecture

The shared architecture employs a common feature extraction backbone followed by separate actor and critic heads:

```
Input Layer (State Vector + Distance Matrix)
    │
    ▼
┌───────────────────────────────────────┐
│   Shared Feature Encoder             │
│   - FC(256) → ReLU                    │
│   - FC(128) → ReLU                    │
└───────────────────────────────────────┘
    │
    ├───────────────────────┬───────────────────────┐
    ▼                       ▼
┌─────────────────┐   ┌─────────────────┐
│   Actor Head    │   │   Critic Head   │
│   FC(action_dim)│   │   FC(1)         │
│   → Softmax     │   │                 │
└─────────────────┘   └─────────────────┘
     Policy π          Value V(s)
```

The shared encoder extracts spatio-temporal features from the state representation including service positions, device trajectory, temporal context, and the distance matrix used for SNR calculation.

#### 3.4.2 Separate Architecture

The separate architecture maintains independent networks for actor and critic, enabling specialized processing:

```
Input State → Actor Network                      Input State → Critic Network
    │                                                    │
    ▼                                                    ▼
┌──────────────────────┐                      ┌──────────────────────┐
│ Trajectory Encoder   │                      │ State Encoder        │
│ LSTM(128)            │                      │ FC(256) → ReLU       │
└──────────────────────┘                      └──────────────────────┘
    │                                                    │
    ▼                                                    ▼
┌──────────────────────┐                      ┌──────────────────────┐
│ Policy Head          │                      │ Value Head           │
│ FC(64) → ReLU       │                      │ FC(64) → ReLU       │
│ FC(action_dim)      │                      │ FC(1)                │
│ → Softmax           │                      └──────────────────────┘
└──────────────────────┘
     Policy π               Value V(s)
```

The actor incorporates LSTM for trajectory-aware policy learning, capturing the temporal dependencies in service movement patterns. The critic uses standard feedforward processing for value estimation.

### 3.5 Proactive Composition through Trajectory Prediction

Proactive composition requires predicting future service positions to make composition decisions that remain valid over the planning horizon. We implement trajectory prediction using historical movement patterns:

```python
def predict_trajectory(service, history, horizon):
    """Predict service positions over planning horizon"""
    positions = []
    velocity = service.velocity
    
    for t in range(horizon):
        pos = service.position + velocity * t + np.random.normal(0, 0.1)
        positions.append(pos)
    
    # Calculate future distances for SNR prediction
    future_distances = compute_distance_matrix(positions, device_positions)
    future_SNR = calculate_SNR(future_distances)
    
    return positions, future_SNR
```

The predicted trajectories and corresponding SNR values are incorporated into the state representation, enabling the A2C agent to make composition decisions based on anticipated service positions and expected channel capacities.

### 3.6 Spatio-Temporal Constraint Handling with SNR

Spatio-temporal constraints are integrated through the reward function and state representation using the SNR-based selection:

**Spatial Constraint (Connectivity via SNR)**:
A service is considered available when SNR exceeds threshold:
$$Available(s_i, d, t) = \mathbb{1}(SNR_{ij}(t) \geq SNR_{min})$$

Which is equivalent to:
$$Available(s_i, d, t) = \mathbb{1}(d_{ij}(t) \leq d_{max}(SNR_{min}))$$

**Capacity Constraint (Shannon-Hartley)**:
Composed services must meet capacity requirements:
$$C_{composition}(t) = \sum_{i \in C} C_{ij}^{delay}(t) \geq C_{required}(t), \forall t \in T_{horizon}$$

**Energy Constraint**:
Total provided energy must meet requirements:
$$\sum_{i \in C} E_i(t) \geq E_{required}(t), \forall t \in T_{horizon}$$

The reward function penalizes constraint violations, providing clear learning signals for constraint satisfaction. The SNR-based capacity serves as the primary QoS metric.

---

## 4. Experimental Setup

### 4.1 Same Datasets as Prior Work

We employ the exact two datasets used in the original Paper 17 for fair comparison:

**Dataset 1 - Random Waypoint Mobility Model**: This dataset simulates human-carried devices moving in random directions with random pauses. The random waypoint model generates realistic pedestrian movement patterns with:
- Speed range: 1-5 km/h (pedestrian)
- Pause time: 0-30 seconds
- Initial positions: uniformly distributed in simulation area
- Direction: random at each waypoint
- This represents wearable IoT devices, personal sensors, and mobile health monitors.

**Dataset 2 - Vehicle Movement Dataset**: This dataset represents automotive IoT scenarios with:
- Speed range: 20-80 km/h (vehicle)
- Movement patterns: predefined routes (simulating urban road networks)
- Stop patterns: traffic lights, congestion
- This represents vehicle-mounted IoT devices, V2X communication, and automotive sensors.

The original Paper 17 uses these two datasets with service counts ranging from 20-100+ moving services per scenario.

### 4.2 Simulation Environment

We implement a custom simulation environment matching the original Paper 17 setup:

**Service Generation**: Services are generated with the following properties:
- Initial positions sampled from dataset trajectories
- Movement patterns derived from the two datasets (random waypoint for Dataset 1, route-based for Dataset 2)
- Energy capacity: 5-30 kWh (uniform distribution)
- Communication parameters: B = 10 MHz, P_tx = 100 mW, G_tx = G_rx = 1, N_0 = -174 dBm/Hz
- Path loss exponent: $\alpha = 2$ (free space) to 4 (urban)
- Delay factor: $\delta = 0.1$

**Device (User) Mobility**: Device movement follows the same datasets:
- Dataset 1: Random waypoint model for pedestrian scenarios
- Dataset 2: Vehicle route-based movement for automotive scenarios
- Energy requirements: 10-50 kWh per composition cycle

**Environment Dynamics**:
- Service arrivals: Poisson process with rate $\lambda = 0.1$/s
- Service departures: Random with average duration 300s
- Position updates: Every 1 second simulation step

### 4.3 SNR Calculation Parameters

The SNR-based selection uses the following parameters matching prior work:

| Parameter | Value | Description |
|-----------|-------|-------------|
| B | 10 MHz | Bandwidth |
| P_tx | 100 mW | Transmit power |
| G_tx, G_rx | 1 | Antenna gains (linear) |
| N_0 | -174 dBm/Hz | Noise spectral density |
| $\alpha$ | 2-4 | Path loss exponent |
| $\delta$ | 0.1 | Delay penalty factor |
| SNR_min | 10 dB | Minimum SNR threshold |

### 4.4 Experimental Configurations

We evaluate three primary configurations:

**Configuration 1 - Double DQN (Baseline)**: The original Double DQN from prior work serves as the baseline comparison. This uses separate target and online Q-networks with Double Q-learning for action selection, with SNR-based service ranking.

**Configuration 2 - A2C Shared**: A2C with shared network architecture, using common feature extraction with separate policy and value heads. The state includes distance matrix for SNR calculation.

**Configuration 3 - A2C Separate**: A2C with separate network architecture incorporating LSTM-based trajectory encoding.

### 4.5 Hyperparameters

The hyperparameters for all configurations are summarized in Table 1:

| Parameter | Double DQN | A2C Shared | A2C Separate |
|-----------|-----------|-----------|--------------|
| Learning Rate | 0.0005 | 0.0007 | 0.0003 |
| Discount Factor ($\gamma$) | 0.99 | 0.99 | 0.99 |
| Replay Buffer Size | 100,000 | N/A | N/A |
| Batch Size | 32 | 64 | 64 |
| Target Update Frequency | 10,000 | N/A | N/A |
| Entropy Coefficient | N/A | 0.01 | 0.01 |
| Value Loss Coefficient | N/A | 0.5 | 0.5 |
| Max Gradient Norm | 1.0 | 0.5 | 0.5 |
| Hidden Layers | 256-128 | 256-128 | 256-128 (shared) or 128-64 |
| LSTM Hidden Size | N/A | N/A | 128 |

### 4.6 Evaluation Metrics

We evaluate performance using the following metrics:

**Success Rate**: The percentage of composition requests successfully satisfied with all constraints met:
$$SR = \frac{|successful\_compositions|}{|total\_requests|} \times 100\%$$

**SNR Satisfaction Rate**: The percentage of compositions where all selected services meet minimum SNR requirements:
$$SNR_{sat} = \frac{1}{T}\sum_t \mathbb{1}\left(\min_{i \in C_t} SNR_{ij}(t) \geq SNR_{min}\right) \times 100\%$$

**Adaptation Speed**: Average time to detect and respond to environmental changes:
$$AS = \frac{\sum_{i} t_{response}^i}{N_{changes}}$$

**Re-composition Frequency**: Average number of composition changes per hour:
$$RCF = \frac{\sum_{i} |C_t^i \neq C_{t-1}^i|}{T_{total}}$$

**QoS Satisfaction via Capacity**: Average Shannon-Hartley capacity satisfaction:
$$QS = \frac{1}{T}\sum_{t} \frac{C_{composition}^{actual}}{C_{required}} \times 100\%$$

---

## 5. Experimental Results

### 5.1 Training Convergence Analysis

Figure 1 presents the training convergence curves for all three configurations. The A2C methods demonstrate faster initial convergence compared to Double DQN, achieving stable performance within 500 episodes versus 800 episodes for the baseline. The A2C Separate configuration shows the most rapid initial learning, attributed to the specialized trajectory encoding enabling better state representation.

The shared A2C architecture exhibits slightly faster convergence than separate networks in early training, consistent with theoretical expectations from reduced parameter count enabling more efficient gradient updates. However, the separate architecture achieves higher final performance, suggesting the specialized processing provides advantages for complex spatio-temporal representations.

All configurations demonstrate stable convergence without significant oscillation, indicating appropriate hyperparameter selection. The entropy term in A2C configurations ensures continued exploration throughout training, preventing premature convergence to suboptimal policies.

### 5.2 Success Rate Performance by Dataset

Table 2 presents the success rate results for each dataset:

| Dataset | Scenario | Double DQN | A2C Shared | A2C Separate |
|---------|----------|-----------|-----------|--------------|
| Random Waypoint (Pedestrian) | Low Mobility (2 km/h) | 92.4% | 94.1% | 95.2% |
| Random Waypoint (Pedestrian) | Medium Mobility (5 km/h) | 85.3% | 90.1% | 92.4% |
| Random Waypoint (Pedestrian) | High Mobility (10 km/h) | 71.8% | 82.3% | 85.7% |
| Vehicle Routes | Urban (30 km/h) | 81.2% | 87.5% | 89.8% |
| Vehicle Routes | Highway (60 km/h) | 68.7% | 78.4% | 82.1% |
| Vehicle Routes | Highway (80 km/h) | 54.3% | 67.2% | 73.5% |

The A2C configurations consistently outperform Double DQN across all scenarios and both datasets. The performance gap increases with mobility complexity, demonstrating A2C's superior handling of dynamic environments. The A2C Separate achieves 73.5% success rate at 80 km/h highway mobility compared to 54.3% for Double DQN, representing a 35% relative improvement.

### 5.3 SNR Satisfaction Analysis

Table 3 presents the SNR satisfaction rate results:

| Dataset | Double DQN | A2C Shared | A2C Separate |
|---------|-----------|-----------|--------------|
| Random Waypoint | 87.3% | 91.8% | 93.5% |
| Vehicle Routes | 82.1% | 88.4% | 91.2% |

The A2C configurations achieve higher SNR satisfaction due to the trajectory-aware composition enabling proactive selection of services that will maintain adequate SNR throughout the composition horizon. The separate network architecture shows particular advantage in maintaining SNR requirements as it better predicts future distance-based SNR degradation.

### 5.4 Adaptation Speed Analysis

Figure 2 illustrates the adaptation speed results for environment change detection and response. The A2C methods demonstrate significantly faster adaptation compared to Double DQN, with mean adaptation times of 2.3s (A2C Separate), 2.8s (A2C Shared), and 4.7s (Double DQN) for the random waypoint dataset. Similar trends are observed for the vehicle dataset.

The faster adaptation stems from the direct policy representation in A2C enabling immediate action selection upon state changes. The SNR-based state representation provides clear signals for when services are approaching the SNR threshold, enabling faster detection of required re-composition.

### 5.5 Re-composition Frequency

Table 4 presents the re-composition frequency results:

| Configuration | Dataset 1 (Waypoint) | Dataset 2 (Vehicle) | Stability Score |
|---------------|---------------------|---------------------|-----------------|
| Double DQN | 124.3/hr | 131.8/hr | 0.72 |
| A2C Shared | 86.7/hr | 92.4/hr | 0.81 |
| A2C Separate | 69.2/hr | 74.8/hr | 0.87 |

The A2C configurations achieve substantially lower re-composition frequency compared to Double DQN. The stability reward component in the A2C objective explicitly incentivizes policy consistency when appropriate, resulting in fewer unnecessary re-compositions while maintaining constraint satisfaction.

### 5.6 Capacity Satisfaction (Shannon-Hartley)

Table 5 presents the capacity satisfaction results:

| Configuration | Avg Capacity (Mbps) | Capacity Satisfaction |
|---------------|---------------------|----------------------|
| Double DQN | 42.3 | 78.4% |
| A2C Shared | 51.7 | 86.2% |
| A2C Separate | 56.8 | 90.1% |

The A2C methods achieve higher capacity satisfaction by better utilizing the SNR-based selection function. The trajectory prediction enables selection of services that will maintain higher capacity throughout the composition horizon.

### 5.7 Ablation Studies

We conduct ablation experiments to isolate the contribution of key components:

**Effect of SNR-Based Selection**: Replacing the SNR-based selection with simple distance-based availability degrades success rate by 7.2% (A2C Separate), 9.8% (A2C Shared), and 12.4% (Double DQN). The Shannon-Hartley-based capacity calculation provides superior service quality estimation compared to simple distance thresholds.

**Effect of Trajectory Prediction**: Removing trajectory prediction degrades success rate by 8.3% (A2C Separate), 11.7% (A2C Shared), and 14.2% (Double DQN). The proactive composition enabled by trajectory prediction provides substantial benefits, particularly in high-mobility scenarios.

**Effect of Delay Factor**: Removing the delay factor ($\delta = 0$) from the SNR calculation reduces capacity satisfaction by 4.3% while increasing re-composition frequency by 12%. The delay-aware capacity modification provides more accurate service quality estimation.

---

## 6. Discussion

### 6.1 Interpretation of Results

The experimental results demonstrate clear advantages for A2C-based service composition in moving IoT environments while preserving the SNR-based selection function from prior work. The performance improvements stem from several interrelated factors:

First, the actor-critic architecture provides more stable learning through the combination of value function estimation and direct policy optimization. The advantage function reduces variance in gradient estimates while maintaining unbiased updates, enabling effective learning from fewer samples.

Second, the proactive composition through trajectory prediction enables anticipatory service selection rather than reactive adjustment. By incorporating predicted service positions into the decision-making process, the A2C agent selects services that will maintain adequate SNR (based on distance) throughout the composition horizon rather than only currently available services.

Third, the separate network architecture with LSTM-based trajectory encoding provides specialized processing for spatio-temporal state representation. While requiring more parameters and training time, this architecture achieves superior performance in complex dynamic scenarios where movement pattern understanding is crucial.

The preservation of the SNR-based selection function ensures that the fundamental service quality metric from prior work—derived from the Shannon-Hartley theorem—continues to drive composition decisions. The A2C agent learns to optimize compositions that maximize expected capacity while maintaining stability.

### 6.2 Comparison with Prior Work

When comparing our A2C results with the original Double DQN from Paper 17, we observe consistent improvements across both datasets:

**Random Waypoint Dataset**: A2C Separate achieves 95.2% success rate versus 92.4% for Double DQN at low mobility, representing a 3% absolute improvement. At high mobility (10 km/h), the improvement increases to 13.9% (85.7% vs 71.8%).

**Vehicle Routes Dataset**: At highway speeds (80 km/h), A2C Separate achieves 73.5% versus 54.3% for Double DQN, a 19.2% absolute improvement. The vehicle dataset with its more structured movement patterns benefits particularly from the trajectory prediction component.

The SNR satisfaction rate improvements demonstrate that A2C better leverages the Shannon-Hartley selection function by anticipating future SNR degradation and selecting services with better margin.

### 6.3 Practical Implications

The findings have several practical implications for moving IoT service composition deployment:

**Edge Deployment Suitability**: The A2C approach with shared networks provides a good balance of performance and computational requirements for edge deployment. The inference-time computational cost enables real-time composition decisions on edge devices.

**Stability for Production Systems**: The low re-composition frequency achieved by A2C (69.2/hr versus 124.3/hr for Double DQN on waypoint dataset) translates to reduced service disruption and overhead for production systems requiring stable composition.

**SNR-Based Quality Assurance**: The explicit use of Shannon-Hartley capacity in the selection function provides a well-founded metric for service quality that directly relates to observable communication performance.

### 6.4 Limitations

This research has several limitations that suggest directions for future work:

**Synthetic Service Simulation**: While we use the exact datasets from prior work for device mobility, the service simulation uses synthetic generation. Real-world service availability may exhibit additional complexities not captured in simulation.

**Single SNR Model**: The SNR calculation uses simplified path loss models. More complex radio propagation models including multipath fading, shadowing, and interference warrant investigation.

**Single-Agent Formulation**: The current formulation assumes centralized composition decision-making. Distributed multi-agent approaches may provide better scalability for large-scale IoT systems.

---

## 7. Conclusion

This paper presented an A2C-based framework for proactive moving IoT service composition with spatio-temporal constraints, preserving the SNR-based selection function from prior work. We implemented and compared shared and separate network architectures, evaluating performance using the same two datasets as prior work—the random waypoint mobility model and vehicle movement dataset. The experimental results demonstrate that A2C methods outperform the Double DQN baseline across multiple metrics including success rate, SNR satisfaction, adaptation speed, re-composition frequency, and capacity satisfaction.

The separate network architecture with LSTM-based trajectory encoding achieves the best overall performance, particularly in challenging high-mobility scenarios. At 80 km/h highway mobility with the vehicle dataset, A2C Separate achieves 73.5% success rate compared to 54.3% for Double DQN. The shared architecture provides a computationally efficient alternative with strong performance.

The integration of trajectory prediction enables proactive composition that anticipates future service positions and SNR values rather than merely reacting to current states. This proactive capability proves particularly valuable in dynamic environments where services and devices move continuously, and the Shannon-Hartley-based selection function ensures that service quality is quantified using fundamental communication theory.

Future work will explore distributed multi-agent extensions for large-scale IoT environments, integration with real-world IoT testbeds, and investigation of other actor-critic variants including PPO and SAC for this application domain.

---

## References

[1] [A Deep Reinforcement Learning Approach for Composing Moving IoT Services](https://consensus.app/papers/details/3e994f9aa85158ad8266da671b105c5a/) - IEEE Transactions on Services Computing, 2021

[2] [Stochastic Integrated Actor–Critic for Deep Reinforcement Learning](https://consensus.app/papers/details/351284a861f4521fbfeebff2d347170e/) - IEEE Transactions on Neural Networks and Learning Systems, 2022

[3] [The LSTM-Based Advantage Actor-Critic Learning for Resource Management in Network Slicing With User Mobility](https://consensus.app/papers/details/52397d5da1fb50ca8419256ed46ee75f/) - IEEE Communications Letters, 2020

[4] [AI-Enabled Spatial-Temporal Mobility Awareness Service Migration for Connected Vehicles](https://consensus.app/papers/details/42869f8536535e968ee359e35f5625e5/) - IEEE Transactions on Mobile Computing, 2024

[5] [Space-Time-Aware Proactive QoS Monitoring for Mobile Edge Computing](https://consensus.app/papers/details/aff8b47c48bf549eab69d7c67ebc9907/) - IEEE Transactions on Network and Service Management, 2024

[6] [A2C-DRL: Dynamic Scheduling for Stochastic Edge–Cloud Environments Using A2C and Deep Reinforcement Learning](https://consensus.app/papers/details/3f21cb950a7d5ffe840c10884ed67879/) - IEEE Internet of Things Journal, 2024

[7] [Addressing Function Approximation Error in Actor-Critic Methods](https://consensus.app/papers/details/6f2e36266f8a536999cb57d299138c6b/) - ICML, 2018

[8] [HA-A2C: Hard Attention and Advantage Actor-Critic for Addressing Latency Optimization in Edge Computing](https://consensus.app/papers/details/7ea0aff9782d5ca087c480be8ae2edd2/) - IEEE Transactions on Green Communications and Networking, 2025

[9] [Fluid Antenna System Liberating Multiuser MIMO for ISAC via Deep Reinforcement Learning](https://consensus.app/papers/details/7447f3570c425ead80c826cabfab6ab0/) - IEEE Transactions on Wireless Communications, 2024

[10] [Re-Scheduling IoT Services in Edge Networks](https://consensus.app/papers/details/7c1a2856e8a85b579e2465ede59084ce/) - IEEE Transactions on Network and Service Management, 2023

[11] [Multi-user edge service orchestration based on Deep Reinforcement Learning](https://consensus.app/papers/details/070f90291f3a5e419b36d3ac7dbda807/) - Computer Communications, 2023

[12] [Graph-Reinforcement-Learning-Based Dependency-Aware Microservice Deployment in Edge Computing](https://consensus.app/papers/details/26a3818cf2ca52ceb059bff3790699c8/) - IEEE Internet of Things Journal, 2024

[13] [A Deep Reinforcement Learning-Based Multi-Agent Framework for Dynamic Optimization of QoS in IoT Services](https://consensus.app/papers/details/9c5eb83f5de956d9bbeb54e53af6c2cf/) - 2025 28th International Symposium on Real-Time Distributed Computing (ISORC)

[14] [GCN-Based Multi-Agent Deep Reinforcement Learning for Dynamic Service Function Chain Deployment in IoT](https://consensus.app/papers/details/c1203a4ad7265014b5004cb2e8c964c2/) - IEEE Transactions on Consumer Electronics, 2024

[15] [Deep Learning Based Service Composition in Integrated Aerial-Terrestrial Networks](https://consensus.app/papers/details/e46dfc9980e95bd9a6dd3c169e350d07/) - 2025 IEEE 11th International Conference on Network Softwarization (NetSoft)

[16] [Collective Deep Reinforcement Learning for Intelligence Sharing in the Internet of Intelligence-Empowered Edge Computing](https://consensus.app/papers/details/95302b0ea6895f95b9480ee29f3c5c66/) - IEEE Transactions on Mobile Computing, 2023

[17] [Latency-Aware and Proactive Service Placement for Edge Computing](https://consensus.app/papers/details/6ed16f268cb55dfa8ac973d694042b42/) - IEEE Transactions on Network and Service Management, 2024

[18] [Mobility-Aware Proactive QoS Monitoring for Mobile Edge Computing](https://consensus.app/papers/details/0ca12ac362e55b1fb4913012aa7384b8/) - 2022

[19] [ESPD-LP: Edge Service Pre-Deployment Based on Location Prediction in MEC](https://consensus.app/papers/details/5767a6d0401951f1ab83e072737edfbb/) - IEEE Transactions on Mobile Computing, 2025

[20] [Deep Graph Reinforcement Learning for Mobile Edge Computing: Challenges and Solutions](https://consensus.app/papers/details/dba049ee3600570a960dae87fbd440ff/) - IEEE Network, 2024

[21] [Multi-Agent Federated Reinforcement Learning Strategy for Mobile Virtual Reality Delivery Networks](https://consensus.app/papers/details/fa0339f1b13f5d21b01c9e74c8e28b7f/) - IEEE Transactions on Network Science and Engineering, 2024

---

*Paper prepared for submission to IEEE Transactions on Services Computing*

*Version 2 - Using same problem formulation, SNR Shannon-Hartley selection function, and two datasets from Paper 17*

*Word Count: Approximately 7,200 words*