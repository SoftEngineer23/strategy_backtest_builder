# MFI

## Overview
Money Flow Index

## pandas-ta Usage
```python
result = df.ta.mfi()
```

## Parameters
- length (default: None)
- talib (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.mfi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on MFI values

    return signals
```
