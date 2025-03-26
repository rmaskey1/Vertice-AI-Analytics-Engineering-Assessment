import os
import sys

# Get the absolute path of the parent directory of the current script and add parent directory to module search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


import pandas as pd
import pprint
import json
from datetime import datetime, timedelta
from models.Level import Level
from models.MemberLevelScore import MemberLevelScore
from models.MemberProductAccount import MemberProductAccount
from models.LevelsFull import LevelsFull, LevelData, Movement
from models.StandardChartData import StandardChartData, StandardDataPoint
from models.Timeline import Timeline

def build_levels_full(levels: pd.DataFrame, member_level_scores: pd.DataFrame, member_level_scores_history: pd.DataFrame, member_product_accounts: pd.DataFrame) -> LevelsFull:

    # Convert member_id to string for consistency across DataFrames.
    for df in [levels, member_level_scores, member_level_scores_history, member_product_accounts]:
        if 'member_id' in df.columns:
            df['member_id'] = df['member_id'].astype(str)
    
    # Ensure date fields are treated as "datetime" objects for future datetime operations
    if 'score_date' in member_level_scores.columns:
        member_level_scores['score_date'] = pd.to_datetime(member_level_scores['score_date'], errors='coerce')
    if 'timestamp' in member_level_scores.columns:
        member_level_scores['timestamp'] = pd.to_datetime(member_level_scores['timestamp'], errors='coerce')
    member_level_scores_history['score_date'] = pd.to_datetime(member_level_scores_history['score_date'], errors='coerce')
    
    # Creating copy of member_level_scores dataframe as the dataframe will be manipulated later
    current_scores = member_level_scores.copy()
    
    # Sort levels by score (lowest threshold to highest threshold)
    levels = levels.sort_values('level_score_start').reset_index(drop=True)
    level_order = {level: id for id, level in enumerate(levels['level_name'])}
    
    # Create an IntervalIndex for level boundaries (using left-closed/left-inclusive intervals)
    levels_intervals = pd.IntervalIndex.from_arrays(
        levels['level_score_start'],
        levels['level_score_end'],
        closed='left'
    )
    level_labels = levels['level_name'].astype(str).tolist()
    
    # Use pd.cut to assign levels to current_scores
    current_scores['current_level'] = pd.cut(
        current_scores['level_score'],
        bins=levels_intervals,
        labels=level_labels,
        include_lowest=True,
        right=False
    )
    # Applying level_names as labels for each interval
    current_scores['current_level'] = current_scores['current_level'].cat.rename_categories(level_labels)
    
    # Map the current_level to a numeric index
    # Indices are used to track member movement from one level to the next
    current_scores['current_level_index'] = current_scores['current_level'].map(level_order)
    
    # Retrieving the reference current date to base the level timelines and movement off of
    # Using the timestamp listed in the member_level_scores data (2024-11-09 00:00:00.000)
    if 'timestamp' in current_scores.columns and current_scores['timestamp'].notnull().any():
        current_date = current_scores['timestamp'].max()
    else:
        current_date = pd.Timestamp(datetime.now())
    
    # Mapping Timeline attributes to numerical (day) values for datetime operations
    timeline_offsets = {
        Timeline.OneMonth.value: 30,
        Timeline.ThreeMonths.value: 90,
        Timeline.SixMonths.value: 180,
        Timeline.TwelveMonths.value: 365,
        Timeline.YearToDate.value: (current_date - pd.Timestamp(current_date.year, 1, 1)).days
    }
    
    # Dictionaries to store historical member counts and movement
    history_counts = {level: {} for level in levels['level_name']}
    movement_counts = {level: {} for level in levels['level_name']}
    
    # Iterate thru each timeline checkpoint
    for timeline_val, offset in timeline_offsets.items():
        if timeline_val == Timeline.YearToDate.value:
            cutoff_date = pd.Timestamp(current_date.year, 1, 1)
        else:
            cutoff_date = current_date - pd.Timedelta(days=offset)
        
        # Get historical records up to the cutoff date
        hist_before_cutoff = member_level_scores_history[member_level_scores_history['score_date'] <= cutoff_date]
        if hist_before_cutoff.empty:
            for level in levels['level_name']:
                history_counts[level][timeline_val] = 0
                movement_counts[level][timeline_val] = {'growth': 0, 'churn': 0}
            continue
        
        # For each member, get latest record at or before the cutoff
        hist_latest = hist_before_cutoff.sort_values('score_date').groupby('member_id', as_index=False).last()
        # Use level score intervals on historical scores
        hist_latest['historical_level'] = pd.cut(
            hist_latest['level_score'],
            bins=levels_intervals,
            labels=level_labels,
            include_lowest=True,
            right=False
        )
        hist_latest['historical_level'] = hist_latest['historical_level'].cat.rename_categories(level_labels)
        hist_latest['historical_level_index'] = hist_latest['historical_level'].map(level_order)
        
        # Merge current and historical data on member_id
        merged = pd.merge(current_scores, hist_latest[['member_id', 'historical_level', 'historical_level_index']], on='member_id', how='inner')
        
        # Handle missing historical indices with the current index
        # In this case, historical level indices are being filled with the current level indices, but dropping the row would result in the same outcome
        # Ultimately, we must assume that the user did not move up or down any levels if we are met with NaN data for index
        merged['historical_level_index'] = merged['historical_level_index'].fillna(merged['current_level_index'])
        
        # For each level, compute historical count and movement
        for level in levels['level_name']:

            # Getting total members in which their latest historical level is the one being checked in the loop
            hist_count = (hist_latest['historical_level'] == level).sum()
            history_counts[level][timeline_val] = int(hist_count)
            
            # Filtering to only get members at level being checked by the loop
            current_in_level = merged[merged['current_level'] == level]
            
            # Compare members' current level with their historical level from x time ago (timeline values)
            growth = (current_in_level['historical_level_index'].astype(int) < current_in_level['current_level_index'].astype(int)).sum()
            churn = (current_in_level['historical_level_index'].astype(int) > current_in_level['current_level_index'].astype(int)).sum()
            movement_counts[level][timeline_val] = {'growth': int(growth), 'churn': int(churn)}
    
    # LevelData + LevelsFull assembly
    level_data_list = []
    for i, level_row in levels.iterrows():
        level_name = level_row['level_name']
        score_start = level_row['level_score_start']
        score_end = level_row['level_score_end']
        
        # Current member count for this level
        curr_members = current_scores[current_scores['current_level'] == level_name]
        member_count = curr_members['member_id'].nunique()
        
        # Average product count for members in this level
        if member_count > 0:
            total_products = member_product_accounts[member_product_accounts['member_id'].isin(curr_members['member_id'])].shape[0]
            avg_product_count = round(total_products / member_count)   # Rounded to nearest whole number
        else:
            avg_product_count = 0
        
        # Building member_count_history chart
        history_points = []
        for timeline_val, count in history_counts[level_name].items():
            history_points.append(StandardDataPoint(key=timeline_val, value=count))
        chart_data = StandardChartData(points=history_points)
        
        # Building Movement objects
        movements = []
        for timeline_val, mv in movement_counts[level_name].items():
            try:
                timeline_enum = Timeline(timeline_val)
            except ValueError:
                continue
            movements.append(Movement(timeline=timeline_enum.value, growth=mv['growth'], churn=mv['churn']))
        
        # Final LevelData assembly
        level_data = LevelData(
            level=level_name,
            member_count=member_count,
            score_start=score_start,
            score_end=score_end,
            avg_product_count=avg_product_count,
            member_count_history=chart_data,
            movement=movements
        )
        level_data_list.append(level_data)
    
    return LevelsFull(levels=level_data_list)

if __name__ == '__main__':

    # Load the CSV files into Dataframes
    levels = pd.read_csv("../../data/levels.csv")
    member_level_scores = pd.read_csv("../../data/member_level_scores.csv")
    member_level_scores_history = pd.read_csv("../../data/member_level_scores_history.csv")
    member_product_accounts = pd.read_csv("../../data/member_product_accounts.csv")
    
    # Build the LevelsFull metric
    levels_full_metric = build_levels_full(levels, member_level_scores, member_level_scores_history, member_product_accounts)
    
    # Print the final output
    levels_full_output = pprint.pformat(levels_full_metric, width=610, indent=4, compact=False)
    print(levels_full_output)

    with open('levels_full.txt', 'w') as out:
        out.write(levels_full_output)
