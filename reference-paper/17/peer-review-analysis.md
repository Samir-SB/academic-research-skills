# Peer Review Analysis: A Deep Reinforcement Learning Approach for Composing Moving IoT Services

## Overview

This paper addresses the challenge of composing IoT services in dynamic environments where services are mobile rather than static. The core problem is that traditional service composition approaches assume fixed service locations, but many real-world IoT scenarios involve moving devices that continuously change their spatial positions.

The paper develops a framework for discovering crowdsourced services that move in close proximity to a user over time. The key insight is that services must be both spatially and temporally valid—they must be within communication range at the exact time of service provisioning.

## Research Questions Answered

### 1. What is the specific problem this paper addresses?

The paper addresses three key research challenges:

1. **Connectivity**: A moving service must stay connected with a service provider (within connectivity proximity). This requires determining co-movement patterns between users and service trajectories.

2. **Service Continuity**: A service provider and user may not share their entire route—they may only overlap for part of the journey. The composition must select an optimal sequence of available moving services ensuring continuity.

3. **Indexing and Scalability**: Existing co-movement discovery methods rely on centralized index structures like R-trees, which degrade dramatically as datasets scale up.

### 2. What is the motivation scenario?

The paper uses WiFi hotspot sharing as the primary scenario. Users can share their smartphone WiFi as moving hotspots while strolling in a city. This creates the need to select and compose moving services that overlap with a user's trajectory to maintain continuous connectivity.

### 3. How does the paper model moving IoT services?

The paper defines:

- **Moving Crowdsourced Service (MS)**: A service provided by an IoT device moving in time, space, or both, modeled as a moving region described by a tuple of `<Ts, Rti(pi)>` where Ts is a service trajectory (sequence of timestamped samples) and Rti(pi) is the coverage region (circular area centered at pi with radius r at time ti).

- **User Trajectory (Tu)**: The path traveled by a user, represented as a set of k timestamped samples `<uti, uxi, uyi>`.

- **Valid Candidate Moving Service**: A moving service paired with the user trajectory over w consecutive timesteps (w > 0).

### 4. How is the state space defined?

The state space includes:
- Current user trajectory sample `<t, x, y>` 
- The agent observes the current user position as the state

### 5. What actions can the agent take?

The action space is discrete:
- Select a valid candidate moving service ID from available services
- Select a **dummy service** (when no valid candidates exist)

### 5.1 What is the purpose of the dummy service?

The dummy service handles the case when there are **no valid candidate services** available for a given user trajectory sample. This addresses two problematic scenarios:

1. **No valid candidates exist**: The user is in a location with no overlapping moving services
2. **Agent selects invalid service**: The agent picks a service that doesn't actually overlap with the user trajectory

The dummy service serves as a valid action the agent can take when no real services are available, preventing the agent from making impossible selections while still learning appropriate behavior:

- **Dummy service selected**: Reward = -1 (less severe, acknowledges "no service available")
- **Invalid service selected**: Penalty = -10 (more severe, teaches agent to avoid invalid selections)

This mechanism teaches the agent to prefer the dummy service (higher reward -1) over selecting an invalid service (punishment -10) when no real services are available.

### 6. What is the reward function?

The reward is based on QoS (capacity) provided by the selected service:
- Positive reward [0, 1] for valid service selection based on capacity
- Reward of -1 for selecting dummy service
- Penalty of -10 for selecting invalid service

The capacity is computed using the Shannon-Hartley theorem, directly proportional to signal strength. Signal strength uses an exponential attenuation model based on distance between user and service.

### 7. What algorithm is used?

The paper uses **Q-learning with Neural Networks** (basic deep Q-learning), NOT DQN or Double DQN. This is confirmed by multiple references in the paper:

- "The Q-learning's discount factor γ is set to 0.9" (experimental section)
- "We rely on the Q-Learning algorithm to learn the optimal execution policy"
- Figure labels refer to "Q-Learning Training Time" and "Q-Learning Testing Time"

**Algorithm Details (from Algorithm 1):**
- **Neural Network**: Dense fully connected, 3 hidden layers with 512 units each
- **Activation**: ReLU in hidden layers, dropout with probability 0.5
- **Learning rate**: 0.001
- **Discount factor (γ)**: 0.9
- **Exploration**: ε-greedy (ε starts at 1.0, decayed by 0.995)
- **Memory**: Basic buffer that stores transitions, trains when full
- **Training/Test split**: 70% / 30%

**What's NOT used:**
- No target network
- No explicit experience replay (just basic memory buffer)
- No Double DQN mechanism
- No prioritized experience replay

The term "deep reinforcement learning" in the paper refers to using a neural network for Q-function approximation (making it "deep" Q-learning), but it's still basic Q-learning implementation.

### 7.1 What are the hyper-parameters?

From the experimental section (6.1 Experiment Setup):

| Hyper-parameter | Value |
|-----------------|-------|
| **Neural Network Architecture** | Dense fully connected |
| **Hidden Layers** | 3 layers |
| **Neurons per Layer** | 512 |
| **Activation Function** | ReLU |
| **Dropout** | 0.5 (probability) |
| **Learning Rate** | 0.001 |
| **Discount Factor (γ)** | 0.9 |
| **Exploration (ε) Start** | 1.0 |
| **ε Decay** | 0.995 (multiplicative) |
| **Training/Test Split** | 70% / 30% |
| **Memory** | Basic buffer (trains when full) |

### 7.2 What is the state space?

From the paper (Section 4):

- **State Definition**: Each state s is a user trajectory sample `<t, x, y>` where:
  - t = timestamp
  - x = longitude coordinate
  - y = latitude coordinate

- **State Space (S)**: Finite set of user trajectory samples representing the user's position at each timestep

- **Initial State (s₀)**: First user trajectory sample
- **Terminal State (sᵣ)**: Last user trajectory sample

The agent observes the current user position (t, x, y) as the state input to the neural network.

### 7.3 What is the action space?

From the paper (Section 4, Definition 5):

- **Action Definition**: Each action represents selecting a **valid candidate moving service**

- **Action Space (A)**: Set of valid candidate moving service IDs available at the current state
  - Actions are replaced with "valid candidate moving services" (see Definition 4)
  - At each state, there is a set of moving services that could be selected

- **Special Actions**:
  - **Dummy Service**: Used when no valid candidates exist for a given user trajectory sample
  - **Invalid Service Selection**: Penalized with -10 reward

The neural network outputs are the possible actions (service IDs) that the agent can select at each state.

### 8. What assumptions are made?

From the paper (Section 3.1 Problem Formulation):

1. **One moving service can only serve one user at any point in time** - No sharing of services between multiple users simultaneously

2. **Constant speed between timestamps** - A moving service moves between any two consecutive timestamps ti and ti+1 with a constant speed. This allows determining the position of the moving service at any given time in the interval [ti, ti+1]. Other speed functions could be considered if the function for finding the moving service's location is constant time.

3. **Fixed coverage region radius** - Radii of all coverage regions of services are fixed to a single value. The region around each service is considered as a circular area with fixed radius.

4. **Deterministic trajectories** - Trajectories of services are deterministic (known in advance). There is a platform that incentivizes WiFi hotspot providers to follow certain assigned trajectories.

5. **Focus on pedestrian trajectories** - The paper focuses on the trajectories of pedestrians.

6. **WiFi hotspot services overlay digital maps** - The services are modeled to overlay digital maps.

7. **Equal bandwidth allocation** - Total available bandwidth is assumed to be equally allocated between different IoT service users.

8. **Fixed error rate** - The error rate is fixed. Increasing the capacity increases the signal strength, which leads to more successful transmissions.

9. **No prior knowledge of QoS** - The Q-learning algorithm does not have prior knowledge about QoS attributes of moving services since they are computed based on the distance between a user and a moving service.

10. **Consumers don't change trajectories** - The proposed framework neither assumes nor requires consumers to change their trajectories for better services.

### 8. How is service continuity/handover addressed?

The paper addresses continuity through:
- **Sequential composition**: The composition plan is a sequence of moving services (CP = {S1, S2, ..., Sn})
- **Overlap detection**: Finding services that intersect with the user's trajectory at each timestep
- **Dummy service**: Handles cases where no valid candidates exist
- **Penalty mechanism**: Penalizes selecting invalid services to encourage valid selections

The key mechanism is not "trajectory prediction" but rather finding trajectory overlaps between user and service paths, and selecting a sequence of services that together cover the user's entire trajectory.

### 9. What datasets are used?

Two real-world pedestrian trajectory datasets:

1. **Indoor (ATC Shopping Center, Osaka)**:
   - 1,777,297,164 samples
   - 185,554 trajectories
   - Sampling rate: 0.03-0.06 seconds (normalized to 0.04s)
   - Represents high-density pedestrian mobility

2. **Illinois Daily Commute**:
   - 357,706 samples
   - 207 trajectories
   - Sampling: strictly every 1 second
   - Represents daily commuter mobility patterns

### 10. What are the key results?

- **Accuracy**: ~95% on indoor dataset (after 500 trajectories), ~93% on Illinois dataset (after 35 trajectories)
- **Scalability**: Q-learning testing time < 0.1s vs ground-truth ~10,000s for 1000 services
- **Convergence**: Polynomial increase with number of moving services

### 11. What is the ground-truth approach?

The paper uses a **Parallel Flock-Based Service Discovery** algorithm as ground-truth:
- Apache Spark with spatio-temporal MapReduce
- Temporal Map Step: Prunes sub-trajectories based on user trajectory timesteps (left outer join)
- Spatial Map Step: Filters candidate services within circular region of user trajectory
- Reduce Phase: Groups by user timestep

### 12. What are the limitations mentioned?

The paper does not explicitly discuss limitations in detail, but potential limitations include:
- Assumption of deterministic trajectories
- Need for extensive training data
- Computational resources required for training
- Assumption of constant speed between timestamps

## Comparison with Your Approach

| Aspect | Paper 17 | Your Approach |
|--------|----------|----------------|
| Algorithm | Q-learning with Neural Network | A2C (Actor-Critic) |
| State | User trajectory sample (t, x, y) | Polar coordinates (r, cosθ, sinθ) |
| Handover | Trajectory overlap detection | A2C learns optimal switching |
| Datasets | ATC Indoor + Illinois | Same datasets |

---

*Based on: A_Deep_Reinforcement_Learning_Approach_for_Composing_Moving_IoT_ServicesM.pdf*
*Reference: Paper 17 in research collection*