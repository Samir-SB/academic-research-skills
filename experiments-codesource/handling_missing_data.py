import pandas as pd
import numpy as np


def create_complete_timeline(df):
    df = df.sort_values('timestamp').copy()
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S', errors='coerce')
    
    # Get time range
    start_time = df['timestamp'].min()
    end_time = df['timestamp'].max()
    
    # Create complete 1-second timeline
    complete_timeline = pd.date_range(start=start_time, end=end_time, freq='1s')
    
    # Create new dataframe with complete timeline
    complete_timeline_df = pd.DataFrame({
        'timestamp': complete_timeline
    })          
    
    # Merge with existing data - this preserves all original values
    complete_timeline_df = complete_timeline_df.merge(df[['timestamp', 'latitude',  'longitude']], on='timestamp', how='left', )

    # Reset index
    complete_timeline_df = complete_timeline_df.reset_index()
    
    return complete_timeline_df


def linear_interpolate_gps(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp",
    gps_cols: list[str] | None = None,
) -> pd.DataFrame:
    """
    Linearly interpolate GPS latitude/longitude columns using time-based interpolation.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe containing timestamp and GPS columns.
    timestamp_col : str
        Name of the timestamp column.
    gps_cols : list[str], optional
        List of GPS columns to interpolate (e.g. ['lat1','lon1','lat2','lon2']).
        If None, all numeric columns except timestamp are interpolated.

    Returns
    -------
    pd.DataFrame
        Interpolated dataframe.
    """

    # ---- Convert timestamp first (robust to bad rows) ----
    # ts = pd.to_datetime(df[timestamp_col], format="%H:%M:%S", errors="coerce")
    ts = pd.to_datetime(df[timestamp_col], errors="coerce")
    
    # Drop rows with invalid timestamps
    valid = ts.notna()
    df = df.loc[valid].copy()
    df[timestamp_col] = ts[valid]

    # ---- Sort and set index ----
    df = df.sort_values(timestamp_col)
    df = df.set_index(timestamp_col)

    # ---- Select GPS columns ----
    if gps_cols is None:
        gps_cols = df.select_dtypes(include=np.number).columns.tolist()

    # ---- Vectorized time interpolation ----
    df[gps_cols] = (
        df[gps_cols]
        .interpolate(method="time", limit_direction="both")
    )

    # ---- Restore column ----
    df = df.reset_index()

    return df
    
if __name__ == "__main__":
    df = pd.read_csv('output02/5/user89_df.csv')  
    
    df = linear_interpolate_gps(df)
    df.to_csv('data_filled.csv', index=False)