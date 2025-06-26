import numpy as np

def simulate_portfolio(agg_df, top_n=10, allocation='equal'):
    values = []
    value = 1.0
    dates = []
    for day, group in agg_df.groupby('date'):
        topn = group.sort_values('score', ascending=False).head(top_n)
        topn_valid = topn[topn['daily_gain'].notna()]
        if not topn_valid.empty:
            if allocation == 'equal':
                weights = np.ones(len(topn_valid)) / len(topn_valid)
            elif allocation == 'proportional':
                scores = topn_valid['score'].to_numpy()
                weights = scores / scores.sum() if scores.sum() > 0 else np.ones(len(scores)) / len(scores)
            else:
                raise ValueError('Unknown allocation type')
            gains = topn_valid['daily_gain'].to_numpy()
            weighted_gain = np.dot(weights, gains)
            value = value * (1 + weighted_gain / 100)
        values.append(value)
        dates.append(day)
    return dates, values

def calculate_daily_change(values):
    values = np.array(values)
    return np.diff(values, prepend=values[0])

def calculate_max_drawdown(values):
    values = np.array(values)
    running_max = np.maximum.accumulate(values)
    drawdowns = (running_max - values) / running_max
    return np.max(drawdowns)

def calculate_drawdown_series(values):
    values = np.array(values)
    running_max = np.maximum.accumulate(values)
    drawdowns = (running_max - values) / running_max
    return drawdowns
