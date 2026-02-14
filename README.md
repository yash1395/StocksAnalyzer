# StocksAnalyzer

A lightweight Python investing app prototype that:

1. Tracks investments and investment updates.
2. Stores notes/updates for each position over time.
3. Generates trade ideas from:
   - social-media style updates (sentiment + ticker mentions)
   - popular stock frequency analysis (momentum + volume spike scan)

## Quick start

```bash
python -m investing_app.demo
```

## Run tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## What's included

- `investing_app/portfolio.py` – portfolio and update tracking.
- `investing_app/ideas.py` – social sentiment and popularity/frequency trade-idea engine.
- `investing_app/demo.py` – runnable demo with sample data.

## Notes

This is an MVP skeleton focused on local logic and extensibility. You can later connect APIs for:

- Brokerage account syncing
- Social data ingestion (X/Reddit/StockTwits)
- Live market data streams
