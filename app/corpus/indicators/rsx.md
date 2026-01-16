# RSX

## Overview
Relative Strength Xtra

## pandas-ta Usage
```python
result = df.ta.rsx()
```

## Parameters
- length (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.rsx()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on RSX values

    return signals
```
