import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pathb = r"C:\Users\Muhammad Haris\Downloads\IPL_Ball_by_Ball_2008_2022.csv"
balls = pd.read_csv(pathb)
pathm = r"C:\Users\Muhammad Haris\Downloads\IPL_Matches_2008_2022.csv"
match = pd.read_csv(pathm)

ipl = balls.merge(match, on='ID')


def batsman_record(batsman_name):
    batsman = ipl[ipl['batter'] == batsman_name]

    # total runs
    runs = batsman.groupby('Season')['batsman_run'].sum().reset_index()
    runs.rename(columns={'batsman_run': 'TotalRuns'}, inplace=True)

    # innings (number of matches)
    matches = batsman.groupby('Season')['MatchNumber'].nunique().reset_index()
    matches.rename(columns={'MatchNumber': 'Innings'}, inplace=True)

    # batting average (runs per innings)
    average = runs.copy()
    average['Avg'] = average['TotalRuns'] / matches['Innings']
    average = average[['Season', 'Avg']]

    # strike rate
    balls_faced = batsman.groupby(
        'Season')['batsman_run'].count().reset_index()
    strike_rate = runs.copy()
    strike_rate['StrikeRate'] = (strike_rate['TotalRuns'] /
                                 balls_faced['batsman_run']) * 100
    strike_rate = strike_rate[['Season', 'StrikeRate']]

    # highest score per season
    high_score = (
        batsman.groupby(['Season', 'MatchNumber'])['batsman_run']
        .sum()
        .reset_index()
        .sort_values('batsman_run', ascending=False)
        .drop_duplicates('Season', keep='first')
        .rename(columns={'batsman_run': 'HighestScore'})
        [['Season', 'HighestScore']]
        .sort_values('Season')
    )

    # merge all
    merged_df = runs.merge(matches, on='Season') \
                    .merge(average, on='Season') \
                    .merge(strike_rate, on='Season') \
                    .merge(high_score, on='Season')

    merged_df.set_index('Season', inplace=True)

    return merged_df


batsman_name = input('enter batsman name which record u want to see')
print(batsman_record(batsman_name))
