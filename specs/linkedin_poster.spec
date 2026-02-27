# SpecKit — linkedin_poster.py
# Step 0.0 Foundation Spec
# Generated: 2026-02-28

[meta]
file    = linkedin_poster.py
version = 1.0
scope   = browser_automation

# ── HARD CONSTRAINTS ────────────────────────────────────────────────────────

[rule: LI-001]
name     = approved_dir_first
severity = CRITICAL
desc     = find_latest_draft() must scan APPROVED_DIR before DRAFTS_DIR.
           CEO-approved files take precedence over raw drafts.
check    = APPROVED_DIR.glob(...) checked before DRAFTS_DIR.glob(...)
current  = PASS

[rule: LI-002]
name     = done_dir_after_post
severity = CRITICAL
desc     = After a successful post, the file must be moved to DONE_DIR.
           Files must not remain in Approved/ after being posted.
check    = shutil.move(filepath, DONE_DIR / filepath.name) called in mark_as_posted()
current  = PASS

[rule: LI-003]
name     = status_regex_update
severity = HIGH
desc     = mark_as_posted() must use re.sub to update **Status:** regardless of
           current value (Draft, Approved, or anything else).
           Simple str.replace("Draft", "Posted") is insufficient.
check    = re.sub(r"\*\*Status:\*\*\s*\S+", "**Status:** Posted", ...) used
current  = PASS

[rule: LI-004]
name     = minimum_strategies
severity = HIGH
desc     = At least 4 strategies must be implemented for clicking "Start a post".
           JS click strategy must be included (most resilient to DOM changes).
check    = len(start_post_strategies) >= 4
           page.evaluate("...best.click()...") present in strategies
current  = PASS — 6 strategies, JS click is Strategy 3

[rule: LI-005]
name     = js_click_strategy_position
severity = MEDIUM
desc     = JavaScript innermost-click strategy must be attempted within the first 3
           strategies (not as last resort). It is the most reliable on 2026 LinkedIn.
check    = JS evaluate click appears at index <= 2 in start_post_strategies list
current  = PASS — Strategy 3 (index 2)

[rule: LI-006]
name     = modal_verification
severity = HIGH
desc     = After each click strategy, code must wait and verify the modal opened
           before declaring success. Must try next strategy if modal not detected.
check    = page.locator("div[role='dialog']...").wait_for() after each strategy
current  = PASS

[rule: LI-007]
name     = skip_already_posted
severity = HIGH
desc     = find_latest_draft() must skip files with **Status:** Posted.
           Re-posting already-posted content is a critical failure.
check    = "Posted" status filter applied before returning file
current  = PASS

[rule: LI-008]
name     = no_shell_true
severity = CRITICAL
desc     = No subprocess call may use shell=True.
check    = no subprocess.run/Popen with shell=True
current  = PASS

# ── BEHAVIOURAL CONTRACTS ────────────────────────────────────────────────────

[contract: LI-C1]
name   = find_latest_draft
desc   = Returns Path to most recent unposted draft. Prefers Approved/, falls back
         to Drafts/. Returns None if nothing found.
outputs= Path | None

[contract: LI-C2]
name   = mark_as_posted
desc   = Updates **Status:** to Posted using regex, appends timestamp,
         moves file to DONE_DIR. Side effect: file no longer exists at original path.
inputs = filepath: Path

[contract: LI-C3]
name   = post_to_linkedin
desc   = Returns bool. True = post submitted. False = any failure.
         Must not raise exceptions (catch all, log, return False).
inputs = content: str
outputs= bool
