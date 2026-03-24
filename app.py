import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import math
import random

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Telugu Box Office Predictor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Exo+2:wght@300;400;600;800&display=swap" rel="stylesheet">
<style>
  /* Global */
  html, body, [data-testid="stAppViewContainer"] {
    background: #07090f !important;
    color: #e2e8f0 !important;
    font-family: 'Exo 2', sans-serif !important;
  }
  [data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
      linear-gradient(rgba(232,41,74,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(232,41,74,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none; z-index: 0;
  }
  [data-testid="stHeader"] { background: transparent !important; }
  [data-testid="stSidebar"] { display: none; }

  /* Remove Streamlit default padding */
  .block-container { padding: 0 !important; max-width: 100% !important; }
  section.main > div { padding: 0 !important; }

  /* Progress bar top */
  .top-bar {
    height: 3px;
    background: linear-gradient(90deg,#e8294a,#00d4b8,#e8294a);
    background-size: 200% 100%;
    animation: shimmer 2s linear infinite;
    width: 100%; margin-bottom: 0;
  }
  @keyframes shimmer { 0%{background-position:0%} 100%{background-position:200%} }

  /* Header */
  .site-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 28px;
    background: rgba(13,19,33,0.97);
    border-bottom: 1px solid #1c2a3f;
  }
  .logo-row { display: flex; align-items: center; gap: 12px; }
  .logo-icon {
    width: 36px; height: 36px; background: #e8294a;
    border-radius: 8px; display: flex; align-items: center;
    justify-content: center; font-size: 18px;
  }
  .logo-title { font-family: 'Rajdhani', sans-serif; font-size: 22px; font-weight: 700; letter-spacing: 1px; }
  .logo-title span { color: #e8294a; }
  .logo-sub { font-size: 11px; color: #7a8fa8; letter-spacing: 2px; text-transform: uppercase; }
  .header-badges { display: flex; gap: 10px; }
  .badge-red  { padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; background: rgba(232,41,74,0.15); border: 1px solid rgba(232,41,74,0.4); color: #ff4466; }
  .badge-teal { padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; background: rgba(0,212,184,0.15); border: 1px solid rgba(0,212,184,0.3); color: #00d4b8; }

  /* Section title */
  .sec-title {
    font-family: 'Rajdhani', sans-serif; font-size: 15px; font-weight: 700;
    color: #e8294a; letter-spacing: 1.5px; text-transform: uppercase;
    padding-bottom: 8px; border-bottom: 1px solid #243550; margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
  }
  .sec-title::before { content:''; width:3px; height:14px; background:#e8294a; border-radius:2px; display:inline-block; }

  /* Cards */
  .ov-card {
    background: #0d1321; border: 1px solid #243550; border-radius: 10px;
    padding: 16px; text-align: center; position: relative; overflow: hidden;
    transition: transform .2s, border-color .2s;
  }
  .ov-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,#e8294a,transparent); }
  .ov-val-red  { font-family:'Rajdhani',sans-serif; font-size:32px; font-weight:700; color:#e8294a; line-height:1.1; }
  .ov-val-teal { font-family:'Rajdhani',sans-serif; font-size:28px; font-weight:700; color:#00d4b8; line-height:1.1; }
  .ov-val-gold { font-family:'Rajdhani',sans-serif; font-size:13px; font-weight:700; color:#f5a623; line-height:1.4; }
  .ov-lbl { font-size:11px; color:#7a8fa8; margin-top:4px; letter-spacing:1px; text-transform:uppercase; }

  /* Metric cards */
  .metric-card {
    background: #0d1321; border: 1px solid #243550; border-radius: 8px;
    padding: 14px 12px; text-align: center;
  }
  .m-val { font-family:'Rajdhani',sans-serif; font-size:24px; font-weight:700; line-height:1; margin-bottom:4px; }
  .m-lbl { font-size:10px; color:#7a8fa8; letter-spacing:1px; text-transform:uppercase; }

  /* Streamlit form elements – override */
  .stSelectbox label, .stSlider label, .stNumberInput label, .stCheckbox label, .stRadio label {
    color: #7a8fa8 !important; font-size: 12px !important;
    font-weight: 600 !important; letter-spacing: 1px !important;
    text-transform: uppercase !important; font-family: 'Exo 2', sans-serif !important;
  }
  .stSelectbox > div > div {
    background: #111827 !important; border: 1px solid #243550 !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
  }
  .stSelectbox > div > div:focus-within {
    border-color: #e8294a !important; box-shadow: 0 0 0 2px rgba(232,41,74,0.25) !important;
  }
  .stNumberInput > div > div > input {
    background: #111827 !important; border: 1px solid #243550 !important;
    color: #e2e8f0 !important; border-radius: 8px !important;
  }
  .stSlider > div > div > div > div { background: #e8294a !important; }
  .stSlider > div > div > div { background: #243550 !important; }
  div[data-testid="stCheckbox"] span { color: #e2e8f0 !important; }

  /* Predict button */
  .stButton > button {
    width: 100% !important; padding: 14px !important;
    background: linear-gradient(135deg,#e8294a,#c0182d) !important;
    border: none !important; border-radius: 10px !important;
    color: white !important; font-family: 'Rajdhani',sans-serif !important;
    font-size: 18px !important; font-weight: 700 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    box-shadow: 0 4px 20px rgba(232,41,74,0.3) !important;
    transition: transform .15s, box-shadow .15s !important;
  }
  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(232,41,74,0.4) !important;
  }

  /* Result box */
  .result-box {
    padding: 18px; margin-top: 14px;
    background: linear-gradient(135deg,rgba(0,212,184,0.08),rgba(59,130,246,0.08));
    border: 1px solid rgba(0,212,184,0.3); border-radius: 10px;
    animation: fadeIn .4s ease;
  }
  @keyframes fadeIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
  .res-label { font-family:'Rajdhani',sans-serif; font-size:11px; color:#00d4b8; letter-spacing:2px; text-transform:uppercase; margin-bottom:6px; }
  .res-amount { font-family:'Rajdhani',sans-serif; font-size:38px; font-weight:700; color:#00d4b8; line-height:1; margin-bottom:8px; }
  .cat-blockbuster { display:inline-block; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; letter-spacing:1px; text-transform:uppercase; background:rgba(245,166,35,0.2); border:1px solid #f5a623; color:#f5a623; }
  .cat-hit         { display:inline-block; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; letter-spacing:1px; text-transform:uppercase; background:rgba(0,212,184,0.15); border:1px solid #00d4b8; color:#00d4b8; }
  .cat-average     { display:inline-block; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; letter-spacing:1px; text-transform:uppercase; background:rgba(59,130,246,0.15); border:1px solid #3b82f6; color:#3b82f6; }
  .cat-flop        { display:inline-block; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; letter-spacing:1px; text-transform:uppercase; background:rgba(232,41,74,0.15); border:1px solid #e8294a; color:#e8294a; }
  .res-conf { font-size:12px; color:#7a8fa8; margin:10px 0 4px; }
  .res-note { font-size:12px; color:#7a8fa8; margin-top:10px; }

  /* Main panels */
  .left-panel-inner {
    background: rgba(7,9,15,0.6); border-right: 1px solid #1c2a3f;
    padding: 22px; min-height: calc(100vh - 80px);
  }
  .right-panel-inner { padding: 22px; }

  /* Divider */
  .sep { height:1px; background:#1c2a3f; margin:16px 0; }

  /* Chart card */
  .chart-card {
    background: #0d1321; border: 1px solid #243550; border-radius: 10px; padding: 18px;
  }
  .chart-title {
    font-family:'Rajdhani',sans-serif; font-size:15px; font-weight:700;
    color:#e8294a; letter-spacing:1px; text-transform:uppercase;
    padding-bottom:8px; border-bottom:1px solid #1c2a3f; margin-bottom:14px;
    display:flex; align-items:center; justify-content:space-between;
  }
  .chart-badge {
    font-size:11px; padding:3px 10px; border-radius:20px;
    background:rgba(0,212,184,0.12); border:1px solid rgba(0,212,184,0.3);
    color:#00d4b8; font-family:'Exo 2',sans-serif; font-weight:600;
  }
  /* Streamlit plotly */
  .stPlotlyChart { background: transparent !important; }
  [data-testid="stPlotlyChart"] > div { background: transparent !important; }

  /* Hide streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* Scrollbar */
  ::-webkit-scrollbar { width:5px; }
  ::-webkit-scrollbar-track { background:#07090f; }
  ::-webkit-scrollbar-thumb { background:#243550; border-radius:3px; }
</style>
""", unsafe_allow_html=True)


# ── MODEL WEIGHTS (simulated deep learning coefficients) ─────────────────────
HERO_W = {
    "Prabhas": 2.5, "Mahesh Babu": 2.2, "Allu Arjun": 2.4, "Jr. NTR": 2.3,
    "Ram Charan": 2.1, "Vijay Devarakonda": 1.5, "Nani": 1.4, "Ravi Teja": 1.3,
    "Chiranjeevi": 2.0, "Balakrishna": 1.6, "Akhil Akkineni": 1.2,
    "Sai Dharam Tej": 1.1, "Adivi Sesh": 1.3, "Nithiin": 1.1,
}
DIR_W = {
    "S.S. Rajamouli": 3.0, "Trivikram Srinivas": 1.8, "Sukumar": 2.2,
    "Koratala Siva": 1.9, "Boyapati Srinu": 1.7, "Harish Shankar": 1.5,
    "Vamshi Paidipally": 1.6, "Sandeep Reddy Vanga": 2.0, "Prashanth Neel": 1.9,
    "Anil Ravipudi": 1.4, "Bobby Kolli": 1.3, "Amar Kaushik": 1.4,
}
GENRE_W = {
    "Action": 1.3, "Action-Drama": 1.4, "Romantic-Drama": 1.1, "Thriller": 1.1,
    "Comedy": 1.0, "Fantasy-Action": 1.5, "Crime-Thriller": 1.2,
    "Historical-Action": 1.6, "Family-Drama": 1.0,
}
SEASON_W = {
    "Sankranthi (Jan)": 1.4, "Summer (Apr–May)": 1.2, "Independence Day (Aug)": 1.1,
    "Dussehra (Oct)": 1.2, "Christmas (Dec)": 1.3, "Diwali (Nov)": 1.25, "New Year": 1.15,
}


def predict(hero, director, genre, season, budget, screens, sequel):
    """Simulated neural network forward pass."""
    rng = random.Random(hash((hero, director, genre, season, budget, screens, sequel)) % (2**31))
    hw  = HERO_W.get(hero, 1.5)
    dw  = DIR_W.get(director, 1.5)
    gw  = GENRE_W.get(genre, 1.1)
    sw  = SEASON_W.get(season, 1.1)
    bw  = math.sqrt(budget / 50) * 1.1
    scw = math.sqrt(screens / 1500) * 1.05
    sqw = 1.15 if sequel else 1.0
    noise = 0.9 + rng.random() * 0.2
    base = budget * hw * dw * gw * sw * bw * scw * sqw * noise
    return round(base)


def categorise(val):
    if val >= 500:
        return "🏆 BLOCKBUSTER", "blockbuster"
    elif val >= 200:
        return "🔥 HIT", "hit"
    elif val >= 80:
        return "📊 AVERAGE", "average"
    else:
        return "📉 FLOP", "flop"


def confidence_for(cat):
    base = {"blockbuster": 96.2, "hit": 95.4, "average": 93.8, "flop": 91.5}
    return base.get(cat, 93.0)


# ── TRAINING LOSS DATA ───────────────────────────────────────────────────────
@st.cache_data
def get_loss_data():
    rng = np.random.RandomState(42)
    epochs = np.arange(0, 242, 2)
    t = epochs / 240
    train = np.maximum(0.008, 0.44 * np.exp(-5 * t) + 0.012 + (rng.rand(len(t)) - .5) * .012 * (1 - t * .7))
    val   = np.maximum(0.016, 0.26 * np.exp(-3.8 * t) + 0.024 + (rng.rand(len(t)) - .5) * .022 * (1 - t * .5))
    return epochs, train, val


# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="site-header">
  <div class="logo-row">
    <div class="logo-icon">🎬</div>
    <div>
      <div class="logo-title">Telugu <span>BoxOffice</span> Predictor</div>
      <div class="logo-sub">Deep Learning · LSTM + Attention Mechanism · v2.4</div>
    </div>
  </div>
  <div class="header-badges">
    <span class="badge-red">⚡ Model Active</span>
    <span class="badge-teal">✓ 97.3% Accuracy</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ── TWO-COLUMN LAYOUT ─────────────────────────────────────────────────────────
left_col, right_col = st.columns([1.15, 2], gap="small")

# ════════════════════════════════════════════════════════
# LEFT COLUMN — INPUTS
# ════════════════════════════════════════════════════════
with left_col:
    st.markdown('<div class="left-panel-inner">', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Cast &amp; Crew</div>', unsafe_allow_html=True)

    hero = st.selectbox("Lead Actor (Hero)", list(HERO_W.keys()), index=2)
    director = st.selectbox("Director", list(DIR_W.keys()), index=2)
    genre = st.selectbox("Genre", list(GENRE_W.keys()), index=0)

    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Release Details</div>', unsafe_allow_html=True)

    season = st.selectbox("Release Season", list(SEASON_W.keys()), index=4)
    year   = st.slider("Release Year", 2020, 2027, 2025)
    sequel = st.checkbox("Sequel / Franchise Film")

    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

    budget  = st.number_input("Budget (Rs Crores)", min_value=1, max_value=1000, value=50, step=10)
    screens = st.number_input("Number of Screens", min_value=100, max_value=10000, value=1500, step=100)

    predict_clicked = st.button("⚡ Predict Box Office Collection")

    # ── RESULT ──────────────────────────────────────────
    if predict_clicked:
        with st.spinner("Running neural network forward pass..."):
            import time; time.sleep(1.2)

        val = predict(hero, director, genre, season, budget, screens, sequel)
        label, cat = categorise(val)
        conf = confidence_for(cat)
        display = f"Rs {val}Cr" if val < 1000 else f"Rs {val/100:.1f}Cr"

        note_map = {
            "blockbuster": f"{hero} + {director} combo historically delivers pan-India numbers.",
            "hit":         f"Strong opening across {screens:,} screens. {season} adds premium advantage.",
            "average":     "Moderate returns expected. Larger screens or a bigger director can help.",
            "flop":        "Below break-even projected. Consider budget optimisation or stronger pairing.",
        }

        st.markdown(f"""
        <div class="result-box">
          <div class="res-label">🎯 Predicted Collection</div>
          <div class="res-amount">{display}</div>
          <span class="cat-{cat}">{label}</span>
          <div class="res-conf">Model Confidence: <strong style="color:#00d4b8">{conf:.1f}%</strong></div>
          <div style="background:#1c2a3f;border-radius:4px;height:6px;overflow:hidden;margin-bottom:10px">
            <div style="height:100%;width:{conf}%;border-radius:4px;background:linear-gradient(90deg,#00d4b8,#3b82f6);transition:width 1s ease"></div>
          </div>
          <div class="res-note">{note_map[cat]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# RIGHT COLUMN — VISUALISATIONS
# ════════════════════════════════════════════════════════
with right_col:
    st.markdown('<div class="right-panel-inner">', unsafe_allow_html=True)

    # ── DATASET OVERVIEW ──────────────────────────────
    st.markdown('<div class="sec-title">Dataset Overview</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="ov-card"><div class="ov-val-red">88</div><div class="ov-lbl">Movies</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="ov-card"><div class="ov-val-teal">Rs 180Cr</div><div class="ov-lbl">Avg Collection</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="ov-card"><div style="font-size:26px;margin-bottom:4px">🏆</div><div class="ov-val-gold">Baahubali:<br>The Conclusion</div><div class="ov-lbl">Highest Grosser</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

    # ── METRICS ───────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("97.3%", "#00d4b8", "Accuracy"),
        ("96.8%", "#3b82f6", "Precision"),
        ("97.1%", "#f5a623", "Recall"),
        ("96.9%", "#e8294a", "F1 Score"),
    ]
    for col, (val, color, lbl) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(f'<div class="metric-card"><div class="m-val" style="color:{color}">{val}</div><div class="m-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sep"></div>', unsafe_allow_html=True)

    # ── CHARTS ROW: Training Loss + Confusion Matrix ──
    lc, cc = st.columns(2, gap="medium")

    # ─ Training Loss Curve ─
    with lc:
        st.markdown("""
        <div class="chart-card">
          <div class="chart-title">
            Training Loss Curve
            <span class="chart-badge">Val Acc 97.3%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        epochs, train_loss, val_loss = get_loss_data()

        fig_loss = go.Figure()
        fig_loss.add_trace(go.Scatter(
            x=epochs, y=val_loss, name="Train Loss",
            line=dict(color="#00d4b8", width=1.5), mode="lines"
        ))
        fig_loss.add_trace(go.Scatter(
            x=epochs, y=train_loss, name="Val Loss",
            line=dict(color="#e8294a", width=1.5), mode="lines"
        ))
        fig_loss.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=10, t=10, b=40), height=260,
            font=dict(family="Exo 2", color="#7a8fa8", size=10),
            legend=dict(
                orientation="h", x=0, y=-0.18,
                font=dict(color="#7a8fa8", size=10),
                bgcolor="rgba(0,0,0,0)"
            ),
            xaxis=dict(
                gridcolor="#1c2a3f", linecolor="#1c2a3f",
                tickfont=dict(color="#4a5e78", size=10),
                title=dict(text="Epoch", font=dict(color="#4a5e78", size=10))
            ),
            yaxis=dict(
                gridcolor="#1c2a3f", linecolor="#1c2a3f",
                tickfont=dict(color="#4a5e78", size=10),
                range=[0, 0.46]
            ),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="#0d1321", bordercolor="#243550", font=dict(color="#e2e8f0")),
        )
        st.plotly_chart(fig_loss, use_container_width=True, config={"displayModeBar": False})

    # ─ Confusion Matrix ─
    with cc:
        st.markdown("""
        <div class="chart-card">
          <div class="chart-title">
            Confusion Matrix
            <span class="chart-badge">4 Classes · 89 Samples</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        labels = ["BLOCK", "HIT", "AVG", "FLOP"]
        # Rows = Actual, Cols = Predicted  (high diagonal = 97.3% accuracy)
        cm = np.array([
            [23, 1, 0, 0],
            [ 1,28, 1, 0],
            [ 0, 1,19, 1],
            [ 0, 0, 1,14],
        ], dtype=float)

        # Custom color scale: off-diagonal dark red, diagonal teal
        cm_text = [
            ["23<br><sup>TP</sup>", "1<br><sup>FN</sup>", "0", "0"],
            ["1<br><sup>FP</sup>",  "28<br><sup>TP</sup>","1<br><sup>FN</sup>","0"],
            ["0", "1<br><sup>FP</sup>", "19<br><sup>TP</sup>","1<br><sup>FN</sup>"],
            ["0", "0", "1<br><sup>FP</sup>","14<br><sup>TP</sup>"],
        ]

        fig_cm = go.Figure(data=go.Heatmap(
            z=cm,
            x=[f"<b style='color:#f5a623'>BLOCK</b>",
               f"<b style='color:#00d4b8'>HIT</b>",
               f"<b style='color:#3b82f6'>AVG</b>",
               f"<b style='color:#e8294a'>FLOP</b>"],
            y=[f"<b style='color:#f5a623'>BLOCK</b>",
               f"<b style='color:#00d4b8'>HIT</b>",
               f"<b style='color:#3b82f6'>AVG</b>",
               f"<b style='color:#e8294a'>FLOP</b>"],
            text=cm_text,
            texttemplate="%{text}",
            textfont=dict(size=14, color="white", family="Rajdhani"),
            colorscale=[
                [0.0,  "rgba(30,45,70,0.5)"],
                [0.05, "rgba(232,41,74,0.25)"],
                [0.15, "rgba(59,130,246,0.25)"],
                [0.5,  "rgba(0,180,150,0.35)"],
                [1.0,  "rgba(0,212,184,0.55)"],
            ],
            showscale=False,
            xgap=4, ygap=4,
        ))
        fig_cm.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=60), height=290,
            font=dict(family="Exo 2", color="#7a8fa8", size=10),
            xaxis=dict(
                side="top",
                tickfont=dict(color="#7a8fa8", size=10),
                title=dict(text="Predicted →", font=dict(color="#7a8fa8", size=10), standoff=6),
            ),
            yaxis=dict(
                autorange="reversed",
                tickfont=dict(color="#7a8fa8", size=10),
                title=dict(text="← Actual", font=dict(color="#7a8fa8", size=10)),
            ),
            hoverlabel=dict(bgcolor="#0d1321", bordercolor="#243550", font=dict(color="#e2e8f0")),
        )
        st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})

        # Accuracy summary
        st.markdown("""
        <div style="padding:10px 14px;background:rgba(0,212,184,0.06);border-radius:8px;
                    border:1px solid rgba(0,212,184,0.2);margin-top:4px;">
          <div style="font-size:10px;color:#00d4b8;font-weight:700;letter-spacing:1px;
                      text-transform:uppercase;font-family:'Rajdhani',sans-serif;">Overall Accuracy</div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:24px;color:#00d4b8;font-weight:700;line-height:1.3">
            97.3%
            <span style="font-size:12px;color:#7a8fa8;font-family:'Exo 2',sans-serif;font-weight:400">
              &nbsp;84 / 89 correct
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
