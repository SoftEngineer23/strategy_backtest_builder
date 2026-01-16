# EXHC

## Overview
Exhaustion Count

## pandas-ta Usage
```python
result = df.ta.exhc()
```

## Parameters
- length (default: None)
- cap (default: None)
- asint (default: None)
- show_all (default: None)
- nozeros (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.exhc()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on EXHC values

    return signals
```
