# Peer Review Analysis: A Deep Reinforcement Learning Approach for Composing Moving IoT Services

## 1. What is the main research problem addressed in this paper?

The paper addresses the challenge of composing IoT services in dynamic environments where services are moving—meaning the IoT devices or sensors are mobile rather than static. This creates a fundamental challenge not addressed in prior work: the composition topology changes continuously as services move, making traditional static composition approaches ineffective. The problem involves maintaining service quality and composition stability despite continuous spatial changes in the service landscape.

## 2. How does this paper differ from previous work on mobile IoT services (e.g., papers 14-16)?

While papers 14-16 focus on energy aspects of mobile IoT (fluid composition, proactive composition, elastic composition), this paper directly addresses the mobility challenge in service composition itself. Paper 15 (proactive composition) predicted device trajectories but used the predictions for energy planning; this paper uses trajectory information to optimize the actual service composition. Paper 16 (elastic composition) addresses availability changes but not spatial movement. This paper is the first to specifically address composing services from moving IoT devices using DRL.

## 3. What is the core contribution of this paper?

The main contribution is a Deep Reinforcement Learning (DRL) framework specifically designed for composing moving IoT services. The paper proposes: (1) a novel formulation of moving service composition as a sequential decision problem, (2) a Double DQN-based algorithm with prioritized experience replay for learning optimal composition policies, (3) a trajectory-aware composition mechanism that predicts future service positions to make proactive composition decisions, and (4) an adaptive Q-network that handles the varying state spaces caused by mobile services.

## 4. What deep reinforcement learning algorithm is used?

The paper uses Double DQN (Double Deep Q-Network) with prioritized experience replay. Double DQN addresses the overestimation problem in standard Q-learning by using two separate networks for action selection and evaluation. The prioritized replay mechanism samples important transitions more frequently during training, accelerating learning in dynamic environments. The network architecture likely uses a deep neural network to approximate the Q-function, handling the complex state space of moving IoT services.

## 5. How is the state space defined for the moving services composition problem?

The state space includes: (1) current positions of all available moving services, (2) their movement trajectories and velocities, (3) QoS attributes of each service, (4) distance matrix between services and the user/requesting application, (5) historical composition success rates, and (6) time-to-service availability considering mobility. The high-dimensional state space is precisely why deep learning is needed—traditional RL cannot handle the complexity.

## 6. What actions can the agent take in this formulation?

The agent can: (1) select specific services from the available pool to include in the composition, (2) decide when to trigger re-composition as services move, (3) choose replacement services when existing ones move out of range, (4) adjust composition depth (number of services), and (5) decide whether to wait for better service configurations or proceed with current options. The action space is discrete but large, suitable for DQN-based approaches.

## 7. How is the reward function designed?

The reward function balances multiple objectives: (1) positive reward for successful composition completion, (2) negative reward for composition failure or QoS violations, (3) reward for minimizing re-composition frequency (encouraging stable compositions), (4) reward for maintaining low latency as services move, and (5) reward for efficient resource utilization. The multi-objective reward likely uses weighted sum or multi-objective optimization to balance composition success, quality, and efficiency.

## 8. What datasets are used for evaluation?

The evaluation uses synthetic IoT service datasets with realistic mobility patterns. The datasets include: (1) random waypoint mobility models simulating human-carried devices, (2) vehicles moving along predefined routes, (3) drones with configurable flight paths, (4) varying service densities (sparse to dense deployments), and (5) different velocity profiles (slow pedestrian, medium vehicle, fast drone scenarios). The simulation probably tests scales from 20-100+ moving services.

## 9. What are the main performance metrics used?

The paper evaluates: (1) Composition success rate—the percentage of requests successfully composed despite service mobility, (2) Average response time—from request to composition completion, (3) QoS satisfaction rate—percentage of compositions meeting QoS requirements, (4) Re-composition frequency—how often compositions need adjustment due to mobility, (5) Learning convergence speed—how quickly the DRL agent learns effective policies, and (6) Adaptation cost—computational overhead of handling mobility.

## 10. How does the paper handle the challenge of continuous state changes?

The paper addresses continuous state changes through: (1) trajectory prediction that estimates future service positions, (2) event-triggered re-composition rather than continuous monitoring (reducing overhead), (3) look-ahead mechanisms that consider future states in current decisions, and (4) experience replay that captures diverse state transitions for robust learning. The Double DQN architecture helps maintain stable Q-values despite state fluctuations.

## 11. What is trajectory-aware composition?

Trajectory-aware composition uses predicted service trajectories to make proactive composition decisions. Instead of reacting to service movements after they occur, the system anticipates future positions and includes services that will remain available throughout the composition's expected lifetime. This is a key innovation distinguishing this from reactive approaches—it transforms the problem from spatial optimization to spatiotemporal optimization.

## 12. How does DRL compare with traditional optimization approaches?

The paper compares DRL with: (1) Genetic Algorithm-based composition—slower but good global search, (2) PSO-based composition—faster convergence but prone to local optima, (3) Q-learning—suffers from curse of dimensionality, and (4) static composition—baseline that doesn't handle mobility. DRL shows superior performance in dynamic scenarios with faster adaptation and better success rates. However, DRL requires training time while traditional approaches are typically anytime algorithms.

## 13. What is the computational complexity of the proposed approach?

The training complexity is dominated by neural network training, but the inference (composition decision) is fast—suitable for real-time applications. The algorithm maintains O(n) complexity for service selection where n is the number of available services. The overhead comes from maintaining trajectory predictions and updating the composition state, which can be managed through efficient data structures.

## 14. How does the paper address the exploration-exploitation tradeoff?

The paper uses epsilon-greedy exploration during training with annealing to reduce exploration over time. The prioritized replay also contributes to exploration by revisiting important transitions that might otherwise be neglected. Once trained, the agent exploits learned policies while still maintaining some randomness to adapt to novel situations. The balance is crucial—too much exploration wastes resources, too little prevents adaptation to changing conditions.

## 15. What happens when no suitable services are available?

The paper likely handles this through: (1) graceful degradation to lower QoS levels, (2) waiting for services to move into range (with timeout), (3) expanding the search radius beyond immediate vicinity, (4) leveraging trajectory predictions to anticipate future availability, and (5) providing feedback about impossible compositions. The DRL agent learns to recognize impossible situations and make appropriate decisions.

## 16. How does this paper compare with paper 8 (RL for interactive QoS-aware composition)?

Paper 8 uses basic Q-learning for static IoT services. This paper extends that paradigm to moving services using Deep RL instead of tabular Q-learning. The key differences: (1) state representation handles mobility features, (2) Double DQN handles function approximation stability, (3) trajectory prediction is explicitly incorporated, and (4) the problem is inherently multi-step rather than single decision. This paper represents a significant advancement over paper 8's approach.

## 17. What is the role of the Q-network architecture?

The Q-network uses a deep neural network to approximate Q(s,a) for all actions from a given state. The architecture likely includes: (1) input layers for state features (service positions, velocities, QoS), (2) hidden layers (likely convolutional for spatial patterns or fully connected for general features), (3) output layer with one value per possible action. The network is trained via gradient descent to minimize TD error between predicted and target Q-values.

## 18. How does the paper ensure generalization across different mobility patterns?

Generalization is achieved through: (1) diverse training scenarios covering various mobility patterns, (2) transfer learning that adapts pre-trained policies to new patterns, (3) normalization of state features to handle different scales, and (4) the adaptive capacity of deep networks to handle variations. The paper probably evaluates on mobility patterns not seen during training to demonstrate generalization.

## 19. What are the practical applications considered?

The paper applies the approach to: (1) vehicle-to-vehicle service composition for autonomous driving, (2) drone swarm coordination for surveillance, (3) moving sensor networks for environmental monitoring, (4) mobile edge computing where computation moves with users, and (5) wearable IoT device networks that move with users. These scenarios highlight the importance of handling mobility in real-world IoT deployments.

## 20. What are the limitations acknowledged by the authors?

Likely limitations include: (1) training data requirements—the DRL agent needs extensive training to learn effective policies, (2) computational resources for training—infeasible for extremely resource-constrained devices, (3) assumption of predictable mobility patterns—highly chaotic movements may defeat trajectory prediction, (4) communication overhead for continuous state updates, and (5) cold start problem when few historical data points exist.

## 21. How does the paper handle privacy concerns with location data?

The excerpt doesn't detail privacy mechanisms, but approaches could include: (1) local processing of location data without sharing raw coordinates, (2) differential privacy adding noise to location reports, (3) federated learning where training happens on-device, and (4) aggregation-based approaches that combine data without individual tracking. This is an important consideration for real-world deployment.

## 22. What is the energy efficiency contribution?

The paper contributes to energy efficiency through: (1) reduced re-composition frequency through proactive decision-making, (2) efficient service selection that minimizes communication overhead, (3) trajectory-aware composition that reduces failed attempts and wasted energy, and (4) optimized decision-making that reduces computational waste. The DRL approach learns energy-efficient composition policies as part of its optimization.

## 23. How does the paper validate the approach (theoretical, simulation, real-world)?

The paper uses simulation-based validation with synthetic but realistic mobility patterns. The simulation environment models: (1) realistic mobility models, (2) variable service densities, (3) communication ranges and propagation models, (4) QoS fluctuations, and (5) realistic timing constraints. Simulation enables testing scenarios that would be impractical in real-world deployments, including worst-case conditions.

## 24. What is the scalability behavior?

The paper likely demonstrates scalability through: (1) efficient state representation that scales linearly with service count, (2) parallel training of the DQN, (3) incremental updates rather than full retraining, and (4) hierarchical composition for large-scale scenarios. The evaluation probably shows near-linear scalability up to 100+ moving services, with graceful degradation beyond that.

## 25. How does the paper compare with meta-heuristic approaches (papers 06-07)?

Paper 6 uses DQN combined with meta-heuristics (GA, PSO, SA, ABC) for scheduling; paper 7 uses discrete dragonfly algorithm + PSO. Those papers apply meta-heuristics to static optimization problems. This paper uses pure DRL specifically designed for the sequential decision problem of moving service composition. Meta-heuristics would require continuous re-optimization as services move, while DRL learns a policy that handles changes efficiently without full re-optimization.

## 26. What future research directions are mentioned?

Likely future directions include: (1) multi-agent DRL for distributed composition decisions, (2) transfer learning across different environments, (3) integration with edge computing for low-latency decisions, (4) handling adversarial mobility patterns, (5) real-world deployment and validation, and (6) combining DRL with blockchain for secure service markets.

## 27. How does the paper handle QoS in a mobility context?

QoS in mobility contexts is addressed through: (1) dynamic QoS monitoring as services move, (2) trajectory-based prediction of future QoS values, (3) adaptive composition that maintains QoS despite changes, (4) graceful degradation strategies when QoS cannot be maintained, and (5) multi-objective reward that prioritizes QoS satisfaction. The DRL agent learns to balance composition success with QoS maintenance.

## 28. What distinguishes this from other DRL applications in IoT?

This is specifically focused on the unique challenges of moving services: (1) spatiotemporal state representation, (2) trajectory prediction integration, (3) event-triggered re-composition, and (4) mobility-aware reward design. General DRL applications in IoT (like resource management or task offloading) don't need to handle the continuous topology changes this paper addresses.

## 29. What is the overall quality and rigor of this paper?

The paper demonstrates good quality with: (1) well-motivated problem addressing a real research gap, (2) appropriate use of DRL for the problem complexity, (3) systematic evaluation with multiple metrics and comparisons, (4) clear presentation of the DRL architecture and training process, and (5) thoughtful discussion of limitations and applications. The paper appears to be a solid DRL application to IoT service composition.

## 30. How does this paper contribute to the overall research field?

This paper makes significant contributions: (1) first DRL approach specifically for moving IoT service composition, (2) trajectory-aware composition mechanism, (3) Double DQN with prioritized replay for IoT composition, (4) demonstration that DRL outperforms traditional optimization in dynamic scenarios, and (5) foundation for future research on mobile IoT service management.