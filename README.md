# 🤖 AI Employee Vault

> **A fully autonomous AI-powered business operations system** — built for Tabraiz Haider, CEO of Multicraft Agency.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-45ba4b?style=flat-square)](https://playwright.dev)
[![License](https://img.shields.io/badge/License-Private-red?style=flat-square)]()

---

## 🏆 System Score: 10 / 10 — Production Ready

The AI Employee Vault is a personal AI operations platform that replaces manual business workflows with autonomous agents. It reads emails, generates LinkedIn content, sends WhatsApp messages, tracks accounting, and gives the CEO full control — all from a single dark-themed dashboard.

---

## ✨ Features

### 🖥️ CEO Command Dashboard (`app.py`)
- **Real-time financial metrics** — net profit, collected, expenses, bank balance (PKR)
- **Odoo accounting bridge** — live JSON + inline mock fallback (always shows data)
- **Kanban task board** — Needs Action / In Progress / Done
- **Agent console** — live tail of `logs/agent_activity.log`
- **Auto-refresh** every 30 seconds

### 📝 AI Post Creator
- Type a 1-line prompt → instant professional LinkedIn post
- Brand selector: **Multicraft Agency** or **Lyvexa AI**
- Live preview & edit in dashboard (`st.text_area`)
- **Publish Now** button — saves, approves, and triggers poster in one click
- Fully isolated subprocess (never freezes the dashboard)

### 📱 Communication Hub
| Channel | Features |
|---|---|
| 📧 Email Inbox | Priority-tagged cards (HIGH / MEDIUM / LOW) |
| 💬 WhatsApp | Task scanner, AI Quick Reply composer, Run Sender button |
| 📊 Social | Activity overview from social_media_agent |
| 💼 LinkedIn | Channel status card, approved post count, Run Poster button |

### 📁 Draft Management
- Lists all drafts with brand, date, and status badges
- **Edit** → in-dashboard text editor
- **Save & Approve** → moves file from `Drafts/` to `Approved/`
- **Cancel** → non-destructive exit
- Approved drafts summary expander

### ⚙️ Background Watchers (Sidebar)
Start/Stop individual agents directly from the dashboard:
- Gmail Bridge
- Desktop Watcher
- Agent Brain
- Social Media Agent
- Odoo Bridge

### 🚀 Quick Actions (Sidebar)
- **Execute All Approved** — LinkedIn + WhatsApp in one click
- **Run Full Audit** — Odoo bridge with live `st.status` steps
- **System Health Check** — scripts, watchers, git status
- **Sync Vault** — git push via `vault_sync.py`
- **Autopilot Toggle** — autonomous 24h LinkedIn posting (single thread, no spam)

---

## 🗂️ Vault Architecture

```
AI_Employee_Vault/
│
├── app.py                    # CEO Dashboard (Streamlit)
├── agent_brain.py            # AI task dispatcher
├── linkedin_agent.py         # LinkedIn post generator
├── linkedin_poster.py        # Playwright browser automation
├── whatsapp_sender.py        # WhatsApp Web automation
├── social_media_agent.py     # Social monitoring
├── odoo_mcp_bridge.py        # Accounting / Odoo bridge
├── vault_sync.py             # Git-based cloud sync (with safety guard)
│
├── watchers/
│   ├── gmail_bridge.py       # Gmail IMAP reader
│   └── desktop_watcher.py    # Local file watcher
│
├── Needs_Action/             # 📥 Incoming tasks
├── In_Progress/              # 🔄 Active work
├── Approved/                 # ✅ CEO-approved, ready to execute
├── Done/                     # 📦 Completed & archived
├── Drafts/                   # 📝 AI-generated content drafts
├── Readings/                 # 📧 Parsed emails & social summaries
├── Plans/                    # 🧠 AI execution plans
├── Commands/                 # 💬 CEO Odoo commands
├── logs/                     # 📋 Agent activity log
└── prompt_history/           # 🗒️ Development changelog
```

---

## 🔄 Automation Pipelines

### LinkedIn Pipeline
```
linkedin_agent.py → Drafts/ → [CEO reviews in Dashboard] → Approved/ → linkedin_poster.py → Done/
```

### WhatsApp Pipeline
```
CEO types reply in Dashboard → Approved/WA_Reply_*.md → whatsapp_sender.py → Done/
```

### Email Pipeline
```
Gmail → watchers/gmail_bridge.py → Readings/EMAIL_*.md → agent_brain.py → Needs_Action/
```

### Accounting Pipeline
```
accounting_status.json → odoo_mcp_bridge.py → Readings/Accounting_Audit.md → Dashboard
```

---

## 🛡️ Stability Features

| Feature | Description |
|---|---|
| `CREATE_NEW_CONSOLE` | Child processes isolated — crashes never propagate to dashboard |
| `PROTECTED_FILES` | `vault_sync.py` never overwrites `app.py` or runtime scripts |
| Mock Odoo fallback | Financial metrics always render, even without live JSON |
| Single autopilot thread | Toggle-on spawns exactly one background thread, 24h delay |
| `close_fds=True` | No file handle inheritance between parent and child processes |

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install streamlit streamlit-autorefresh plotly pandas playwright
playwright install chromium
```

### 2. Run the dashboard
```bash
streamlit run app.py
```

Open **http://localhost:8501**

### 3. First-time LinkedIn login
```bash
python linkedin_poster.py --login
```

### 4. Configure Gmail (optional)
Add credentials to `watchers/credentials.json` and `watchers/token.json`.

---

## 📊 Live Financial Snapshot

| Metric | Value |
|---|---|
| Net Profit | PKR 435,500 |
| Collected | PKR 570,000 |
| Total Expenses | PKR 134,500 |
| Bank Balance | PKR 612,000 |
| Overdue Invoices | 1 |

---

## 🏗️ Built With

- **[Streamlit](https://streamlit.io)** — Dashboard UI
- **[Playwright](https://playwright.dev/python/)** — Browser automation (LinkedIn, WhatsApp Web)
- **[Plotly](https://plotly.com/python/)** — Financial charts
- **[Claude AI](https://anthropic.com)** — AI content generation backbone
- **Python 3.11+** — Core runtime

---

## 👤 Author

**Tabraiz Haider**
CEO — Multicraft Agency & Lyvexa AI
GIAIC Hackathon 0

---

*Built with the AI Employee Vault framework — where every agent is a digital FTE.*
