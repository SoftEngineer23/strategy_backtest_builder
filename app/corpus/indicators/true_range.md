# TRUE_RANGE

## Overview
True Range

## pandas-ta Usage
```python
result = df.ta.true_range()
```

## Parameters
- talib (default: None)
- prenan (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.true_range()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on TRUE_RANGE values

    return signals
```
