# Position Sizing in Trading: The Key to Profitable Trading

**Source:** TTrades Education
**Category:** core_concepts
**Concepts:** position_sizing, risk_management, account_size, lot_size, drawdown

---

## Introduction

Many traders focus extensively on win rate versus risk-to-reward ratios, yet overlook a critical component: position sizing. Position sizing ensures that your risk per trade stays consistent. This consistency is what makes win rate and R:R work in your favor.

## Why Position Sizing Matters

Proper position sizing is foundational because it keeps risk uniform across trades, allowing mathematical trading systems to perform as intended.

### Example of Impact
Consider this scenario:
- System: 1:2 risk-to-reward ratio, 50% win rate
- Risk per trade: $1,000

If the first trade loses (-$1,000) and the second wins (+$2,000), the net result is +$1,000. However, reducing risk on the second trade after a loss undermines the system's mathematics, resulting in breakeven instead of profits.

## Two Primary Methods

### Fixed Contract Size
Trading the same number of contracts (e.g., always 2 NQ contracts) presents a significant problem: Risk could be $400 on one trade and $1,600 on another, creating inconsistent R values.

### Fixed Dollar or Percentage Risk
This approach - risking a consistent dollar amount or account percentage per trade - maintains uniform risk across all positions, ensuring mathematical outcomes remain reliable.

## Position Size Formula

To calculate proper position size, you need:
- Defined risk per trade (e.g., $1,000)
- Value per point (instrument-specific; NQ = $20/point)
- Stop loss size (in points/pips)

**Formula:**
```
Contracts = (Risk $) / (Value per point * Stop size)
```

### Worked Example
- Risk: $1,000
- NQ Value: $20/point
- Stop: 20 points

Result: $1,000 / (20 * 20) = 2.5 contracts

Since futures do not allow fractional contracts, using micro contracts provides greater flexibility.

## Tools for Position Sizing

Recommended tools:
- **Spreadsheets/Calculators** - Input account size, desired risk, and stop size for instant position calculations
- **TradingView Risk-Reward Tool** - Set entry, stop, and account risk percentage for automatic quantity calculations

## Prop Firm Considerations

Proprietary trading accounts introduce complexity. While traders may access a $25,000 account, the actual constraint is the drawdown limit (e.g., $1,500).

### Key Problem
Risking 1% of the account ($250) may actually equal approximately 17% of drawdown, dramatically increasing blow-up risk after minimal consecutive losses.

### Recommended Approach
Size positions using 7-10% of drawdown per trade, allowing approximately 10-15 losing trades before account elimination. After achieving funded status, reduce risk for greater cushion.

## Key Takeaways

- Consistent position sizing forms the foundation of profitable trading
- Choose between fixed contract or fixed dollar risk methodology (micros enhance flexibility)
- Utilize calculators or TradingView tools to eliminate manual calculation errors
- For prop firm accounts, always base sizing on drawdown limits, not total account balance

Position sizing is not glamorous, but it is what keeps traders alive long enough to let their strategies work.
