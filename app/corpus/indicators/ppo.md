# PPO

## Overview
Percentage Price Oscillator

## pandas-ta Usage
```python
result = df.ta.ppo()
```

## Parameters
- fast (default: None)
- slow (default: None)
- signal (default: None)
- scalar (default: None)
- mamode (default: None)
- talib (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ppo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PPO values

    return signals
```
