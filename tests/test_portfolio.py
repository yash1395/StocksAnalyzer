import tempfile
import unittest
from pathlib import Path

from investing_app.portfolio import Portfolio


class PortfolioTests(unittest.TestCase):
    def test_add_position_and_blend_cost(self):
        p = Portfolio()
        p.add_position("aapl", 10, 100)
        p.add_position("AAPL", 10, 120)
        self.assertEqual(p.positions["AAPL"].quantity, 20)
        self.assertAlmostEqual(p.positions["AAPL"].average_cost, 110)

    def test_add_update(self):
        p = Portfolio()
        p.add_position("NVDA", 1, 900)
        update = p.add_update("NVDA", "Test note", "journal")
        self.assertEqual(update.note, "Test note")
        self.assertEqual(len(p.positions["NVDA"].updates), 1)

    def test_load_positions_from_sheet(self):
        content = "ticker,quantity,average_cost\nAAPL,10,180\nNVDA,5,900\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "portfolio.csv"
            path.write_text(content, encoding="utf-8")

            p = Portfolio()
            p.load_positions_from_sheet(path)

            self.assertIn("AAPL", p.positions)
            self.assertIn("NVDA", p.positions)
            self.assertEqual(p.positions["AAPL"].quantity, 10)
            self.assertEqual(p.positions["NVDA"].average_cost, 900)

    def test_load_positions_from_sheet_with_alias_headers(self):
        content = "tickr,qty,averagecost,notes\nMSFT,3,410,long term\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "portfolio_alias.csv"
            path.write_text(content, encoding="utf-8")

            p = Portfolio()
            p.load_positions_from_sheet(path)

            self.assertIn("MSFT", p.positions)
            self.assertEqual(p.positions["MSFT"].quantity, 3)
            self.assertEqual(p.positions["MSFT"].average_cost, 410)


if __name__ == "__main__":
    unittest.main()
