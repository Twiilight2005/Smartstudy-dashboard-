import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, date

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartStudy AI Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS  (dark theme matching the prototype)
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0d0f14;
    color: #e2e8f0;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 1.5rem 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #141720 !important;
    border-right: 1px solid #2a2f3e;
}
[data-testid="stSidebar"] * { color: #8892a4 !important; }
[data-testid="stSidebar"] .sidebar-title {
    color: #e2e8f0 !important;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #1a1e2a;
    border: 1px solid #2a2f3e;
    border-radius: 12px;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] { color: #8892a4 !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-size: 26px !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

/* ── Cards ── */
.dash-card {
    background: #141720;
    border: 1px solid #2a2f3e;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 16px;
}
.section-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #555f72;
    text-transform: uppercase;
    margin-bottom: 14px;
}

/* ── Priority badges ── */
.badge-critical {
    background: #3d0f0f; color: #f87171;
    border: 1px solid #f8717144;
    font-size: 10px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
    display: inline-block;
}
.badge-high {
    background: #2d1a06; color: #fb923c;
    border: 1px solid #fb923c44;
    font-size: 10px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
    display: inline-block;
}
.badge-medium {
    background: #2d2206; color: #fbbf24;
    border: 1px solid #fbbf2444;
    font-size: 10px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
    display: inline-block;
}

/* ── Task rows ── */
.task-row {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #2a2f3e;
    font-size: 14px;
}
.task-done { text-decoration: line-through; color: #555f72; }
.tag { font-size: 10px; padding: 3px 9px; border-radius: 10px; font-weight: 500; }
.tag-study    { background:#1e2a1e; color:#4ade80; border:1px solid #4ade8044; }
.tag-practice { background:#1a1f2e; color:#38bdf8; border:1px solid #38bdf844; }
.tag-revise   { background:#261a2e; color:#a78bfa; border:1px solid #a78bfa44; }
.tag-project  { background:#1e2226; color:#00c9a7; border:1px solid #00c9a744; }
.tag-quiz     { background:#2a1e2a; color:#f472b6; border:1px solid #f472b644; }

/* ── Revision items ── */
.rev-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 12px;
    background: #1a1e2a; border-radius: 10px;
    margin-bottom: 8px;
}

/* ── Streak / date badges in header ── */
.streak-badge {
    background: #2a1f0a; color: #fb923c;
    border: 1px solid #fb923c44;
    font-size: 13px; font-weight: 600;
    padding: 6px 14px; border-radius: 20px;
    display: inline-block;
}
.date-badge {
    background: #1a1e2a; color: #8892a4;
    border: 1px solid #2a2f3e;
    font-size: 13px;
    padding: 6px 14px; border-radius: 20px;
    display: inline-block;
}

/* ── Chat ── */
.chat-wrap {
    background: #141720;
    border: 1px solid #2a2f3e;
    border-radius: 14px;
    overflow: hidden;
}
.chat-header {
    padding: 10px 16px;
    background: #1a1e2a;
    border-bottom: 1px solid #2a2f3e;
    font-size: 13px; font-weight: 600; color: #e2e8f0;
}
.msg-ai {
    background: #1a1e2a; color: #e2e8f0;
    border: 1px solid #2a2f3e;
    border-radius: 10px; padding: 10px 13px;
    font-size: 13px; line-height: 1.6;
    margin-bottom: 8px; max-width: 82%;
}
.msg-user {
    background: linear-gradient(135deg,#1a3a30,#1a2040);
    color: #00c9a7;
    border: 1px solid #00c9a733;
    border-radius: 10px; padding: 10px 13px;
    font-size: 13px; line-height: 1.6;
    margin-bottom: 8px; max-width: 82%;
    margin-left: auto;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: #1a1e2a !important;
    border: 1px solid #2a2f3e !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: #00c9a7 !important;
    color: #0d0f14 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
}
.stButton > button:hover {
    background: #00b090 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #141720;
    border-bottom: 1px solid #2a2f3e;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #8892a4 !important;
    border-radius: 8px 8px 0 0 !important;
    font-size: 13px !important;
}
.stTabs [aria-selected="true"] {
    color: #00c9a7 !important;
    border-bottom: 2px solid #00c9a7 !important;
    background: #1a1e2a !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #0d0f14 !important;
    padding: 16px 0 !important;
}

/* ── Selectbox / radio ── */
.stSelectbox > div > div,
.stRadio > div { background: #1a1e2a !important; border-color: #2a2f3e !important; }

/* ── Progress bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00c9a7, #a78bfa) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MOCK DATA
# ─────────────────────────────────────────────
STUDENT = {
    "name": "Arjun Rajan",
    "grade": "Grade 11 · Science",
    "streak": 14,
    "ai_score": 74.2,
    "score_delta": 3.8,
    "tasks_today": 5,
    "tasks_total": 5,
    "hours_week": 18.5,
    "exam": {"name": "Physics Final", "days_left": 12},
}

SUBJECTS = [
    {"name": "Mathematics", "pct": 54, "color": "#fb923c"},
    {"name": "Physics",      "pct": 71, "color": "#a78bfa"},
    {"name": "Programming",  "pct": 88, "color": "#00c9a7"},
    {"name": "Chemistry",    "pct": 43, "color": "#f472b6"},
    {"name": "English",      "pct": 76, "color": "#38bdf8"},
]

WEAK_TOPICS = [
    {"name": "Organic Reactions",    "subject": "Chemistry",    "dot": "#f472b6", "priority": "Critical", "score": 28, "reason": "28% mastery · 3 repeated errors · low quiz accuracy 24%"},
    {"name": "Differential Calculus","subject": "Mathematics",  "dot": "#fb923c", "priority": "High",     "score": 41, "reason": "41% mastery · slow solving speed · 5-day revision gap"},
    {"name": "Matrix Algebra",       "subject": "Mathematics",  "dot": "#fb923c", "priority": "High",     "score": 48, "reason": "48% mastery · consistent first-attempt errors"},
    {"name": "Electromagnetism",     "subject": "Physics",      "dot": "#a78bfa", "priority": "Medium",   "score": 62, "reason": "62% mastery · VSEPR / field lines confusion"},
    {"name": "Newton's Laws",        "subject": "Physics",      "dot": "#a78bfa", "priority": "Medium",   "score": 61, "reason": "61% retention · 14 days since last revision"},
]

TASKS = [
    {"time": "09:00", "name": "Organic Reactions",    "meta": "Chemistry · 45 min",    "tag": "Study",    "tag_class": "tag-study",    "done": True},
    {"time": "10:00", "name": "Differential Calculus","meta": "Mathematics · 60 min",  "tag": "Practice", "tag_class": "tag-practice", "done": True},
    {"time": "14:00", "name": "Electromagnetism",     "meta": "Physics · 45 min",      "tag": "Revise",   "tag_class": "tag-revise",   "done": True},
    {"time": "16:00", "name": "Data Structures",      "meta": "Programming · 90 min",  "tag": "Project",  "tag_class": "tag-project",  "done": True},
    {"time": "19:00", "name": "Matrix Algebra",       "meta": "Mathematics · 30 min",  "tag": "Quiz",     "tag_class": "tag-quiz",     "done": True},
]

REVISIONS = [
    {"name": "Quadratic Equations", "meta": "Mathematics · 7d ago",  "icon": "📐", "retention": 72,  "ret_color": "#fbbf24", "interval": "1-day"},
    {"name": "Newton's Laws",       "meta": "Physics · 14d ago",     "icon": "⚡", "retention": 61,  "ret_color": "#fb923c", "interval": "1-day"},
    {"name": "Python Functions",    "meta": "Programming · 3d ago",  "icon": "💻", "retention": 88,  "ret_color": "#4ade80", "interval": "7-day"},
    {"name": "Integration",         "meta": "Mathematics · 2d ago",  "icon": "∫",  "retention": 71,  "ret_color": "#a78bfa", "interval": "3-day"},
]

MASTERY_TREND = {
    "weeks": ["Week 1", "Week 2", "Week 3", "Week 4"],
    "overall":     [66, 69, 71, 74],
    "chemistry":   [30, 34, 38, 43],
    "programming": [80, 84, 86, 88],
    "physics":     [64, 66, 69, 71],
}

QUIZ_ACCURACY = {
    "subjects": ["Programming", "English", "Physics", "Mathematics", "Chemistry"],
    "accuracy": [91, 78, 68, 52, 24],
    "colors":   ["#00c9a7", "#38bdf8", "#a78bfa", "#fb923c", "#f87171"],
}

AI_RESPONSES = {
    "What should I study today?":
        "📌 Based on your weak topics and today's schedule:\n\n"
        "1. **Organic Reactions** (45 min) — Chemistry at 28%, critical priority.\n"
        "2. **Differential Calculus** revision (30 min) — score 41%, 1-day interval due.\n"
        "3. **Matrix Algebra** quiz (20 min) — 48%, needs frequent reinforcement.\n\n"
        "You've already completed 5/5 tasks today — amazing consistency! 🎯",
    "Why is Organic Reactions weak?":
        "🔍 **Organic Reactions breakdown:**\n\n"
        "• Mastery score: **28/100** — Critical\n"
        "• Quiz accuracy: only **24%**\n"
        "• Repeated errors in: mechanism reactions, reagent identification\n"
        "• Root cause: concepts unclear before practice\n\n"
        "**Recommendation:** Watch reaction mechanism videos first, then attempt MCQs. Revise daily until score crosses 50.",
    "Show my progress this week":
        "📊 **This week's progress report:**\n\n"
        "• AI Score: **74.2** (↑3.8 from last week) ⭐\n"
        "• Programming: **88%** — your best subject!\n"
        "• Study streak: **14 days** — phenomenal!\n"
        "• Tasks completed: **5/5** today\n"
        "• Chemistry still critical at **28%** — needs daily work.\n\n"
        "Overall trend is positive. Keep Chemistry as your #1 focus this week.",
    "Plan my exam week":
        "📅 **Exam prep plan (7 days):**\n\n"
        "**Day 1–2:** Organic Reactions intensive (1h/day) + Calculus revision\n"
        "**Day 3–4:** Matrix Algebra drills + Physics mock tests\n"
        "**Day 5:** Full Chemistry mock paper\n"
        "**Day 6:** Error analysis — redo all wrong answers\n"
        "**Day 7:** Light revision only + good rest\n\n"
        "This prioritises your 3 critical weak topics while protecting strong subjects.",
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#8892a4",
    font_family="Space Grotesk",
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8892a4", size=11),
    ),
)

GRID_STYLE = dict(
    gridcolor="#1f2435",
    linecolor="#2a2f3e",
    tickfont=dict(color="#8892a4", size=10),
    zerolinecolor="#2a2f3e",
)


def gauge_ring(value: int, color: str, size: int = 110) -> go.Figure:
    fig = go.Figure(go.Pie(
        values=[value, 100 - value],
        hole=0.72,
        marker_colors=[color, "#1f2435"],
        textinfo="none",
        hoverinfo="skip",
        sort=False,
    ))
    fig.update_layout(
        width=size, height=size,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        annotations=[dict(
            text=f"<b>{value}%</b>",
            x=0.5, y=0.5,
            font=dict(size=16, color="#e2e8f0", family="Space Grotesk"),
            showarrow=False,
        )],
    )
    return fig


def priority_badge_html(priority: str) -> str:
    cls = {"Critical": "badge-critical", "High": "badge-high", "Medium": "badge-medium"}.get(priority, "badge-medium")
    return f'<span class="{cls}">{priority}</span>'


def score_color(score: int) -> str:
    if score < 40:  return "#f87171"
    if score < 60:  return "#fb923c"
    if score < 75:  return "#fbbf24"
    return "#4ade80"


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Student card
    st.markdown(f"""
    <div style="background:#1a1e2a;border:1px solid #2a2f3e;border-radius:12px;padding:14px;margin-bottom:14px">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <div style="width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#a78bfa,#00c9a7);
                 display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700;color:#0d0f14">A</div>
            <div>
                <div style="font-size:14px;font-weight:600;color:#e2e8f0">{STUDENT['name']}</div>
                <div style="font-size:11px;color:#8892a4">{STUDENT['grade']}</div>
            </div>
        </div>
        <span class="streak-badge">🔥 {STUDENT['streak']}-day streak</span>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    page = st.radio(
        "Navigation",
        ["📊 Overview", "⚠️ Weak Topics", "✅ Study Tasks", "↺ Revision", "📈 Progress", "🤖 AI Coach"],
        label_visibility="collapsed",
    )

    # Exam countdown
    st.markdown(f"""
    <div style="background:#1a1e2a;border:1px solid #2a2f3e;border-radius:12px;padding:14px;margin-top:16px">
        <div style="font-size:10px;font-weight:600;letter-spacing:1.2px;color:#555f72;text-transform:uppercase;margin-bottom:4px">Next Exam</div>
        <div style="font-size:13px;font-weight:600;color:#e2e8f0">{STUDENT['exam']['name']}</div>
        <div style="font-size:26px;font-weight:700;color:#f87171;line-height:1.2">{STUDENT['exam']['days_left']}
            <span style="font-size:12px;color:#8892a4">days left</span></div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TOPBAR
# ─────────────────────────────────────────────
today_str = datetime.now().strftime("%a, %b %d")
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            background:#141720;border:1px solid #2a2f3e;border-radius:12px;
            padding:12px 20px;margin-bottom:20px">
    <span style="font-size:18px;font-weight:700;color:#e2e8f0">SmartStudy AI</span>
    <div style="display:flex;gap:10px;align-items:center">
        <span class="streak-badge">🔥 {STUDENT['streak']} day streak</span>
        <span class="date-badge">{today_str}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════
if page == "📊 Overview":

    # ── AI Performance Score ──
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"""
        <div class="section-label">AI Performance Score</div>
        <div style="font-size:52px;font-weight:700;color:#e2e8f0;line-height:1">{STUDENT['ai_score']}</div>
        <div style="color:#4ade80;font-size:13px;font-weight:500;margin-top:6px">▲ +{STUDENT['score_delta']} from last week</div>
        """, unsafe_allow_html=True)
    with c2:
        fig = gauge_ring(74, "#00c9a7", size=120)
        fig.update_layout(
            annotations=[dict(
                text="<b>74%</b><br><span style='font-size:10px'>Overall</span>",
                x=0.5, y=0.5,
                font=dict(size=15, color="#e2e8f0"),
                showarrow=False,
            )]
        )
        st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Stat boxes ──
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🔥 Study Streak",    f"{STUDENT['streak']} days")
    m2.metric("✓  Tasks Today",     f"{STUDENT['tasks_today']}/{STUDENT['tasks_total']}")
    m3.metric("⏱  Hours This Week", f"{STUDENT['hours_week']} h")
    m4.metric("📅 Exam In",         f"{STUDENT['exam']['days_left']} days")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Subject mastery rings ──
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Subject Mastery</div>', unsafe_allow_html=True)
    cols = st.columns(len(SUBJECTS))
    for col, s in zip(cols, SUBJECTS):
        with col:
            fig = gauge_ring(s["pct"], s["color"], size=90)
            st.plotly_chart(fig, use_container_width=False, config={"displayModeBar": False})
            st.markdown(f'<div style="text-align:center;font-size:11px;color:#8892a4;margin-top:-8px">{s["name"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Weak Topic Alerts ──
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    hcol1, hcol2 = st.columns([3, 1])
    hcol1.markdown('<div class="section-label" style="margin-bottom:0">⚠ Weak Topic Alerts</div>', unsafe_allow_html=True)
    hcol2.markdown('<div style="text-align:right"><span style="background:#3d0f0f;color:#f87171;border:1px solid #f8717144;font-size:12px;font-weight:600;padding:4px 12px;border-radius:20px">3 Critical</span></div>', unsafe_allow_html=True)

    for w in WEAK_TOPICS[:3]:
        sc = score_color(w["score"])
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid #2a2f3e">
            {priority_badge_html(w['priority'])}
            <div style="flex:1">
                <div style="font-size:14px;font-weight:600;color:#e2e8f0">{w['name']}</div>
                <div style="font-size:12px;color:{w['dot']};margin-top:2px">⬤ {w['subject']}</div>
            </div>
            <div style="font-size:16px;font-weight:700;color:{sc}">{w['score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: WEAK TOPICS
# ═══════════════════════════════════════════════
elif page == "⚠️ Weak Topics":

    # Alert list
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    hcol1, hcol2 = st.columns([3, 1])
    hcol1.markdown('<div class="section-label" style="margin-bottom:0">⚠ Weak Topic Alerts</div>', unsafe_allow_html=True)
    hcol2.markdown('<div style="text-align:right"><span style="background:#3d0f0f;color:#f87171;border:1px solid #f8717144;font-size:12px;font-weight:600;padding:4px 12px;border-radius:20px">3 Critical</span></div>', unsafe_allow_html=True)

    for w in WEAK_TOPICS:
        sc = score_color(w["score"])
        bar_pct = w["score"]
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;padding:12px 0;border-bottom:1px solid #2a2f3e">
            {priority_badge_html(w['priority'])}
            <div style="flex:1">
                <div style="font-size:14px;font-weight:600;color:#e2e8f0">{w['name']}</div>
                <div style="font-size:11px;color:#8892a4;margin-top:2px">{w['reason']}</div>
                <div style="height:4px;background:#1f2435;border-radius:2px;margin-top:6px;overflow:hidden">
                    <div style="width:{bar_pct}%;height:4px;background:{sc};border-radius:2px"></div>
                </div>
            </div>
            <div style="font-size:18px;font-weight:700;color:{sc};min-width:42px;text-align:right">{w['score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Mastery vs quiz accuracy</div>', unsafe_allow_html=True)
        names = [w["name"] for w in WEAK_TOPICS]
        mastery  = [w["score"] for w in WEAK_TOPICS]
        accuracy = [w["score"] - 4 for w in WEAK_TOPICS]  # simulated
        fig = go.Figure()
        fig.add_bar(name="Mastery",       x=names, y=mastery,  marker_color="#a78bfa")
        fig.add_bar(name="Quiz Accuracy", x=names, y=accuracy, marker_color="#00c9a7")
        fig.update_layout(**PLOT_LAYOUT, barmode="group", height=260,
                          xaxis=dict(**GRID_STYLE, tickangle=-25),
                          yaxis=dict(**GRID_STYLE, range=[0, 100]))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Recommended actions</div>', unsafe_allow_html=True)
        actions = [
            ("#f87171", "Study Organic Reactions 45 min today. Focus on mechanism reactions — you've missed this 3×."),
            ("#fb923c", "Practice Calculus MCQs daily to build speed. Target: under 2 min/Q by next week."),
            ("#fbbf24", "Revise Matrix Algebra using flashcards — eigenvalues and determinants first."),
        ]
        for color, text in actions:
            st.markdown(f"""
            <div style="padding:10px;background:#1a1e2a;border-radius:10px;border-left:3px solid {color};
                        font-size:12px;color:#e2e8f0;line-height:1.6;margin-bottom:8px">{text}</div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: STUDY TASKS
# ═══════════════════════════════════════════════
elif page == "✅ Study Tasks":

    if "tasks" not in st.session_state:
        st.session_state.tasks = [t.copy() for t in TASKS]

    done_count = sum(1 for t in st.session_state.tasks if t["done"])
    total = len(st.session_state.tasks)
    progress = done_count / total

    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    hcol1, hcol2 = st.columns([3, 1])
    hcol1.markdown('<div class="section-label" style="margin-bottom:0">Today\'s Study Tasks</div>', unsafe_allow_html=True)
    hcol2.markdown(f'<div style="text-align:right;font-size:14px;font-weight:600;color:#00c9a7">{done_count}/{total} done</div>', unsafe_allow_html=True)

    st.progress(progress)

    for i, task in enumerate(st.session_state.tasks):
        c1, c2, c3, c4, c5 = st.columns([0.4, 0.7, 2.5, 1.2, 0.8])
        with c1:
            checked = st.checkbox("", value=task["done"], key=f"task_{i}", label_visibility="collapsed")
            st.session_state.tasks[i]["done"] = checked
        with c2:
            st.markdown(f'<div style="font-size:12px;color:#555f72;padding-top:6px">{task["time"]}</div>', unsafe_allow_html=True)
        with c3:
            name_style = "text-decoration:line-through;color:#555f72" if checked else "color:#e2e8f0"
            st.markdown(f"""
            <div style="{name_style};font-size:14px;font-weight:500;padding-top:4px">{task['name']}</div>
            <div style="font-size:11px;color:#8892a4">{task['meta']}</div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div style="padding-top:6px"><span class="tag {task["tag_class"]}">{task["tag"]}</span></div>', unsafe_allow_html=True)
        with c5:
            if not checked:
                if st.button("Start →", key=f"start_{i}"):
                    st.toast(f"Starting {task['name']}!", icon="📖")
        st.markdown('<hr style="border:none;border-top:1px solid #2a2f3e;margin:2px 0">', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Revision due today
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">↺ Revision Due Today</div>', unsafe_allow_html=True)
    for r in REVISIONS:
        rc = r["ret_color"]
        st.markdown(f"""
        <div class="rev-item">
            <div style="font-size:22px;width:38px;text-align:center">{r['icon']}</div>
            <div style="flex:1">
                <div style="font-size:13px;font-weight:600;color:#e2e8f0">{r['name']}</div>
                <div style="font-size:11px;color:#8892a4;margin-top:2px">{r['meta']}</div>
            </div>
            <div style="text-align:right">
                <div style="font-size:15px;font-weight:700;color:{rc}">{r['retention']}%</div>
                <div style="font-size:10px;color:#8892a4">retention</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: REVISION
# ═══════════════════════════════════════════════
elif page == "↺ Revision":

    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">↺ Spaced Repetition Queue</div>', unsafe_allow_html=True)

    for r in REVISIONS:
        rc = r["ret_color"]
        interval_color = "#f87171" if r["interval"] == "1-day" else "#fbbf24" if r["interval"] == "3-day" else "#4ade80"
        st.markdown(f"""
        <div class="rev-item">
            <div style="font-size:22px;width:38px;text-align:center">{r['icon']}</div>
            <div style="flex:1">
                <div style="font-size:13px;font-weight:600;color:#e2e8f0">{r['name']}</div>
                <div style="font-size:11px;color:#8892a4;margin-top:2px">{r['meta']}</div>
            </div>
            <div style="margin-right:12px">
                <span style="background:#1f2435;color:{interval_color};border:1px solid {interval_color}44;
                             font-size:10px;padding:3px 9px;border-radius:10px">{r['interval']}</span>
            </div>
            <div style="text-align:right">
                <div style="font-size:15px;font-weight:700;color:{rc}">{r['retention']}%</div>
                <div style="font-size:10px;color:#8892a4">retention</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Rules
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Spaced repetition rules</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #f87171"><div style="font-weight:600;color:#f87171;margin-bottom:4px;font-size:13px">Score &lt; 50 · 1-day</div><div style="font-size:12px;color:#8892a4">Very weak — daily reinforcement needed</div></div>', unsafe_allow_html=True)
    with r2:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #fbbf24"><div style="font-weight:600;color:#fbbf24;margin-bottom:4px;font-size:13px">Score 50–74 · 3-day</div><div style="font-size:12px;color:#8892a4">Medium — steady consolidation</div></div>', unsafe_allow_html=True)
    with r3:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #00c9a7"><div style="font-weight:600;color:#00c9a7;margin-bottom:4px;font-size:13px">Score 75+ · 7-day</div><div style="font-size:12px;color:#8892a4">Strong — long-term retention</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: PROGRESS
# ═══════════════════════════════════════════════
elif page == "📈 Progress":

    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Mastery gain (4 wks)", "+14%", delta="+14%")
    m2.metric("Study consistency",    "86%")
    m3.metric("Avg quiz accuracy",    "72%",  delta="-2%")
    m4.metric("Avg solve speed",      "2.1 min")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Mastery trend (4 weeks)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        trend = MASTERY_TREND
        fig.add_scatter(x=trend["weeks"], y=trend["overall"],     name="Overall",     line=dict(color="#00c9a7", width=2), fill="tozeroy", fillcolor="rgba(0,201,167,0.08)")
        fig.add_scatter(x=trend["weeks"], y=trend["chemistry"],   name="Chemistry",   line=dict(color="#f472b6", width=2))
        fig.add_scatter(x=trend["weeks"], y=trend["programming"], name="Programming", line=dict(color="#38bdf8", width=2))
        fig.add_scatter(x=trend["weeks"], y=trend["physics"],     name="Physics",     line=dict(color="#a78bfa", width=2))
        fig.update_layout(**PLOT_LAYOUT, height=250,
                          xaxis=dict(**GRID_STYLE),
                          yaxis=dict(**GRID_STYLE, range=[20, 100]))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Quiz accuracy by subject</div>', unsafe_allow_html=True)
        qa = QUIZ_ACCURACY
        fig = go.Figure(go.Bar(
            x=qa["accuracy"], y=qa["subjects"],
            orientation="h",
            marker_color=qa["colors"],
            text=[f"{v}%" for v in qa["accuracy"]],
            textposition="outside",
            textfont=dict(color="#8892a4", size=10),
        ))
        fig.update_layout(**PLOT_LAYOUT, height=250,
                          xaxis=dict(**GRID_STYLE, range=[0, 105]),
                          yaxis=dict(**GRID_STYLE))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Coach insights
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Coach insights</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    with i1:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #4ade80;font-size:12px;color:#e2e8f0;line-height:1.6;margin-bottom:10px"><strong style="color:#4ade80">Programming ↑ 88%</strong> — Best subject. Keep it maintained with weekly revision.</div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #fbbf24;font-size:12px;color:#e2e8f0;line-height:1.6"><strong style="color:#fbbf24">Physics at 71%</strong> — Good, but Newton\'s Laws needs revision — 14 days overdue.</div>', unsafe_allow_html=True)
    with i2:
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #4ade80;font-size:12px;color:#e2e8f0;line-height:1.6;margin-bottom:10px"><strong style="color:#4ade80">14-day streak</strong> — Excellent! You\'ve studied every single day this fortnight.</div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:12px;background:#1a1e2a;border-radius:10px;border-left:3px solid #f87171;font-size:12px;color:#e2e8f0;line-height:1.6"><strong style="color:#f87171">Chemistry critical (28%)</strong> — Organic Reactions needs urgent daily practice starting today.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PAGE: AI COACH
# ═══════════════════════════════════════════════
elif page == "🤖 AI Coach":

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "ai", "content": "Hi! I've analysed your data. Chemistry (28%) is your biggest risk right now. Organic Reactions needs daily attention. Want me to build a focused rescue plan?"}
        ]

    # Chat window
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">🟢 SmartStudy AI Coach · Online</div>', unsafe_allow_html=True)

    # Messages
    chat_html = '<div style="padding:14px;min-height:200px;max-height:400px;overflow-y:auto;display:flex;flex-direction:column;gap:8px">'
    for msg in st.session_state.messages:
        cls = "msg-ai" if msg["role"] == "ai" else "msg-user"
        content = msg["content"].replace("\n", "<br>")
        chat_html += f'<div class="{cls}" style="white-space:pre-line">{content}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick-ask buttons
    st.markdown("**Quick questions:**")
    qcols = st.columns(4)
    quick_qs = list(AI_RESPONSES.keys())
    for col, q in zip(qcols, quick_qs):
        with col:
            if st.button(q, key=f"quick_{q[:20]}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.messages.append({"role": "ai",   "content": AI_RESPONSES[q]})
                st.rerun()

    # Free input
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        fc1, fc2 = st.columns([5, 1])
        with fc1:
            user_input = st.text_input("Ask your AI coach...", placeholder="e.g. Why is Chemistry weak?", label_visibility="collapsed")
        with fc2:
            submitted = st.form_submit_button("Send →", use_container_width=True)

    if submitted and user_input.strip():
        reply = AI_RESPONSES.get(
            user_input.strip(),
            "Based on your performance data: Chemistry needs the most attention (28% mastery). "
            "Your Programming skills are strong at 88%. Shall I create a balanced revision schedule?"
        )
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        st.session_state.messages.append({"role": "ai",   "content": reply})
        st.rerun()

    if st.button("🗑 Clear chat"):
        st.session_state.messages = [
            {"role": "ai", "content": "Hi! I'm your SmartStudy AI Coach. Ask me anything about your study plan, weak topics, or progress!"}
        ]
        st.rerun()
