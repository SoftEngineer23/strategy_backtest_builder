# CDL_DOJI

## Overview
Doji

## pandas-ta Usage
```python
result = df.ta.cdl_doji()
```

## Parameters
- length (default: None)
- factor (default: None)
- scalar (default: None)
- asint (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cdl_doji()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CDL_DOJI values

    return signals
```
