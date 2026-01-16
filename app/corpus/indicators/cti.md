# CTI

## Overview
Correlation Trend Indicator

## pandas-ta Usage
```python
result = df.ta.cti()
```

## Parameters
- length (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cti()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CTI values

    return signals
```
