# KURTOSIS

## Overview
Rolling Kurtosis

## pandas-ta Usage
```python
result = df.ta.kurtosis()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.kurtosis()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on KURTOSIS values

    return signals
```
