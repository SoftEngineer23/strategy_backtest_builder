# MAD

## Overview
Rolling Mean Absolute Deviation

## pandas-ta Usage
```python
result = df.ta.mad()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.mad()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on MAD values

    return signals
```
