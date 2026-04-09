from pathlib import Path
from dataclasses import dataclass
import logging
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ProcessorConfig:
    input_dir: Path
    output_dir: Path
    max_sampled_pairs: int = 200
    random_seed: int = 42

# =============================================================================
# DATA CORE LOGIC
# =============================================================================

def generate_overlapping_interactions(
    df: pd.DataFrame, 
    overlap_map: pd.DataFrame
) -> pd.DataFrame:
    """
    Vectorized generation of overlapping User-AP trajectories based on an overlap map.
    
    This replaces nested for-loops by utilizing relational database merge strategies.
    """
    logger.info("Starting DRL dataset generation (Vectorized)")
    
    # 1. Split IDs into Users and Access Points (APs)
    user_ids = overlap_map['id'].unique()
    ap_ids = overlap_map['s_id'].unique()
    
    # 2. Create sub-dataframes [latitude,longitude,timestamp,id]
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

def run_pipeline(cfg: ProcessorConfig) -> None:
    logger.info("Phase 1: Loading datasets")       
    
    illinois_data_path = cfg.input_dir / 'illinois_data.csv'
    overlap_data_path = cfg.input_dir / 'overlap_data.csv'
    
    if not illinois_data_path.exists() or not overlap_data_path.exists():
        logger.error("Required input files are missing. Check directory paths.")
        return

    # Load data
    illinois_data = pd.read_csv(illinois_data_path) 
    overlap_data = pd.read_csv(overlap_data_path)[['id','s_id']]
    # print(overlap_data.head(2))
    # overlap_data = overlap_data[['id','s_id']]
    # overlap_data = overlap_data.drop(columns=['nb_overlap_1000','nb_overlap_500','nb_overlap_200'])
        
    # Phase 1: Generate overlapped state vectors
    merged_df = generate_overlapping_interactions(illinois_data, overlap_data)
    
    
    # Phase 2: Sample and shuffle
    final_states_df = sample_unique_pairs(merged_df, cfg.max_sampled_pairs, cfg.random_seed)        

    # Phase 3: Save to disk
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    output_file = cfg.output_dir / f'df_shuffled_{cfg.max_sampled_pairs}.csv'
    
    final_states_df.to_csv(output_file, index=False)
    logger.info(f"Processing complete. Saved to: {output_file}")

def main():
    # Setup Paths
    input_path = Path('dataset')
    output_path = Path('data/selected')
    
    config = ProcessorConfig(
        input_dir=input_path, 
        output_dir=output_path,
        max_sampled_pairs=300
    )
    
    run_pipeline(config)

if __name__ == "__main__":
    main()