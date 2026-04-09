import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
import logging
import time
import math

from helper_env import get_reshaped_rewards, get_reshaped_states, fill_states_columns

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
LOGGING = False

class APSelectionEnv(gym.Env):
    """
    Custom Environment for Access Point selection based on pre-calculated 
    polar coordinates and capacity rewards.
    """
    metadata = {"render_modes": ["human"]}

    def __init__(self, df, num_aps=5, on_line = False, final_nb_aps=None, p = None ):
        super(APSelectionEnv, self).__init__()

        if p is not None:
            logger.warning(
                "APSelectionEnv constructor argument 'p' is deprecated and ignored. "
                "Permutation is now generated at reset()."
            )

        # Validation
        # final_nb_aps must be greater than or equal to num_aps
        if final_nb_aps is not None and final_nb_aps < num_aps:
            raise ValueError(f"final_nb_aps cannot be lower the num_aps . Received: {final_nb_aps}")

        self.final_nb_aps = final_nb_aps
        self.num_shunks = num_aps
        self.requires_padding_shuffle = final_nb_aps is not None and final_nb_aps > num_aps
        self.num_aps = final_nb_aps if self.requires_padding_shuffle else num_aps
        self.current_permutation = None

        self.data = df.iloc[:, :4]      
        self.is_on_line = on_line       
        self.total_steps = len(self.data) // num_aps
        self.current_step = 0

        if not self.is_on_line:
            self.base_states_df = get_reshaped_states(self.data, num_aps)
            self.base_rewards_df = get_reshaped_rewards(self.data, num_aps)
            self.states_df = self.base_states_df
            self.rewards_df = self.base_rewards_df

        self.num_states = 3 * self.num_aps

        # 2. Action Space: Discrete selection of an AP (0 to N-1)
        self.action_space = spaces.Discrete(self.num_aps + 1 ) # +1 for dummy service

        # 3. Observation Space: Relative polar coordinates for N APs
        # Flattened shape: (N * 3,) or (N, 3)
        # Format: [r1, cos1, sin1, r2, cos2, sin2, ...]
        low = np.array([-np.inf] * self.num_states)
        high = np.array([np.inf] * self.num_states)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float64)
    
    def _get_raw_obs(self):
        s_idx = self.current_step * self.num_shunks
        e_idx = s_idx + self.num_shunks
        self.states_chunk_df = self.data.iloc[s_idx:e_idx, :]     
       
    def _get_obs(self):
        # Extract the current row as a flat numpy array
        if self.is_on_line :
            self._get_raw_obs()
            self.state = get_reshaped_states(self.states_chunk_df, self.num_shunks)#.values[0, :]           
            self.rewards = get_reshaped_rewards(self.states_chunk_df, self.num_shunks)#.values[0, :]
            
            if self.num_shunks < self.num_aps :
                self.state, self.rewards = fill_states_columns(
                    self.state,
                    self.rewards,
                    self.num_aps,
                    self.current_permutation,
                )
                
            self.state = self.state.values[0, :]
            self.rewards = self.rewards.values[0, :]
            
        else: 
            self.state = self.states_df.values[self.current_step, :]
            self.rewards = self.rewards_df.values[self.current_step, :]
            
        return self.state

    def _refresh_episode_permutation(self):
        if self.requires_padding_shuffle:
            self.current_permutation = self.np_random.permutation(self.num_aps)
        else:
            self.current_permutation = None

    def _refresh_offline_episode_data(self):
        if self.is_on_line:
            return
        if self.requires_padding_shuffle:
            self.states_df, self.rewards_df = fill_states_columns(
                self.base_states_df.copy(),
                self.base_rewards_df.copy(),
                self.num_aps,
                self.current_permutation,
            )
        else:
            self.states_df = self.base_states_df
            self.rewards_df = self.base_rewards_df

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._refresh_episode_permutation()
        self._refresh_offline_episode_data()
        self.current_step = 0
        observation = self._get_obs()       
        info = {}
        
        return observation, info

    def step(self, action):
        # 1. Calculate Reward
        # Action is the index of the AP chosen  
        reward = self.rewards[action]

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
            self.current_step -= 1
            observation = self._get_obs()

        info = {
            "step": self.current_step,
            "chosen_ap": action,
            "capacity": reward
        }

        return observation, float(reward), terminated, truncated, info

    def render(self):
        print(f"Step: {self.current_step} | Last Reward: {self.rewards_df.iloc[self.current_step-self.step_value].max()}")
        
        

# ----------------------------- Main Processing -----------------------------

if __name__ == "__main__":
    
    DATA_PATH = 'data/random/df_shuffled_100.csv'
    df = pd.read_csv(DATA_PATH)
    # TODO
    env = APSelectionEnv(df.iloc[:21, :], num_aps = 5, final_nb_aps=10, on_line=False)
    actions_dim = env.action_space.n
    states_dim = env.num_states
    
    logger.info(f'ENV: states({states_dim }) * actions({actions_dim }) num_aps: {env.num_aps} is_online: {env.is_on_line}')    

    start_time = time.perf_counter()
    
    obs, info = env.reset()
    terminated = False
    total_reward = 0
    idx = 0
    while not terminated:
        action = env.action_space.sample()  # Replace with agent.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action) 
        total_reward += reward 
        if terminated:
            logger.info(f"Terminated at {env.current_step} step {idx}")
            break
        
        idx += 1
        
    end_time = time.perf_counter()
    print('total reward: ', total_reward)
    logger.info(f"Execution time: {end_time - start_time:.4f} seconds")
    LOGGING and logger.info("Testing Env completed")
