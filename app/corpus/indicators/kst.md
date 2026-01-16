# KST

## Overview
'Know Sure Thing'

## pandas-ta Usage
```python
result = df.ta.kst()
```

## Parameters
- signal (default: None)
- roc1 (default: None)
- roc2 (default: None)
- roc3 (default: None)
- roc4 (default: None)
- sma1 (default: None)
- sma2 (default: None)
- sma3 (default: None)
- sma4 (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.kst()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on KST values

    return signals
```
