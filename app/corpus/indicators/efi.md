# EFI

## Overview
Elder's Force Index

## pandas-ta Usage
```python
result = df.ta.efi()
```

## Parameters
- length (default: None)
- mamode (default: None)
- drift (default: None)
- offset (default: None)

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.efi()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on EFI values

    return signals
```
