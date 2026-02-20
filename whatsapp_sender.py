"""
WhatsApp Sender — Browser Automation
Reads approved .md files from Approved/ and sends WhatsApp messages via WhatsApp Web.
"""

import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout
except ImportError:
    print("[ERROR] playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# ──────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
APPROVED_DIR = BASE_DIR / "Approved"
DONE_DIR = BASE_DIR / "Done"
PROFILE_DIR = BASE_DIR / ".playwright_profile"

APPROVED_DIR.mkdir(exist_ok=True)
DONE_DIR.mkdir(exist_ok=True)
PROFILE_DIR.mkdir(exist_ok=True)


# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def close_chrome():
    """Kill any running Chrome instances to avoid profile lock conflicts."""
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["taskkill", "/F", "/IM", "chrome.exe"],
                capture_output=True, text=True,
            )
            if result.returncode == 0:
                print("[INFO] Chrome is running — closing it to avoid profile conflicts...")
        else:
            subprocess.run(["pkill", "-f", "chrome"], capture_output=True)
    except Exception:
        pass


def get_browser_context(playwright):
    """Launch persistent Chromium context with saved profile."""
    return playwright.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
        channel="chrome",
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
        ],
        viewport={"width": 1280, "height": 900},
        ignore_default_args=["--enable-automation"],
    )


def parse_message_file(filepath):
    """Extract To and Message from an approved .md file."""
    text = filepath.read_text(encoding="utf-8")
    to_match = re.search(r"\*\*To:\*\*\s*(.+)", text)
    msg_match = re.search(r"## Message\s*\n+([\s\S]+?)(?:\n---|\Z)", text)
    if not to_match:
        return None, None
    contact = to_match.group(1).strip()
    message = msg_match.group(1).strip() if msg_match else ""
    return contact, message


# ──────────────────────────────────────────────
# LOGIN FLOW
# ──────────────────────────────────────────────
def login_flow():
    """Open browser for QR code scan, then save session."""
    print("[INFO] Opening browser for WhatsApp Web login...")
    print("[INFO] Scan the QR code, then close the browser window.")

    with sync_playwright() as p:
        context = get_browser_context(p)
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.whatsapp.com/", timeout=60000, wait_until="domcontentloaded")

        try:
            page.wait_for_event("close", timeout=300000)
        except Exception:
            pass

        try:
            context.close()
        except Exception:
            pass

    print("[OK] Session saved. You can now run without --login.")


# ──────────────────────────────────────────────
# SEND MESSAGE
# ──────────────────────────────────────────────
def send_whatsapp(contact, message):
    """Launch browser and send a WhatsApp message to the given contact."""
    print(f"[INFO] Sending to '{contact}' via WhatsApp Web...")

    with sync_playwright() as p:
        try:
            context = get_browser_context(p)
        except Exception as e:
            print(f"[ERROR] Could not launch browser: {e}")
            return False

        page = context.pages[0] if context.pages else context.new_page()

        try:
            # Navigate to WhatsApp Web with retry
            for attempt in range(3):
                try:
                    print(f"[INFO] Navigating to WhatsApp Web (attempt {attempt+1}/3)...")
                    page.goto("https://web.whatsapp.com/", timeout=120000, wait_until="commit")
                    break
                except Exception as nav_err:
                    if attempt < 2:
                        print(f"[WARN] Navigation failed, retrying in 5s... ({nav_err})")
                        page.wait_for_timeout(5000)
                    else:
                        raise nav_err

            # Wait for WhatsApp to fully load (QR scan or session restore)
            print("[INFO] Waiting for WhatsApp to load...")
            page.wait_for_selector(
                'div[contenteditable="true"][data-tab="3"], '
                'div[title="Search input textbox"]',
                timeout=60000,
            )
            page.wait_for_timeout(2000)

            # Search for contact
            print(f"[INFO] Searching for contact: {contact}")
            search_box = page.locator(
                'div[contenteditable="true"][data-tab="3"], '
                'div[title="Search input textbox"]'
            )
            search_box.first.click(timeout=10000)
            page.keyboard.type(contact, delay=50)
            page.wait_for_timeout(2000)

            # Click on the contact from search results
            contact_result = page.locator(
                f'span[title="{contact}"], span.matched-text'
            )
            contact_result.first.click(timeout=15000)
            page.wait_for_timeout(1000)

            # Type the message
            print("[INFO] Typing message...")
            msg_box = page.locator(
                'div[contenteditable="true"][data-tab="10"], '
                'div[title="Type a message"], '
                'footer div[contenteditable="true"]'
            )
            msg_box.first.click(timeout=10000)

            lines = message.split("\n")
            for i, line in enumerate(lines):
                if i > 0:
                    page.keyboard.press("Shift+Enter")
                page.keyboard.type(line, delay=10)

            page.wait_for_timeout(500)

            # Send the message
            print("[INFO] Sending message...")
            page.keyboard.press("Enter")
            print("[INFO] Waiting 10s for message to deliver...")
            page.wait_for_timeout(10000)

            print(f"[OK] Message sent to {contact}!")
            success = True

        except PwTimeout as e:
            print(f"[ERROR] Timeout waiting for element: {e}")
            print("[HINT] WhatsApp Web may have updated its UI. Check selectors in whatsapp_sender.py.")
            success = False
        except Exception as e:
            print(f"[ERROR] {e}")
            success = False
        finally:
            try:
                context.close()
            except Exception:
                pass

        return success


# ──────────────────────────────────────────────
# WATCH MODE
# ──────────────────────────────────────────────
def watch_loop():
    """Poll Approved/ every 60s and process new files."""
    import time
    print("[INFO] Watch mode — polling Approved/ every 60s. Press Ctrl+C to stop.")
    while True:
        process_approved()
        time.sleep(60)


# ──────────────────────────────────────────────
# MAIN PROCESSING
# ──────────────────────────────────────────────
def process_approved():
    """Find all approved .md files and send WhatsApp messages."""
    files = sorted(APPROVED_DIR.glob("*.md"))
    if not files:
        print("[INFO] No approved messages found.")
        return

    print(f"[INFO] Found {len(files)} approved message(s)\n")

    sent = 0
    for f in files:
        print(f"--- Processing: {f.name} ---")
        contact, message = parse_message_file(f)

        if not contact:
            print(f"  [SKIP] {f.name} — no **To:** field found\n")
            continue

        if not message:
            print(f"  [SKIP] {f.name} — no ## Message content found\n")
            continue

        ok = send_whatsapp(contact, message)
        if ok:
            dest = DONE_DIR / f.name
            shutil.move(str(f), str(dest))
            print(f"[OK] Moved {f.name} -> Done/\n")
            sent += 1
        else:
            print(f"  [FAILED] Could not send to {contact}. File remains in Approved/.\n")

    print(f"\n[DONE] Sent {sent} message(s).")


def main():
    print("=" * 50)
    print("  WhatsApp Sender — Browser Automation")
    print("=" * 50)
    print()

    if "--login" in sys.argv:
        login_flow()
    elif "--watch" in sys.argv:
        watch_loop()
    else:
        process_approved()


if __name__ == "__main__":
    main()
