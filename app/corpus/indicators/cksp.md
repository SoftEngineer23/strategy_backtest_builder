# CKSP

## Overview
Chande Kroll Stop

## pandas-ta Usage
```python
result = df.ta.cksp()
```

## Parameters
- p (default: None)
- x (default: None)
- q (default: None)
- tvmode (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cksp()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CKSP values

    return signals
```
