# SSF3

## Overview
Ehlers's 3 Pole Super Smoother Filter

## pandas-ta Usage
```python
result = df.ta.ssf3()
```

## Parameters
- length (default: None)
- pi (default: None)
- sqrt3 (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ssf3()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SSF3 values

    return signals
```
