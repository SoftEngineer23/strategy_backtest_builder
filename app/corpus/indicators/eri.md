# ERI

## Overview
Elder Ray Index

## pandas-ta Usage
```python
result = df.ta.eri()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.eri()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on ERI values

    return signals
```
