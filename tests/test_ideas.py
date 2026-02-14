import unittest

from investing_app.ideas import MarketPoint, SocialPost, TradeIdeaEngine


class TradeIdeaEngineTests(unittest.TestCase):
    def test_social_analysis_scores_mentions(self):
        engine = TradeIdeaEngine()
        posts = [
            SocialPost("AAPL bullish buy"),
            SocialPost("AAPL weak sell"),
            SocialPost("NVDA strong growth"),
        ]
        scores = engine.analyze_social_posts(posts, ["AAPL", "NVDA"])
        self.assertIn("AAPL", scores)
        self.assertIn("NVDA", scores)

    def test_generate_ideas(self):
        engine = TradeIdeaEngine()
        popularity = {
            "AAPL": [
                MarketPoint(100, 100),
                MarketPoint(101, 98),
                MarketPoint(102, 99),
                MarketPoint(106, 140),
            ]
        }
        pop_scores = engine.analyze_popularity_frequency(popularity)
        ideas = engine.generate_trade_ideas({"AAPL": 2}, pop_scores, min_score=1)
        self.assertTrue(any(i.ticker == "AAPL" for i in ideas))


if __name__ == "__main__":
    unittest.main()
