import numpy as np

def add_score_column(df, weight_player_level, weight_two_year_gain, weight_months_active, weight_days_since_post, score_col='score'):
    weighted_sum = (
        weight_player_level * df['PlayerLevel'] +
        weight_two_year_gain * df['TwoYearGain'] +
        weight_months_active * df['MonthsActive'] +
        weight_days_since_post * np.maximum(0, 365 - df['daysSincePost'])
    )
    df[score_col] = weighted_sum
    return df

def aggregate_scores(merged_df, score_columns='score'):
    if isinstance(score_columns, str):
        score_columns = [score_columns]
    sum_columns = score_columns  # List of columns to sum
    sum_dict = {col: 'sum' for col in sum_columns if col in merged_df.columns}
    agg_df = merged_df.groupby(['date', 'Symbol'], as_index=False).agg(sum_dict)
    if 'daily_gain' in merged_df.columns:
        daily_gain_df = merged_df[['date', 'Symbol', 'daily_gain']].drop_duplicates(subset=['date', 'Symbol'])
        agg_df = agg_df.merge(daily_gain_df, on=['date', 'Symbol'], how='left')
    return agg_df

def filter_date_range(agg_df, start_date, end_date):
    agg_df = agg_df[(agg_df['date'] >= start_date) & (agg_df['date'] <= end_date)]
    agg_df = agg_df.sort_values('date')
    return agg_df
