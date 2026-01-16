# PVI

## Overview
Positive Volume Index

## pandas-ta Usage
```python
result = df.ta.pvi()
```

## Parameters
- length (default: None)
- initial (default: None)
- mamode (default: None)
- overlay (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.pvi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PVI values

    return signals
```
