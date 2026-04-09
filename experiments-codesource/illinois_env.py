import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd

class APSelectionEnv(gym.Env):
    """
    Custom Environment for Access Point selection based on pre-calculated 
    polar coordinates and capacity rewards.
    """
    metadata = {"render_modes": ["human"]}

    def __init__(self, states_df, rewards_df):
        super(APSelectionEnv, self).__init__()

        # 1. Data Validation
        assert len(states_df) == len(rewards_df), "States and Rewards DataFrames must have the same length."
        self.states_df = states_df.reset_index(drop=True)
        self.rewards_df = rewards_df.reset_index(drop=True)
        
        # Calculate N (number of APs)
        # Assuming states_df has 3 columns per AP: [r, cos, sin]
        self.num_aps = self.rewards_df.shape[1]
        self.total_steps = len(self.states_df)
        self.current_step = 0

        # 2. Action Space: Discrete selection of an AP (0 to N-1)
        self.action_space = spaces.Discrete(self.num_aps)

        # 3. Observation Space: Relative polar coordinates for N APs
        # Flattened shape: (N * 3,) or (N, 3)
        # Format: [r1, cos1, sin1, r2, cos2, sin2, ...]
        low = np.array([-np.inf] * ((self.num_aps - 1) * 3))
        high = np.array([np.inf] * ((self.num_aps - 1) * 3))
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float64)

    def _get_obs(self):
        # Extract the current row as a flat numpy array
        return self.states_df.iloc[self.current_step].values.astype(np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.current_step = 0
        observation = self._get_obs()
        info = {}
        
        return observation, info

    def step(self, action):
        # 1. Calculate Reward
        # Action is the index of the AP chosen
        reward = self.rewards_df.iloc[self.current_step, action]

        # 2. Transition to next state
        self.current_step += 1
        
        # 3. Check if sequence is finished
        terminated = self.current_step >= self.total_steps - 1
        truncated = False
        
        # 4. Get next observation
        if not terminated:
            observation = self._get_obs()
        else:
            # Return last observation if terminated
            observation = self.states_df.iloc[-1].values.astype(np.float32)

        info = {
            "step": self.current_step,
            "chosen_ap": action,
            "capacity": reward
        }

        return observation, float(reward), terminated, truncated, info

    def render(self):
        print(f"Step: {self.current_step} | Last Reward: {self.rewards_df.iloc[self.current_step-1].max()}")
        
        

# ----------------------------- Main Processing -----------------------------

if __name__ == "__main__":
    states_df = pd.read_csv('data_5.csv')
    rewards_df = pd.read_csv('cap.csv')
    env = APSelectionEnv(states_df, rewards_df)
    
    state, info = env.reset() 
    reward = env.rewards_df.iloc[env.current_step, 0]
    reward2 = env.rewards_df.iloc[env.current_step, 3]
    print(state)
    print(reward, reward2)
    
    obs, info = env.reset()
    for _ in range(100):
        action = env.action_space.sample()  # Replace with agent.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        
        if terminated:
            break