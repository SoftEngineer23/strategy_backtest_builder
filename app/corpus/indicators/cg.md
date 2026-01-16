# CG

## Overview
Center of Gravity

## pandas-ta Usage
```python
result = df.ta.cg()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cg()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CG values

    return signals
```
