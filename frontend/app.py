"""
FinSight AI — White & Purple Premium Theme
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #F8F7FF; color: #1A1A2E; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2D1B69 0%, #4C1D95 100%);
        border-right: none;
    }
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    .metric-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 22px 24px;
        margin: 8px 0;
        box-shadow: 0 4px 20px rgba(109,40,217,0.1);
        border-left: 5px solid #7C3AED;
    }
    .metric-value {
        font-size: 34px;
        font-weight: 800;
        color: #7C3AED;
        margin: 8px 0 4px 0;
    }
    .metric-label {
        font-size: 11px;
        color: #6B7280;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 600;
    }
    .metric-delta-bad { font-size: 13px; color: #EF4444; margin-top: 6px; }
    .metric-delta-good { font-size: 13px; color: #10B981; margin-top: 6px; }
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #2D1B69;
        border-left: 4px solid #7C3AED;
        padding-left: 12px;
        margin: 24px 0 16px 0;
    }
    .page-title { font-size: 36px; font-weight: 800; color: #2D1B69; margin-bottom: 4px; }
    .page-subtitle { font-size: 14px; color: #6B7280; margin-bottom: 24px; }
    .chat-answer {
        background: linear-gradient(135deg, #F3F0FF 0%, #FAF5FF 100%);
        border: 1px solid #DDD6FE;
        border-left: 5px solid #7C3AED;
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
        color: #374151;
        line-height: 1.8;
        box-shadow: 0 4px 20px rgba(109,40,217,0.08);
    }
    .chat-label {
        font-size: 11px;
        color: #7C3AED;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .stButton button {
        background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }
    .top-accent {
        height: 4px;
        background: linear-gradient(90deg, #7C3AED, #A78BFA, #C4B5FD);
        margin-bottom: 24px;
        border-radius: 2px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

API_URL = "https://finsight-ai-p18w.onrender.com"


@st.cache_data(ttl=30)
def get_summary():
    try:
        r = requests.get(f"{API_URL}/api/summary", timeout=5)
        return r.json()
    except:
        return None

@st.cache_data(ttl=30)
def get_anomalies():
    try:
        r = requests.get(f"{API_URL}/api/anomalies", timeout=5)
        return r.json()
    except:
        return None

@st.cache_data(ttl=30)
def get_pl():
    try:
        r = requests.get(f"{API_URL}/api/pl", timeout=5)
        return r.json()
    except:
        return None

def ask_ai(question):
    try:
        r = requests.post(f"{API_URL}/api/ask", json={"question": question}, timeout=60)
        return r.json().get("answer", "No answer")
    except:
        return "Error connecting to API."

# SIDEBAR
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding:28px 0 16px 0;'>
            <div style='font-size:48px;'>💜</div>
            <div style='font-size:24px; font-weight:800; color:#FFFFFF;'>FinSight AI</div>
            <div style='font-size:12px; color:#C4B5FD; margin-top:4px;'>
                Financial Intelligence Platform
            </div>
        </div>
        <hr style='border-color:rgba(255,255,255,0.15);'>
    """, unsafe_allow_html=True)

    page = st.radio("", ["📊 Dashboard", "🤖 AI Chat", "🚨 Anomalies", "📋 Transactions"],
                    label_visibility="collapsed")

    st.markdown("""
        <hr style='border-color:rgba(255,255,255,0.15);'>
        <div style='text-align:center; font-size:12px; color:#C4B5FD;'>
            <div style='font-weight:700; font-size:14px; color:#FFFFFF; margin-bottom:6px;'>FinCorp Ltd</div>
            <div>4 Entities · 2020–2024</div>
            <div>11,431 Transactions</div>
            <div style='margin-top:10px;'>
                <span style='background:rgba(16,185,129,0.2); color:#34D399;
                             padding:3px 10px; border-radius:20px; font-size:11px;'>
                    🟢 API Connected
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

summary = get_summary()

# DASHBOARD
if page == "📊 Dashboard":
    st.markdown("<div class='top-accent'></div>", unsafe_allow_html=True)
    st.markdown("<div class='page-title'>📊 Financial Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>FinCorp Ltd · 2020–2024 · AI-Powered Analytics</div>", unsafe_allow_html=True)
    st.divider()

    if summary:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""<div class='metric-card'>
                <div class='metric-label'>Total Revenue 2024</div>
                <div class='metric-value'>91.3M</div>
                <div class='metric-delta-bad'>↓ -3.1M vs 2023</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Anomalies Detected</div>
                <div class='metric-value'>{summary.get('anomaly_count',0)}</div>
                <div class='metric-delta-bad'>⚠ Needs review</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Overdue Invoices</div>
                <div class='metric-value'>{summary.get('overdue_count',0):,}</div>
                <div class='metric-delta-bad'>↑ {summary.get('overdue_amount_pln',0)/1e6:.0f}M PLN</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Budget Overruns</div>
                <div class='metric-value'>{summary.get('budget_overrun_count',0)}</div>
                <div class='metric-delta-bad'>↑ months exceeded</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='section-header'>Revenue by Year</div>", unsafe_allow_html=True)
            rev_data = summary.get("revenue_by_year", [])
            if rev_data:
                df_rev = pd.DataFrame(rev_data)
                df_rev = df_rev[df_rev["year"] <= 2024]
                df_rev["revenue_M"] = df_rev["amount_pln"] / 1_000_000
                fig = go.Figure(go.Bar(
                    x=df_rev["year"], y=df_rev["revenue_M"],
                    marker=dict(color=df_rev["revenue_M"],
                                colorscale=[[0,"#DDD6FE"],[1,"#7C3AED"]]),
                    text=df_rev["revenue_M"].apply(lambda x: f"{x:.1f}M"),
                    textposition="outside",
                    textfont=dict(color="#7C3AED", size=12),
                ))
                fig.update_layout(
                    plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                    font=dict(color="#374151"),
                    xaxis=dict(gridcolor="#F3F4F6", tickfont=dict(color="#374151")),
                    yaxis=dict(gridcolor="#F3F4F6", tickfont=dict(color="#374151"), title="Revenue (M PLN)"),
                    margin=dict(t=20,b=20), showlegend=False, height=300,
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("<div class='section-header'>Entity Comparison</div>", unsafe_allow_html=True)
            entity_data = summary.get("entity_comparison", [])
            if entity_data:
                df_e = pd.DataFrame(entity_data)
                df_e["revenue_M"] = df_e["revenue_pln"] / 1_000_000
                df_e["net_M"] = df_e["net_income_pln"] / 1_000_000
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(name="Revenue", x=df_e["entity_id"], y=df_e["revenue_M"], marker_color="#A78BFA"))
                fig2.add_trace(go.Bar(name="Net Income", x=df_e["entity_id"], y=df_e["net_M"], marker_color="#7C3AED"))
                fig2.update_layout(
                    plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                    font=dict(color="#374151"),
                    xaxis=dict(gridcolor="#F3F4F6", tickfont=dict(color="#374151")),
                    yaxis=dict(gridcolor="#F3F4F6", tickfont=dict(color="#374151"), title="M PLN"),
                    barmode="group",
                    legend=dict(bgcolor="#FFFFFF", font=dict(color="#374151")),
                    margin=dict(t=20,b=20), height=300,
                )
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<div class='section-header'>Monthly Revenue Trend</div>", unsafe_allow_html=True)
        pl_data = get_pl()
        if pl_data:
            df_pl = pd.DataFrame(pl_data["data"])
            df_pl["period"] = pd.to_datetime(df_pl["period"])
            df_pl = df_pl[df_pl["period"].dt.year <= 2024]
            col1, col2 = st.columns([4,1])
            with col2:
                ef = st.selectbox("Entity", ["All","FINCORP-PL","FINCORP-DE","FINCORP-CZ","FINCORP-SE"])
            if ef != "All":
                df_pl = df_pl[df_pl["entity_id"] == ef]
            df_pl["revenue_M"] = df_pl["revenue_pln"] / 1_000_000
            colors_map = {"FINCORP-PL":"#7C3AED","FINCORP-DE":"#A78BFA","FINCORP-CZ":"#6D28D9","FINCORP-SE":"#C4B5FD"}
            fig3 = go.Figure()
            for ent in df_pl["entity_id"].unique():
                df_e2 = df_pl[df_pl["entity_id"] == ent]
                fig3.add_trace(go.Scatter(
                    x=df_e2["period"], y=df_e2["revenue_M"], name=ent,
                    mode="lines", line=dict(color=colors_map.get(ent,"#7C3AED"), width=2.5),
                ))
            fig3.update_layout(
                plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
                font=dict(color="#374151"),
                xaxis=dict(gridcolor="#F3F4F6", tickfont=dict(color="#374151")),
                yaxis=dict(gridcolor="#F3F4F6", tickfont=dict(color="#374151"), title="Revenue (M PLN)"),
                legend=dict(bgcolor="#FFFFFF", font=dict(color="#374151")),
                margin=dict(t=20,b=20), height=340,
            )
            st.plotly_chart(fig3, use_container_width=True)
        st.markdown("<div class='section-header'>📄 Download Report</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1,3])
        with col1:
            if st.button("📄 Download PDF Report", type="primary"):
                import requests as req
                response = req.get(f"{API_URL}/api/report/download")
                if response.status_code == 200:
                    st.download_button(
                        label="💾 Save PDF",
                        data=response.content,
                        file_name="FinSight_AI_Report.pdf",
                        mime="application/pdf"
                    )
           
   
    else:
        st.error("Cannot connect to API. Run: python backend/main.py")
        

   


   

# AI CHAT
elif page == "🤖 AI Chat":
    st.markdown("<div class='top-accent'></div>", unsafe_allow_html=True)
    st.markdown("<div class='page-title'>🤖 AI Financial Analyst</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Ask anything about FinCorp finances in plain English</div>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<div class='section-header'>Quick Questions</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    quick_q = None
    with col1:
        if st.button("💰 Most profitable entity?"): quick_q = "Which entity is most profitable and why?"
        if st.button("📉 COVID revenue impact?"): quick_q = "What happened to revenue during COVID in 2020?"
    with col2:
        if st.button("🚨 Suspicious transactions?"): quick_q = "Are there any suspicious transactions?"
        if st.button("📊 Budget overruns?"): quick_q = "Which entity had the worst budget overrun?"
    with col3:
        if st.button("⚠️ Vendor problems?"): quick_q = "Which vendors are causing payment problems?"
        if st.button("💳 Overdue invoices?"): quick_q = "How many overdue invoices do we have?"

    st.markdown("<div class='section-header'>Ask Your Own Question</div>", unsafe_allow_html=True)
    question = st.text_input("", placeholder="e.g. What is our EBITDA margin trend?",
                              value=quick_q if quick_q else "", label_visibility="collapsed")

    if st.button("🤖 Ask FinSight AI", type="primary") or quick_q:
        q = quick_q if quick_q else question
        if q:
            with st.spinner("Analyzing 11,431 transactions..."):
                answer = ask_ai(q)
            st.markdown(f"""
                <div class='chat-answer'>
                    <div class='chat-label'>✦ FinSight AI Analysis</div>
                    <div style='font-size:15px;'>{answer}</div>
                </div>""", unsafe_allow_html=True)

# ANOMALIES
elif page == "🚨 Anomalies":
    st.markdown("<div class='top-accent'></div>", unsafe_allow_html=True)
    st.markdown("<div class='page-title'>🚨 Anomaly Detection</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>AI-detected suspicious transactions requiring review</div>", unsafe_allow_html=True)
    st.divider()

    anomaly_data = get_anomalies()
    if anomaly_data:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Total Anomalies</div>
                <div class='metric-value'>{anomaly_data['total']}</div>
                <div class='metric-delta-bad'>⚠ Flagged for review</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            total = anomaly_data.get("total_amount_pln", 0)
            st.markdown(f"""<div class='metric-card'>
                <div class='metric-label'>Amount at Risk</div>
                <div class='metric-value'>{total/1000:.0f}K</div>
                <div class='metric-delta-bad'>PLN pending investigation</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class='metric-card'>
                <div class='metric-label'>Risk Level</div>
                <div class='metric-value' style='color:#EF4444;'>HIGH</div>
                <div class='metric-delta-bad'>⚠ Immediate action needed</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        df_anomalies = pd.DataFrame(anomaly_data["data"])
        if not df_anomalies.empty:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("<div class='section-header'>By Type</div>", unsafe_allow_html=True)
                tc = df_anomalies["anomaly_type"].value_counts().reset_index()
                tc.columns = ["type", "count"]
                fig = go.Figure(go.Pie(
                    labels=tc["type"], values=tc["count"], hole=0.55,
                    marker=dict(colors=["#7C3AED","#A78BFA","#6D28D9","#C4B5FD"]),
                ))
                fig.update_layout(
                    paper_bgcolor="#FFFFFF", font=dict(color="#374151"),
                    legend=dict(bgcolor="#FFFFFF", font=dict(color="#374151")),
                    height=300, margin=dict(t=20,b=20),
                )
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.markdown("<div class='section-header'>Flagged Transactions</div>", unsafe_allow_html=True)
                disp = df_anomalies[["txn_id","date","entity_id","amount_pln","anomaly_type"]].copy()
                disp["amount_pln"] = disp["amount_pln"].apply(lambda x: f"{x:,.0f} PLN")
                st.dataframe(disp, use_container_width=True, hide_index=True, height=280)

# TRANSACTIONS
elif page == "📋 Transactions":
    st.markdown("<div class='top-accent'></div>", unsafe_allow_html=True)
    st.markdown("<div class='page-title'>📋 Transactions</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Browse and filter all 11,431 financial transactions</div>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1: entity_f = st.selectbox("Entity", ["All","FINCORP-PL","FINCORP-DE","FINCORP-CZ","FINCORP-SE"])
    with col2: year_f = st.selectbox("Year", ["All",2020,2021,2022,2023,2024])
    with col3: type_f = st.selectbox("Type", ["All","REVENUE","EXPENSE"])

    try:
        url = f"{API_URL}/api/transactions?limit=200"
        if entity_f != "All": url += f"&entity={entity_f}"
        if year_f != "All": url += f"&year={year_f}"
        if type_f != "All": url += f"&type={type_f}"
        r = requests.get(url, timeout=5)
        txn_data = r.json()
        st.markdown(f"""<div class='metric-card' style='display:inline-block; margin-bottom:20px;'>
            <div class='metric-label'>Transactions Found</div>
            <div class='metric-value'>{txn_data['total']:,}</div>
        </div>""", unsafe_allow_html=True)
        df_txn = pd.DataFrame(txn_data["data"])
        if not df_txn.empty:
            disp = df_txn[["txn_id","date","entity_id","type","amount_pln","currency","counterparty_name","status"]].copy()
            disp["amount_pln"] = disp["amount_pln"].apply(lambda x: f"{float(x):,.0f}")
            st.dataframe(disp, use_container_width=True, hide_index=True, height=500)
    except:
        st.error("Cannot connect to API. Run: python backend/main.py")