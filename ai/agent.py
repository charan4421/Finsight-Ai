"""
FinSight AI — The Brain
Connects our financial data to Groq LLM
So you can ask questions in plain English
"""

import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Load .env file
load_dotenv()

# Add project root to path
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))
from backend.core.database import db

# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are FinSight AI — a senior financial analyst for FinCorp Ltd.
FinCorp is a Polish manufacturing company with 4 subsidiaries:
- FINCORP-PL: Poland HQ + Manufacturing (45% of revenue)
- FINCORP-DE: Germany Distribution (28% of revenue)
- FINCORP-CZ: Czech Republic Logistics (15% of revenue)
- FINCORP-SE: Sweden Sales (12% of revenue)

You have access to 5 years of financial data (2020-2024).
Always answer with SPECIFIC NUMBERS from the data.
Be clear, concise and professional like a senior consultant.
Always respond in English."""


class FinSightAgent:

    def __init__(self):
        self.llm = None
        self._ready = False

    def setup(self):
        """Initialize LLM and load data"""
        # Load data
        if not db.is_loaded:
            db.load()

        # Setup LLM
        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key or api_key == "your_groq_api_key_here":
            print("WARNING: No Groq API key found — running in demo mode")
            self._ready = True
            return

        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=1024,
        )
        self._ready = True
        print("Agent ready!")

    def _get_context(self, question):
        """Pick relevant data based on the question"""
        q = question.lower()
        context = []

        # Revenue / profit questions
        if any(w in q for w in ["revenue", "profit", "ebitda", "income", "margin"]):
            rev = db.revenue_by_year()
            context.append(f"REVENUE BY YEAR:\n{rev.to_string(index=False)}")
            entities = db.entity_comparison()
            context.append(f"\nENTITY COMPARISON:\n{entities.to_string(index=False)}")

        # Anomaly questions
        if any(w in q for w in ["anomal", "suspicious", "duplicate", "fraud"]):
            anomalies = db.anomalies()
            context.append(
                f"ANOMALIES FOUND ({len(anomalies)}):\n"
                f"{anomalies[['txn_id','date','amount_pln','anomaly_type']].head(10).to_string(index=False)}"
            )

        # Overdue / payment questions
        if any(w in q for w in ["overdue", "late", "payment", "receivable"]):
            overdue = db.overdue_invoices()
            context.append(
                f"OVERDUE INVOICES: {len(overdue)} total\n"
                f"Total amount: {overdue['amount_pln'].sum():,.0f} PLN"
            )

        # Budget questions
        if any(w in q for w in ["budget", "variance", "overrun", "target"]):
            overruns = db.budget_overruns()
            context.append(
                f"BUDGET OVERRUNS: {len(overruns)} months\n"
                f"{overruns[['period','entity_id','opex_variance_pct']].head(5).to_string(index=False)}"
            )

        # Vendor questions
        if any(w in q for w in ["vendor", "supplier", "payable"]):
            vendors = db.get("vendors")
            poor = vendors[vendors["payment_reliability"] == "POOR"]
            context.append(
                f"PROBLEMATIC VENDORS:\n"
                f"{poor[['vendor_id','name','category']].to_string(index=False)}"
            )

        # Default — always include yearly summary
        if not context:
            rev = db.revenue_by_year()
            entities = db.entity_comparison()
            context.append(f"REVENUE BY YEAR:\n{rev.to_string(index=False)}")
            context.append(f"\nENTITY COMPARISON:\n{entities.to_string(index=False)}")

        return "\n\n".join(context)

    def ask(self, question):
        """Ask the AI a financial question"""
        if not self._ready:
            self.setup()

        # Build context from data
        context = self._get_context(question)

        # No API key — show demo response
        if self.llm is None:
            return (
                f"DEMO MODE — Add real GROQ_API_KEY to .env\n\n"
                f"Question: {question}\n\n"
                f"Data available:\n{context[:500]}..."
            )

        # Ask the LLM
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"""
DATA:
{context}

QUESTION: {question}

Give a specific, data-backed answer with numbers.
""")
        ]

        response = self.llm.invoke(messages)
        return response.content


# Global agent instance
agent = FinSightAgent()