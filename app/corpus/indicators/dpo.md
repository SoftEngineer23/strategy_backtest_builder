# DPO

## Overview
Detrend Price Oscillator

## pandas-ta Usage
```python
result = df.ta.dpo()
```

## Parameters
- length (default: None)
- centered (default: True)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.dpo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on DPO values

    return signals
```
