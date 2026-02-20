import streamlit as st
import pandas as pd
import plotly.express as px
import json
import re
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Tabraiz Haider | CEO Command",
    page_icon="briefcase",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# AUTO-REFRESH every 30 seconds
# ──────────────────────────────────────────────
st_autorefresh(interval=30000, key="datarefresh")

# ──────────────────────────────────────────────
# CLEAN CSS — Professional SaaS Theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Base ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    div.block-container {
        padding-top: 1rem;
        max-width: 1200px;
    }

    /* ── Sticky Header ── */
    .sticky-header {
        position: sticky;
        top: 0; z-index: 999;
        background: #0D1117;
        padding: 12px 0;
        border-bottom: 1px solid #1C2028;
        margin: -1rem -1rem 0 -1rem;
        padding-left: 1rem; padding-right: 1rem;
    }
    .sticky-header h1 {
        margin: 0; padding: 0;
        font-size: 1.1rem; font-weight: 600;
        color: #E6EDF3;
        letter-spacing: -0.01em;
    }
    .sticky-header .subtitle {
        color: #6E7681; font-size: 0.72rem;
        margin-top: 1px; letter-spacing: 0.02em;
    }

    /* ── Metric cards — slim ── */
    div[data-testid="stMetric"] {
        background: transparent;
        border: 1px solid #1C2028;
        border-radius: 8px;
        padding: 14px 16px;
    }
    div[data-testid="stMetric"] label {
        color: #6E7681 !important;
        font-size: 0.68rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        color: #E6EDF3 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        font-size: 0.65rem !important;
    }

    /* ── Sidebar — minimal ── */
    section[data-testid="stSidebar"] {
        background: #0D1117 !important;
        border-right: 1px solid #1C2028;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    .sb-name {
        font-size: 0.92rem; font-weight: 600; color: #E6EDF3;
        letter-spacing: -0.01em;
    }
    .sb-role {
        font-size: 0.65rem; color: #6E7681; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.08em;
        margin-top: 1px;
    }
    .sb-divider {
        border: none; height: 1px; background: #1C2028; margin: 14px 0;
    }
    .sb-label {
        color: #6E7681; font-size: 0.65rem; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.08em;
        margin-bottom: 2px;
    }
    .sb-value {
        color: #C9D1D9; font-size: 0.82rem; font-weight: 500;
    }
    .sb-badge {
        display: inline-block; font-size: 0.6rem; font-weight: 600;
        padding: 2px 8px; border-radius: 10px;
        letter-spacing: 0.04em;
    }
    .sb-badge-live { background: #1B3D2F; color: #3FB950; }
    .sb-badge-on   { background: #1C1D3E; color: #A78BFA; }
    .sb-badge-off  { background: #161B22; color: #6E7681; }
    .sb-footer {
        color: #484F58; font-size: 0.62rem; text-align: center; margin-top: 8px;
    }

    /* ── Section headers — understated ── */
    .section-header {
        font-size: 0.78rem; font-weight: 600; color: #8B949E;
        text-transform: uppercase; letter-spacing: 0.06em;
        margin: 32px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #1C2028;
    }

    /* ── Unified card style ── */
    .card {
        background: #0D1117;
        border: 1px solid #1C2028;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }
    .card-title {
        color: #E6EDF3; font-weight: 500; font-size: 0.84rem;
        line-height: 1.35;
    }
    .card-meta {
        color: #6E7681; font-size: 0.7rem; margin-top: 3px;
    }
    .card-body {
        color: #8B949E; font-size: 0.76rem; margin-top: 6px;
        line-height: 1.45;
    }

    /* ── Tags — subtle ── */
    .tag {
        display: inline-block;
        font-size: 0.58rem; font-weight: 600;
        padding: 1px 6px; border-radius: 3px;
        letter-spacing: 0.04em; margin-right: 6px;
        vertical-align: middle;
    }
    .tag-ai     { background: #1C1D3E; color: #A78BFA; }
    .tag-social { background: #0C2D48; color: #58A6FF; }
    .tag-finance{ background: #2D2306; color: #E3B341; }
    .tag-plan   { background: #1C1D3E; color: #A78BFA; }

    /* ── Priority badges ── */
    .pri {
        display: inline-block; font-size: 0.58rem; font-weight: 600;
        padding: 1px 6px; border-radius: 3px;
        letter-spacing: 0.04em; margin-right: 6px;
        vertical-align: middle;
    }
    .pri-high   { background: #3D1518; color: #F85149; }
    .pri-medium { background: #2D2306; color: #E3B341; }
    .pri-low    { background: #1B3D2F; color: #3FB950; }

    /* ── Kanban ── */
    .kanban-col-header {
        font-size: 0.68rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.06em;
        padding: 8px 12px;
        border: 1px solid #1C2028;
        border-radius: 8px 8px 0 0;
        background: #0D1117;
    }
    .kanban-col-header .dot {
        display: inline-block; width: 8px; height: 8px;
        border-radius: 50%; margin-right: 6px;
        vertical-align: middle;
    }
    .dot-todo  { background: #D29922; }
    .dot-doing { background: #58A6FF; }
    .dot-done  { background: #3FB950; }
    .kanban-col-header .count {
        color: #6E7681; font-weight: 500; margin-left: 4px;
    }
    .kanban-body {
        border: 1px solid #1C2028;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 10px; min-height: 180px;
        background: transparent;
    }
    .kanban-card {
        background: #0D1117;
        border: 1px solid #1C2028;
        border-radius: 6px;
        padding: 10px 12px;
        margin-bottom: 8px;
    }
    .kanban-card-title {
        color: #C9D1D9; font-weight: 500; font-size: 0.78rem;
    }
    .kanban-card-meta {
        color: #484F58; font-size: 0.65rem; margin-top: 3px;
    }

    /* ── Financial row ── */
    .fin-row {
        display: flex; gap: 16px; flex-wrap: wrap;
        margin-bottom: 8px;
    }
    .fin-item {
        flex: 1; min-width: 120px;
        border: 1px solid #1C2028; border-radius: 8px;
        padding: 12px 14px;
        background: transparent;
    }
    .fin-value {
        font-size: 1.1rem; font-weight: 600; color: #E6EDF3;
    }
    .fin-value.green { color: #3FB950; }
    .fin-value.amber { color: #E3B341; }
    .fin-value.blue  { color: #58A6FF; }
    .fin-label {
        color: #6E7681; font-size: 0.62rem; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.05em;
        margin-top: 2px;
    }

    /* ── Plan steps ── */
    .plan-step {
        color: #8B949E; font-size: 0.76rem; margin-left: 8px;
        line-height: 1.5;
    }

    /* ── Charts ── */
    .js-plotly-plot { border-radius: 8px; }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        font-weight: 600 !important; color: #C9D1D9 !important;
        font-size: 0.82rem !important;
    }

    /* ── Footer ── */
    .footer-text {
        text-align: center; color: #484F58; font-size: 0.65rem;
        margin-top: 48px; padding: 14px 0;
        border-top: 1px solid #1C2028;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
READINGS_DIR = BASE_DIR / "Readings"
BRIEFING_FILE = BASE_DIR / "CEO_Briefing_Feb_17.md"
ACCOUNTING_FILE = BASE_DIR / "accounting_status.json"
NEEDS_ACTION_DIR = BASE_DIR / "Needs_Action"
IN_PROGRESS_DIR = BASE_DIR / "In_Progress"
DONE_DIR = BASE_DIR / "Done"
PLANS_DIR = BASE_DIR / "Plans"
DRAFTS_DIR = BASE_DIR / "Drafts"
COMMANDS_DIR = BASE_DIR / "Commands"

COMMANDS_DIR.mkdir(exist_ok=True)


def load_briefing():
    if BRIEFING_FILE.exists():
        return BRIEFING_FILE.read_text(encoding="utf-8")
    return ""


def load_accounting():
    if ACCOUNTING_FILE.exists():
        with open(ACCOUNTING_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


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


def load_kanban_files(directory):
    items = []
    if not directory.exists():
        return items
    for f in sorted(directory.glob("*.md")):
        if f.name == ".gitkeep":
            continue
        text = f.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s*(.+)", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f.stem
        tag = ""
        if f.name.startswith("AI_TASK"):
            tag = "ai"
        elif f.name.startswith("SOCIAL_TASK"):
            tag = "social"
        elif f.name.startswith("ACCT_TASK"):
            tag = "finance"
        items.append({"title": title, "file": f.name, "tag": tag})
    for sub in directory.iterdir():
        if sub.is_dir():
            for f in sorted(sub.glob("*.md")):
                if f.name == ".gitkeep":
                    continue
                text = f.read_text(encoding="utf-8")
                title_match = re.search(r"^#\s*(.+)", text, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else f.stem
                tag = "social" if f.name.startswith("SOCIAL") else ""
                items.append({"title": title, "file": f"{sub.name}/{f.name}", "tag": tag})
    return items


def load_plans():
    plans = []
    if not PLANS_DIR.exists():
        return plans
    for f in sorted(PLANS_DIR.glob("PLAN_*.md")):
        text = f.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s*Execution Plan:\s*(.+)", text, re.MULTILINE)
        sender_match = re.search(r"\*\*Sender:\*\*\s*(.+)", text)
        status_match = re.search(r"\*\*Status:\*\*\s*(.+)", text)
        steps = re.findall(r"^\d+\.\s*(.+)", text, re.MULTILINE)
        plans.append({
            "title": title_match.group(1).strip() if title_match else f.stem,
            "sender": sender_match.group(1).strip() if sender_match else "",
            "status": status_match.group(1).strip() if status_match else "Not Started",
            "steps": steps[:5],
            "file": f.name,
        })
    return plans


def load_social_summary():
    path = READINGS_DIR / "Social_Summary.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def fmt_pkr(amount):
    return f"PKR {amount:,.0f}"


# ── Load all data ──
briefing_raw = load_briefing()
accounting = load_accounting()
df_emails = load_emails()
df_inbox = parse_inbox_intelligence(briefing_raw)

kanban_todo = load_kanban_files(NEEDS_ACTION_DIR)
kanban_doing = load_kanban_files(IN_PROGRESS_DIR)
kanban_done = load_kanban_files(DONE_DIR)
plans = load_plans()
social_summary = load_social_summary()

total_emails = len(df_emails)
unread_count = (df_emails["Status"].str.lower() == "unread").sum() if not df_emails.empty else 0
high_priority = (df_inbox["Priority"] == "HIGH").sum() if not df_inbox.empty else 0

if accounting:
    invoices = accounting.get("invoices", [])
    expenses = accounting.get("expenses", [])
    total_invoiced = sum(i["amount"] for i in invoices)
    collected = sum(i["amount"] for i in invoices if i["status"] == "paid")
    total_expenses = sum(e["amount"] for e in expenses)
    net_profit = collected - total_expenses
    bank_balance = accounting.get("bank_balance", {}).get("balance", 0)
    overdue_count = sum(1 for i in invoices if i["status"] == "overdue")
    outstanding = sum(i["amount"] for i in invoices if i["status"] in ("pending", "overdue"))
else:
    total_invoiced = collected = total_expenses = net_profit = bank_balance = 0
    overdue_count = 0
    outstanding = 0
    invoices = []
    expenses = []

# ──────────────────────────────────────────────
# SIDEBAR — Minimalist
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sb-name">Tabraiz Haider</p>', unsafe_allow_html=True)
    st.markdown('<p class="sb-role">CEO Command</p>', unsafe_allow_html=True)
    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

    st.markdown('<p class="sb-label">Status</p>', unsafe_allow_html=True)
    st.markdown(
        f'<span class="sb-badge sb-badge-live">LIVE</span> &nbsp; '
        f'<span class="sb-value" style="font-size:0.72rem;">{datetime.now().strftime("%b %d, %Y")}</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)

    # Auto-Pilot hidden under expander
    with st.expander("Agent Settings"):
        autopilot = st.toggle("Autonomous Posting Mode", value=False, key="autopilot_toggle")
        if autopilot:
            st.markdown('<span class="sb-badge sb-badge-on">AUTO-PILOT ON</span>', unsafe_allow_html=True)
            st.caption("LinkedIn Agent runs every 24h")
            if "autopilot_started" not in st.session_state:
                st.session_state["autopilot_started"] = True
                st.session_state["autopilot_last_run"] = None

                def autopilot_loop():
                    while True:
                        try:
                            subprocess.run(
                                ["python", str(BASE_DIR / "linkedin_agent.py"), "--both"],
                                cwd=str(BASE_DIR), timeout=120,
                            )
                            st.session_state["autopilot_last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        except Exception:
                            pass
                        time.sleep(86400)

                t = threading.Thread(target=autopilot_loop, daemon=True)
                t.start()
            if st.session_state.get("autopilot_last_run"):
                st.caption(f"Last run: {st.session_state['autopilot_last_run']}")
        else:
            st.markdown('<span class="sb-badge sb-badge-off">OFF</span>', unsafe_allow_html=True)
            if "autopilot_started" in st.session_state:
                del st.session_state["autopilot_started"]

        st.markdown("---")

        if st.button("Execute All Approved", key="execute_approved_btn"):
            with st.spinner("Running LinkedIn poster and WhatsApp sender..."):
                errors = []
                # Run LinkedIn poster
                try:
                    lp_result = subprocess.run(
                        ["python", str(BASE_DIR / "linkedin_poster.py")],
                        cwd=str(BASE_DIR), timeout=120,
                        capture_output=True, text=True,
                    )
                    if lp_result.returncode == 0:
                        st.success("LinkedIn: Post submitted")
                    else:
                        errors.append(f"LinkedIn: {lp_result.stderr or lp_result.stdout or 'Unknown error'}")
                except subprocess.TimeoutExpired:
                    errors.append("LinkedIn: Timed out after 120s")
                except Exception as e:
                    errors.append(f"LinkedIn: {e}")

                # Run WhatsApp sender
                try:
                    wa_result = subprocess.run(
                        ["python", str(BASE_DIR / "whatsapp_sender.py")],
                        cwd=str(BASE_DIR), timeout=120,
                        capture_output=True, text=True,
                    )
                    if wa_result.returncode == 0:
                        st.success("WhatsApp: Messages sent")
                    else:
                        errors.append(f"WhatsApp: {wa_result.stderr or wa_result.stdout or 'Unknown error'}")
                except subprocess.TimeoutExpired:
                    errors.append("WhatsApp: Timed out after 120s")
                except Exception as e:
                    errors.append(f"WhatsApp: {e}")

                for err in errors:
                    st.error(err)

    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
    st.markdown(
        f'<p class="sb-footer">Auto-refresh 30s &middot; {datetime.now().strftime("%H:%M:%S")}</p>',
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────
# STICKY HEADER — Thin, clean
# ──────────────────────────────────────────────
st.markdown(
    f"""<div class="sticky-header">
        <h1>Tabraiz Haider &nbsp;|&nbsp; CEO Command</h1>
        <div class="subtitle">{datetime.now().strftime('%A, %B %d, %Y')} &middot; AI Employee Vault</div>
    </div>""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# FINANCIAL ROW — Slim cards
# ──────────────────────────────────────────────
profit_class = "green" if net_profit > 0 else "amber"
st.markdown(f"""
<div class="fin-row">
    <div class="fin-item">
        <div class="fin-value {profit_class}">{fmt_pkr(net_profit)}</div>
        <div class="fin-label">Net Profit</div>
    </div>
    <div class="fin-item">
        <div class="fin-value amber">{fmt_pkr(outstanding)}</div>
        <div class="fin-label">Outstanding</div>
    </div>
    <div class="fin-item">
        <div class="fin-value blue">{fmt_pkr(bank_balance)}</div>
        <div class="fin-label">Bank Balance</div>
    </div>
    <div class="fin-item">
        <div class="fin-value">{fmt_pkr(collected)}</div>
        <div class="fin-label">Collected</div>
    </div>
    <div class="fin-item">
        <div class="fin-value">{fmt_pkr(total_expenses)}</div>
        <div class="fin-label">Expenses</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# OPERATIONAL METRICS
# ──────────────────────────────────────────────
o1, o2, o3, o4, o5 = st.columns(5)
o1.metric("Emails", total_emails)
o2.metric("Unread", unread_count)
o3.metric("High Priority", high_priority,
          delta="Attention" if high_priority > 0 else "Clear",
          delta_color="inverse" if high_priority > 0 else "normal")
o4.metric("To Do", len(kanban_todo))
o5.metric("In Progress", len(kanban_doing))

# ──────────────────────────────────────────────
# KANBAN BOARD
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">Task Board</div>', unsafe_allow_html=True)

col_todo, col_doing, col_done = st.columns(3)

TAG_HTML = {
    "ai": '<span class="tag tag-ai">AI</span>',
    "social": '<span class="tag tag-social">SOCIAL</span>',
    "finance": '<span class="tag tag-finance">FINANCE</span>',
}


def render_kanban(col, dot_class, label, count, items):
    with col:
        st.markdown(
            f'<div class="kanban-col-header">'
            f'<span class="dot {dot_class}"></span>{label}'
            f'<span class="count">{count}</span></div>',
            unsafe_allow_html=True,
        )
        html = ""
        if items:
            for item in items:
                tag = TAG_HTML.get(item["tag"], "")
                html += (
                    f'<div class="kanban-card">'
                    f'<div class="kanban-card-title">{tag}{item["title"]}</div>'
                    f'<div class="kanban-card-meta">{item["file"]}</div>'
                    f'</div>'
                )
        else:
            html = '<p style="color:#484F58; font-size:0.75rem; text-align:center; padding:24px 0;">No items</p>'
        st.markdown(f'<div class="kanban-body">{html}</div>', unsafe_allow_html=True)


render_kanban(col_todo, "dot-todo", "Needs Action", len(kanban_todo), kanban_todo)
render_kanban(col_doing, "dot-doing", "In Progress", len(kanban_doing), kanban_doing)
render_kanban(col_done, "dot-done", "Done", len(kanban_done), kanban_done)

# ──────────────────────────────────────────────
# UNIFIED COMMUNICATION HUB
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">Communications</div>', unsafe_allow_html=True)

hub_left, hub_right = st.columns(2)

with hub_left:
    st.markdown("**Inbox**")
    if not df_inbox.empty:
        for _, row in df_inbox.iterrows():
            p = row["Priority"]
            p_class = {"HIGH": "pri-high", "MEDIUM": "pri-medium", "LOW": "pri-low"}.get(p, "pri-low")
            st.markdown(
                f'<div class="card">'
                f'<div><span class="pri {p_class}">{p}</span>'
                f'<span class="card-meta">{row["Sender"]}</span></div>'
                f'<div class="card-title">{row["Subject"]}</div>'
                f'<div class="card-body">{row["Action Required"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No inbox data.")

with hub_right:
    st.markdown("**Social**")
    if social_summary:
        msg_match = re.search(r"Total Messages \| (\d+)", social_summary)
        biz_match = re.search(r"Business Inquiries \| (\d+)", social_summary)
        notif_match = re.search(r"Notifications \| (\d+)", social_summary)
        st.markdown(
            f'<div class="card">'
            f'<div class="card-title"><span class="tag tag-social">SOCIAL</span>Activity Overview</div>'
            f'<div class="card-body">'
            f'Messages: <strong style="color:#C9D1D9;">{msg_match.group(1) if msg_match else "0"}</strong> &middot; '
            f'Inquiries: <strong style="color:#C9D1D9;">{biz_match.group(1) if biz_match else "0"}</strong> &middot; '
            f'Alerts: <strong style="color:#C9D1D9;">{notif_match.group(1) if notif_match else "0"}</strong>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        with st.expander("Full Social Summary"):
            st.markdown(social_summary)
    else:
        st.info("No social data yet.")

# ──────────────────────────────────────────────
# LINKEDIN POST STATUS
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">LinkedIn Post Status</div>', unsafe_allow_html=True)
if DRAFTS_DIR.exists():
    draft_files = sorted(DRAFTS_DIR.glob("LinkedIn_Post*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    if draft_files:
        rows = []
        for f in draft_files:
            text = f.read_text(encoding="utf-8")
            brand_m = re.search(r"\*\*Brand:\*\*\s*(.+)", text)
            gen_m = re.search(r"\*\*Generated:\*\*\s*(.+)", text)
            stat_m = re.search(r"\*\*Status:\*\*\s*(.+)", text)
            rows.append({
                "Brand": brand_m.group(1).strip() if brand_m else "—",
                "Generated": gen_m.group(1).strip() if gen_m else "—",
                "Status": stat_m.group(1).strip() if stat_m else "—",
                "File": f.name,
            })
        df_posts = pd.DataFrame(rows)
        posted = len(df_posts[df_posts["Status"] == "Posted"])
        drafts = len(df_posts[df_posts["Status"] == "Draft"])
        st.markdown(
            f'<div class="card"><div class="card-body">'
            f'Total: <strong style="color:#C9D1D9;">{len(df_posts)}</strong> &middot; '
            f'Posted: <strong style="color:#3FB950;">{posted}</strong> &middot; '
            f'Drafts: <strong style="color:#58A6FF;">{drafts}</strong>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        with st.expander("All LinkedIn Drafts"):
            st.dataframe(df_posts, use_container_width=True, hide_index=True)
    else:
        st.info("No LinkedIn drafts found.")
else:
    st.info("Drafts folder not found.")

# ──────────────────────────────────────────────
# CHARTS
# ──────────────────────────────────────────────
chart_left, chart_right = st.columns(2)

with chart_left:
    st.markdown('<div class="section-header">Email Distribution</div>', unsafe_allow_html=True)
    if not df_inbox.empty:
        sender_counts = df_inbox["Sender"].value_counts().reset_index()
        sender_counts.columns = ["Sender", "Count"]
        fig_pie = px.pie(
            sender_counts, names="Sender", values="Count", hole=0.5,
            color_discrete_sequence=["#6E7681", "#8B949E", "#A78BFA", "#58A6FF", "#3FB950"],
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#8B949E", font_size=11,
            legend=dict(font=dict(size=10)),
            margin=dict(t=10, b=10, l=10, r=10), height=300,
        )
        fig_pie.update_traces(
            textinfo="label+percent", textfont_size=10,
            marker=dict(line=dict(color="#0D1117", width=1.5)),
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No email data.")

with chart_right:
    st.markdown('<div class="section-header">Expense Breakdown</div>', unsafe_allow_html=True)
    if accounting and expenses:
        by_cat = {}
        for e in expenses:
            by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["amount"]
        cat_df = pd.DataFrame(list(by_cat.items()), columns=["Category", "Amount"])
        cat_df = cat_df.sort_values("Amount", ascending=True)
        fig_exp = px.bar(
            cat_df, x="Amount", y="Category", orientation="h", text="Amount",
            color_discrete_sequence=["#8B949E"],
        )
        fig_exp.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#8B949E", font_size=11, showlegend=False,
            xaxis=dict(showgrid=True, gridcolor="#1C2028"),
            yaxis=dict(showgrid=False),
            margin=dict(t=10, b=10, l=10, r=10), height=300,
        )
        fig_exp.update_traces(
            texttemplate="PKR %{x:,.0f}", textposition="outside",
            marker_line_color="#0D1117", marker_line_width=1,
        )
        st.plotly_chart(fig_exp, use_container_width=True)
    else:
        st.info("No accounting data.")

# ──────────────────────────────────────────────
# AI STRATEGY
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">AI Strategy</div>', unsafe_allow_html=True)
if plans:
    for p in plans:
        steps_html = "".join(f'<div class="plan-step">{i+1}. {s}</div>' for i, s in enumerate(p["steps"]))
        st.markdown(
            f'<div class="card">'
            f'<div class="card-title"><span class="tag tag-plan">PLAN</span>{p["title"]}</div>'
            f'<div class="card-meta">{p["sender"]} &middot; {p["status"]} &middot; {p["file"]}</div>'
            f'<div style="margin-top:6px;">{steps_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
else:
    st.info("No execution plans. Run agent_brain.py to generate.")

# ──────────────────────────────────────────────
# ODOO QUICK COMMAND
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">Odoo Command</div>', unsafe_allow_html=True)
cmd_left, cmd_right = st.columns([5, 1])
with cmd_left:
    odoo_cmd = st.text_input(
        "Command Odoo Agent",
        placeholder="e.g. Generate invoice for CloudNeurix — PKR 150,000",
        key="odoo_command_input",
        label_visibility="collapsed",
    )
with cmd_right:
    send = st.button("Send", key="odoo_cmd_btn", use_container_width=True)
if send:
    if odoo_cmd.strip():
        cmd_file = COMMANDS_DIR / "odoo_cmd.md"
        cmd_content = (
            f"# Odoo Command\n\n"
            f"**Sent:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"**From:** CEO Dashboard\n\n"
            f"## Command\n\n{odoo_cmd.strip()}\n\n"
            f"---\n*Status: Pending*\n"
        )
        cmd_file.write_text(cmd_content, encoding="utf-8")
        st.success("Command saved.")
    else:
        st.warning("Enter a command first.")

# ──────────────────────────────────────────────
# CEO BRIEFING & AI RECOMMENDATION
# ──────────────────────────────────────────────
st.markdown('<div class="section-header">Briefing</div>', unsafe_allow_html=True)
with st.expander("CEO Briefing — February 17, 2026"):
    st.markdown(briefing_raw)

rec_match = re.search(r"## AI Recommendation\n\n(.+?)(?:\n---|\Z)", briefing_raw, re.DOTALL)
if rec_match:
    st.info(rec_match.group(1).strip())

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown(
    '<p class="footer-text">'
    'Tabraiz Haider &middot; CEO Command &middot; AI Employee Vault &middot; GIAIC Hackathon 0'
    '</p>',
    unsafe_allow_html=True,
)
