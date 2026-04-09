from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass
import logging

import pandas as pd
import numpy as np

# Assuming these are in your helper_env.py
# from helper_env import reshape_data, build_ego_polar_states, compute_rewards

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ProcessorConfig:
    input_dir: Path
    output_dir: Path
    max_sampled_pairs: int = 100
    num_user_trajectories: int = 50
    random_seed: int = 42

# =============================================================================
# DATA CORE LOGIC
# =============================================================================

def generate_user_ap_interactions(
    df: pd.DataFrame, 
    num_users: int, 
    seed: int
) -> pd.DataFrame:
    """
    Vectorized generation of User-Access Point pairs matched by timestamp.
    
    Instead of looping through users and services, we split the IDs and 
    perform a single 'inner merge' on timestamp to find all possible overlaps.
    """
    logger.info(f"Generating interactions for {num_users} users")
    
    unique_ids = df['id'].unique()
    
    # 1. Split IDs into Users and Access Points (APs)
    user_ids = pd.Series(unique_ids).sample(n=num_users, random_state=seed)
    ap_ids = unique_ids[~np.isin(unique_ids, user_ids)]
    
    # 2. Create sub-dataframes
    users_df = df[df['id'].isin(user_ids)]
    aps_df = df[df['id'].isin(ap_ids)]
    
    # 3. Vectorized Merge: Match by timestamp
    # This finds every instance where a user and an AP were recorded at the same time
    interactions = pd.merge(
        users_df,
        aps_df,
        on='timestamp',
        suffixes=('_user', '_ap')
    )
    
    # 4. Create a unique identifier for the specific User-AP pair
    interactions['pair_id'] = (
        interactions['id_user'].astype(str) + '_' + 
        interactions['id_ap'].astype(str)
    )
    
    # Clean up columns: we no longer need the raw ID columns or timestamp for state building
    interactions = interactions.drop(columns=['id_user', 'id_ap', 'timestamp'])
    
    return interactions

def sample_unique_pairs(
    df: pd.DataFrame, 
    max_pairs: int, 
    seed: int
) -> pd.DataFrame:
    """Samples unique User-AP pairs and shuffles the resulting observations."""
    unique_pairs = df['pair_id'].unique()
    num_available = len(unique_pairs)
    
    logger.info(f"Total unique User-AP pairs found: {num_available}")
    
    # Determine how many pairs to sample
    sample_count = min(num_available, max_pairs)
    if num_available < max_pairs:
        logger.warning(f"Requested {max_pairs} pairs, but only {num_available} exist.")

    # Randomly select the pair IDs
    sampled_pair_ids = pd.Series(unique_pairs).sample(n=sample_count, random_state=seed)
    
    # Filter the main dataframe to only include these pairs
    sampled_df = df[df['pair_id'].isin(sampled_pair_ids)]
    
    # Global shuffle of all observations
    shuffled_df = sampled_df.sample(frac=1, random_state=seed).reset_index(drop=True)
    
    logger.info(f"Final dataset size: {len(shuffled_df)} observations")
    return shuffled_df

# =============================================================================
# EXECUTION PIPELINE
# =============================================================================

def run_pipeline(cfg: ProcessorConfig):
    """Orchestrates the data augmentation and sampling process."""
    input_path = cfg.input_dir / 'illinois_data.csv'
    
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        return

    # Phase 1: Load and Augment
    logger.info("Phase 1: Loading and merging trajectories")
    raw_trajectories = pd.read_csv(input_path)
    
    # Generate the full interaction matrix (Vectorized)
    interaction_df = generate_user_ap_interactions(
        raw_trajectories, 
        cfg.num_user_trajectories, 
        cfg.random_seed
    )
    
    # Phase 2: Sample and Shuffle
    logger.info("Phase 2: Sampling unique pairs")
    final_states_df = sample_unique_pairs(
        interaction_df, 
        cfg.max_sampled_pairs, 
        cfg.random_seed
    )
    
    # Phase 3: Export
    output_filename = f'df_shuffled_{cfg.max_sampled_pairs}.csv'
    output_path = cfg.output_dir / output_filename
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    
    final_states_df.to_csv(output_path, index=False)
    logger.info(f"Pipeline complete. File saved to: {output_path}")

def main():
    config = ProcessorConfig(
        input_dir=Path('dataset'),
        output_dir=Path('data/random'),
        max_sampled_pairs=100,
        num_user_trajectories=50
    )
    
    run_pipeline(config)

if __name__ == "__main__":
    main()