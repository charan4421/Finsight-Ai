"""
FinSight AI — FastAPI Backend
REST API that serves financial data and AI answers
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.core.database import db
from ai.agent import agent

# ── APP SETUP ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="FinSight AI",
    description="AI-powered Financial Intelligence Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# ── STARTUP ───────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    print("Starting FinSight AI...")
    db.load()
    agent.setup()
    print("Ready!")

# ── REQUEST MODEL ─────────────────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str

# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {
        "app": "FinSight AI",
        "version": "1.0.0",
        "status": "running",
    }

@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {
        "status": "healthy",
        "data_loaded": db.is_loaded,
    }

@app.post("/api/ask")
def ask_question(req: QuestionRequest):
    """Ask the AI a financial question"""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    answer = agent.ask(req.question)
    return {
        "question": req.question,
        "answer": answer,
        "status": "success"
    }

@app.get("/api/summary")
def get_summary():
    """Get overview of all data"""
    return {
        "revenue_by_year": db.revenue_by_year().to_dict(orient="records"),
        "entity_comparison": db.entity_comparison().to_dict(orient="records"),
        "anomaly_count": len(db.anomalies()),
        "overdue_count": len(db.overdue_invoices()),
        "overdue_amount_pln": float(db.overdue_invoices()["amount_pln"].sum()),
        "budget_overrun_count": len(db.budget_overruns()),
    }

@app.get("/api/anomalies")
def get_anomalies():
    """Get all suspicious transactions"""
    anomalies = db.anomalies()
    return {
        "total": len(anomalies),
        "total_amount_pln": float(anomalies["amount_pln"].sum()),
        "data": anomalies[[
            "txn_id", "date", "entity_id",
            "amount_pln", "anomaly_type", "counterparty_name"
        ]].to_dict(orient="records")
    }

@app.get("/api/transactions")
def get_transactions(
    entity: Optional[str] = None,
    year: Optional[int] = None,
    type: Optional[str] = None,
    limit: int = 100
):
    """Get filtered transactions"""
    import math
    txn = db.get("transactions")

    if entity:
        txn = txn[txn["entity_id"] == entity]
    if year:
        txn = txn[txn["year"] == year]
    if type:
        txn = txn[txn["type"] == type.upper()]

    txn = txn.head(limit).copy()

    # Convert dates to string
    txn["date"] = txn["date"].astype(str)

    # Fill ALL NaN values
    txn = txn.fillna(0)

    # Convert numeric columns safely
    for col in txn.select_dtypes(include=["float64", "float32"]).columns:
        txn[col] = txn[col].apply(
            lambda x: 0 if (math.isnan(x) or math.isinf(x)) else round(x, 2)
        )

    # Convert bool columns to string
    for col in txn.select_dtypes(include=["bool"]).columns:
        txn[col] = txn[col].astype(str)

    return {
        "total": len(txn),
        "data": txn.to_dict(orient="records")
    }
@app.get("/api/pl")
def get_pl(entity: Optional[str] = None, year: Optional[int] = None):
    """Get P&L data"""
    pl = db.get("pl_monthly")

    if entity:
        pl = pl[pl["entity_id"] == entity]
    if year:
        pl = pl[pl["year"] == year]

    return {
        "total": len(pl),
        "data": pl.to_dict(orient="records")
    }

@app.get("/api/vendors")
def get_vendors(reliability: Optional[str] = None):
    """Get vendor list"""
    vendors = db.get("vendors")
    if reliability:
        vendors = vendors[vendors["payment_reliability"] == reliability.upper()]
    return {
        "total": len(vendors),
        "data": vendors.to_dict(orient="records")
    }

@app.get("/api/budget")
def get_budget(entity: Optional[str] = None):
    """Get budget vs actual"""
    bv = db.get("budget_vs_actual")
    if entity:
        bv = bv[bv["entity_id"] == entity]
    overruns = bv[bv["is_budget_overrun"] == True]
    return {
        "total_months": len(bv),
        "overrun_months": len(overruns),
        "data": bv.to_dict(orient="records")
    }

from fastapi.responses import FileResponse
import tempfile
import os

@app.get("/api/report/download")
def download_report():
    """Generate and download PDF report"""
    from backend.report import generate_report
    tmp_path = os.path.join(tempfile.gettempdir(), "finsight_report.pdf")
    generate_report(tmp_path)
    return FileResponse(
        tmp_path,
        media_type="application/pdf",
        filename="FinSight_AI_Report.pdf"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)