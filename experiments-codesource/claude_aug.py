# https://claude.ai/chat/fc49b934-9b21-45e0-8efe-f13b449fe30a
"""
Deep Reinforcement Learning Dataset Processor

This module processes GPS trajectory data and prepares it for deep reinforcement
learning models. It handles coordinate transformations, state space construction,
and reward function calculations.

Key Features:
- GPS to ENU (East-North-Up) coordinate transformation
- Polar coordinate conversion for ego-centric representation
- Vectorized distance and signal quality calculations
- Efficient batch processing of trajectory data
"""

from pathlib import Path
from typing import List, Tuple, Optional
import logging

import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

class Config:
    """Configuration constants for data processing and model parameters."""
    
    # Earth and GPS constants
    EARTH_RADIUS_METERS = 6378137.0
    EARTH_RADIUS_KM = 6371000.0
    
    # Signal propagation parameters
    REFERENCE_DISTANCE = 300.0  # meters, distance below which SNR = 1.0
    DECAY_RATE = 0.05  # exponential decay rate for SNR
    MAX_SIGNAL_RANGE = 500.0  # meters, distance beyond which SNR = 0.0
    
    # State space parameters
    MAX_RANGE = 500.0  # meters, maximum range for state representation
    
    # Data sampling defaults
    DEFAULT_RANDOM_SEED = 42
    DEFAULT_NUM_SAMPLES = 200
    DEFAULT_NUM_ACCESS_POINTS = 20


# =============================================================================
# DATA FILTERING AND MERGING
# =============================================================================

def filter_by_timestamp(
    grouped_data: pd.core.groupby.DataFrameGroupBy,
    user_df: pd.DataFrame,
    service_ids: np.ndarray
) -> List[pd.DataFrame]:
    """
    Filter and merge user trajectory data with service provider data by timestamp.
    
    Args:
        grouped_data: Grouped DataFrame by service ID
        user_df: User trajectory data with timestamp, latitude, longitude
        service_ids: Array of service IDs to process
    
    Returns:
        List of merged DataFrames, one per service ID
    """
    result_dfs = []
    
    for service_id in service_ids:
        try:
            service_df = grouped_data.get_group(service_id)
        except KeyError:
            logger.warning(f"Service ID {service_id} not found in grouped data")
            continue
        
        # Merge on timestamp, keeping all user records
        merged_df = pd.merge(
            user_df,
            service_df,
            on='timestamp',
            how='left',
            suffixes=('', '_ap')
        )
        
        # Remove rows with missing access point coordinates
        merged_df = merged_df.dropna(subset=['latitude_ap', 'longitude_ap'])
        
        if merged_df.empty:
            logger.warning(f"No valid data after merge for service ID {service_id}")
            continue
        
        # Create composite ID for pedestrian-access point pairs
        merged_df['id_p'] = (
            merged_df['id'].astype(str) + '_' + 
            merged_df['id_ap'].astype(str)
        )
        
        # Drop unnecessary columns
        merged_df = merged_df.drop(columns=['timestamp', 'id', 'id_ap'])
        
        result_dfs.append(merged_df)
    
    logger.info(f"Processed {len(result_dfs)} service IDs successfully")
    return result_dfs


def generate_drl_datasets(
    illinois_data: pd.DataFrame,
    overlap_data: pd.DataFrame
) -> List[pd.DataFrame]:
    """
    Generate datasets for deep reinforcement learning from trajectory data.
    
    This function processes overlapping trajectory data between users and
    service providers, creating paired datasets for each user-service combination.
    
    Args:
        illinois_data: Main trajectory data with columns [id, timestamp, latitude, longitude]
        overlap_data: Overlap information with columns [id, s_id]
    
    Returns:
        List of processed DataFrames ready for DRL training
    """
    logger.info("Starting DRL dataset generation")
    
    # Group data by ID for efficient lookups
    grouped_illinois = illinois_data.groupby('id')
    grouped_overlap = overlap_data.groupby('id')
    
    all_dfs = []
    
    for user_id, overlap_group in grouped_overlap:
        try:
            user_df = grouped_illinois.get_group(user_id)
        except KeyError:
            logger.warning(f"User ID {user_id} not found in Illinois data")
            continue
        
        service_ids = overlap_group['s_id'].values
        user_service_dfs = filter_by_timestamp(grouped_illinois, user_df, service_ids)
        all_dfs.extend(user_service_dfs)
    
    logger.info(f"Generated {len(all_dfs)} datasets total")
    return all_dfs


# =============================================================================
# COORDINATE TRANSFORMATIONS
# =============================================================================

def gps_to_enu(
    lat_pedestrian: np.ndarray,
    lon_pedestrian: np.ndarray,
    lat_goal: np.ndarray,
    lon_goal: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convert GPS coordinates to local ENU (East-North-Up) coordinates.
    
    The ENU coordinate system is a local Cartesian coordinate system with:
    - x-axis pointing East
    - y-axis pointing North
    - Origin at the pedestrian position
    
    Args:
        lat_pedestrian: Pedestrian latitude in degrees
        lon_pedestrian: Pedestrian longitude in degrees
        lat_goal: Goal/provider latitude in degrees
        lon_goal: Goal/provider longitude in degrees
    
    Returns:
        Tuple of (x, y) coordinates in meters (East, North)
    """
    lat_p_rad = np.deg2rad(lat_pedestrian)
    lat_g_rad = np.deg2rad(lat_goal)
    
    dlat = lat_g_rad - lat_p_rad
    dlon = np.deg2rad(lon_goal - lon_pedestrian)
    
    # Calculate ENU coordinates
    x = Config.EARTH_RADIUS_METERS * np.cos(lat_p_rad) * dlon  # East
    y = Config.EARTH_RADIUS_METERS * dlat  # North
    
    return x, y


def enu_to_polar(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convert ENU Cartesian coordinates to polar coordinates.
    
    Args:
        x: East coordinate in meters
        y: North coordinate in meters
    
    Returns:
        Tuple of (r, theta) where:
        - r: radial distance in meters
        - theta: angle in radians (0 = North, clockwise positive)
    """
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(x, y)  # atan2(East, North) gives 0 = North
    return r, theta


def compute_ego_polar(
    lat_pedestrian: np.ndarray,
    lon_pedestrian: np.ndarray,
    lat_goal: np.ndarray,
    lon_goal: np.ndarray,
    heading: float = 0.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute ego-centric polar representation of goal position.
    
    This transformation creates a representation relative to the agent's
    heading, suitable for reinforcement learning state space.
    
    Args:
        lat_pedestrian: Pedestrian latitude in degrees
        lon_pedestrian: Pedestrian longitude in degrees
        lat_goal: Goal latitude in degrees
        lon_goal: Goal longitude in degrees
        heading: Agent heading in radians (0 = North, clockwise)
    
    Returns:
        Tuple of (r, cos_theta, sin_theta) where:
        - r: distance to goal in meters
        - cos_theta: cosine of relative angle
        - sin_theta: sine of relative angle
    """
    # Convert to local ENU coordinates
    x, y = gps_to_enu(lat_pedestrian, lon_pedestrian, lat_goal, lon_goal)
    
    # Convert to polar
    r, theta_global = enu_to_polar(x, y)
    
    # Adjust for agent heading (ego-centric frame)
    theta_relative = theta_global - heading
    
    # Normalize angle to [-π, π]
    theta_relative = np.arctan2(np.sin(theta_relative), np.cos(theta_relative))
    
    return r, np.cos(theta_relative), np.sin(theta_relative)


# =============================================================================
# STATE SPACE CONSTRUCTION
# =============================================================================

def build_state_from_row(
    row: pd.Series,
    heading: float = 0.0,
    max_range: float = Config.MAX_RANGE
) -> Tuple[float, float, float]:
    """
    Build state representation from a single data row.
    
    Args:
        row: Data row with [latitude, longitude, latitude_ap, longitude_ap]
        heading: Agent heading in radians
        max_range: Maximum range for clipping distant access points
    
    Returns:
        Tuple of (r, cos_theta, sin_theta) state representation
    """
    lat_user, lon_user = row.iloc[0], row.iloc[1]
    lat_ap, lon_ap = row.iloc[2], row.iloc[3]
    
    r, cos_theta, sin_theta = compute_ego_polar(
        lat_user, lon_user, lat_ap, lon_ap, heading
    )
    
    # Clip distant providers and zero out direction
    if r > max_range:
        r = max_range
        cos_theta, sin_theta = 0.0, 0.0
    
    return r, cos_theta, sin_theta


def build_states_from_dataframe(
    df: pd.DataFrame,
    heading: float = 0.0,
    max_range: float = Config.MAX_RANGE
) -> pd.DataFrame:
    """
    Build state representations for all rows in a DataFrame.
    
    Args:
        df: DataFrame with GPS coordinates
        heading: Agent heading in radians
        max_range: Maximum range for state representation
    
    Returns:
        DataFrame with columns [r, cos, sin]
    """
    logger.info(f"Building states from {len(df)} rows")
    
    states = df.apply(
        lambda row: build_state_from_row(row, heading, max_range),
        axis=1
    )
    
    # Convert list of tuples to numpy array
    states_array = np.vstack(states.values)
    
    # Create DataFrame with descriptive column names
    states_df = pd.DataFrame(
        states_array,
        columns=['r', 'cos', 'sin']
    )
    
    return states_df


def reshape_data(
    df: pd.DataFrame,
    n_groups: int
) -> pd.DataFrame:
    """
    Reshape DataFrame by grouping consecutive rows.
    
    This function reshapes data so that every n_groups consecutive rows
    are combined into a single row. Useful for creating observation
    vectors with multiple access points.
    
    Args:
        df: Input DataFrame
        n_groups: Number of rows to group together
    
    Returns:
        Reshaped DataFrame with n_groups times more columns
    
    Note:
        Data is truncated to fit evenly into groups (rows % n_groups are dropped)
    """
    n_rows, n_cols = df.shape
    n_complete_groups = n_rows // n_groups
    n_truncated_rows = n_rows - (n_complete_groups * n_groups)
    
    if n_truncated_rows > 0:
        logger.warning(
            f"Truncating {n_truncated_rows} rows to fit {n_groups}-row groups"
        )
    
    # Truncate to fit evenly
    valid_length = n_complete_groups * n_groups
    reshaped_values = df.iloc[:valid_length, :].values.reshape(
        n_complete_groups, n_groups * n_cols
    )
    
    reshaped_df = pd.DataFrame(reshaped_values)
    logger.info(f"Reshaped from {n_rows}x{n_cols} to {reshaped_df.shape}")
    
    return reshaped_df


# =============================================================================
# REWARD FUNCTION COMPONENTS
# =============================================================================

def compute_haversine_distance(
    lat1: np.ndarray,
    lon1: np.ndarray,
    lat2: np.ndarray,
    lon2: np.ndarray
) -> np.ndarray:
    """
    Calculate great-circle distance between points using Haversine formula.
    
    Vectorized implementation for efficient batch processing.
    
    Args:
        lat1, lon1: First point coordinates in degrees
        lat2, lon2: Second point coordinates in degrees
    
    Returns:
        Distance in meters
    """
    # Convert to radians
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    
    # Haversine formula
    a = (np.sin(dphi / 2)**2 + 
         np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2)**2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    return Config.EARTH_RADIUS_KM * c


def compute_snr(
    distance: np.ndarray,
    reference_distance: float = Config.REFERENCE_DISTANCE,
    decay_rate: float = Config.DECAY_RATE,
    max_range: float = Config.MAX_SIGNAL_RANGE
) -> np.ndarray:
    """
    Calculate Signal-to-Noise Ratio based on distance.
    
    Uses a piecewise function:
    - SNR = 1.0 for distance <= reference_distance
    - SNR = exp(-k * (distance - reference_distance)) for intermediate distances
    - SNR = 0.0 for distance >= max_range
    
    Args:
        distance: Distance in meters
        reference_distance: Distance threshold for perfect signal
        decay_rate: Exponential decay rate constant
        max_range: Distance beyond which signal is zero
    
    Returns:
        SNR values (0.0 to 1.0)
    """
    conditions = [
        distance <= reference_distance,
        distance >= max_range
    ]
    choices = [
        1.0,
        0.0
    ]
    
    # Exponential decay for intermediate distances
    default = np.exp(-decay_rate * (distance - reference_distance))
    
    return np.select(conditions, choices, default=default)


def compute_capacity(snr: np.ndarray) -> np.ndarray:
    """
    Calculate channel capacity using Shannon's formula.
    
    Capacity = log2(1 + SNR)
    
    Args:
        snr: Signal-to-Noise Ratio
    
    Returns:
        Channel capacity in bits per second per Hertz
    """
    return np.log2(1 + snr)


# =============================================================================
# PIPELINE EXECUTION
# =============================================================================

class DRLDataProcessor:
    """
    Complete pipeline for processing trajectory data for DRL training.
    """
    
    def __init__(
        self,
        input_dir: Path,
        output_dir: Path,
        num_samples: int = Config.DEFAULT_NUM_SAMPLES,
        num_access_points: int = Config.DEFAULT_NUM_ACCESS_POINTS,
        random_seed: int = Config.DEFAULT_RANDOM_SEED
    ):
        """
        Initialize the data processor.
        
        Args:
            input_dir: Directory containing input CSV files
            output_dir: Directory for output files
            num_samples: Number of user-AP pairs to sample
            num_access_points: Number of APs per observation
            random_seed: Random seed for reproducibility
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.num_samples = num_samples
        self.num_access_points = num_access_points
        self.random_seed = random_seed
        
        # Create output directory if needed
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized processor: {num_samples} samples, "
                   f"{num_access_points} APs per sample")
    
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load input data from CSV files."""
        logger.info("Loading input data")
        
        overlap_path = self.input_dir / 'overlap_data.csv'
        illinois_path = self.input_dir / 'combined_illinois_data.csv'
        
        overlap_data = pd.read_csv(overlap_path)
        illinois_data = pd.read_csv(illinois_path)
        
        logger.info(f"Loaded {len(overlap_data)} overlap records, "
                   f"{len(illinois_data)} Illinois records")
        
        return overlap_data, illinois_data
    
    def process_and_merge(
        self,
        overlap_data: pd.DataFrame,
        illinois_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Process and merge datasets."""
        logger.info("Phase 1: Processing and merging datasets")
        
        dfs_list = generate_drl_datasets(illinois_data, overlap_data)
        combined_df = pd.concat(dfs_list, axis=0, ignore_index=True)
        
        # # Save intermediate result
        # output_path = self.output_dir / 'merged_data.csv'
        # combined_df.to_csv(output_path, index=False)
        # logger.info(f"Saved merged data: {len(combined_df)} rows")
        
        return combined_df
    
    def sample_and_shuffle(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sample unique user-AP pairs and shuffle."""
        logger.info(f"Phase 2: Sampling {self.num_samples} unique pairs")
        
        # Sample unique user-AP pairs
        unique_ids = df['id_p'].drop_duplicates()
        
        if len(unique_ids) < self.num_samples:
            logger.warning(
                f"Only {len(unique_ids)} unique pairs available, "
                f"sampling all of them"
            )
            sampled_ids = unique_ids
        else:
            sampled_ids = unique_ids.sample(
                n=self.num_samples,
                random_state=self.random_seed
            )
        
        # Filter and shuffle
        df_sampled = df[df['id_p'].isin(sampled_ids)]
        df_shuffled = df_sampled.sample(
            frac=1,
            random_state=self.random_seed
        ).reset_index(drop=True)
        
        logger.info(f"Sampled and shuffled: {len(df_shuffled)} rows")
        return df_shuffled
    
    def build_states(self, df: pd.DataFrame) -> pd.DataFrame:
        """Build state representations."""
        logger.info("Phase 3: Building state representations")
        
        states_df = build_states_from_dataframe(df)
        reshaped_states = reshape_data(states_df, self.num_access_points)
        
        # Save states
        output_path = self.output_dir / 'states.csv'
        reshaped_states.to_csv(output_path, index=False)
        logger.info(f"Saved state data: {reshaped_states.shape}")
        
        return reshaped_states, df
    
    def compute_rewards(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute reward function values."""
        logger.info("Phase 4: Computing reward function")
        
        # Extract coordinates
        u_lat = df['latitude'].values
        u_lon = df['longitude'].values
        ap_lat = df['latitude_ap'].values
        ap_lon = df['longitude_ap'].values
        
        # Vectorized calculations
        distances = compute_haversine_distance(u_lat, u_lon, ap_lat, ap_lon)
        snr_values = compute_snr(distances)
        capacity_values = compute_capacity(snr_values)
        
        # Reshape capacity
        capacity_df = pd.DataFrame(capacity_values, columns=['capacity'])
        reshaped_capacity = reshape_data(capacity_df, self.num_access_points)
        
        # Add penalty flag for rows with all-zero capacity
        reshaped_capacity['all_zero_penalty'] = (
            (reshaped_capacity == 0).all(axis=1).astype(float)
        )
        
        # Save rewards
        output_path = self.output_dir / 'rewards.csv'
        reshaped_capacity.to_csv(output_path, index=False)
        logger.info(f"Saved reward data: {reshaped_capacity.shape}")
        
        return reshaped_capacity
    
    def run(self) -> None:
        """Execute the complete processing pipeline."""
        logger.info("=" * 70)
        logger.info("Starting DRL Data Processing Pipeline")
        logger.info("=" * 70)
        
        try:
            # Load data
            overlap_data, illinois_data = self.load_data()
            
            # Phase 1: Merge and process
            merged_df = self.process_and_merge(overlap_data, illinois_data)
            
            # Phase 2: Sample and shuffle
            shuffled_df = self.sample_and_shuffle(merged_df)
            
            # Phase 3: Build states
            states_df, original_df = self.build_states(shuffled_df)
            
            # Phase 4: Compute rewards
            rewards_df = self.compute_rewards(original_df)
            
            logger.info("=" * 70)
            logger.info("Pipeline completed successfully!")
            logger.info(f"Output files saved to: {self.output_dir}")
            logger.info("=" * 70)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            raise


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    
    # Configuration
    INPUT_DIR = Path('data')
    OUTPUT_DIR = Path('data')
    
    # Initialize and run processor
    processor = DRLDataProcessor(
        input_dir=INPUT_DIR,
        output_dir=OUTPUT_DIR,
        num_samples=200,
        num_access_points=25,
        random_seed=64
    )
    
    processor.run()


if __name__ == "__main__":
    main()