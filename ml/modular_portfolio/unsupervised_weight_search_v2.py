import numpy as np
from scipy.optimize import differential_evolution
from feature_engineering import add_score_column, aggregate_scores, filter_date_range
from portfolio_simulation import simulate_portfolio
import pandas as pd
import multiprocessing
import gc

# Caching for expensive gain calculations
gain_cache = {}

def calc_total_gain(weights, df):
    key = tuple(np.round(weights, 8))
    if key in gain_cache:
        gain = gain_cache[key]
        print(f"[CACHE] Objective called with weights={weights}, gain={gain}")
        return gain
    df = add_score_column(
        df,
        weights[0], weights[1], weights[2], weights[3],
        score_col='score')
    agg_df = aggregate_scores(df, score_columns='score')
    agg_df = filter_date_range(agg_df, pd.to_datetime('2024-06-01'), pd.to_datetime('2025-05-31'))
    dates, values = simulate_portfolio(agg_df, top_n=10, allocation='equal')
    if len(values) > 0:
        total_gain = (values[-1] - 1.0) * 100
        gain_cache[key] = total_gain
        return total_gain
    gain_cache[key] = None
    return None

def objective(weights, merged_df):
    df = merged_df.copy()
    gain = calc_total_gain(weights, df)
    del df
    print(f"Objective called with weights={weights}, gain={gain if gain is not None else 'None (penalty applied)'}")
    if gain is None:
        return 1e6
    return -gain

def find_best_vector(merged_df):
    cpu_count = multiprocessing.cpu_count()
    print(f"CPU count: {cpu_count}")
    bounds = [(0, 1)] * 4  # 4 weights
    print("Running global optimization with differential_evolution...")
    result = differential_evolution(
        objective,
        bounds,
        args=(merged_df,),  # keep comma so interpreted as tuple instead of object
        polish=True,
        disp=True,
        updating='deferred',
        workers=cpu_count,  # Use single worker to avoid memory issues
        popsize=15,
        maxiter=100,
    )
    print("Best weights found (unsupervised optimization):", result.x)
    print("Actual total gain with optimized weights:", -result.fun)
    return result.x, -result.fun
