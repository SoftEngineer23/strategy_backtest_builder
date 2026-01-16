# MCGD

## Overview
McGinley Dynamic Indicator

## pandas-ta Usage
```python
result = df.ta.mcgd()
```

## Parameters
- length (default: None)
- c (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.mcgd()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on MCGD values

    return signals
```
