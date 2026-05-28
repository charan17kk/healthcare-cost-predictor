import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="HealthCost Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
#  GLOBAL CSS  —  Apple Health × Hospital Portal · Clean Light Theme
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:opsz,wght@6..12,300;6..12,400;6..12,500;6..12,600;6..12,700;6..12,800&family=Playfair+Display:wght@600;700&display=swap');

/* ── Variables ── */
:root {
    --white:         #ffffff;
    --bg:            #f5f7fa;
    --bg-subtle:     #eef1f7;
    --card:          #ffffff;
    --border:        #e4e9f2;
    --border-focus:  #2563eb;

    --blue-600:      #2563eb;
    --blue-500:      #3b82f6;
    --blue-100:      #dbeafe;
    --blue-50:       #eff6ff;

    --green-600:     #16a34a;
    --green-100:     #dcfce7;
    --green-50:      #f0fdf4;

    --amber-600:     #d97706;
    --amber-100:     #fef3c7;
    --amber-50:      #fffbeb;

    --red-600:       #dc2626;
    --red-100:       #fee2e2;
    --red-50:        #fef2f2;

    --text-900:      #0f172a;
    --text-700:      #334155;
    --text-500:      #64748b;
    --text-400:      #94a3b8;

    --shadow-xs:     0 1px 3px rgba(15,23,42,0.06), 0 1px 2px rgba(15,23,42,0.04);
    --shadow-sm:     0 2px 8px rgba(15,23,42,0.08), 0 1px 3px rgba(15,23,42,0.06);
    --shadow-md:     0 4px 16px rgba(15,23,42,0.10), 0 2px 6px rgba(15,23,42,0.06);
    --radius:        14px;
    --radius-sm:     9px;
}

/* ── Base reset ── */
html, body, [class*="css"] {
    font-family: 'Nunito Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text-900);
}
.stApp { background: var(--bg) !important; }

/* ── Hide chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Page container ── */
.block-container {
    padding: 1.75rem 2.5rem 3rem 2.5rem !important;
    max-width: 1180px !important;
}

/* ══════════════════════════════════════
   TOP NAV BAR
══════════════════════════════════════ */
.topnav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 1.25rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.75rem;
}
.nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-brand-icon {
    width: 36px; height: 36px;
    background: var(--blue-600);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    box-shadow: 0 2px 8px rgba(37,99,235,0.3);
}
.nav-brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-900);
    letter-spacing: -0.01em;
}
.nav-brand-sub {
    font-size: 0.72rem;
    color: var(--text-400);
    font-weight: 400;
    margin-top: -2px;
}
.nav-status {
    display: flex;
    align-items: center;
    gap: 7px;
    background: var(--green-50);
    border: 1px solid var(--green-100);
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--green-600);
}
.nav-dot {
    width: 7px; height: 7px;
    background: var(--green-600);
    border-radius: 50%;
    animation: blink 2s infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* ══════════════════════════════════════
   PAGE HEADER
══════════════════════════════════════ */
.page-header {
    margin-bottom: 1.75rem;
}
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text-900);
    line-height: 1.2;
    margin: 0 0 0.35rem 0;
    letter-spacing: -0.02em;
}
.page-desc {
    font-size: 0.9rem;
    color: var(--text-500);
    font-weight: 400;
    margin: 0;
    line-height: 1.5;
}

/* ══════════════════════════════════════
   FORM CARDS
══════════════════════════════════════ */
.form-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem 1.6rem 1.6rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1rem;
}
.card-header {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 1.1rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--border);
}
.card-header-icon {
    width: 30px; height: 30px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem;
    flex-shrink: 0;
}
.icon-blue   { background: var(--blue-50);  }
.icon-teal   { background: #f0fdfa; }
.icon-violet { background: #f5f3ff; }
.card-header-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text-700);
    letter-spacing: 0.01em;
    text-transform: uppercase;
}

/* ══════════════════════════════════════
   INPUT OVERRIDES
══════════════════════════════════════ */
label, .stSelectbox label, .stNumberInput label, .stSlider label {
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: var(--text-500) !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: var(--bg) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-900) !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: var(--blue-500) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
    outline: none !important;
    background: var(--white) !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: var(--bg) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-900) !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--blue-500) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}

/* Slider track */
div[data-testid="stSlider"] > div > div > div > div[role="slider"] {
    background: var(--blue-600) !important;
    border: 2px solid var(--white) !important;
    box-shadow: 0 1px 4px rgba(37,99,235,0.35) !important;
}
div[data-testid="stSlider"] > div > div > div > div:first-child {
    background: var(--blue-100) !important;
}

/* ══════════════════════════════════════
   HEALTH SCORE CARD
══════════════════════════════════════ */
.health-score-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    flex-wrap: wrap;
}
.score-ring-wrap {
    position: relative;
    width: 90px; height: 90px;
    flex-shrink: 0;
}
.score-ring-wrap svg { transform: rotate(-90deg); }
.score-center {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    line-height: 1;
}
.score-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-900);
}
.score-label {
    font-size: 0.6rem;
    color: var(--text-400);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.score-details { flex: 1; min-width: 200px; }
.score-title {
    font-size: 0.82rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-500);
    margin-bottom: 0.3rem;
}
.score-headline {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-900);
    margin-bottom: 0.5rem;
}
.score-bars { display: flex; flex-direction: column; gap: 5px; }
.score-bar-row {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.73rem; color: var(--text-500); font-weight: 600;
}
.score-bar-row span:first-child { width: 72px; text-align: right; flex-shrink: 0; }
.score-bar-track {
    flex: 1; height: 5px;
    background: var(--bg-subtle);
    border-radius: 99px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%; border-radius: 99px;
    transition: width 0.4s ease;
}
.score-bar-row span:last-child { width: 28px; flex-shrink: 0; font-weight: 700; color: var(--text-700); }

/* Factors grid */
.factors-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    flex: 2;
    min-width: 280px;
}
.factor-chip {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 9px 10px;
    text-align: center;
}
.factor-chip-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 2px;
}
.factor-chip-lbl {
    font-size: 0.65rem;
    color: var(--text-400);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ══════════════════════════════════════
   PREDICT BUTTON
══════════════════════════════════════ */
div[data-testid="stButton"] > button {
    background: var(--blue-600) !important;
    color: #fff !important;
    font-family: 'Nunito Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2.5rem !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 2px 10px rgba(37,99,235,0.28) !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stButton"] > button:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 4px 18px rgba(37,99,235,0.38) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ══════════════════════════════════════
   RESULT SECTION
══════════════════════════════════════ */
.result-wrapper {
    animation: fadeUp 0.45s cubic-bezier(0.16,1,0.3,1) forwards;
}
@keyframes fadeUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}

/* Cost card */
.cost-card {
    background: var(--card);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow-md);
    text-align: center;
    border-top: 4px solid transparent;
    position: relative;
    overflow: hidden;
}
.cost-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
}
.cost-card.low    { border-top-color: var(--green-600); }
.cost-card.medium { border-top-color: var(--amber-600); }
.cost-card.high   { border-top-color: var(--red-600);   }

.cost-eyebrow {
    font-size: 0.72rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-400);
    margin-bottom: 0.5rem;
}
.cost-amount {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.6rem;
    letter-spacing: -0.02em;
}
.cost-card.low    .cost-amount { color: var(--green-600); }
.cost-card.medium .cost-amount { color: var(--amber-600); }
.cost-card.high   .cost-amount { color: var(--red-600);   }

.cost-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    letter-spacing: 0.03em;
}
.cost-card.low    .cost-badge { background:var(--green-100); color:var(--green-600); }
.cost-card.medium .cost-badge { background:var(--amber-100); color:var(--amber-600); }
.cost-card.high   .cost-badge { background:var(--red-100);   color:var(--red-600);   }

/* Insight panel */
.insight-panel {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    text-align: left;
    font-size: 0.84rem;
    color: var(--text-700);
    line-height: 1.65;
}
.insight-panel strong { color: var(--text-900); font-weight: 700; }

/* Summary chips below cost card */
.summary-chips {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
    justify-content: center;
}
.s-chip {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 0.75rem;
    color: var(--text-700);
    font-weight: 600;
}
.s-chip span { color: var(--text-400); font-weight: 500; }

/* ══════════════════════════════════════
   HEALTH SCORE RESULT (circular gauge)
══════════════════════════════════════ */
.hs-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
}
.hs-title {
    font-size: 0.78rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: var(--text-500);
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.hs-score-big {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.hs-score-sub {
    font-size: 0.75rem;
    color: var(--text-400);
    font-weight: 600;
    margin-bottom: 1rem;
}
.hs-bar { height: 8px; border-radius: 99px; background: var(--bg-subtle); overflow: hidden; margin-bottom: 1rem; }
.hs-bar-fill { height: 100%; border-radius: 99px; }
.hs-factor-list { display: flex; flex-direction: column; gap: 6px; }
.hs-factor {
    display: flex; justify-content: space-between; align-items: center;
    font-size: 0.78rem; color: var(--text-700); font-weight: 600;
    padding: 5px 8px;
    background: var(--bg);
    border-radius: 7px;
}
.hs-factor-dot {
    width: 7px; height: 7px; border-radius: 50%; margin-right: 6px; display: inline-block; flex-shrink: 0;
}

/* ══════════════════════════════════════
   MISC UTILITIES
══════════════════════════════════════ */
div[data-testid="column"] { padding: 0 0.45rem !important; }
.row-gap { margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  LOAD MODEL  ← backend unchanged
# ═══════════════════════════════════════════════════════════════════════════════

prod_files = joblib.load("MmodelL_prod_files.pkl")
model  = prod_files['model']
OHE    = prod_files['cat_encod']
scaler = prod_files['num_encod']


# ═══════════════════════════════════════════════════════════════════════════════
#  TOP NAV
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="topnav">
    <div class="nav-brand">
        <div class="nav-brand-icon">🏥</div>
        <div>
            <div class="nav-brand-name">HealthCost Portal</div>
            <div class="nav-brand-sub">Annual Medical Expense Estimator</div>
        </div>
    </div>
    <div class="nav-status">
        <div class="nav-dot"></div>
        Model Ready
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="page-header">
    <h1 class="page-title">Personalized Healthcare Expense Estimator</h1>
    <p class="page-desc">Complete the form below to receive an estimated annual healthcare expenditure and risk profile.</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 1  — Demographics & Lifestyle
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="form-card">
  <div class="card-header">
    <div class="card-header-icon icon-blue">👤</div>
    <div class="card-header-title">Demographics &amp; Lifestyle</div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        age    = st.number_input("Age", min_value=18, max_value=100, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with c2:
        bmi    = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0, step=0.1)
        smoker = st.selectbox("Smoker", ["Yes", "No"])
    with c3:
        physical_activity_level = st.selectbox("Physical Activity Level", ["Low", "Medium", "High"])
        daily_steps = st.number_input("Daily Steps", min_value=0, max_value=30000, value=5000, step=500)
    with c4:
        sleep_hours  = st.slider("Sleep Hours", min_value=0.0, max_value=12.0, value=7.0, step=0.5)
        stress_level = st.slider("Stress Level (1–10)", min_value=1, max_value=10, value=5)
        city_type    = st.selectbox("City Type", ["Urban", "Semi-Urban", "Rural"])

st.markdown('<div class="row-gap"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  SECTION 2  — Medical History + Insurance (side by side)
# ═══════════════════════════════════════════════════════════════════════════════

col_med, col_ins = st.columns(2)

with col_med:
    st.markdown("""
    <div class="form-card">
      <div class="card-header">
        <div class="card-header-icon icon-teal">🩺</div>
        <div class="card-header-title">Medical History</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        diabetes      = st.selectbox("Diabetes",      ["No", "Yes"])
        heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
    with m2:
        hypertension = st.selectbox("Hypertension", ["No", "Yes"])
        asthma       = st.selectbox("Asthma",        ["No", "Yes"])

with col_ins:
    st.markdown("""
    <div class="form-card">
      <div class="card-header">
        <div class="card-header-icon icon-violet">📋</div>
        <div class="card-header-title">Healthcare Usage &amp; Insurance</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    with i1:
        doctor_visits_per_year = st.slider("Doctor Visits / Year",  min_value=0, max_value=15, value=2)
        hospital_admissions    = st.slider("Hospital Admissions",   min_value=0, max_value=10, value=0)
        medication_count       = st.slider("Medications",           min_value=0, max_value=10, value=1)
    with i2:
        insurance_type         = st.selectbox("Insurance Type", ["Government", "Private", "unknown"])
        insurance_coverage_pct = st.slider("Coverage %",        min_value=0, max_value=100, value=50)
        previous_year_cost     = st.number_input("Prev. Year Cost (₹)", min_value=0, max_value=100000, value=5000, step=500)

st.markdown('<div class="row-gap"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  HEALTH SCORE  (computed from inputs before prediction)
# ═══════════════════════════════════════════════════════════════════════════════

# Compute a 0–100 health score from lifestyle signals (UI only — no ML)
def compute_health_score(age, bmi, smoker, physical_activity_level,
                          daily_steps, sleep_hours, stress_level,
                          diabetes, hypertension, heart_disease, asthma,
                          medication_count, doctor_visits_per_year):
    score = 100
    # BMI
    if bmi < 18.5 or bmi >= 30: score -= 12
    elif bmi >= 25:              score -= 6
    # Smoking
    if smoker == "Yes":          score -= 15
    # Activity
    if physical_activity_level == "Low":    score -= 10
    elif physical_activity_level == "High": score += 5
    # Steps
    if daily_steps < 3000:   score -= 8
    elif daily_steps >= 8000: score += 4
    # Sleep
    if sleep_hours < 6 or sleep_hours > 9: score -= 6
    # Stress
    score -= max(0, (stress_level - 5)) * 2
    # Conditions
    if diabetes == "Yes":     score -= 10
    if hypertension == "Yes": score -= 8
    if heart_disease == "Yes":score -= 12
    if asthma == "Yes":       score -= 6
    # Medications
    score -= min(medication_count * 2, 10)
    # Doctor visits (positive signal up to 3)
    score += min(doctor_visits_per_year, 3) * 2
    # Age
    if age > 60:   score -= 8
    elif age > 45: score -= 4
    return max(10, min(100, score))

hs = compute_health_score(
    age, bmi, smoker, physical_activity_level,
    daily_steps, sleep_hours, stress_level,
    diabetes, hypertension, heart_disease, asthma,
    medication_count, doctor_visits_per_year
)

hs_color  = "#16a34a" if hs >= 70 else ("#d97706" if hs >= 45 else "#dc2626")
hs_grade  = "Good"    if hs >= 70 else ("Fair"    if hs >= 45 else "Poor")

# Sub-scores for bars
lifestyle_score  = min(100, max(0, 100
    - (0  if physical_activity_level=="High" else (5 if physical_activity_level=="Medium" else 20))
    - (0  if daily_steps >= 8000 else (10 if daily_steps >= 4000 else 20))
    - (0  if sleep_hours >= 7 else 15)
    - (smoker == "Yes") * 20
))
medical_score = min(100, max(0, 100
    - (diabetes=="Yes")*20 - (hypertension=="Yes")*15
    - (heart_disease=="Yes")*25 - (asthma=="Yes")*10
))
stress_score = max(0, 100 - (stress_level - 1) * 10)

st.markdown(f"""
<div class="health-score-card">
  <!-- Ring -->
  <div class="score-ring-wrap">
    <svg width="90" height="90" viewBox="0 0 90 90">
      <circle cx="45" cy="45" r="36" fill="none" stroke="#e4e9f2" stroke-width="8"/>
      <circle cx="45" cy="45" r="36" fill="none" stroke="{hs_color}" stroke-width="8"
        stroke-dasharray="{2*3.14159*36}" stroke-dashoffset="{2*3.14159*36*(1-hs/100)}"
        stroke-linecap="round"/>
    </svg>
    <div class="score-center">
      <div class="score-number">{hs}</div>
      <div class="score-label">/ 100</div>
    </div>
  </div>
  <!-- Details -->
  <div class="score-details">
    <div class="score-title">Health Score</div>
    <div class="score-headline" style="color:{hs_color}">{hs_grade} Health Profile</div>
    <div class="score-bars">
      <div class="score-bar-row">
        <span>Lifestyle</span>
        <div class="score-bar-track"><div class="score-bar-fill" style="width:{lifestyle_score}%;background:#3b82f6"></div></div>
        <span>{lifestyle_score}</span>
      </div>
      <div class="score-bar-row">
        <span>Medical</span>
        <div class="score-bar-track"><div class="score-bar-fill" style="width:{medical_score}%;background:#10b981"></div></div>
        <span>{medical_score}</span>
      </div>
      <div class="score-bar-row">
        <span>Stress</span>
        <div class="score-bar-track"><div class="score-bar-fill" style="width:{stress_score}%;background:#f59e0b"></div></div>
        <span>{stress_score}</span>
      </div>
    </div>
  </div>
  <!-- Factor chips -->
  <div class="factors-grid">
    <div class="factor-chip">
      <div class="factor-chip-val" style="color:{'#16a34a' if bmi<25 else '#d97706' if bmi<30 else '#dc2626'}">{bmi:.1f}</div>
      <div class="factor-chip-lbl">BMI</div>
    </div>
    <div class="factor-chip">
      <div class="factor-chip-val" style="color:{'#dc2626' if smoker=='Yes' else '#16a34a'}">{'Yes' if smoker=='Yes' else 'No'}</div>
      <div class="factor-chip-lbl">Smoker</div>
    </div>
    <div class="factor-chip">
      <div class="factor-chip-val" style="color:{'#16a34a' if daily_steps>=8000 else '#d97706' if daily_steps>=4000 else '#dc2626'}">{daily_steps:,}</div>
      <div class="factor-chip-lbl">Steps/day</div>
    </div>
    <div class="factor-chip">
      <div class="factor-chip-val" style="color:{'#16a34a' if 7<=sleep_hours<=8 else '#d97706'}">{sleep_hours:.1f}h</div>
      <div class="factor-chip-lbl">Sleep</div>
    </div>
    <div class="factor-chip">
      <div class="factor-chip-val" style="color:{'#dc2626' if stress_level>=7 else '#d97706' if stress_level>=5 else '#16a34a'}">{stress_level}/10</div>
      <div class="factor-chip-lbl">Stress</div>
    </div>
    <div class="factor-chip">
      <div class="factor-chip-val" style="color:{'#d97706' if age>45 else '#16a34a'}">{age}</div>
      <div class="factor-chip-lbl">Age</div>
    </div>
    <div class="factor-chip">
      <div class="factor-chip-val" style="color:{'#16a34a' if physical_activity_level=='High' else '#d97706' if physical_activity_level=='Medium' else '#dc2626'}">{physical_activity_level[:3]}</div>
      <div class="factor-chip-lbl">Activity</div>
    </div>
    <div class="factor-chip">
      <div class="factor-chip-val" style="color:{'#dc2626' if medication_count>3 else '#d97706' if medication_count>1 else '#16a34a'}">{medication_count}</div>
      <div class="factor-chip-lbl">Meds</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PREDICT BUTTON
# ═══════════════════════════════════════════════════════════════════════════════

col_b1, col_b2, col_b3 = st.columns([1.5, 2, 1.5])
with col_b2:
    predict_clicked = st.button("Calculate Annual Medical Cost →")


# ═══════════════════════════════════════════════════════════════════════════════
#  PREDICTION  ←  BACKEND LOGIC UNCHANGED
# ═══════════════════════════════════════════════════════════════════════════════

if predict_clicked:

    with st.spinner("Analysing patient profile…"):
        time.sleep(0.7)

    # ── Binary conversion ──────────────────────────────────────────────────────
    diabetes_val      = 1 if diabetes      == "Yes" else 0
    hypertension_val  = 1 if hypertension  == "Yes" else 0
    heart_disease_val = 1 if heart_disease == "Yes" else 0
    asthma_val        = 1 if asthma        == "Yes" else 0

    # ── Build DataFrame ────────────────────────────────────────────────────────
    input_df = pd.DataFrame({
        'age':                    [age],
        'gender':                 [gender],
        'bmi':                    [bmi],
        'smoker':                 [smoker],
        'diabetes':               [diabetes_val],
        'hypertension':           [hypertension_val],
        'heart_disease':          [heart_disease_val],
        'asthma':                 [asthma_val],
        'physical_activity_level':[physical_activity_level],
        'daily_steps':            [daily_steps],
        'sleep_hours':            [sleep_hours],
        'stress_level':           [stress_level],
        'doctor_visits_per_year': [doctor_visits_per_year],
        'hospital_admissions':    [hospital_admissions],
        'medication_count':       [medication_count],
        'insurance_type':         [insurance_type],
        'insurance_coverage_pct': [insurance_coverage_pct],
        'city_type':              [city_type],
        'previous_year_cost':     [previous_year_cost]
    })

    # ── Split features ─────────────────────────────────────────────────────────
    cat_df   = input_df.select_dtypes(include='object')
    num_df   = input_df[[
        'age','bmi','daily_steps','sleep_hours','stress_level',
        'doctor_visits_per_year','hospital_admissions',
        'medication_count','insurance_coverage_pct','previous_year_cost'
    ]]
    no_trans = input_df[['diabetes','hypertension','heart_disease','asthma']]

    # ── Transform ──────────────────────────────────────────────────────────────
    cat_df_trans = OHE.transform(cat_df)
    num_df_trans = scaler.transform(num_df)
    final_input  = pd.concat([cat_df_trans, num_df_trans, no_trans], axis=1)

    # ── Predict ────────────────────────────────────────────────────────────────
    prediction     = model.predict(final_input)
    predicted_cost = round(prediction[0][0], 2)
    # ══════════════════════════════════════════════════════════════════════════

    # ── Risk tier (UI only) ───────────────────────────────────────────────────
    if predicted_cost < 15000:
        risk_cls   = "low"
        risk_label = "✓ Low Risk"
        insight    = (
            f"The predicted cost of <strong>₹{predicted_cost:,.2f}</strong> falls in the "
            f"<strong>low-risk</strong> tier. The patient's lifestyle and medical profile "
            f"suggest manageable health expenses. Maintaining current habits is advised."
        )
    elif predicted_cost < 40000:
        risk_cls   = "medium"
        risk_label = "⚠ Moderate Risk"
        insight    = (
            f"The predicted cost of <strong>₹{predicted_cost:,.2f}</strong> indicates "
            f"<strong>moderate</strong> healthcare expenditure. Reviewing lifestyle factors "
            f"such as stress, physical activity, and medication count may help reduce costs."
        )
    else:
        risk_cls   = "high"
        risk_label = "! High Risk"
        insight    = (
            f"The predicted cost of <strong>₹{predicted_cost:,.2f}</strong> places this patient "
            f"in the <strong>high-risk</strong> tier. Factors such as chronic conditions, "
            f"hospital admissions, or low insurance coverage are likely driving costs. "
            f"Proactive intervention is recommended."
        )

    # ── Result layout ─────────────────────────────────────────────────────────
    st.markdown('<div class="result-wrapper">', unsafe_allow_html=True)

    res_l, res_r = st.columns([3, 2])

    with res_l:
        st.markdown(f"""
        <div class="cost-card {risk_cls}">
            <div class="cost-eyebrow">Predicted Annual Medical Expense</div>
            <div class="cost-amount">₹ {predicted_cost:,.2f}</div>
            <div class="cost-badge">{risk_label}</div>
            <div class="insight-panel">{insight}</div>
            <div class="summary-chips">
                <div class="s-chip"><span>Age </span>{age}</div>
                <div class="s-chip"><span>BMI </span>{bmi:.1f}</div>
                <div class="s-chip"><span>Smoker </span>{smoker}</div>
                <div class="s-chip"><span>Coverage </span>{insurance_coverage_pct}%</div>
                <div class="s-chip"><span>Dr Visits </span>{doctor_visits_per_year}/yr</div>
                <div class="s-chip"><span>Admissions </span>{hospital_admissions}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with res_r:
        # Health score result card (same computed score, now shown in results context)
        hs_bar_w = hs
        cond_count = sum([
            diabetes=="Yes", hypertension=="Yes",
            heart_disease=="Yes", asthma=="Yes"
        ])
        active_conditions = []
        if diabetes=="Yes":      active_conditions.append(("Diabetes",     "#dc2626"))
        if hypertension=="Yes":  active_conditions.append(("Hypertension", "#d97706"))
        if heart_disease=="Yes": active_conditions.append(("Heart Disease","#dc2626"))
        if asthma=="Yes":        active_conditions.append(("Asthma",       "#d97706"))
        if not active_conditions:
            active_conditions.append(("No conditions flagged", "#16a34a"))

        factors_html = "".join([
            f'<div class="hs-factor">'
            f'<span><span class="hs-factor-dot" style="background:{col}"></span>{name}</span>'
            f'</div>'
            for name, col in active_conditions
        ])

        st.markdown(f"""
        <div class="hs-card">
            <div class="hs-title">Health Score Summary</div>
            <div class="hs-score-big" style="color:{hs_color}">{hs}</div>
            <div class="hs-score-sub">out of 100 — {hs_grade}</div>
            <div class="hs-bar">
                <div class="hs-bar-fill" style="width:{hs_bar_w}%;background:{hs_color}"></div>
            </div>
            <div style="font-size:0.75rem;font-weight:700;color:var(--text-500);
                        text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.5rem;">
                Flagged Conditions
            </div>
            <div class="hs-factor-list">{factors_html}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="
text-align:center;
padding:2rem 0 1rem 0;
font-size:0.75rem;
color:#94a3b8;
">
Healthcare Cost Prediction Dashboard • Built with Streamlit & Machine Learning
</div>
""", unsafe_allow_html=True)
