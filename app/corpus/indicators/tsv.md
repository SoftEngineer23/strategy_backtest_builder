# TSV

## Overview
Time Segmented Value

## pandas-ta Usage
```python
result = df.ta.tsv()
```

## Parameters
- length (default: None)
- signal (default: None)
- mamode (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.tsv()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on TSV values

    return signals
```
