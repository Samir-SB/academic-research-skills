import numpy as np
import pandas as pd

# --- Columns -------------------------------------------------------

def drop_columns(df, columns = []):    
    df = df.drop(columns=columns)
    return df

def move_columns(df, col_name, new_position='front'):
    cols = df.columns.tolist()
    
    if new_position == 'front':
        cols.insert(0, cols.pop(cols.index(col_name)))
        
    elif new_position == 'end':
        cols.append(cols.pop(cols.index(col_name)))  
        
    df = df[cols]
    return df

def drop_duplicated_columns(df):
    # Removed duplicate columns
    duplicate_cols = df.columns[df.T.duplicated()]
    print("Removed duplicate columns:", duplicate_cols.tolist())
    df = df.loc[:, ~df.T.duplicated()]
    return df

def rename_columns(df):
    # rename columns
    
    # Move 'timestamp' to the first position   
    df = move_columns(df, 'timestamp')
    
    # Base columns that must appear first
    base_columns = ["timestamp", "user_lat", "user_lon"]
    
    # Generate AP names based on half the number of columns
    num_aps = df.shape[1] // 2
    aps = [f"ap{i}" for i in range(1, num_aps)]
        
    # Generate latitude and longitude columns for each AP
    ap_columns = [col for ap in aps for col in (f"{ap}_lat", f"{ap}_lon")]
    # Final ordered columns
    columns = base_columns + ap_columns
  
    df.columns = columns
    return df
    
# ---------------------MSG------------------------------------------------
def iterate_chunks(csv_file):
    # Iterate through the file in chunks of 10,000 rows
    for chunk in pd.read_csv('large_file.csv', chunksize=10000):
        # Process each chunk (e.g., perform analysis or filtering)
        print(f"Processing chunk of size: {len(chunk)}")
        
        
        
# # Fetches exactly N rows for every single group (if N rows exist)
    # df_sampled = df.groupby('id_p').sample(n=N, replace=True)