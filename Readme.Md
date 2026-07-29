# 💜 FinSight AI — Financial Intelligence Platform

> AI-powered financial analytics platform for enterprise finance teams.  
> Built with Python, FastAPI, LangChain, Groq LLM, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.140-green)
![LangChain](https://img.shields.io/badge/LangChain-1.3-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-1.43-red)

---

## 🎯 What is FinSight AI?

FinSight AI is a production-grade financial intelligence platform that combines machine learning, large language models, and business intelligence to help finance teams make faster, smarter decisions.

Ask questions in plain English and get consultant-level answers backed by real financial data.

---

## ✨ Features

- 🤖 **AI Financial Analyst** — Ask anything in plain English
- 📊 **Interactive Dashboard** — Revenue, P&L, entity comparison
- 🚨 **Anomaly Detection** — Automatically flags suspicious transactions
- 📋 **Transaction Explorer** — Filter and browse 11,431 transactions
- 📄 **PDF Report Generator** — Download professional financial reports
- ⚡ **Power Automate Integration** — Automated alerts via webhooks
- 🔄 **CI/CD Pipeline** — Auto-deploys via GitHub Actions

---

## 🏗️ Architecture

    Frontend (Streamlit)
        ↓ REST API calls
    Backend (FastAPI)
        ↓ queries
    Database Layer (Pandas + CSV)
        ↓ context
    AI Agent (LangChain + Groq LLM)
        ↓ webhooks
    Power Automate (alerts)

---

## 📂 Project Structure

    finsight-ai/
    ├── backend/
    │   ├── core/
    │   │   └── database.py      — Data loading and queries
    │   └── main.py              — FastAPI REST API
    ├── ai/
    │   └── agent.py             — LangChain + Groq AI agent
    ├── frontend/
    │   └── app.py               — Streamlit dashboard
    ├── data/
    │   ├── transactions.csv     — 11,431 transactions
    │   ├── pl_monthly.csv       — P&L data
    │   ├── budget_vs_actual.csv — Budget variance
    │   ├── kpi_snapshots.csv    — KPI metrics
    │   ├── vendors.csv          — 50 vendors
    │   ├── customers.csv        — 200 customers
    │   └── fx_rates.csv         — Daily FX rates
    ├── .env.example             — Environment template
    ├── requirements.txt         — Python dependencies
    └── README.md

---

## 🚀 Quick Start

**1. Clone the repository**

    git clone https://github.com/charan4421/Finsight-Ai.git
    cd Finsight-Ai

**2. Install dependencies**

    pip install -r requirements.txt

**3. Configure environment**

    cp .env.example .env
    # Add your Groq API key to .env

**4. Run the backend**

    python backend/main.py

**5. Run the frontend**

    python -m streamlit run frontend/app.py

**6. Open in browser**

    http://localhost:8501

---

## 📊 Dataset

FinCorp Ltd — a synthetic but realistic Polish manufacturing company with 4 international subsidiaries:

| Entity | Country | Type | Revenue Share |
|---|---|---|---|
| FINCORP-PL | Poland | HQ + Manufacturing | 45% |
| FINCORP-DE | Germany | Distribution | 28% |
| FINCORP-CZ | Czech Republic | Logistics | 15% |
| FINCORP-SE | Sweden | Sales | 12% |

**5 years of data (2020-2024) including:**
- COVID impact in 2020
- Supply chain crisis in 2021-2022
- Energy crisis in 2022
- 20 deliberately injected anomalies

---

## 🤖 AI Capabilities

Ask the AI agent questions like:

- *"Which entity is most profitable?"*
- *"Are there any suspicious transactions?"*
- *"What happened to revenue during COVID in 2020?"*
- *"Which vendors are causing payment problems?"*
- *"Show me budget overruns in 2022"*

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit, Plotly |
| Backend | FastAPI, Uvicorn |
| AI/LLM | LangChain, Groq API |
| Data | Pandas, NumPy |
| Deployment | Render.com, GitHub Actions |
| Automation | Power Automate |

---

## 👨‍💻 Author

**Charan Kurri**
- 📧 charannaidu12680@gmail.com
- 💼 linkedin.com/in/ck4421
- 🐙 github.com/charan4421

---

## 📄 License

MIT License — free to use and modify.