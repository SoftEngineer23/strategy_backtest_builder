# HT_TRENDLINE

## Overview
Hilbert Transform TrendLine

## pandas-ta Usage
```python
result = df.ta.ht_trendline()
```

## Parameters
- talib (default: None)
- prenan (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ht_trendline()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on HT_TRENDLINE values

    return signals
```
