import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from pathlib import Path
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Tabraiz Haider | AI Command Center",
    page_icon="briefcase",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# AUTO-REFRESH every 30 seconds
# ──────────────────────────────────────────────
st_autorefresh(interval=30000, key="datarefresh")

# ──────────────────────────────────────────────
# CUSTOM CSS — premium dark theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Fix header cut-off ── */
    div.block-container { padding-top: 2rem; }

    /* ── Metric cards ── */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #161B22 0%, #1C2333 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 4px 24px rgba(0,0,0,.35);
    }
    div[data-testid="stMetric"] label {
        color: #8B949E !important;
        font-size: 0.82rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #E6EDF3 !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1117 0%, #161B22 100%) !important;
        border-right: 1px solid #21262D;
    }
    .brand-title {
        font-size: 1.65rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6C63FF, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    .brand-sub {
        font-size: 0.78rem;
        color: #58A6FF;
        font-weight: 600;
        letter-spacing: 0.08em;
    }
    .sidebar-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #30363D, transparent);
        margin: 16px 0;
    }
    .sidebar-label {
        color: #8B949E;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 4px;
    }
    .sidebar-value {
        color: #C9D1D9;
        font-size: 0.92rem;
        font-weight: 500;
    }
    .sidebar-status {
        display: inline-block;
        background: #238636;
        color: #fff;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        letter-spacing: 0.06em;
    }

    /* ── Section headers ── */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #E6EDF3;
        border-left: 3px solid #6C63FF;
        padding-left: 12px;
        margin: 28px 0 14px 0;
    }

    /* ── Dataframe ── */
    .stDataFrame { border-radius: 10px; overflow: hidden; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-weight: 700 !important;
        font-size: 1rem !important;
        color: #C9D1D9 !important;
    }

    /* ── Plotly ── */
    .js-plotly-plot { border-radius: 12px; }

    /* ── AI Task badge ── */
    .ai-tag {
        display: inline-block;
        background: linear-gradient(135deg, #6C63FF, #A78BFA);
        color: #fff;
        font-size: 0.65rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.08em;
        margin-right: 8px;
        vertical-align: middle;
    }
    .ai-task-card {
        background: linear-gradient(135deg, #1C1636 0%, #161B22 100%);
        border: 1px solid #6C63FF33;
        border-left: 3px solid #6C63FF;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .ai-task-title {
        color: #E6EDF3;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .ai-task-meta {
        color: #8B949E;
        font-size: 0.78rem;
        margin-top: 4px;
    }
    .ai-task-action {
        color: #A78BFA;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 6px;
    }

    /* ── Footer ── */
    .footer-text {
        text-align: center;
        color: #484F58;
        font-size: 0.72rem;
        margin-top: 40px;
        padding: 12px 0;
        border-top: 1px solid #21262D;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATA LOADING — robust paths via Path(__file__)
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
READINGS_DIR = BASE_DIR / "Readings"
BRIEFING_FILE = BASE_DIR / "CEO_Briefing_Feb_17.md"
TASKS_DIR = BASE_DIR / "Needs_Action"


def load_briefing():
    if BRIEFING_FILE.exists():
        return BRIEFING_FILE.read_text(encoding="utf-8")
    return ""


def parse_email_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    subject = re.search(r"^#\s*Email:\s*(.+)", text, re.MULTILINE)
    sender = re.search(r"\*\*From:\*\*\s*(.+)", text)
    date = re.search(r"\*\*Date:\*\*\s*(.+)", text)
    status = re.search(r"\*\*Status:\*\*\s*(.+)", text)
    summary = re.search(r"## Summary\n(.+)", text)
    return {
        "Subject": subject.group(1).strip() if subject else filepath.stem,
        "From": sender.group(1).strip() if sender else "Unknown",
        "Date": date.group(1).strip() if date else "",
        "Status": status.group(1).strip() if status else "Unknown",
        "Summary": summary.group(1).strip()[:120] + "..." if summary else "",
    }


def load_emails():
    emails = []
    if READINGS_DIR.exists():
        for f in sorted(READINGS_DIR.glob("EMAIL_*.md")):
            emails.append(parse_email_file(f))
    return pd.DataFrame(emails)


def parse_inbox_intelligence(briefing_text):
    rows = []
    pattern = r"\|\s*\*\*(\w+)\*\*\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|"
    for m in re.finditer(pattern, briefing_text):
        rows.append({
            "Priority": m.group(1),
            "Sender": m.group(2).strip(),
            "Subject": m.group(3).strip(),
            "Action Required": m.group(4).strip(),
        })
    return pd.DataFrame(rows)


def parse_tasks(briefing_text):
    tasks = []
    for m in re.finditer(r"- \[([ xX])\]\s*(.+)", briefing_text):
        done = m.group(1).lower() == "x"
        tasks.append({"Task": m.group(2).strip(), "Status": "Done" if done else "Pending"})
    return pd.DataFrame(tasks)


def load_ai_tasks():
    """Load AI-generated task files from Needs_Action/AI_TASK_*.md."""
    tasks = []
    if not TASKS_DIR.exists():
        return tasks
    for f in sorted(TASKS_DIR.glob("AI_TASK_*.md")):
        text = f.read_text(encoding="utf-8")
        title = re.search(r"^#\s*AI Task:\s*(.+)", text, re.MULTILINE)
        sender = re.search(r"\*\*Sender:\*\*\s*(.+)", text)
        detected = re.search(r"\*\*Detected:\*\*\s*(.+)", text)
        status = re.search(r"\*\*Status:\*\*\s*(.+)", text)
        action_line = re.search(r"Suggested action:\s*(.+)", text)
        tasks.append({
            "title": title.group(1).strip() if title else f.stem,
            "sender": sender.group(1).strip() if sender else "Unknown",
            "detected": detected.group(1).strip() if detected else "",
            "status": status.group(1).strip() if status else "Pending",
            "action": action_line.group(1).strip() if action_line else "",
            "file": f.name,
        })
    return tasks


# Load all data
briefing_raw = load_briefing()
df_emails = load_emails()
df_inbox = parse_inbox_intelligence(briefing_raw)
df_tasks = parse_tasks(briefing_raw)

ai_tasks = load_ai_tasks()

total_emails = len(df_emails)
unread_count = (df_emails["Status"].str.lower() == "unread").sum() if not df_emails.empty else 0
high_priority = (df_inbox["Priority"] == "HIGH").sum() if not df_inbox.empty else 0
pending_tasks = (df_tasks["Status"] == "Pending").sum() if not df_tasks.empty else 0
ai_task_count = len(ai_tasks)

# ──────────────────────────────────────────────
# SIDEBAR — minimalist personal branding
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="brand-title">Tabraiz Haider</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-sub">AI Command Center</p>', unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-label">Report Date</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="sidebar-value">{datetime.now().strftime("%B %d, %Y")}</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-label">System Status</p>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-status">LIVE</span>', unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    st.markdown(
        '<p style="color:#484F58; font-size:0.68rem; text-align:center;">'
        f'Auto-refreshes every 30s<br>Last: {datetime.now().strftime("%H:%M:%S")}</p>',
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.markdown(
    '<p class="brand-title" style="font-size:2rem; margin-bottom:0;">AI Command Center</p>',
    unsafe_allow_html=True,
)
st.caption(f"Personal Intelligence Dashboard  |  {datetime.now().strftime('%A, %B %d, %Y')}  |  AI Employee Vault")

# ──────────────────────────────────────────────
# KPI METRICS ROW
# ──────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Emails", total_emails)
k2.metric("Unread Emails", unread_count)
k3.metric("High Priority", high_priority, delta="Needs Attention", delta_color="inverse")
k4.metric("Pending Tasks", pending_tasks)
k5.metric("AI Tasks", ai_task_count, delta="Auto-Generated", delta_color="off")

st.markdown("")

# ──────────────────────────────────────────────
# CHARTS ROW
# ──────────────────────────────────────────────
chart_left, chart_right = st.columns(2)

with chart_left:
    st.markdown('<p class="section-header">Email Distribution by Sender</p>', unsafe_allow_html=True)
    if not df_inbox.empty:
        sender_counts = df_inbox["Sender"].value_counts().reset_index()
        sender_counts.columns = ["Sender", "Count"]
        fig_pie = px.pie(
            sender_counts,
            names="Sender",
            values="Count",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Purples_r,
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#C9D1D9",
            legend=dict(font=dict(size=11)),
            margin=dict(t=20, b=20, l=20, r=20),
            height=360,
        )
        fig_pie.update_traces(
            textinfo="label+percent",
            textfont_size=11,
            marker=dict(line=dict(color="#0E1117", width=2)),
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No email data to chart.")

with chart_right:
    st.markdown('<p class="section-header">Task Status Breakdown</p>', unsafe_allow_html=True)
    if not df_tasks.empty:
        status_counts = df_tasks["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        color_map = {"Pending": "#D29922", "Done": "#238636"}
        fig_bar = px.bar(
            status_counts,
            x="Status",
            y="Count",
            color="Status",
            color_discrete_map=color_map,
            text="Count",
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#C9D1D9",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#21262D"),
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=360,
        )
        fig_bar.update_traces(
            textposition="outside",
            marker_line_color="#0E1117",
            marker_line_width=1.5,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No task data to chart.")

# ──────────────────────────────────────────────
# PRIORITY DISTRIBUTION — horizontal bar
# ──────────────────────────────────────────────
st.markdown('<p class="section-header">Priority Distribution</p>', unsafe_allow_html=True)
if not df_inbox.empty:
    priority_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    priority_colors = {"HIGH": "#DA3633", "MEDIUM": "#D29922", "LOW": "#238636"}
    prio_counts = df_inbox["Priority"].value_counts().reset_index()
    prio_counts.columns = ["Priority", "Count"]
    prio_counts["sort"] = prio_counts["Priority"].map(priority_order)
    prio_counts = prio_counts.sort_values("sort")

    fig_prio = go.Figure()
    for _, row in prio_counts.iterrows():
        fig_prio.add_trace(go.Bar(
            y=[row["Priority"]],
            x=[row["Count"]],
            orientation="h",
            marker_color=priority_colors.get(row["Priority"], "#6C63FF"),
            text=str(row["Count"]),
            textposition="auto",
            name=row["Priority"],
        ))
    fig_prio.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#C9D1D9",
        xaxis=dict(showgrid=True, gridcolor="#21262D", title="Count"),
        yaxis=dict(showgrid=False),
        showlegend=False,
        margin=dict(t=10, b=40, l=10, r=10),
        height=200,
        bargap=0.35,
    )
    st.plotly_chart(fig_prio, use_container_width=True)

# ──────────────────────────────────────────────
# INBOX INTELLIGENCE TABLE
# ──────────────────────────────────────────────
st.markdown('<p class="section-header">Inbox Intelligence</p>', unsafe_allow_html=True)

if not df_inbox.empty:
    def color_priority(val):
        colors = {"HIGH": "#DA3633", "MEDIUM": "#D29922", "LOW": "#238636"}
        c = colors.get(val, "#6C63FF")
        return f"background-color: {c}; color: #fff; font-weight: 700; border-radius: 4px; text-align: center;"

    styled = df_inbox.style.applymap(color_priority, subset=["Priority"])
    st.dataframe(
        styled,
        use_container_width=True,
        height=min(45 * len(df_inbox) + 50, 450),
        column_config={
            "Priority": st.column_config.TextColumn("Priority", width="small"),
            "Sender": st.column_config.TextColumn("Sender", width="medium"),
            "Subject": st.column_config.TextColumn("Subject", width="large"),
            "Action Required": st.column_config.TextColumn("Action", width="large"),
        },
    )
else:
    st.info("No inbox intelligence data found.")

# ──────────────────────────────────────────────
# EMAIL DETAILS TABLE
# ──────────────────────────────────────────────
st.markdown('<p class="section-header">Email Details (Readings/)</p>', unsafe_allow_html=True)

if not df_emails.empty:
    st.dataframe(
        df_emails,
        use_container_width=True,
        height=min(45 * len(df_emails) + 50, 500),
        column_config={
            "Subject": st.column_config.TextColumn("Subject", width="large"),
            "From": st.column_config.TextColumn("From", width="medium"),
            "Date": st.column_config.TextColumn("Date", width="small"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Summary": st.column_config.TextColumn("Summary", width="large"),
        },
    )
else:
    st.info("No emails found in Readings/ folder.")

# ──────────────────────────────────────────────
# DESKTOP TASKS
# ──────────────────────────────────────────────
st.markdown('<p class="section-header">Desktop & Local Tasks</p>', unsafe_allow_html=True)
if not df_tasks.empty:
    for _, row in df_tasks.iterrows():
        icon = "white_check_mark" if row["Status"] == "Done" else "hourglass_flowing_sand"
        st.markdown(f":{icon}: &nbsp; {row['Task']}")
else:
    st.info("No tasks found.")

# ──────────────────────────────────────────────
# AI-GENERATED TASKS (from agent_brain.py)
# ──────────────────────────────────────────────
st.markdown('<p class="section-header">AI-Generated Tasks</p>', unsafe_allow_html=True)
if ai_tasks:
    for t in ai_tasks:
        st.markdown(f"""
        <div class="ai-task-card">
            <div>
                <span class="ai-tag">AI</span>
                <span class="ai-task-title">{t['title']}</span>
            </div>
            <div class="ai-task-meta">
                Sender: {t['sender']} &nbsp;&middot;&nbsp;
                Detected: {t['detected']} &nbsp;&middot;&nbsp;
                Status: {t['status']}
            </div>
            <div class="ai-task-action">{t['action']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No AI-generated tasks yet. Run agent_brain.py to scan for high-priority items.")

# ──────────────────────────────────────────────
# CEO BRIEFING — FULL TEXT
# ──────────────────────────────────────────────
st.markdown('<p class="section-header">Full CEO Briefing</p>', unsafe_allow_html=True)
with st.expander("View CEO Briefing  —  February 17, 2026", expanded=False):
    st.markdown(briefing_raw)

# ──────────────────────────────────────────────
# AI RECOMMENDATION
# ──────────────────────────────────────────────
rec_match = re.search(r"## AI Recommendation\n\n(.+?)(?:\n---|\Z)", briefing_raw, re.DOTALL)
if rec_match:
    st.markdown('<p class="section-header">AI Recommendation</p>', unsafe_allow_html=True)
    st.info(rec_match.group(1).strip())

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown(
    '<p class="footer-text">'
    'Tabraiz Haider &nbsp;&bull;&nbsp; AI Command Center &nbsp;&bull;&nbsp; AI Employee Vault &nbsp;&bull;&nbsp; '
    'Auto-generated from Gmail Bridge &amp; Desktop Watcher'
    '</p>',
    unsafe_allow_html=True,
)
