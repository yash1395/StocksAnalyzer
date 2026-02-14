from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List


@dataclass
class InvestmentUpdate:
    timestamp: datetime
    note: str
    source: str = "manual"


@dataclass
class Position:
    ticker: str
    quantity: float
    average_cost: float
    updates: List[InvestmentUpdate] = field(default_factory=list)

    @property
    def cost_basis(self) -> float:
        return self.quantity * self.average_cost


class Portfolio:
    def __init__(self) -> None:
        self.positions: Dict[str, Position] = {}

    def add_position(self, ticker: str, quantity: float, average_cost: float) -> Position:
        ticker = ticker.upper()
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if average_cost <= 0:
            raise ValueError("average_cost must be positive")

        if ticker in self.positions:
            existing = self.positions[ticker]
            new_total_qty = existing.quantity + quantity
            blended_cost = ((existing.quantity * existing.average_cost) + (quantity * average_cost)) / new_total_qty
            existing.quantity = new_total_qty
            existing.average_cost = blended_cost
            return existing

        position = Position(ticker=ticker, quantity=quantity, average_cost=average_cost)
        self.positions[ticker] = position
        return position

    def add_update(self, ticker: str, note: str, source: str = "manual") -> InvestmentUpdate:
        ticker = ticker.upper()
        if ticker not in self.positions:
            raise KeyError(f"Ticker {ticker} not found in portfolio")
        update = InvestmentUpdate(timestamp=datetime.utcnow(), note=note, source=source)
        self.positions[ticker].updates.append(update)
        return update

    def total_cost_basis(self) -> float:
        return sum(position.cost_basis for position in self.positions.values())

    def snapshot(self) -> Dict[str, dict]:
        return {
            ticker: {
                "quantity": p.quantity,
                "average_cost": p.average_cost,
                "cost_basis": p.cost_basis,
                "updates": [
                    {
                        "timestamp": u.timestamp.isoformat(),
                        "note": u.note,
                        "source": u.source,
                    }
                    for u in p.updates
                ],
            }
            for ticker, p in self.positions.items()
        }

    def load_positions_from_sheet(self, sheet_path: str | Path) -> None:
        """
        Load portfolio positions from a CSV sheet.

        Required headers:
        - ticker
        - quantity
        - average_cost
        """
        path = Path(sheet_path)
        with path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            required = {"ticker", "quantity", "average_cost"}
            if not reader.fieldnames or not required.issubset({f.strip() for f in reader.fieldnames}):
                raise ValueError("Sheet must include headers: ticker, quantity, average_cost")

            for row in reader:
                ticker = (row.get("ticker") or "").strip()
                quantity = float((row.get("quantity") or "0").strip())
                average_cost = float((row.get("average_cost") or "0").strip())
                self.add_position(ticker=ticker, quantity=quantity, average_cost=average_cost)
