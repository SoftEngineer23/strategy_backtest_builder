# PSAR

## Overview
Parabolic Stop and Reverse

## pandas-ta Usage
```python
result = df.ta.psar()
```

## Parameters
- af0 (default: None)
- af (default: None)
- max_af (default: None)
- tv (default: False)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.psar()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on PSAR values

    return signals
```
