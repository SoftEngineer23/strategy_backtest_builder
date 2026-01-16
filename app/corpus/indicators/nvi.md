# NVI

## Overview
Negative Volume Index

## pandas-ta Usage
```python
result = df.ta.nvi()
```

## Parameters
- length (default: None)
- initial (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.nvi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on NVI values

    return signals
```
