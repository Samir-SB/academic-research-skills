"""
A2C-Based Moving IoT Service Composition - Annex A
STR Calculator and Environment

This module implements:
1. STRCalculator - Signal Transmission Reward calculation based on Euclidean distance
2. MovingIoTEnvironment - Simulation environment for moving IoT services

Based on the hierarchical model: distance → STR → capacity → reward
"""

import numpy as np


class STRCalculator:
    """
    Signal Transmission Reward (STR) Calculator
    Based on Euclidean distance with exponential attenuation

    Hierarchy:
    1. Calculate Euclidean distance: d_ij = sqrt((x_i - x_j)^2 + (y_i - y_j)^2)
    2. Calculate STR: STR(d_ij) = 1 if d <= Rc, else exp(-k * (d - Rc))
    3. Calculate Capacity: C_ij = B * log2(1 + STR * SNR_max)
    4. Calculate Reward: R = +C_total if C_total > C_min, else -1
    """

    def __init__(self, Rc=250, k=0.03, B=10e6, SNR_max=1000, C_min=1e6):
        """
        Initialize STR Calculator with parameters from Paper 17

        Args:
            Rc: Confident radius (m) - default 250m
            k: Decay factor - default 0.03
            B: Bandwidth (Hz) - default 10 MHz
            SNR_max: Maximum SNR at zero distance - default 1000 (30 dB)
            C_min: Minimum required capacity - default 1 Mbps
        """
        self.Rc = Rc
        self.k = k
        self.B = B
        self.SNR_max = SNR_max
        self.C_min = C_min

    def calculate_distance(self, pos1, pos2):
        """
        Calculate Euclidean distance between two positions

        Args:
            pos1: [x, y] position tuple
            pos2: [x, y] position tuple

        Returns:
            float: Euclidean distance
        """
        return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def calculate_str(self, distance):
        """
        Calculate STR based on distance with exponential attenuation

        STR(d) = 1 if d <= Rc
               = exp(-k * (d - Rc)) if d > Rc

        Args:
            distance: Euclidean distance

        Returns:
            float: STR value between 0 and 1
        """
        if distance <= self.Rc:
            return 1.0
        else:
            return np.exp(-self.k * (distance - self.Rc))

    def calculate_capacity(self, distance):
        """
        Calculate channel capacity using STR and Shannon-Hartley

        C = B * log2(1 + STR * SNR_max)

        Args:
            distance: Euclidean distance

        Returns:
            float: Channel capacity in bps
        """
        str_value = self.calculate_str(distance)
        snr_effective = str_value * self.SNR_max
        capacity = self.B * np.log2(1 + snr_effective)
        return capacity

    def calculate_reward(self, total_capacity):
        """
        Calculate reward based on capacity

        Args:
            total_capacity: Sum of capacities for all services

        Returns:
            float: Reward value
        """
        if total_capacity > self.C_min:
            return total_capacity / 1e6  # Normalize to Mbps
        else:
            return -1.0

    def select_service(self, services, user_pos, energy_req=None, time_req=None):
        """
        Select best service using hierarchical STR → Capacity → Score

        Score = C_ij * E_i * T_available

        Args:
            services: List of service dictionaries
            user_pos: User/device position [x, y]
            energy_req: Energy requirement (optional)
            time_req: Time requirement (optional)

        Returns:
            tuple: (best_service, best_score)
        """
        best_service = None
        best_score = -float("inf")

        for service in services:
            distance = self.calculate_distance(service["position"], user_pos)
            capacity = self.calculate_capacity(distance)

            # Score combines capacity with service attributes
            energy = service.get("energy", 1.0)
            available_time = service.get("available_time", 1.0)
            score = capacity * energy * available_time

            if score > best_score:
                best_score = score
                best_service = service

        return best_service, best_score

    def get_effective_radius(self, str_min=0.3):
        """
        Calculate effective coverage radius for given STR threshold

        R_effective = Rc - (1/k) * ln(STR_min)

        Args:
            str_min: Minimum STR threshold

        Returns:
            float: Effective radius in meters
        """
        return self.Rc - (1.0 / self.k) * np.log(str_min)


class MovingIoTEnvironment:
    """
    Simulation environment for moving IoT service composition

    Implements:
    - Service mobility (random waypoint model)
    - Device mobility
    - STR-based reward calculation
    """

    def __init__(self, num_services=50, area_size=1000, str_calc=None):
        """
        Initialize moving IoT environment

        Args:
            num_services: Number of moving services
            area_size: Size of simulation area (meters)
            str_calc: STRCalculator instance
        """
        self.num_services = num_services
        self.area_size = area_size
        self.str_calc = str_calc or STRCalculator()
        self.services = []
        self.device_pos = [area_size / 2, area_size / 2]
        self.device_velocity = [0, 0]
        self.time_step = 0

        self._initialize_services()

    def _initialize_services(self):
        """Initialize moving IoT services with random positions"""
        for i in range(self.num_services):
            service = {
                "id": i,
                "position": [
                    np.random.uniform(0, self.area_size),
                    np.random.uniform(0, self.area_size),
                ],
                "velocity": [np.random.uniform(-2, 2), np.random.uniform(-2, 2)],
                "energy": np.random.uniform(5, 30),
                "available_time": np.random.uniform(100, 500),
            }
            self.services.append(service)

    def reset(self):
        """Reset environment to initial state"""
        self._initialize_services()
        self.device_pos = [self.area_size / 2, self.area_size / 2]
        self.device_velocity = [np.random.uniform(-1, 1), np.random.uniform(-1, 1)]
        self.time_step = 0
        return self._get_state()

    def _get_state(self):
        """Get current state representation"""
        state = {
            "services": self.services.copy(),
            "device_pos": self.device_pos.copy(),
            "device_velocity": self.device_velocity.copy(),
            "time_step": self.time_step,
        }
        return state

    def step(self, action):
        """
        Execute action and return next state, reward, done

        Actions:
        - 0: Maintain (no change)
        - 1 to n: Select service i
        - n+1 to 2n: Replace service i with j

        Args:
            action: Integer action index

        Returns:
            tuple: (next_state, reward, done)
        """
        num_services = len(self.services)

        if action == 0:
            # Maintain - no change
            pass
        elif 1 <= action <= num_services:
            # Select service
            service_idx = action - 1
            if service_idx < len(self.services):
                self.services[service_idx]["available_time"] -= 1
        elif num_services < action < 2 * num_services:
            # Replace service
            old_idx = (action - num_services - 1) // num_services
            new_idx = (action - num_services - 1) % num_services
            if old_idx < len(self.services) and new_idx < len(self.services):
                self.services[old_idx] = self.services[new_idx].copy()

        # Update service positions (random waypoint model)
        for service in self.services:
            service["position"][0] += service["velocity"][0]
            service["position"][1] += service["velocity"][1]

            # Boundary reflection
            for dim in range(2):
                if (
                    service["position"][dim] < 0
                    or service["position"][dim] > self.area_size
                ):
                    service["velocity"][dim] *= -1
                    service["position"][dim] = np.clip(
                        service["position"][dim], 0, self.area_size
                    )

        # Update device position
        self.device_pos[0] += self.device_velocity[0]
        self.device_pos[1] += self.device_velocity[1]

        for dim in range(2):
            if self.device_pos[dim] < 0 or self.device_pos[dim] > self.area_size:
                self.device_velocity[dim] *= -1
                self.device_pos[dim] = np.clip(self.device_pos[dim], 0, self.area_size)

        self.time_step += 1

        # Calculate reward using STR-based capacity
        total_capacity = 0
        for service in self.services:
            distance = self.str_calc.calculate_distance(
                service["position"], self.device_pos
            )
            capacity = self.str_calc.calculate_capacity(distance)
            total_capacity += capacity

        reward = self.str_calc.calculate_reward(total_capacity)

        # Check done
        done = self.time_step >= 1000

        return self._get_state(), reward, done

    def get_distance_matrix(self):
        """
        Get distance matrix between all services and device

        Returns:
            numpy.ndarray: Distance matrix of shape (n_services, 1)
        """
        distances = []
        for service in self.services:
            dist = self.str_calc.calculate_distance(
                service["position"], self.device_pos
            )
            distances.append(dist)
        return np.array(distances)


if __name__ == "__main__":
    # Test STR Calculator
    str_calc = STRCalculator(Rc=250, k=0.03)

    # Test distance calculation
    pos1 = [0, 0]
    pos2 = [100, 100]
    distance = str_calc.calculate_distance(pos1, pos2)
    print(f"Distance: {distance:.2f} m")

    # Test STR calculation
    str_value = str_calc.calculate_str(distance)
    print(f"STR: {str_value:.4f}")

    # Test capacity calculation
    capacity = str_calc.calculate_capacity(distance)
    print(f"Capacity: {capacity / 1e6:.2f} Mbps")

    # Test environment
    env = MovingIoTEnvironment(num_services=10, area_size=500)
    state = env.reset()
    print(f"Initial state: {state['time_step']}")

    next_state, reward, done = env.step(0)
    print(f"Step result: reward={reward:.2f}, done={done}")
