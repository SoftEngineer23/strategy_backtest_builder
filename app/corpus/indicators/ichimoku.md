# ICHIMOKU

## Overview
Ichimoku Kinkō Hyō

## pandas-ta Usage
```python
result = df.ta.ichimoku()
```

## Parameters
- tenkan (default: None)
- kijun (default: None)
- senkou (default: None)
- include_chikou (default: True)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ichimoku()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ICHIMOKU values

    return signals
```
