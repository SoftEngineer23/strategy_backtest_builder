# SQUEEZE_PRO

## Overview
Squeeze Pro

## pandas-ta Usage
```python
result = df.ta.squeeze_pro()
```

## Parameters
- bb_length (default: None)
- bb_std (default: None)
- kc_length (default: None)
- kc_scalar_narrow (default: None)
- kc_scalar_normal (default: None)
- kc_scalar_wide (default: None)
- mom_length (default: None)
- mom_smooth (default: None)
- use_tr (default: None)
- mamode (default: None)
- prenan (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.squeeze_pro()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on SQUEEZE_PRO values

    return signals
```
