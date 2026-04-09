import pandas as pd
import haversine as hs
from haversine import Unit
from datetime import datetime, timedelta, time, date
import math
import time as t
import ast
import numpy as np
import os

from helper_env import build_ego_polar_states



def flock_based_algorithm(df, user_df, user_id):
    tem_filter_out = 0
    spat_filter_out = 0
    # add new column with empty list as value

    output_set = {}
    output_set['timestamp'] = user_df['timestamp']
    for ap_id in ap_ids:
        if ap_id == user_id:
            continue
        
        print('ap_id: ',ap_id)
        print('user_id: ',user_id)
        ap_df = df[df['id'] == ap_id]
        print(ap_df.head(2))
        print(user_df.head(2))
        
        '''
        STEP 1 : Temporal Mapper Phase.    
        '''
        # apply left_join to user trajectory and ms trajectory ON 'timestamp'
        merged_df = pd.merge(user_df, ap_df.reset_index(
            drop=True), on='timestamp', how='left', suffixes=('_u', '_s'))  

        # skip
        if merged_df.empty:
            tem_filter_out += 1
            continue
            
        if(len(merged_df.dropna()) < minimum_timestep):
            tem_filter_out += 1
            continue
        
        merged_df = merged_df.drop(columns=['timestamp', 'id_s'])

        '''
        STEP 2: Spatial Mapper Phase
        '''
        
        new_df = build_ego_polar_states(merged_df)
        distances = new_df['r'].values
        
        candidate_services_col = distances  < D       
        
        candidate_services_nb = np.count_nonzero(candidate_services_col)       

        # skip ms trajectory if overlap points number is less than 1
        if(candidate_services_nb < 1):
            spat_filter_out += 1
            continue

        output_set[ap_id] = candidate_services_col
        user_df.insert(loc=len(user_df.columns),
                       column=ap_id, value=df['id'])

    return user_df, pd.DataFrame(output_set), tem_filter_out, spat_filter_out


'''
 Initialization
'''
# user trajectory index
user_index = 0
# Moving IoT service provider number
ms_number = 10
# signal range radius is 300m
D = 500
minimum_timestep = 10
max_sampled_pairs=100,
num_users=50

# load dataset
# columns: latitude,longitude,timestamp,id
df = pd.read_csv('dataset/illinois_data.csv')
# 2. Convert 'timestamp' column to datetime, then extract only the time
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S').dt.time

# gathering all trajectory IDs
unique_ids = df['id'].unique()


# 1. Split IDs into Users and Access Points (APs)
user_ids = pd.Series(unique_ids).sample(n=num_users, random_state=42)
ap_ids = unique_ids[~np.isin(unique_ids, user_ids)]

''' 
flock_based_algorithm 
'''
for user_id in user_ids:
    if(user_index >= 56):
        user_index += 1
        continue
    
    # 2. Create sub-dataframes
    user_df = df[df['id'] == user_id]
    

    input_df, output_df, tem_filter_out, spat_filter_out = flock_based_algorithm(df, 
        user_df.reset_index(drop=True), user_id)
    
    print(output_df.shape[1])
    cs_number = output_df.shape[1] - 1
    print('#' * 30, {user_index}, '#' * 30)
    print(f'condidate services number = {cs_number} ',)
    print(f'{tem_filter_out} service dropped by temporal_mapper')
    print(f'{spat_filter_out} service dropped by spatial_mapper')
    if(cs_number > 2):
        folder_path = f'{cs_number}-{user_index}'
        # Check if the folder exists
        if not os.path.exists(folder_path):
            # Create the folder if it doesn't exist
            os.makedirs(folder_path)
        output_df.to_csv(f'{folder_path}/output.csv', index=False)
        input_df.to_csv(f'{folder_path}/input.csv', index=False)
    user_index += 1
    t.sleep(2)
