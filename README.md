# StocksAnalyzer

A lightweight Python investing app prototype that:

1. Tracks investments and investment updates.
2. Stores notes/updates for each position over time.
3. Reads portfolio holdings from a CSV sheet.
4. Generates trade ideas from:
   - social-media style updates (sentiment + ticker mentions)
   - popular stock frequency analysis (momentum + volume spike scan)

## Quick start

Run with default demo positions:

```bash
python -m investing_app.demo
```

Run by passing your sheet file path:

```bash
python -m investing_app.demo --portfolio-sheet /path/to/portfolio.csv
```

## Portfolio sheet format

The loader auto-detects common header variants. It will understand columns like:

- Ticker: `ticker`, `tickr`, `symbol`
- Quantity: `quantity`, `qty`, `shares`
- Average cost: `average_cost`, `averagecost`, `avgcost`, `avgprice`

Extra columns are allowed and ignored.

Example:

```csv
tickr,qty,averagecost,notes
AAPL,10,180,long-term core
NVDA,5,900,watch volatility
```

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## What's included

- `investing_app/portfolio.py` – portfolio, update tracking, and sheet import.
- `investing_app/ideas.py` – social sentiment and popularity/frequency trade-idea engine.
- `investing_app/demo.py` – runnable demo with sample data.
