# CMF

## Overview
Chaikin Money Flow

## pandas-ta Usage
```python
result = df.ta.cmf()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cmf()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CMF values

    return signals
```
