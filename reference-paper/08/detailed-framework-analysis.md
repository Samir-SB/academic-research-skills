# Paper 08: Detailed Solution Framework Analysis

## Paper Information
- **Title**: Reinforcement Learning for Interactive QoS-Aware Services Composition
- **Year**: 2019
- **Algorithm**: Q-Learning + Interactive Service Composition

---

## 1. Functions Used for Selection and Aggregation

### 1.1 QoS Aggregation Functions

#### Sequential Composition (Service Chain)
$$Q_s = \prod_{i=1}^{n} q_i$$

Where:
- $Q_s$ = composite QoS for sequential composition
- $q_i$ = QoS attribute of service $i$

#### Parallel Composition (Concurrent Execution)
$$Q_p = \min_{i \in S} q_i$$

Where:
- $Q_p$ = composite QoS for parallel composition
- $\min$ selects worst-case among parallel services

#### Conditional Composition (Branch)
$$Q_c = \sum_{j} p_j \cdot q_j$$

Where:
- $p_j$ = probability of branch $j$
- $q_j$ = QoS for branch $j$

### 1.2 Q-Learning Value Function

Q-learning computes action-value for state-action pairs:

$$Q(s, a) \leftarrow Q(s, a) + \alpha \cdot [R(s, a) + \gamma \max_{a'} Q(s', a') - Q(s, a)]$$

Where:
- $s$ = current state (current task in workflow)
- $a$ = action (selected service for current task)
- $s'$ = next state (next task)
- $\alpha$ = learning rate (0.1-0.3)
- $\gamma$ = discount factor (0.8-0.95)
- $R(s, a)$ = reward for selecting service $a$ at state $s$

### 1.3 Reward Function

$$R(s, a) = w_1 \cdot \text{QoS}(a) + w_2 \cdot \text{CompositionScore}(S) + w_3 \cdot \text{InteractiveBonus}$$

Where:
- $\text{QoS}(a)$ = QoS attribute of selected service $a$
- $\text{CompositionScore}(S)$ = score of partial composition $S$
- $\text{InteractiveBonus}$ = bonus for interactive collaboration
- $w_1 + w_2 + w_3 = 1$

### 1.4 State Representation

$$s = (t, q_1, ..., q_m, \text{history})$$

Where:
- $t$ = current task index in workflow
- $q_1, ..., q_m$ = accumulated QoS values from previous selections
- $\text{history}$ = sequence of previously selected services

### 1.5 Action Space

$$A(s) = \{s_i | s_i \text{ implements required functionality for current task}\}$$

Where:
- Actions are available services matching current task requirements

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Q-Learning Algorithm

The core RL algorithm:

#### Q-Table Representation
- State space: workflow tasks × QoS levels
- Action space: available services per task
- Q-values stored in table: Q[s][a]

#### Exploration (ε-Greedy)
$$\pi(a|s) = \begin{cases} \text{random} & \text{if } rand() < \epsilon \\ \arg\max_a Q(s, a) & \text{otherwise} \end{cases}$$

Where:
- $\epsilon$ = exploration rate (0.1-0.3)
- Decays over time: $\epsilon = \epsilon \cdot \epsilon_{decay}$

#### Exploitation
Select action with highest Q-value:
$$a^* = \arg\max_a Q(s, a)$$

### 2.2 Interactive Composition Mechanism

The "Interactive" aspect enables collaboration:

#### Interactive Service Discovery
- Query for services with similar functionality
- Rank by compatibility with current composition
- Select based on learned Q-values

#### Interactive Feedback Loop
```
For each step in composition:
    1. Get current state s
    2. Choose action via ε-greedy
    3. Execute service, observe reward
    4. Update Q-value
    5. Get user feedback (if interactive mode)
    6. Adjust reward based on feedback
    7. Move to next state
```

### 2.3 Exploration-Exploitation Balance

| Mechanism | Exploration | Exploitation |
|-----------|-------------|--------------|
| ε-Greedy | Random action selection (ε) | Best Q-value action (1-ε) |
| Learning Rate | High α early (learn fast) | Low α later (stabilize) |
| Discount Factor | γ determines future importance | Higher γ = more exploitation |
| Interactive | Explore new services | Use learned good services |

### 2.4 Algorithm Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| α (learning rate) | 0.1-0.3 | Speed of learning |
| γ (discount) | 0.8-0.95 | Future reward importance |
| ε (exploration) | 0.1-0.3 | Random action probability |
| ε_decay | 0.95-0.99 | Decay exploration rate |
| Episodes | 1000-5000 | Training episodes |

---

## 3. Dataset Used

### 3.1 Synthetic IoT Service Registry

#### Service Registry Structure
Each service has:
- **Service ID**: Unique identifier
- **Functionality**: Service type/category
- **QoS Attributes**:
  - Response time
  - Cost
  - Reliability
  - Availability

#### Dataset Characteristics
| Parameter | Value |
|-----------|-------|
| Number of Services | 50-150 |
| Service Categories | 5-10 functional categories |
| QoS Attributes | 4 per service |
| Workflow Tasks | 5-10 tasks |

### 3.2 Evaluation Scenarios

| Scenario | Services | Tasks | Interactive | Purpose |
|----------|----------|-------|-------------|---------|
| Basic | 50 | 5 | No | Baseline |
| Interactive | 80 | 7 | Yes | Test interaction |
| Complex | 150 | 10 | Yes | Scalability |

### 3.3 QoS Distribution
- Uniform random within realistic ranges
- Some correlated attributes (high reliability → higher cost)

---

## 4. Complete Workflow

### 4.1 Phase 1: Preprocessing - Q-Table Initialization

```
┌─────────────────────────────────────────────────────────────┐
│               Q-LEARNING INITIALIZATION                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Generate synthetic IoT service registry                  │
│     - Service categories and types                          │
│     - Assign QoS values                                     │
│                                                              │
│  2. Define workflow structure                               │
│     - Task sequence with dependencies                       │
│     - QoS requirements                                      │
│                                                              │
│  3. Initialize Q-table                                      │
│     - All Q(s,a) = 0 or random small values                │
│                                                              │
│  4. Set learning parameters                                 │
│     - α = 0.1-0.3, γ = 0.8-0.95                             │
│     - ε = 0.1-0.3, ε_decay = 0.95-0.99                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Phase 2: Q-Learning Training

```
┌─────────────────────────────────────────────────────────────┐
│                  Q-LEARNING TRAINING LOOP                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ EPISODE LOOP (repeat for max_episodes)              │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │                                                      │   │
│  │ 1. INITIALIZE EPISODE                               │   │
│  │    - Start at first task (s = task_0)               │   │
│  │    - Empty composition S = {}                       │   │
│  │    - Reset accumulated QoS                          │   │
│  │                                                      │   │
│  │ 2. STEP LOOP (until workflow complete)             │   │
│  │    - Get available actions A(s)                     │   │
│  │    - Choose action via ε-greedy:                   │   │
│  │        * With probability ε: random service         │   │
│  │        * Else: service with max Q(s,a)              │   │
│  │    - Execute service, observe reward               │   │
│  │    - Get next state s'                             │   │
│  │    - Update Q(s,a):                                 │   │
│  │        Q(s,a) = Q(s,a) + α*(R + γ*max Q(s',a') - Q(s,a)) │   │
│  │    - s = s'                                         │   │
│  │    - Add service to composition S                  │   │
│  │                                                      │   │
│  │ 3. EPISODE COMPLETE                                │   │
│  │    - Compute final composition score               │   │
│  │    - Decay exploration rate: ε = ε * ε_decay       │   │
│  │                                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Phase 3: Solution Extraction

```
┌─────────────────────────────────────────────────────────────┐
│                  SOLUTION EXTRACTION                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Use learned policy: π(s) = argmax_a Q(s,a)             │
│  2. For each task in workflow:                              │
│     - Select service with highest Q-value                  │
│     - Add to composition                                    │
│  3. Compute final aggregated QoS                           │
│  4. Verify constraints satisfied                           │
│  5. Return optimal composition S*                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.4 Complete Flowchart

```
                          ┌─────────────────────┐
                          │  Initialize          │
                          │  - Q-table           │
                          │  - Parameters        │
                          └──────────┬──────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │     EPISODE LOOP               │
                     │                               │
                     │  ┌─────────────┐              │
                     │  │ Initialize  │              │
                     │  │ Episode     │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Get State   │              │
                     │  │ s           │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ ε-Greedy    │              │
                     │  │ Action      │              │
                     │  │ Selection   │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Execute    │              │
                     │  │ Service    │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Observe     │              │
                     │  │ Reward      │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     │         ▼                     │
                     │  ┌─────────────┐              │
                     │  │ Update      │              │
                     │  │ Q(s,a)      │              │
                     │  └──────┬──────┘              │
                     │         │                     │
                     └─────────┼─────────────────────┘
                               │
                               ▼
                     ┌───────────────────────┐
                     │  Convergence Check    │
                     │  - Max episodes       │
                     │  - Q-value convergence│
                     └───────────┬───────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
               YES               │               NO
                │                │                │
                ▼                │                ▼
     ┌──────────────────┐        │    ┌──────────────────────┐
     │ Extract Policy   │        │    │ Continue Episode      │
     │ π(s) = argmax Q  │        │    └──────────────────────┘
     └──────────────────┘        │
                                 │
                                 └──────────────────────────┘
                                             (back to loop)
```

### 4.5 Pseudocode

```
ALGORITHM: Q-Learning for Interactive QoS-Aware Service Composition

INPUT:
  - Service registry R = {s1, ..., sn}
  - Workflow tasks T = {t1, ..., tk}
  - QoS weights W = {w1, ..., wm}
  - Parameters: α, γ, ε, ε_decay, max_episodes

OUTPUT:
  - Optimal service composition S*

// Phase 1: Initialization
1. Initialize Q-table: Q(s, a) = 0 for all s, a
2. Set ε = initial_exploration_rate

// Phase 2: Training
3. For episode = 1 to max_episodes:
   
   a. s = first_task  // Initial state
   b. S = {}  // Empty composition
   c. accumulated_QoS = {}
   
   d. While s is not terminal:
         // Get available actions (services for current task)
         A = get_available_services(s)
         
         // ε-greedy action selection
         If rand() < ε:
            a = random(A)  // Explore
         Else:
            a = argmax_{a∈A} Q(s, a)  // Exploit
         
         // Execute and observe
         s', reward = execute_service(s, a, S)
         
         // Update Q-value (Bellman equation)
         max_a_prime = max_{a'∈A(s')} Q(s', a')
         Q(s, a) = Q(s, a) + α * (reward + γ * max_a_prime - Q(s, a))
         
         // Move to next state
         s = s'
         S = S ∪ {a}
      
   e. Decay exploration rate
      ε = ε * ε_decay

// Phase 3: Solution Extraction
4. Use learned policy:
   For each task in workflow:
      s = current_state
      A = available_services
      a = argmax_{a∈A} Q(s, a)
      Add a to composition

5. Return S*

END ALGORITHM
```

---

## 5. Summary

| Component | Details |
|-----------|---------|
| **Selection Function** | Q-learning: Q(s,a) with ε-greedy selection |
| **Aggregation Functions** | Sequential (∏), Parallel (min), Conditional (Σp·q) |
| **State Representation** | (task_index, accumulated_QoS, history) |
| **Reward Function** | R = w₁·QoS + w₂·CompositionScore + w₃·InteractiveBonus |
| **Exploration** | ε-greedy with decay (ε = 0.1-0.3) |
| **Exploitation** | argmax_a Q(s,a) policy |
| **Novel Contribution** | Interactive composition with RL + user feedback |
| **Dataset** | Synthetic IoT (50-150 services), 5-10 workflow tasks |
| **Workflow** | Q-Table Init → Training Loop (episodes) → Policy Extraction |

---

*This document provides detailed analysis of Paper 08's solution framework.*