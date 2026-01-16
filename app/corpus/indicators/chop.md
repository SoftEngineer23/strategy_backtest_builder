# CHOP

## Overview
Choppiness Index

## pandas-ta Usage
```python
result = df.ta.chop()
```

## Parameters
- length (default: None)
- atr_length (default: None)
- ln (default: None)
- scalar (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.chop()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CHOP values

    return signals
```
