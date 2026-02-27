# SpecKit — app.py (CEO Dashboard)
# Step 0.0 Foundation Spec
# Generated: 2026-02-28

[meta]
file    = app.py
version = 1.0
scope   = streamlit_dashboard

# ── HARD CONSTRAINTS ────────────────────────────────────────────────────────

[rule: DASH-001]
name     = isolated_subprocess
severity = CRITICAL
desc     = ALL subprocess calls that launch external scripts MUST use _safe_run()
           or _safe_popen(). Direct subprocess.run() with capture_output=True and
           creationflags is FORBIDDEN (causes WinError 87 on Windows).
check    = no subprocess.run(...creationflags..., capture_output=True) in file
current  = PASS — _safe_run() and _safe_popen() used throughout

[rule: DASH-002]
name     = create_new_console_flag
severity = CRITICAL
desc     = On Windows, child processes must use CREATE_NEW_CONSOLE (0x00000010)
           so crashes in child processes cannot propagate to the Streamlit tab.
check    = _CREATE_NEW_CONSOLE = 0x00000010 defined and used in _safe_run/_safe_popen
current  = PASS

[rule: DASH-009]
name     = sys_executable_not_python_string
severity = CRITICAL
desc     = All subprocess/Popen calls MUST use sys.executable (_PY) as the interpreter,
           never the bare string "python". Bare "python" can resolve to the wrong
           interpreter or fail entirely if Python is not on PATH (common in venv/conda).
           Define _PY = sys.executable at module level and use it everywhere.
check    = no ["python", ...] lists in subprocess calls — all use _PY variable
current  = PASS — _PY = sys.executable defined; all 9 call sites updated

[rule: DASH-010]
name     = safe_popen_devnull_only_on_windows
severity = CRITICAL
desc     = _safe_popen() on Windows MUST route stdout/stderr to DEVNULL only.
           Passing an open file handle with CREATE_NEW_CONSOLE triggers WinError 87
           (invalid parameter — inherited handles incompatible with new console).
           Callers that want logging must write their own log file inside the child process.
check    = _safe_popen Windows branch uses subprocess.DEVNULL for stdout and stderr
current  = PASS — fixed in Step 0.0 revision

[rule: DASH-003]
name     = mock_accounting_fallback
severity = HIGH
desc     = load_accounting() must ALWAYS return data. If accounting_status.json
           is missing or invalid, _mock_accounting() must be used as fallback.
           The dashboard must never show zero financial metrics due to missing JSON.
check    = load_accounting() returns _mock_accounting() on any exception or missing file
current  = PASS

[rule: DASH-004]
name     = single_autopilot_thread
severity = HIGH
desc     = The autopilot background thread must only be spawned once per session.
           Must check thread.is_alive() before spawning a new one.
           Thread must sleep BEFORE first run (no immediate execution on toggle).
check    = session_state["autopilot_thread"].is_alive() guard present
           time.sleep(86400) is FIRST statement in autopilot_loop
current  = PASS

[rule: DASH-005]
name     = protected_files_no_overwrite
severity = CRITICAL
desc     = vault_sync.py must never overwrite app.py or other runtime scripts.
           PROTECTED_FILES set must be defined in vault_sync.py.
check    = PROTECTED_FILES defined in vault_sync.py
           git add uses pathspec exclusions for protected files
current  = PASS

[rule: DASH-006]
name     = autorefresh_interval
severity = MEDIUM
desc     = st_autorefresh interval must be >= 30000 ms (30 seconds).
           Shorter intervals cause excessive CPU usage and session resets.
check    = st_autorefresh(interval=...) >= 30000
current  = PASS — 30000ms

[rule: DASH-007]
name     = draft_editor_state
severity = MEDIUM
desc     = Draft editing state must be tracked in st.session_state["editing_draft"].
           Editing must be non-destructive until Save is explicitly clicked.
check    = session_state["editing_draft"] used as editing gate
current  = PASS

[rule: DASH-008]
name     = no_shell_true
severity = CRITICAL
desc     = No subprocess call may use shell=True (path injection / security risk).
check    = no subprocess calls with shell=True
current  = PASS

# ── BEHAVIOURAL CONTRACTS ────────────────────────────────────────────────────

[contract: DASH-C1]
name   = _safe_run
desc   = _safe_run(cmd, cwd, timeout) -> (returncode: int, output: str)
         Must use temp file for output capture on Windows (never PIPE + creationflags).
         Must delete temp file in finally block.
inputs = cmd: list[str], cwd: str | None, timeout: int
outputs= (int, str)

[contract: DASH-C2]
name   = _safe_popen
desc   = _safe_popen(cmd, cwd, stdout, stderr, detach) -> Popen
         Fire-and-forget launcher. No output capture.
         Must use CREATE_NEW_CONSOLE on Windows.
inputs = cmd: list[str]
outputs= subprocess.Popen

[contract: DASH-C3]
name   = load_accounting
desc   = Always returns a dict with keys: invoices, expenses, bank_balance.
         Never returns None.
outputs= dict
