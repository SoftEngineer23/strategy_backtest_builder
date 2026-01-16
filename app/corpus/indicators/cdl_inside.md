# CDL_INSIDE

## Overview
Inside Bar

## pandas-ta Usage
```python
result = df.ta.cdl_inside()
```

## Parameters
- asbool (default: None)
- scalar (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.cdl_inside()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on CDL_INSIDE values

    return signals
```
