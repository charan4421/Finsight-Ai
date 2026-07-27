"""
FinSight AI — Database
Loads our CSV files into memory for fast querying
"""

import pandas as pd
from pathlib import Path

# This finds the data folder automatically
DATA_DIR = Path(__file__).parent.parent.parent / "data"


class FinSightDB:

    def __init__(self):
        self._data = {}
        self._loaded = False

    def load(self):
        print("Loading data files...")

        files = {
            "transactions":     "transactions.csv",
            "pl_monthly":       "pl_monthly.csv",
            "budget_vs_actual": "budget_vs_actual.csv",
            "kpi_snapshots":    "kpi_snapshots.csv",
            "vendors":          "vendors.csv",
            "customers":        "customers.csv",
            "fx_rates":         "fx_rates.csv",
        }

        for name, filename in files.items():
            path = DATA_DIR / filename
            if path.exists():
                self._data[name] = pd.read_csv(path)
                print(f"  Loaded {name}: {len(self._data[name])} rows")
            else:
                print(f"  WARNING: {filename} not found!")

        self._process()
        self._loaded = True
        print("All files loaded!")

    def _process(self):
        if "transactions" in self._data:
            txn = self._data["transactions"]
            txn["date"] = pd.to_datetime(txn["date"], errors="coerce")
            txn["amount_pln"] = pd.to_numeric(txn["amount_pln"], errors="coerce")
            txn["year"] = txn["date"].dt.year
            txn["month"] = txn["date"].dt.month
            txn["is_anomaly"] = txn["is_anomaly"].astype(str).str.upper() == "TRUE"
            txn["is_overdue"] = txn["is_overdue"].astype(str).str.upper() == "TRUE"
            self._data["transactions"] = txn

        if "pl_monthly" in self._data:
            pl = self._data["pl_monthly"]
            pl["period"] = pd.to_datetime(pl["period"], format="%Y-%m", errors="coerce")
            pl["year"] = pl["period"].dt.year
            self._data["pl_monthly"] = pl

        if "budget_vs_actual" in self._data:
            bv = self._data["budget_vs_actual"]
            bv["period"] = pd.to_datetime(bv["period"], format="%Y-%m", errors="coerce")
            bv["year"] = bv["period"].dt.year
            bv["is_budget_overrun"] = bv["is_budget_overrun"].astype(str).str.upper() == "TRUE"
            self._data["budget_vs_actual"] = bv

    def get(self, table_name):
        if not self._loaded:
            self.load()
        return self._data.get(table_name)

    @property
    def is_loaded(self):
        return self._loaded

    def revenue_by_year(self):
        txn = self.get("transactions")
        return (txn[txn["type"] == "REVENUE"]
                .groupby("year")["amount_pln"]
                .sum()
                .reset_index())

    def anomalies(self):
        txn = self.get("transactions")
        return txn[txn["is_anomaly"] == True]

    def overdue_invoices(self):
        txn = self.get("transactions")
        return txn[(txn["type"] == "REVENUE") & (txn["is_overdue"] == True)]

    def entity_comparison(self):
        pl = self.get("pl_monthly")
        return (pl.groupby("entity_id")[["revenue_pln", "ebitda_pln", "net_income_pln"]]
                .sum()
                .reset_index()
                .sort_values("revenue_pln", ascending=False))

    def budget_overruns(self):
        bv = self.get("budget_vs_actual")
        return bv[bv["is_budget_overrun"] == True]


# Global instance
db = FinSightDB()