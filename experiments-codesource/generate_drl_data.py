import pandas as pd
import numpy as np

import helper_pandas as h_pd
import handling_missing_data as h_data

def filtering_by_timestamp(grouped_illinois_data, user_df, service_ids):
    
    for service_id in service_ids:    
        service_df = grouped_illinois_data.get_group(service_id)        
        
        # merge left user_df and service_df
        user_df = pd.merge(user_df, service_df, on='timestamp', how='left', suffixes=('', f'_{service_id}'))
        
        # drop unused columns
        user_df = user_df.drop(columns=[f'id_{service_id}'])
    
    # Drop unused columns
    user_df = user_df.drop(columns=['id'])     
    
    # Move timestamp column to front   
    user_df = h_pd.move_columns(user_df, 'timestamp')
    
    # Remove duplicated columns
    user_df = h_pd.drop_duplicated_columns(user_df)
    
    # Rename columns to be like ['timestamp', user_lat, user_lon, ap1_lat, ap1_lon, ...]
    user_df = h_pd.rename_columns(user_df)
    
    return user_df

def generate_drl_datasets(illinois_data, overlap_data, nb_aps = 5, all=False) -> pd.DataFrame:
    
    # Group by ID
    grouped_illinois_data = illinois_data.groupby('id') 
    grouped_overlap = overlap_data.groupby('id') 
    
    dfs = []
    for g_name, g_df in grouped_overlap:
        user_df = grouped_illinois_data.get_group(g_name) 
        
        service_ids = g_df['s_id'].values
        if len(service_ids) != nb_aps : # nb_aps: AP's number
            continue
        
        user_df = filtering_by_timestamp(grouped_illinois_data, user_df, service_ids)
        
        if user_df.shape[1] != (nb_aps *2 + 3) : # nb_aps: AP's number
            print("Duplicated columns on the Group:", g_name)
            continue
        
        # [x]: handling rows in which all APs coordinates is NaN (Delete or fill)
        
        user_df = h_data.linear_interpolate_gps(user_df)
        
        user_df.to_csv(f'{output_directory}/{nb_aps}/user{g_name}_df.csv', index=False)
        
        dfs.append(user_df)
        
    return dfs

    
# -------------------------------------------------------------------------------------------
# Example usage
# -------------------------------------------------------------------------------------------

if __name__ == "__main__":

    input_directory = 'output01' 
    output_directory = 'output02'  
    
    overlap_data = pd.read_csv(f'{input_directory}/overlap_data.csv') 
    illinois_data = pd.read_csv(f'{input_directory}/combined_illinois_data.csv') 
    
    nb_aps = 5
    dfs = generate_drl_datasets(illinois_data, overlap_data, nb_aps)
    print(len(dfs))
    
    df = pd.concat(dfs)
    df.to_csv(f'{output_directory}/{nb_aps}/combined_data.csv', index=False)
   


    
   