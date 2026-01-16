# HILO

## Overview
Gann HiLo Activator

## pandas-ta Usage
```python
result = df.ta.hilo()
```

## Parameters
- high_length (default: None)
- low_length (default: None)
- mamode (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.hilo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on HILO values

    return signals
```
