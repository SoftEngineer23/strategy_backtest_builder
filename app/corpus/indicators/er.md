# ER

## Overview
Efficiency Ratio

## pandas-ta Usage
```python
result = df.ta.er()
```

## Parameters
- length (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.er()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ER values

    return signals
```
