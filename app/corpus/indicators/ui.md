# UI

## Overview
Ulcer Index

## pandas-ta Usage
```python
result = df.ta.ui()
```

## Parameters
- length (default: None)
- scalar (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.ui()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on UI values

    return signals
```
