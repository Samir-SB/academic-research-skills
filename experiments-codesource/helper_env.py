import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
LOGGING = False


class Config:
    """Configuration constants for data processing and model parameters."""
    
    # Earth and GPS constants
    EARTH_RADIUS_METERS = 6371000.0 #6378137.0
        
    # Signal propagation parameters
    REFERENCE_DISTANCE = 300.0  # meters, distance below which SNR = 1.0
    DECAY_RATE = 0.01  # exponential decay rate for SNR
    MAX_SIGNAL_RANGE = 500.0  # meters, distance beyond which SNR = 0.0
    
    # State space parameters
    MAX_RANGE = 500.0  # meters, maximum range for state representation

    OUTPUT_DIR = Path('data/random')
    DATA_PATH = OUTPUT_DIR/'df_shuffled_100.csv'
    AP_NUM = 10
cfg = Config()

# =============================================================================
# COORDINATE TRANSFORMATIONS
# =============================================================================

def extract_coords(data: pd.DataFrame | pd.Series) -> np.ndarray:
    arr = data.to_numpy()
    # Ensure 2D
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    
    # Force numeric dtype
    arr = arr.astype(float)
    
    return arr[:, :4].T

def gps_to_enu(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """Convert GPS coordinates to local ENU (East-North-Up) coordinates."""
    lat1, lon1, lat2, lon2 = extract_coords(df)
    
    lat_p_rad = np.deg2rad(lat1)
    lat_g_rad = np.deg2rad(lat2)
    
    dlat = lat_g_rad - lat_p_rad
    dlon = np.deg2rad(lon2 - lon1)
    
    # Calculate ENU coordinates
    x = Config.EARTH_RADIUS_METERS * np.cos(lat_p_rad) * dlon  # East
    y = Config.EARTH_RADIUS_METERS * dlat  # North
    
    return x, y

def enu_to_polar(x: np.ndarray, y: np.ndarray, heading: float = 0.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert ENU Cartesian coordinates to polar coordinates."""
    r = np.hypot(x, y)
    theta_global = np.arctan2(x, y) 

    # Adjust for agent heading (ego-centric frame)
    theta_relative = theta_global - heading
    
    # Normalize angle to [-π, π]
    theta_relative = np.arctan2(np.sin(theta_relative), np.cos(theta_relative))
    
    return r, np.cos(theta_relative), np.sin(theta_relative)

def build_ego_polar_states(df: pd.DataFrame, heading: float = 0.0, max_range: float = cfg.MAX_RANGE) -> pd.DataFrame:
    """Build polar state representations for all rows efficiently using vectorization."""
    LOGGING and logger.info(f"Building states from {len(df)} rows")
    
    if df.empty:
        return pd.DataFrame(columns=['r', 'cos', 'sin'])    
    
    x, y = gps_to_enu(df)
    r, cos_theta, sin_theta = enu_to_polar(x, y, heading)
    
    # Vectorized clipping
    mask = r > max_range
    r[mask] = max_range
    cos_theta[mask] = 0.0
    sin_theta[mask] = 0.0
    
    return pd.DataFrame({
        'r': r,
        'cos': cos_theta,
        'sin': sin_theta
    }, index=df.index)

def compute_capacity(distance: np.ndarray, reference_distance: float = cfg.REFERENCE_DISTANCE, decay_rate: float = cfg.DECAY_RATE, max_range: float = cfg.MAX_RANGE) -> np.ndarray:
    """Calculate channel capacity using Shannon's formula."""
    snr = np.zeros_like(distance, dtype=float)
    
    close_mask = distance <= reference_distance
    snr[close_mask] = 1.0
    
    mid_mask = (distance > reference_distance) & (distance < max_range)
    snr[mid_mask] = np.exp(-decay_rate * (distance[mid_mask] - reference_distance))
    
    return np.log2(1 + snr)

def compute_rewards(df: pd.DataFrame) -> pd.DataFrame:
    """Compute reward function values."""
    LOGGING and logger.info("Phase 4: Computing reward function")
    
    if df.empty:
        return pd.DataFrame()
    
    x, y = gps_to_enu(df)
    distances = np.hypot(x, y)       
    capacity_values = compute_capacity(distances) 
    
    return pd.DataFrame(capacity_values, columns=['capacity']) 

def reshape_data(df: pd.DataFrame, ap_num: int) -> pd.DataFrame:
    """Reshapes a DataFrame by flattening 'ap_num' consecutive rows into a single row."""
    raw_data = df.values
    total_rows, num_features = raw_data.shape
    
    num_samples = total_rows // ap_num
    total_valid_rows = num_samples * ap_num
    num_columns_new = ap_num * num_features
    
    if total_rows % ap_num > 0:
        remainder = total_rows % ap_num
        logger.warning(f"Truncating {remainder} rows to fit ap_num of {ap_num}")

    flattened_data = raw_data[:total_valid_rows].reshape(num_samples, num_columns_new)
    
    new_column_names = [
        f"{col_name}_{step}" 
        for step in range(ap_num) 
        for col_name in df.columns
    ]
    
    reshaped_df = pd.DataFrame(
        data=flattened_data, 
        columns=new_column_names,
        index=range(num_samples)
    )
    
    LOGGING and logger.info(f"Reshaped: {total_rows}x{num_features} -> {reshaped_df.shape}")
    return reshaped_df

def get_reshaped_states(df, num_aps):
    transformed_data = build_ego_polar_states(df)
    return reshape_data(transformed_data, num_aps)

def get_reshaped_rewards(df, num_aps):
    rewards_df = compute_rewards(df)
    rewards_df = reshape_data(rewards_df, num_aps)
    
    # Add dummy service reward
    all_zero_penalty = (rewards_df.values == 0).all(axis=1).astype(float)
    rewards_df['all_zero_penalty'] = all_zero_penalty
    
    return rewards_df

def shuffling_columns(states, rewards, p=None):
    if p is None:
        N = len(rewards.columns) - 1 # exclude dummy service
        p = np.random.permutation(N)

    new_p = np.append(p, len(p))
    
    rewards_shuffled = rewards.iloc[:, new_p]  
    state_indices = np.concatenate([np.arange(i*3, (i+1)*3) for i in p])
    states_shuffled = states.iloc[:, state_indices]
    
    return states_shuffled, rewards_shuffled

def fill_states_columns(states, rewards, final_nb_aps, p=None):
    """Pads the state and reward DataFrames up to final_nb_aps."""
    # 1. Accurately calculate the current number of APs
    # (Rewards columns length minus 1 for the 'all_zero_penalty' column)
    current_aps = len(rewards.columns) - 1
    
    # 2. Prepare new columns to concatenate
    new_states_cols = {}
    new_rewards_cols = {}
    
    # Loop starts from current_aps up to the final target
    for i in range(current_aps, final_nb_aps):                
        new_states_cols[f'r_{i}'] = 500.0
        new_states_cols[f'cos_{i}'] = 0.0
        new_states_cols[f'sin_{i}'] = 0.0
        
        # Fixed: Changed from 'cap_i' to 'capacity_i' to match compute_rewards output
        new_rewards_cols[f'capacity_{i}'] = 0.0

    # 3. Concatenate using pandas blocks to prevent memory fragmentation
    if new_states_cols: 
        new_states_df = pd.DataFrame(new_states_cols, index=states.index)
        new_rewards_df = pd.DataFrame(new_rewards_cols, index=rewards.index)

        states = pd.concat([states, new_states_df], axis=1)
        rewards = pd.concat([rewards, new_rewards_df], axis=1)
    
    # 4. Move the penalty column cleanly to the end of the DataFrame
    if 'all_zero_penalty' in rewards.columns:
        rewards['all_zero_penalty'] = rewards.pop('all_zero_penalty')
    
    # 5. Shuffle and return
    states, rewards = shuffling_columns(states, rewards, p)
    return states, rewards


# ----------------------------- Main Processing -----------------------------

if __name__ == "__main__":
    
    # Mock data generation for safe testing if the CSV is missing locally
    if not cfg.DATA_PATH.exists():
        logger.warning(f"{cfg.DATA_PATH} not found. Creating mock DataFrame for execution.")
        df = pd.DataFrame(np.random.rand(100, 4) * 100, columns=['lat_user', 'lon_user', 'lat_ap', 'lon_ap'])
    else:
        df = pd.read_csv(cfg.DATA_PATH)
    
    # Method 1: Multiple DRL models (fixed num_aps)
    states = get_reshaped_states(df, num_aps=5)
    rewards = get_reshaped_rewards(df, num_aps=5)
   
    # Method 2: Only one Model (Variable num_aps)
    final_nb_aps = 10
    new_states, new_rewards = fill_states_columns(states, rewards, final_nb_aps)
   
    new_df = new_rewards[new_rewards['all_zero_penalty'] > 0]
    print('new_df')
    print(new_df)