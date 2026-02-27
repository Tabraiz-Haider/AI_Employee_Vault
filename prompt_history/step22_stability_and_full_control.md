# Step 22: Stability & Full Control

**Date:** 2026-02-26
**Type:** Stability Fix + Control Center Hardening

## Problem
Streamlit tab was crashing or closing when background scripts ran or when cleanup happened. The root cause: child processes shared handles with the Streamlit parent process, so crashes propagated upward.

## Fixes Applied

### 1. Isolated Subprocess Execution (`app.py`)
- Added `_CREATE_NEW_CONSOLE = 0x00000010` Windows flag constant
- Added `_safe_popen()` helper that wraps `subprocess.Popen` with:
  - `creationflags=CREATE_NEW_CONSOLE` on Windows — child process gets its own console, cannot crash parent
  - `close_fds=True` — no shared file descriptor inheritance
  - `start_new_session=True` on Linux/Mac — separate process group
- All watcher launches now go through `_safe_popen()`
- All `subprocess.run()` calls in Quick Actions (audit, sync, LinkedIn, WhatsApp) now pass `creationflags` on Windows

### 2. Odoo Mock Bridge Inline (`app.py`)
- Added `_mock_accounting()` function with full realistic PKR data:
  - 4 invoices (2 paid, 1 overdue, 1 pending)
  - 5 expense categories
  - Bank balance, fiscal month, company name
- `load_accounting()` now always returns data — real JSON if it exists and is valid, mock otherwise
- Removed fragile `if accounting:` guard — financial metrics always render
- Added data-source badge below financial row: green "Live JSON" or orange "Mock Data"
- Fixed expense chart guard: `if accounting and expenses:` → `if expenses:`

### 3. Safety Guard in vault_sync.py
- Added `PROTECTED_FILES` set listing all runtime scripts (app.py, watchers, agents, posters)
- `push()` now uses `git add -- . :!app.py :!vault_sync.py ...` to skip protected files
- `pull()` now prints a guard notice listing protected files before fetching
- Result: clicking "Sync Vault" can never overwrite the running app.py

## Files Modified
- `app.py` — subprocess isolation, mock data fallback, safety fixes
- `vault_sync.py` — PROTECTED_FILES guard, selective staging
- `prompt_history/step22_stability_and_full_control.md` — this file
