# SpecKit — whatsapp_sender.py
# Step 0.0 Foundation Spec
# Generated: 2026-02-28

[meta]
file    = whatsapp_sender.py
version = 1.0
scope   = browser_automation

# ── HARD CONSTRAINTS ────────────────────────────────────────────────────────

[rule: WA-001]
name     = minimum_send_timeout
severity = CRITICAL
desc     = WhatsApp Web navigation timeout must be >= 300000 ms (5 minutes).
           Shorter timeouts cause failures on slow networks or session restores.
check    = file contains "timeout=300000" OR timeout value >= 300000
current  = page.goto timeout=120000, login wait=300000
status   = PARTIAL — goto uses 120s, login flow uses 300s. Raise goto to 300s.

[rule: WA-002]
name     = approved_dir_source
severity = CRITICAL
desc     = Must read messages exclusively from APPROVED_DIR (Approved/).
           Never read directly from Drafts/ or hardcoded paths.
check    = APPROVED_DIR defined and used in main loop
current  = PASS

[rule: WA-003]
name     = done_dir_archive
severity = HIGH
desc     = Successfully sent messages must be moved to DONE_DIR (Done/).
           Files must not remain in Approved/ after sending.
check    = shutil.move(... DONE_DIR ...) called after successful send
current  = PASS

[rule: WA-004]
name     = playwright_persistent_profile
severity = HIGH
desc     = Must use launch_persistent_context with a dedicated profile dir.
           Ephemeral contexts require QR scan on every run.
check    = launch_persistent_context called with user_data_dir
current  = PASS

[rule: WA-005]
name     = contact_search_retry
severity = MEDIUM
desc     = Navigation to WhatsApp Web must include retry logic (>= 2 attempts).
check    = retry loop with attempt counter exists
current  = PASS — 3 attempts implemented

[rule: WA-006]
name     = no_shell_true
severity = CRITICAL
desc     = subprocess calls must NOT use shell=True (security + path injection risk).
check    = no subprocess.run(..., shell=True) in file
current  = PASS — no subprocess.run calls

# ── BEHAVIOURAL CONTRACTS ────────────────────────────────────────────────────

[contract: WA-C1]
name   = parse_message_file
desc   = parse_message_file(filepath) must return (contact, message) tuple.
         Returns (None, None) if **To:** field is missing.
inputs = filepath: Path to a .md file in Approved/
outputs= (str | None, str | None)

[contract: WA-C2]
name   = send_whatsapp
desc   = send_whatsapp(contact, message) returns bool.
         True = sent successfully. False = any failure (log reason).
inputs = contact: str, message: str
outputs= bool
