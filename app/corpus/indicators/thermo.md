# THERMO

## Overview
Elders Thermometer

## pandas-ta Usage
```python
result = df.ta.thermo()
```

## Parameters
- length (default: None)
- long (default: None)
- short (default: None)
- mamode (default: None)
- asint (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.thermo()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on THERMO values

    return signals
```
