from __future__ import annotations

import argparse
from pathlib import Path

from investing_app.ideas import MarketPoint, SocialPost, TradeIdeaEngine
from investing_app.portfolio import Portfolio


def run_demo(portfolio_sheet_path: str | None = None) -> None:
    portfolio = Portfolio()

    if portfolio_sheet_path:
        portfolio.load_positions_from_sheet(portfolio_sheet_path)
    else:
        portfolio.add_position("AAPL", 10, 180)
        portfolio.add_position("NVDA", 5, 900)

    portfolio.add_update("AAPL", "Added on pullback after earnings", source="journal")
    portfolio.add_update("NVDA", "Watching AI demand trend", source="journal")

    posts = [
        SocialPost("AAPL looks strong buy into next quarter"),
        SocialPost("NVDA bullish but high risk after huge run"),
        SocialPost("AAPL upgrade and growth momentum"),
        SocialPost("TSLA weak delivery numbers, bearish reaction"),
    ]

    history = {
        "AAPL": [
            MarketPoint(178, 100),
            MarketPoint(179, 95),
            MarketPoint(181, 98),
            MarketPoint(185, 140),
        ],
        "NVDA": [
            MarketPoint(870, 80),
            MarketPoint(890, 90),
            MarketPoint(910, 92),
            MarketPoint(935, 120),
        ],
        "TSLA": [
            MarketPoint(190, 85),
            MarketPoint(188, 88),
            MarketPoint(185, 87),
            MarketPoint(180, 130),
        ],
    }

    engine = TradeIdeaEngine()
    social = engine.analyze_social_posts(posts, tracked_tickers=["AAPL", "NVDA", "TSLA"])
    popularity = engine.analyze_popularity_frequency(history)
    ideas = engine.generate_trade_ideas(social, popularity, min_score=1.0)

    print("Portfolio Snapshot:")
    print(portfolio.snapshot())
    print("\nTrade Ideas:")
    for idea in ideas:
        print(f"- {idea.ticker}: score={idea.score:.2f} | {idea.rationale}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run StocksAnalyzer demo")
    parser.add_argument(
        "--portfolio-sheet",
        type=Path,
        help="Path to a CSV sheet with headers: ticker,quantity,average_cost",
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()
    run_demo(str(args.portfolio_sheet) if args.portfolio_sheet else None)
