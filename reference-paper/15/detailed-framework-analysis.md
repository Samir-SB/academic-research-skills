# Paper 15: Detailed Solution Framework Analysis

## Paper Information
- **Title**: Proactive Composition of Mobile IoT Energy Services
- **Year**: 2022
- **Algorithm**: Trajectory Prediction + Proactive Composition Algorithm

---

## 1. Functions Used for Selection and Aggregation

### 1.1 Trajectory Prediction Function

The paper predicts device movement to enable proactive service composition:

#### Movement Model
$$P(t+\Delta t | S_t) = \text{Transition}(p_t, v_t, \Delta t)$$

Where:
- $P(t+\Delta t)$ = predicted position at future time
- $S_t$ = current state (position, velocity, time)
- $p_t$ = current position vector
- $v_t$ = velocity vector

#### Trajectory Prediction using Historical Patterns
$$\hat{T}_{device} = f(H_{device}, C_{context})$$

Where:
- $\hat{T}_{device}$ = predicted trajectory
- $H_{device}$ = historical movement data
- $C_{context}$ = contextual factors (time, day, location)

### 1.2 Energy Service Aggregation

For aggregating energy services along predicted path:

$$E_{path}(t) = \sum_{i=1}^{n} E_i(t) \cdot \phi(d_{device}(t), d_i)$$

Where:
- $E_{path}(t)$ = total energy available along path at time $t$
- $E_i(t)$ = energy from service $i$ at time $t$
- $\phi$ = spatial availability function based on distance
- $d_{device}(t)$ = device position at time $t$
- $d_i$ = service location

#### Spatial Availability Function
$$\phi(d_{device}, d_i) = \begin{cases} 1 & \text{if } d(device, d_i) \leq R_{range} \\ 0 & \text{otherwise} \end{cases}$$

Where $R_{range}$ = service communication range

### 1.3 Proactive Selection Function

The proactive score evaluates service suitability:

$$Score_{proactive}(S, T) = w_1 \cdot E_{path}(S, T) + w_2 \cdot C_{coverage}(S, T) - w_3 \cdot H_{handoff}(S, T)$$

Where:
- $S$ = service set
- $T$ = predicted trajectory
- $E_{path}(S, T)$ = energy along trajectory
- $C_{coverage}(S, T)$ = trajectory coverage percentage
- $H_{handoff}(S, T)$ = expected handoff count
- $w_1, w_2, w_3$ = weights (∑w = 1)

### 1.4 Coverage Calculation

Coverage measures trajectory portion with available services:

$$C_{coverage}(S, T) = \frac{1}{|T|} \sum_{t \in T} I(E_{available}(t) \geq E_{required}(t))$$

Where:
- $I(\cdot)$ = indicator function (1 if true, 0 otherwise)
- $E_{required}(t)$ = energy required at time $t$

### 1.5 Handoff Cost Function

Expected service switching cost:

$$H_{handoff}(S, T) = \sum_{t \in T} \delta(service(t) \neq service(t-1))$$

Where $\delta$ = number of handoffs along trajectory

---

## 2. Algorithms Used for Exploration and Exploitation

### 2.1 Trajectory Prediction Algorithm

Uses historical movement patterns to predict future paths:

#### Pattern Mining
1. Collect movement history $H = \{p_1, p_2, ..., p_n\}$
2. Identify recurring routes using clustering
3. Build transition probabilities between locations

#### Prediction Execution
```
predict_trajectory(current_position, time_horizon):
    route = identify_route(current_position)
    waypoints = predict_waypoints(route, time_horizon)
    return waypoints
```

### 2.2 Proactive Composition Algorithm

The composition algorithm plans services along predicted trajectory:

#### Phase 1: Trajectory Prediction (Exploration)
- Analyze device movement patterns
- Predict likely path and timeline
- Identify service coverage gaps

#### Phase 2: Service Planning (Exploitation)
- Select services maximizing coverage
- Position services along predicted path
- Minimize handoff frequency

#### Phase 3: Pre-Configuration (Exploitation)
- Initialize services before device arrives
- Establish connections in advance
- Reduce activation latency

### 2.3 Exploration vs Exploitation Strategy

| Phase | Strategy | Mechanism |
|-------|----------|-----------|
| Trajectory | Exploration | Multiple path hypotheses |
| Service Selection | Exploitation | Coverage maximization |
| Pre-configuration | Exploitation | Advance setup |
| Handoff | Exploration | Alternative routes |

### 2.4 Handoff Management Algorithm

Manages service transitions during movement:

```
handoff_manager(device, current_service, new_location):
    next_services = find_services_near(new_location)
    
    if current_service.available_at(new_location):
        maintain current_service
    else:
        pre_auth = pre_authenticate(next_services[0])
        prepare handoff to pre_auth
        execute seamless transition
```

### 2.5 Service Pre-Configuration Algorithm

Prepares services before device arrival:

```
preconfigure(services, trajectory, arrival_times):
    for service, arrival in zip(services, arrival_times):
        t_prepare = arrival - LOOKAHEAD_TIME
        if current_time >= t_prepare:
            service.activate()
            service.authenticate(device)
            service.reserve_resources()
```

---

## 3. Dataset Used

### 3.1 Synthetic Mobile IoT Scenarios

The evaluation uses synthetic datasets representing mobile IoT environments:

#### Device Types
| Type | Velocity | Movement Pattern | Examples |
|------|----------|------------------|----------|
| Pedestrian | 1-5 km/h | Random waypoint | Wearables |
| Vehicle | 30-120 km/h | Route-based | EVs, cars |
| Drone | 10-50 km/h | Predefined paths | UAVs |

#### Trajectory Characteristics
- **Duration**: 5-60 minutes per trip
- **Distance**: 1-50 km
- **Waypoints**: 3-20 per trajectory

### 3.2 Energy Service Distribution

#### Service Types
- **Static Charging Stations**: Fixed locations, high capacity
- **Mobile Charging Units**: Moving vehicles with charging capability
- **Wireless Charging Zones**: Area-based charging pads

#### Spatial Distribution
- Urban: Dense, 50-100 services per km²
- Suburban: Moderate, 10-30 services per km²
- Highway: Sparse, 2-5 services per km

### 3.3 Movement Pattern Dataset

| Parameter | Value Range |
|-----------|-------------|
| Speed | 1-120 km/h |
| Pause Time | 0-30 min |
| Home Base | Random |
| Destination Types | Work, Shop, Home, Random |

### 3.4 Evaluation Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Coverage | % trajectory with service | >90% |
| Handoff Count | Service switches per trip | <3 |
| Setup Latency | Pre-configuration time | <60s |
| Continuity | Service availability during trip | >95% |

---

## 4. Complete Workflow

### 4.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Proactive Composition Framework                 │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  │
│  │   Trajectory  │  │    Service    │  │    Handoff    │  │
│  │   Predictor   │  │    Planner    │  │   Manager     │  │
│  └────────────────┘  └────────────────┘  └────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                    Pre-Configuration Engine                  │
├─────────────────────────────────────────────────────────────┤
│              Energy Service Network                          │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐              │
│  │Station1│ │Station2│ │Zone A  │ │Mobile 1│ ...           │
│  └────────┘ └────────┘ └────────┘ └────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Workflow Flowchart

```
START
  │
  ▼
┌─────────────────────┐
│ Receive Service     │
│ Request (with       │
│ device trajectory)  │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Analyze Historical  │
│ Movement Patterns   │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Predict Future     │
│ Trajectory          │
└─────────────────────┘
  │
  ▼
┌─────────────────────┐
│ Identify Service   │
│ Coverage Along     │
│ Predicted Path     │
└─────────────────────┘
  │
  ▼
         ┌─────────────────────┐
         │ Coverage > Threshold│
         └──────────┬────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
      YES                        NO
        │                        │
        ▼                        ▼
┌───────────────────┐    ┌─────────────────────┐
│ Proceed to       │    │ Find Alternative    │
│ Pre-configuration │    │ Service Routes      │
└───────────────────┘    └─────────────────────┘
        │                        │
        ▼                        ▼
┌─────────────────────┐
│ Pre-Configure      │
│ Services Along     │
│ Trajectory          │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Execute Service    │
│ During Movement    │
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│ Manage Handoffs    │
│ (if needed)        │
└─────────────────────┘
        │
        ▼
    END
```

### 4.3 Complete Pseudocode

```python
class ProactiveCompositionEngine:
    def __init__(self, config):
        self.services = ServiceRegistry()
        self.predictor = TrajectoryPredictor()
        self.coverage_threshold = 0.9
        self.lookahead = config.lookahead_time
        
    def compose(self, device, requirements):
        """Main proactive composition method"""
        # Phase 1: Predict trajectory
        trajectory = self.predictor.predict(
            device,
            horizon=requirements.duration
        )
        
        # Phase 2: Identify required services
        needed_energy = self.calculate_energy_requirement(
            requirements,
            trajectory.duration
        )
        
        # Phase 3: Find coverage along path
        coverage = self.analyze_coverage(
            trajectory,
            needed_energy
        )
        
        if coverage.percentage < self.coverage_threshold:
            # Exploration: find alternative routes
            trajectory = self.explore_alternative_paths(
                device,
                requirements
            )
        
        # Phase 4: Select services (Exploitation)
        selected = self.select_services(
            trajectory,
            needed_energy,
            requirements
        )
        
        # Phase 5: Pre-configure
        self.preconfigure_services(selected, trajectory)
        
        return ProactiveComposition(selected, trajectory)
    
    def select_services(self, trajectory, energy_req, requirements):
        """Select optimal services along trajectory"""
        waypoints = trajectory.get_waypoints()
        selected = []
        
        current_energy = 0
        for waypoint in waypoints:
            nearby = self.services.near(waypoint.position, radius=1km)
            
            if current_energy < energy_req * 0.3:
                # Need to refuel
                best = max(nearby, 
                          key=lambda s: s.capacity * s.reliability)
                selected.append((waypoint, best))
                current_energy += best.capacity
                
        return selected
    
    def preconfigure_services(self, composition, trajectory):
        """Pre-configure services before device arrival"""
        for waypoint, service in composition:
            arrival_time = waypoint.time
            prepare_time = arrival_time - self.lookahead
            
            if current_time >= prepare_time:
                service.activate()
                service.reserve()
                service.authenticate_device(device_id)
    
    def analyze_coverage(self, trajectory, energy_requirement):
        """Analyze service coverage along trajectory"""
        waypoints = trajectory.get_waypoints()
        covered = 0
        
        for waypoint in waypoints:
            nearby = self.services.near(waypoint.position)
            available = sum(s.capacity for s in nearby)
            
            if available >= energy_requirement * 0.1:  # per waypoint
                covered += 1
                
        percentage = covered / len(waypoints)
        return CoverageResult(percentage, covered, len(waypoints))
    
    def explore_alternative_paths(self, device, requirements):
        """Explore alternative routes for better coverage"""
        alternatives = self.route_planner.find_alternatives(
            device.current_position,
            requirements.destination,
            constraints={
                'max_distance_increase': 0.2,
                'min_service_spacing': 2km
            }
        )
        
        best = max(alternatives, 
                  key=lambda r: self.analyze_coverage(r, requirements).percentage)
        
        return best
    
    def handle_handoff(self, device, current_service, new_location):
        """Manage service handoff during movement"""
        if current_service.available_at(new_location):
            return current_service
        
        # Pre-authenticated service at new location
        next_service = self.services.get_preauthenticated(
            near=new_location
        )
        
        if next_service:
            # Seamless handoff
            return next_service
        else:
            # Emergency fallback
            return self.find_emergency_service(new_location)
```

### 4.4 Trajectory Prediction Details

```
┌─────────────────────────────────────────┐
│       Trajectory Prediction Process      │
├─────────────────────────────────────────┤
│                                         │
│  Historical Data ──► Route Mining       │
│         │              │                 │
│         ▼              ▼                 │
│  ┌─────────────────────────────┐        │
│  │   Movement Pattern Library  │        │
│  └─────────────────────────────┘        │
│                │                          │
│                ▼                          │
│  ┌─────────────────────────────┐        │
│  │   Context Processing        │        │
│  │   (time, day, location)     │        │
│  └─────────────────────────────┘        │
│                │                          │
│                ▼                          │
│  ┌─────────────────────────────┐        │
│  │   Trajectory Prediction     │        │
│  │   (waypoints + times)       │        │
│  └─────────────────────────────┘        │
│                                         │
└─────────────────────────────────────────┘
```

### 4.5 Proactive vs Reactive Comparison

| Aspect | Reactive | Proactive |
|--------|----------|-----------|
| Timing | After movement | Before movement |
| Service Setup | On-demand | Pre-configured |
| Handoff | Emergency | Planned |
| Coverage | Often partial | Maximized |
| Latency | Higher | Lower |

---

## 5. Summary

### Key Framework Components

| Component | Function | Innovation |
|-----------|----------|------------|
| Trajectory Predictor | Movement forecasting | Pattern-based prediction |
| Service Planner | Optimal selection | Coverage maximization |
| Pre-Configuration | Advance setup | Lookahead activation |
| Handoff Manager | Service transitions | Seamless transfer |

### Algorithm Characteristics

- **Exploration**: Alternative trajectory search, route planning
- **Exploitation**: Service selection based on coverage, pre-configuration
- **Balance**: Prediction horizon controls exploration depth

### Dataset Characteristics

- **Type**: Synthetic mobile device trajectories
- **Scale**: 10-100 services, various device types
- **Patterns**: Pedestrian, vehicle, drone movement

---

*Analysis Date: April 2026*
*Paper Type: Original Research*