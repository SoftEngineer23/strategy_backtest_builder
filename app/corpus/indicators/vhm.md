# VHM

## Overview
Volume Heatmap

## pandas-ta Usage
```python
result = df.ta.vhm()
```

## Parameters
- length (default: None)
- std_length (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.vhm()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on VHM values

    return signals
```
