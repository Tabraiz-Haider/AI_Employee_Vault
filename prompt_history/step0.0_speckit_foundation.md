# Step 0.0: SpecKit Foundation

**Date:** 2026-02-28
**Type:** Project Specification Layer — Foundation
**Logical Position:** Start of all steps (precedes Step 1)

## Purpose

SpecKit is the formal specification and validation layer for the AI Employee Vault.
It defines hard constraints, behavioural contracts, and automated checks that ensure
the codebase remains stable, secure, and consistent as new features are added.

---

## Files Created

### `/specs/app.spec`
Specification for `app.py` (CEO Dashboard).
- **8 rules**, 5 CRITICAL
- Key constraints: `_safe_run()` for all subprocesses, `CREATE_NEW_CONSOLE` flag,
  mock accounting fallback, single autopilot thread, PROTECTED_FILES guard

### `/specs/whatsapp_sender.spec`
Specification for `whatsapp_sender.py`.
- **6 rules**, 3 CRITICAL
- Key constraint: **minimum 300,000ms (5 minute) timeout** for any WhatsApp operation
- Contracts: `parse_message_file()`, `send_whatsapp()` return types defined

### `/specs/linkedin_poster.spec`
Specification for `linkedin_poster.py`.
- **8 rules**, 4 CRITICAL
- Key constraints: APPROVED_DIR scanned before DRAFTS_DIR, files moved to DONE_DIR
  after posting, JS click strategy must be in top 3 positions, modal verification required

### `validate_specs.py`
Automated validation script. Checks all CRITICAL and HIGH rules against live code.
```bash
python validate_specs.py
```
- Exit code `0` = all CRITICAL rules pass
- Exit code `1` = one or more CRITICAL rules fail
- Colour-coded output: GREEN=PASS, RED=FAIL, YELLOW=WARN

---

## Hard-Coded Constraints Summary

| Rule | File | Constraint |
|---|---|---|
| WA-001 | whatsapp_sender.py | Minimum 300,000ms (5 min) timeout |
| DASH-001 | app.py | `_safe_run()` — no capture_output+creationflags |
| DASH-002 | app.py | `CREATE_NEW_CONSOLE = 0x00000010` |
| DASH-005 | vault_sync.py | PROTECTED_FILES prevents overwriting app.py |
| LI-001 | linkedin_poster.py | APPROVED_DIR scanned before DRAFTS_DIR |
| LI-002 | linkedin_poster.py | Sent files moved to DONE_DIR |
| LI-005 | linkedin_poster.py | JS click in Strategy 1–3 |

---

## Validation Results (Step 0.0)

All CRITICAL rules: **PASS** ✅
- DASH-001: No WinError 87 risk — `_safe_run()` used throughout
- DASH-002: CREATE_NEW_CONSOLE defined
- DASH-005: PROTECTED_FILES guard in vault_sync.py
- WA-001: 300,000ms timeout present in login flow
- LI-001: APPROVED_DIR first
- LI-002: DONE_DIR archive on post

One advisory note (non-breaking):
- WA-001 PARTIAL: `goto()` timeout is 120,000ms. Login flow timeout is 300,000ms.
  Consider raising `goto()` to 300,000ms for maximum resilience.

---

## How to Use SpecKit

### Run validation before any commit
```bash
python validate_specs.py
```

### Add a new rule
Edit the relevant `.spec` file in `/specs/` and add a corresponding check
in `validate_specs.py`.

### Spec file format
```
[rule: RULE-ID]
name     = rule_name
severity = CRITICAL | HIGH | MEDIUM
desc     = What this rule enforces and why.
check    = How to verify compliance (human-readable)
current  = PASS | FAIL | PARTIAL — current status
```

---

## Logical Step Order

This step is **Step 0.0** — it logically precedes all other steps because:
1. It codifies the constraints that all subsequent steps must respect
2. It provides a regression check (`validate_specs.py`) that catches regressions
3. It documents the "why" behind key implementation decisions

```
Step 0.0  SpecKit Foundation          ← YOU ARE HERE
Step 0    Bronze Tier (initial setup)
Step 1    Silver Tier (Gmail)
Step 2    Gold Tier (Dashboard)
...
Step 22   Stability & Full Control
Step 24   Perfect Score Certification
```
