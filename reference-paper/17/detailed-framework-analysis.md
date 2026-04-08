# Paper 17: Detailed Solution Framework Analysis

## Paper Information
- **Title**: A Deep Reinforcement Learning Approach for Composing Moving IoT Services
- **Year**: 2022
- **Algorithm**: Double DQN (Deep Reinforcement Learning) with Trajectory-Aware Composition

---

## 1. Functions Used for Selection and Aggregation

### 1.1 State Representation for Moving Services

The paper represents the composition problem as a Markov Decision Process:

#### State Definition
$$s_t = \{P_{services}, P_{device}, V_{device}, t\}$$

Where:
- $P_{services} = \{p_1, p_2, ..., p_n\}$ = set of service positions
- $P_{device}$ = current device position
- $V_{device}$ = device velocity vector
- $t$ = current time

#### Extended State with Trajectory
$$s_t^{extended} = \{s_t, T_{predicted}, E_{req}, QoS_{constraints}\}$$

Where:
- $T_{predicted}$ = predicted trajectory of moving services
- $E_{req}$ = energy requirements
- $QoS_{constraints}$ = quality of service parameters

### 1.2 Action Space Definition

The action space defines service selection decisions:

$$a_t \in \{Select(s_i), Replace(s_i, s_j), Add(s_k), Remove(s_l)\}$$

Where each action modifies the current composition.

#### Composition Representation
- Binary vector: $C_t = [c_1, c_2, ..., c_n]$ where $c_i \in \{0, 1\}$
- $c_i = 1$ if service $i$ is selected in composition at time $t$

### 1.3 Reward Function Design

The reward function guides learning toward optimal compositions:

$$r(s_t, a_t) = r_{success} + r_{QoS} + r_{efficiency} + r_{stability}$$

#### Success Reward
$$r_{success} = \begin{cases} +1 & \text{if composition successful} \\ -0.5 & \text{if composition failed } \end{cases}$$

#### QoS Reward
$$r_{QoS} = \sum_{k} w_k \cdot \frac{QoS_k}{QoS_k^{target}}$$

Where:
- $w_k$ = weight for k-th QoS attribute
- $QoS_k$ = actual QoS value
- $QoS_k^{target}$ = target QoS value

#### Efficiency Reward
$$r_{efficiency} = \alpha \cdot \frac{E_{provided}}{E_{required}} - \beta \cdot |C_t|$$

Where:
- $E_{provided}$ = energy provided by composition
- $E_{required}$ = energy required by device
- $|C_t|$ = number of services in composition (cost)

#### Stability Reward
$$r_{stability} = \begin{cases} +0.2 & \text{if } C_t = C_{t-1} \text{ (no change)} \\ -0.1 \cdot |changes| & \text{otherwise} \end{cases}$$

### 1.4 Q-Function Approximation

The Double DQN approximates the action-value function:

$$Q(s, a; \theta) \approx Q^*(s, a)$$

Where:
- $\theta$ = neural network parameters
- $Q(s, a)$ = expected cumulative reward for taking action $a$ in state $s$

#### Network Architecture
```
Input Layer (State):     [service positions, device position, velocity, time]
                              │
                              ▼
Hidden Layer 1:           Dense(256, ReLU)
                              │
                              ▼
Hidden Layer 2:           Dense(128, ReLU)
                              │
                              ▼
Output Layer:             Dense(|A|) → Q-values for each action
```

### 1.5 Aggregation Function for Services

For combining multiple moving services in composition:

$$E_{composition}(t) = \sum_{i \in C_t} E_i(t) \cdot \phi(p_i(t), p_{device}(t))$$

Where:
- $E_i(t)$ = energy from service $i$ at time $t$
- $\phi$ = spatial availability function based on connectivity

#### Trajectory-Aware Aggregation
$$E_{horizon} = \int_{t}^{t+H} E_{composition}(\tau) d\tau$$

Where $H$ = prediction horizon (e.g., 30 minutes)

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Double DQN Algorithm

The paper uses Double DQN to address overestimation in standard Q-learning:

#### Double Q-Learning Update
$$Y_t^{Double} = r_{t+1} + \gamma \cdot Q(s_{t+1}, \arg\max_a Q(s_{t+1}, a; \theta); \theta^-)$$

Where:
- $\theta$ = online network parameters
- $\theta^-$ = target network parameters
- $\gamma$ = discount factor

#### Two-Network Architecture
```
┌─────────────────┐     ┌─────────────────┐
│  Online Network │     │  Target Network │
│    (θ)         │     │     (θ⁻)        │
├─────────────────┤     ├─────────────────┤
│ - Updates fast  │     │ - Updates slow  │
│ - Every step    │     │ - Every C steps │
│ - Chooses best  │     │ - Evaluates Q   │
└─────────────────┘     └─────────────────┘
```

### 2.2 Prioritized Experience Replay

To accelerate learning in dynamic environments:

#### Priority Calculation
$$p_i = |r_i + \gamma \max_a Q(s_i', a; \theta^-) - Q(s_i, a_i; \theta)|^\alpha + \epsilon$$

Where:
- $p_i$ = priority of experience $i$
- $\alpha$ = prioritization exponent (typically 0.6)
- $\epsilon$ = small constant for exploration

#### Sampling Strategy
```python
def sample_batch(buffer, batch_size):
    priorities = buffer.get_priorities()
    probs = priorities / sum(priorities)
    indices = np.random.choice(len(buffer), batch_size, p=probs)
    return buffer[indices]
```

### 2.3 Exploration Strategy (ε-greedy with Annealing)

The exploration uses decaying epsilon:

$$\epsilon_t = \epsilon_{min} + (\epsilon_{max} - \epsilon_{min}) \cdot e^{-\lambda t}$$

#### Exploration Schedule
| Phase | ε Value | Behavior |
|-------|---------|----------|
| Initial | 1.0 | Pure exploration |
| Early | 0.5-0.7 | Mixed |
| Late | 0.1-0.2 | Exploitation |
| Final | 0.01 | Near-optimal |

### 2.4 Exploration vs Exploitation Balance

| Mechanism | Type | Purpose |
|-----------|------|---------|
| ε-greedy | Exploration | Action space exploration |
| Experience replay | Both | Efficient learning from diverse experiences |
| Target network | Stability | Stable value estimates |
| Double Q | Exploitation | Reduce overestimation |
| Reward shaping | Exploitation | Guide toward desired behaviors |

### 2.5 Trajectory-Aware Policy

The key innovation is using predicted service trajectories:

#### Trajectory Prediction
```python
def predict_trajectory(service, horizon):
    # Use movement model for service
    positions = []
    for t in range(horizon):
        pos = service.position + service.velocity * t
        positions.append(pos)
    return positions
```

#### Policy with Trajectory
```python
def get_action(state):
    # Include trajectory in state
    extended_state = state + predicted_trajectories
    
    # Get Q-values
    q_values = Q_network(extended_state)
    
    # Select action (ε-greedy)
    if random() < epsilon:
        return random_action()
    else:
        return argmax(q_values)
```

---

## 3. Dataset Used

### 3.1 Synthetic Moving IoT Service Scenarios

The evaluation uses synthetic datasets representing mobile IoT environments:

#### Service Types with Mobility
| Type | Movement Pattern | Speed Range | Energy Capacity |
|------|-----------------|-------------|-----------------|
| Mobile Charger | Random waypoint | 5-30 km/h | 10-30 kWh |
| Vehicle Service | Route-based | 20-80 km/h | 15-40 kWh |
| Drone Service | Flight path | 10-50 km/h | 5-15 kWh |
| Pedestrian Service | Random walk | 1-5 km/h | 2-5 kWh |

### 3.2 Mobility Models

#### Random Waypoint Model
```
Initialize: position, pick random destination
While running:
    move toward destination
    if reached:
        pause (optional)
        pick new destination
```

#### Vehicle Route Model
```
Routes: predefined paths (highway, urban)
Movement: follow route with slight variation
Speed: varies by route type
Stops: at traffic points
```

#### Drone Flight Path Model
```
Pattern: grid or circular patrol
Altitude: 50-100m
Speed: constant during flight
Waypoints: predetermined
```

### 3.3 Scale Configurations

| Scale | Services | Device Speed | Duration |
|-------|----------|--------------|----------|
| Small | 20 | 5-20 km/h | 10 min |
| Medium | 50 | 10-50 km/h | 30 min |
| Large | 100 | 20-80 km/h | 60 min |

### 3.4 Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Success Rate | % compositions meeting requirements | >90% |
| Adaptation Speed | Time to respond to changes | <5s |
| QoS Maintenance | % time constraints satisfied | >85% |
| Re-composition Freq | Compositions per hour | <10 |

---

## 4. Complete Workflow

### 4.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│          Deep Reinforcement Learning Composition           │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐│
│  │   State        │  │   Double DQN  │  │   Experience   ││
│  │   Extractor   │  │   Agent        │  │   Replay       ││
│  └────────────────┘  └────────────────┘  └────────────────┘│
├─────────────────────────────────────────────────────────────┤
│              Trajectory-Aware Module                        │
├─────────────────────────────────────────────────────────────┤
│              Moving Service Network                         │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐              │
│  │Mobile 1│ │Vehicle │ │Drone   │ │Pedestr.│ ...          │
│  │        │ │Service │ │Service │ │Service │              │
│  └────────┘ └────────┘ └────────┘ └────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Training Workflow

```
START
  │
  ▼
┌─────────────────────┐
│ Initialize Networks │
│ (Online + Target)   │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Initialize Replay   │
│ Buffer              │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Reset Environment   │
│ (New Episode)       │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Get State s_t      │
│ (include trajectories)│
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Select Action a_t  │
│ (ε-greedy)         │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Execute Action     │
│ in Environment     │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Observe Reward r_t │
│ and Next State s_t+1│
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Store Experience   │
│ in Replay Buffer   │
│ (with priority)    │
└─────────────────────┘
  │
  ▼
         ┌─────────────────────┐
         │ Enough samples?     │
         └──────────┬────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
       YES                        NO
        │                        │
        ▼                        ▼
┌───────────────────┐    ┌─────────────────────┐
│ Sample Batch      │    │ Continue Episode   │
│ (Prioritized)     │    │                     │
└───────────────────┘    └─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Compute TD Target  │
│ (Double DQN)       │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Update Online      │
│ Network            │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Update Target      │
│ Network (periodic) │
└─────────────────────┘
        │
        ▼
    Continue
```

### 4.3 Runtime Composition Flow

```
Runtime START
  │
  ▼
┌─────────────────────┐
│ Observe Current    │
│ State (services,   │
│ device, time)      │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Predict Service    │
│ Trajectories       │
│ (horizon H)        │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Extend State with  │
│ Trajectories       │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Forward Pass       │
│ through Q-Network  │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Select Best Action │
│ (greedy)           │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Apply Action       │
│ (select/replace/   │
│  add/remove)       │
└─────────────────────┘
        │
        ▼
         ┌─────────────────────┐
         │ Event Triggered?     │
         │ (service moves out,  │
         │  QoS violation)      │
         └──────────┬────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
       YES                        NO
        │                        │
        ▼                        ▼
┌───────────────────┐    ┌─────────────────────┐
│ Trigger Re-       │    │ Continue Current    │
│ composition       │    │ Composition        │
└───────────────────┘    └─────────────────────┘
        │
        ▼
    Continue
```

### 4.4 Complete Pseudocode

```python
class MovingServiceComposer:
    def __init__(self, config):
        self.state_dim = config.state_dim
        self.action_dim = config.action_dim
        self.gamma = config.discount_factor
        self.epsilon = config.epsilon_start
        
        # Double DQN networks
        self.q_network = QNetwork(self.state_dim, self.action_dim)
        self.target_network = QNetwork(self.state_dim, self.action_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Replay buffer
        self.replay = PrioritizedReplayBuffer(config.buffer_size)
        
    def train(self, env, num_episodes):
        """Training loop"""
        for episode in range(num_episodes):
            state = env.reset()
            total_reward = 0
            
            while not done:
                # Select action (ε-greedy)
                action = self.select_action(state)
                
                # Execute
                next_state, reward, done, info = env.step(action)
                
                # Store with priority
                priority = self.compute_priority(
                    state, action, reward, next_state, done
                )
                self.replay.add(state, action, reward, 
                               next_state, done, priority)
                
                # Learn
                if len(self.replay) > config.batch_size:
                    self.learn()
                    
                state = next_state
                total_reward += reward
                
            # Decay epsilon
            self.epsilon = self.epsilon * config.epsilon_decay
            
            # Update target network periodically
            if episode % config.target_update_freq == 0:
                self.target_network.load_state_dict(
                    self.q_network.state_dict()
                )
                
    def select_action(self, state, training=True):
        """Select action using ε-greedy"""
        if training and random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        else:
            return self.greedy_action(state)
            
    def greedy_action(self, state):
        """Greedy action selection"""
        q_values = self.q_network(state)
        return torch.argmax(q_values).item()
    
    def learn(self):
        """Train on batch from replay buffer"""
        # Sample batch with priority
        batch = self.replay.sample(config.batch_size)
        
        states, actions, rewards, next_states, dones = batch
        
        # Double DQN: use online network to select, target to evaluate
        next_q_online = self.q_network(next_states)
        next_actions = torch.argmax(next_q_online, dim=1)
        
        next_q_target = self.target_network(next_states)
        next_q = next_q_target.gather(1, next_actions.unsqueeze(1))
        
        # TD target
        target = rewards + self.gamma * (1 - dones) * next_q.squeeze()
        
        # Compute loss
        current_q = self.q_network(states).gather(1, actions.unsqueeze(1))
        loss = self.mse_loss(current_q.squeeze(), target.detach())
        
        # Update
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Update priorities
        td_errors = abs(target - current_q.squeeze().detach())
        self.replay.update_priorities(td_errors)
        
    def compose_runtime(self, services, device, requirements):
        """Runtime composition using trained policy"""
        # Build state
        state = self.build_state(services, device, requirements)
        
        # Extend with predicted trajectories
        trajectories = self.predict_trajectories(services, horizon=30)
        extended_state = self.extend_state(state, trajectories)
        
        # Get action
        action = self.greedy_action(extended_state)
        
        # Apply action
        composition = self.apply_action(action, services)
        
        return composition
    
    def build_state(self, services, device, requirements):
        """Build state representation"""
        # Service positions
        service_pos = torch.tensor([s.position for s in services])
        
        # Device position and velocity
        device_state = torch.tensor([
            device.position[0], device.position[1],
            device.velocity[0], device.velocity[1]
        ])
        
        # Requirements
        req_state = torch.tensor([
            requirements.energy,
            requirements.min_qos
        ])
        
        return torch.cat([service_pos, device_state, req_state])
    
    def predict_trajectories(self, services, horizon):
        """Predict future service positions"""
        trajectories = []
        
        for service in services:
            path = []
            pos = service.position
            vel = service.velocity
            
            for t in range(horizon):
                pos = pos + vel * t
                path.append(pos)
                
            trajectories.append(path)
            
        return trajectories
    
    def event_triggered_recompose(self, event, current_composition):
        """Event-triggered re-composition"""
        if event.type == 'service_moved_out':
            affected = event.affected_services
            
            # Find replacements
            candidates = [s for s in self.services 
                        if s not in current_composition]
            
            best = max(candidates, 
                      key=lambda s: self.estimate_value(
                          self.build_state(candidates, self.device, 
                                         self.requirements), 
                          s.id
                      ))
            
            # Replace
            current_composition.replace(affected[0], best)
            
        elif event.type == 'qos_violation':
            # Find composition that improves QoS
            improved = self.search_improved_composition()
            return improved
            
        return current_composition
```

### 4.5 DQN vs Traditional Optimization

| Aspect | GA/PSO | Double DQN |
|--------|--------|------------|
| Problem View | Static optimization | Sequential decision |
| Re-computation | Full re-run | Policy application |
| Adaptation Speed | Slow | Fast |
| Trajectory Awareness | Not native | Built-in |
| Scalability | Limited | Good |

---

## 5. Summary

### Key Framework Components

| Component | Function | Innovation |
|-----------|----------|------------|
| Double DQN | Action selection | Reduced overestimation |
| Prioritized Replay | Efficient learning | Fast convergence |
| Trajectory Module | Future prediction | Proactive composition |
| Event Trigger | Change detection | Efficient adaptation |

### Algorithm Characteristics

- **Exploration**: ε-greedy with annealing, diverse experience sampling
- **Exploitation**: Double Q-learning reduces overestimation, greedy action selection
- **Balance**: Decaying exploration vs stable target network

### Dataset Characteristics

- **Type**: Synthetic moving service scenarios
- **Scale**: 20-100 moving services
- **Patterns**: Random waypoint, vehicle routes, drone flight paths

---

*Analysis Date: April 2026*
*Paper Type: Original Research*