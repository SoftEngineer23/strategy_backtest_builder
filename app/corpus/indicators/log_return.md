# LOG_RETURN

## Overview
Log Return

## pandas-ta Usage
```python
result = df.ta.log_return()
```

## Parameters
- length (default: None)
- cumulative (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.log_return()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on LOG_RETURN values

    return signals
```
