# JMA

## Overview
Jurik Moving Average Average

## pandas-ta Usage
```python
result = df.ta.jma()
```

## Parameters
- length (default: None)
- phase (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.jma()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on JMA values

    return signals
```
