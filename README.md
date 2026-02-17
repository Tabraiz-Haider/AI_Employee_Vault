# AI Employee Vault

**Owner:** Tabraiz Haider
**Project:** GIAIC Hackathon 0 — Personal AI Employee
**Architecture:** Local-First, Agent-Driven, Human-in-the-Loop

---

## Overview

The AI Employee Vault is an autonomous personal assistant system that monitors Gmail, social media, desktop files, and accounting data — then reasons about priorities, generates tasks, drafts content, and presents everything in a real-time dashboard.

Built with Claude Code as the brain, Obsidian as the knowledge base, and Python watchers as the senses.

---

## Vault Structure

```
AI_Employee_Vault/
├── Needs_Action/          # Tasks awaiting pickup (Cloud Agent writes here)
│   └── Social/            # Business inquiries from Facebook/Instagram
├── In_Progress/           # Tasks claimed by Local Agent (move to claim)
├── Pending_Approval/      # Completed tasks awaiting human review
├── Done/                  # Archived completed tasks
├── Readings/              # Email summaries, social reports, accounting audits
├── Plans/                 # AI-generated execution plans for HIGH priority items
├── Drafts/                # LinkedIn post drafts and content
├── watchers/              # Python watcher scripts (Gmail, Desktop)
├── prompt_history/        # Step-by-step documentation of every feature
├── .streamlit/            # Dashboard theme configuration
├── app.py                 # Streamlit CEO Dashboard
├── agent_brain.py         # Autonomous task generator
├── linkedin_agent.py      # LinkedIn post draft generator
├── social_media_agent.py  # Facebook/Instagram scanner
├── odoo_mcp_bridge.py     # Accounting agent (Odoo JSON-RPC ready)
├── vault_sync.py          # Git-based cloud-local sync
└── CEO_Briefing_Feb_17.md # Auto-generated Monday morning briefing
```

---

## Cloud-Local Delegation Model

The Platinum Tier introduces a two-agent architecture where a Cloud Agent and a Local Agent collaborate through the shared vault via Git.

### How It Works

```
┌─────────────────────┐         Git Push/Pull        ┌─────────────────────┐
│    CLOUD AGENT       │ ◄──────────────────────────► │    LOCAL AGENT       │
│    (Always-on VM)    │                              │    (Your machine)    │
│                      │                              │                      │
│  - Gmail Bridge      │                              │  - Streamlit Dashboard│
│  - Social Media Agent│                              │  - Desktop Watcher   │
│  - Odoo MCP Bridge   │                              │  - Human Review      │
│  - Agent Brain       │                              │  - Task Execution    │
│                      │                              │                      │
│  Writes to:          │                              │  Moves tasks:        │
│  /Needs_Action       │                              │  /Needs_Action       │
│  /Readings           │                              │    → /In_Progress    │
│  /Plans              │                              │    → /Pending_Approval│
│                      │                              │    → /Done           │
└─────────────────────┘                              └─────────────────────┘
```

### Claim-by-Move Workflow

Tasks flow through the vault using the file system as a Kanban board:

1. **Cloud Agent** detects a high-priority email or social inquiry
2. **Cloud Agent** creates a task file in `/Needs_Action`
3. **Cloud Agent** pushes changes via `vault_sync.py`
4. **Local Agent** pulls updates and sees new tasks in the dashboard
5. **Human/Local Agent** moves a task to `/In_Progress` (claims it)
6. After completion, moves to `/Pending_Approval`
7. After review, moves to `/Done`

### Security Rules

- `credentials.json`, `token.json`, `.env` — **NEVER** synced (in `.gitignore`)
- OAuth tokens stay on the machine that created them
- API keys are local-only; each agent authenticates independently
- No secrets cross the Git boundary

---

## Agents

| Agent | Script | Function | Loop Interval |
|-------|--------|----------|---------------|
| Gmail Bridge | `watchers/gmail_bridge.py` | Fetch unread emails → `Readings/` | 2 min |
| Desktop Watcher | `watchers/desktop_watcher.py` | Monitor desktop files → `Desktop_Log.md` | 5 sec |
| Agent Brain | `agent_brain.py` | Detect HIGH priority → `Needs_Action/` + `Plans/` | 5 min |
| LinkedIn Agent | `linkedin_agent.py` | Draft posts → `Drafts/` | On demand |
| Social Media Agent | `social_media_agent.py` | Scan FB/IG → `Readings/` + `Needs_Action/Social/` | 5 min |
| Odoo MCP Bridge | `odoo_mcp_bridge.py` | Accounting audit → `Readings/` + overdue tasks | 10 min |
| Vault Sync | `vault_sync.py` | Git push/pull for cloud-local delegation | On demand |

---

## Dashboard

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` — auto-refreshes every 30 seconds.

Features: KPI metrics, Plotly charts (pie, bar, horizontal), priority-coded inbox table, AI task cards with purple tags, CEO briefing expander, AI recommendations.

---

## Vault Sync Commands

```bash
python vault_sync.py              # Full sync (pull + push)
python vault_sync.py status       # Show git status and remote
python vault_sync.py pull         # Pull latest from remote
python vault_sync.py push         # Commit and push all changes
python vault_sync.py push "msg"   # Push with custom commit message
python vault_sync.py init         # Initialize structure and first commit
```

---

## Setup

### Prerequisites
- Python 3.13+
- Git
- Obsidian (optional, for vault browsing)

### Install Dependencies
```bash
pip install streamlit pandas plotly streamlit-autorefresh
pip install google-auth google-auth-oauthlib google-api-python-client
```

### First Run
```bash
python vault_sync.py init
streamlit run app.py
```

---

## Documentation

Every feature is documented step-by-step in `prompt_history/`:

| File | Step |
|------|------|
| `step0_bronze_tier.md` | Vault setup, Desktop Watcher |
| `step1_silver_tier_gmail.md` | Gmail API, OAuth, email summaries |
| `step2_gold_tier_dashboard.md` | Streamlit dashboard, Plotly charts |
| `step4_agent_brain.md` | Autonomous HIGH priority task generator |
| `step6_silver_completion.md` | LinkedIn Agent, execution plans |
| `step7_platinum_vault_setup.md` | Claim-by-move workflow directories |
| `step8_social_media_integration.md` | Facebook/Instagram agent |
| `step9_odoo_accounting_setup.md` | Odoo bridge, accounting audit |
| `step10_platinum_sync_setup.md` | Git sync, cloud-local delegation |

---

## License

Private — GIAIC Hackathon Project

---

> Built by Tabraiz Haider | AI Employee Vault | Powered by Claude Code
