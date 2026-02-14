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

Create a CSV with headers:

- `ticker`
- `quantity`
- `average_cost`

Example:

```csv
ticker,quantity,average_cost
AAPL,10,180
NVDA,5,900
```

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## What's included

- `investing_app/portfolio.py` – portfolio, update tracking, and sheet import.
- `investing_app/ideas.py` – social sentiment and popularity/frequency trade-idea engine.
- `investing_app/demo.py` – runnable demo with sample data.
