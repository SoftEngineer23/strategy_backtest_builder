"""
Auto-generate indicator documentation from pandas-ta.
"""

import pandas_ta as ta
import pandas as pd
import inspect
from pathlib import Path


def get_all_indicators():
    """Get all available indicators from pandas-ta."""
    indicators = set()

    for name in dir(ta):
        obj = getattr(ta, name)
        if callable(obj) and not name.startswith('_'):
            try:
                sig = inspect.signature(obj)
                params = list(sig.parameters.keys())
                if any(p in params for p in ['close', 'high', 'low', 'open_', 'volume']):
                    indicators.add(name)
            except (ValueError, TypeError):
                continue

    return sorted(indicators)


def get_indicator_info(name):
    """Extract documentation from a pandas-ta indicator."""
    try:
        func = getattr(ta, name)
        docstring = inspect.getdoc(func) or "No description available."

        sig = inspect.signature(func)
        params = []
        for param_name, param in sig.parameters.items():
            if param_name in ['open_', 'high', 'low', 'close', 'volume', 'kwargs']:
                continue
            default = param.default if param.default != inspect.Parameter.empty else 'required'
            params.append((param_name, default))

        return {
            'name': name,
            'docstring': docstring,
            'params': params
        }
    except Exception as e:
        print(f"  Skipping {name}: {e}")
        return None


def format_as_markdown(info):
    """Convert indicator info to markdown format."""
    name_upper = info['name'].upper()

    param_lines = []
    for param_name, default in info['params']:
        param_lines.append(f"- {param_name} (default: {default})")
    params_section = '\n'.join(param_lines) if param_lines else "- No configurable parameters"

    overview = info['docstring'].split('\n\n')[0].replace('\n', ' ')

    md = f"""# {name_upper}

## Overview
{overview}

## pandas-ta Usage
```python
result = df.ta.{info['name']}()
```

## Parameters
{params_section}

## Example Strategy
```python
def strategy(df):
    indicator = df.ta.{info['name']}()

    signals = pd.Series(0, index=df.index)
    # Add your signal logic here based on {name_upper} values

    return signals
```
"""
    return md


def build_corpus():
    """Generate markdown files for all indicators."""
    output_dir = Path(__file__).parent.parent / 'app' / 'corpus' / 'indicators'
    output_dir.mkdir(parents=True, exist_ok=True)

    indicators = get_all_indicators()
    print(f"Found {len(indicators)} indicators in pandas-ta")
    print(f"Building corpus in {output_dir}")

    created = 0
    for name in indicators:
        info = get_indicator_info(name)
        if info:
            md_content = format_as_markdown(info)
            output_path = output_dir / f"{name}.md"
            output_path.write_text(md_content, encoding='utf-8')
            print(f"  Created {name}.md")
            created += 1

    print(f"\nDone! Created {created} indicator docs.")


if __name__ == '__main__':
    build_corpus()
