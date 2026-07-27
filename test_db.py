import sys
sys.path.insert(0, ".")
from backend.core.database import db

db.load()

print("\n--- REVENUE BY YEAR ---")
print(db.revenue_by_year())

print("\n--- ANOMALIES ---")
print(f"Total: {len(db.anomalies())}")

print("\n--- OVERDUE ---")
overdue = db.overdue_invoices()
print(f"Total: {len(overdue)}, Amount: {overdue['amount_pln'].sum():,.0f} PLN")

print("\n--- ENTITIES ---")
print(db.entity_comparison())