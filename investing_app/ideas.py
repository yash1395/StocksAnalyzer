from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from statistics import mean
from typing import Dict, Iterable, List


POSITIVE_WORDS = {"buy", "bullish", "moon", "strong", "growth", "up", "beat", "upgrade"}
NEGATIVE_WORDS = {"sell", "bearish", "weak", "down", "miss", "downgrade", "risk"}


@dataclass
class SocialPost:
    text: str


@dataclass
class MarketPoint:
    close: float
    volume: float


@dataclass
class TradeIdea:
    ticker: str
    score: float
    rationale: str


class TradeIdeaEngine:
    def analyze_social_posts(self, posts: Iterable[SocialPost], tracked_tickers: Iterable[str]) -> Dict[str, float]:
        tracked = {t.upper() for t in tracked_tickers}
        sentiment_scores = defaultdict(float)

        for post in posts:
            tokens = [token.strip(".,!?;:()[]{}\"").upper() for token in post.text.split()]
            positives = sum(1 for t in tokens if t.lower() in POSITIVE_WORDS)
            negatives = sum(1 for t in tokens if t.lower() in NEGATIVE_WORDS)
            post_score = positives - negatives

            mentions = [token for token in tokens if token in tracked]
            mention_count = Counter(mentions)
            for ticker, count in mention_count.items():
                sentiment_scores[ticker] += post_score * count

        return dict(sentiment_scores)

    def analyze_popularity_frequency(self, price_volume_history: Dict[str, List[MarketPoint]]) -> Dict[str, float]:
        """
        Produces a popularity score using:
        - recent momentum: last close / average of prior closes
        - relative volume: last volume / average prior volume
        """
        scores: Dict[str, float] = {}
        for ticker, history in price_volume_history.items():
            if len(history) < 3:
                continue

            closes = [p.close for p in history]
            volumes = [p.volume for p in history]

            baseline_close = mean(closes[:-1])
            baseline_volume = mean(volumes[:-1])
            momentum = closes[-1] / baseline_close if baseline_close else 0
            volume_ratio = volumes[-1] / baseline_volume if baseline_volume else 0

            scores[ticker.upper()] = (momentum - 1.0) * 60 + (volume_ratio - 1.0) * 40

        return scores

    def generate_trade_ideas(
        self,
        social_scores: Dict[str, float],
        popularity_scores: Dict[str, float],
        min_score: float = 1.0,
    ) -> List[TradeIdea]:
        all_tickers = set(social_scores) | set(popularity_scores)
        ideas: List[TradeIdea] = []

        for ticker in all_tickers:
            social = social_scores.get(ticker, 0.0)
            popularity = popularity_scores.get(ticker, 0.0)
            total = social * 0.5 + popularity * 0.5

            if total >= min_score:
                rationale = (
                    f"Social sentiment={social:.2f}, popularity/momentum={popularity:.2f}; "
                    "combined score crossed threshold."
                )
                ideas.append(TradeIdea(ticker=ticker, score=total, rationale=rationale))

        return sorted(ideas, key=lambda i: i.score, reverse=True)
