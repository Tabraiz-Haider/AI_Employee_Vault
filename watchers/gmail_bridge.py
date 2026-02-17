"""
Gmail Bridge — Silver Tier Watcher
Fetches unread emails from Gmail and saves Markdown summaries into Readings/.
"""

import os
import sys
import time
import webbrowser
from datetime import datetime
from email.utils import parsedate_to_datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- Configuration ---
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = os.path.dirname(SCRIPT_DIR)
READINGS_DIR = os.path.join(VAULT_DIR, "Readings")
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "credentials.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")
MAX_EMAILS = 10
POLL_INTERVAL = 120  # seconds


def authenticate():
    """Authenticate with Gmail API using OAuth2."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[AUTH] Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"[ERROR] credentials.json not found at {CREDENTIALS_FILE}")
                print("Download it from Google Cloud Console and place it in watchers/")
                sys.exit(1)
            print("[AUTH] Starting Google sign-in...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            # Use fixed port so the redirect URI is predictable
            auth_url, _ = flow.authorization_url(prompt="consent")
            print()
            print("=" * 50)
            print("  Open this URL in your browser to sign in:")
            print()
            print(f"  {auth_url}")
            print()
            print("=" * 50)
            print()
            # Try to open browser automatically
            webbrowser.open(auth_url)
            creds = flow.run_local_server(port=8090, open_browser=False)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
        print("[AUTH] Token saved.")

    return build("gmail", "v1", credentials=creds)


def extract_header(headers, name):
    """Extract a specific header value from email headers."""
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return "Unknown"


def format_date(date_str):
    """Parse email date header into a clean format."""
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return date_str


def save_email_as_markdown(msg_id, subject, sender, date_str, snippet):
    """Save a single email summary as a Markdown file in Readings/."""
    os.makedirs(READINGS_DIR, exist_ok=True)

    filename = f"EMAIL_{msg_id}.md"
    filepath = os.path.join(READINGS_DIR, filename)

    if os.path.exists(filepath):
        return False  # already processed

    clean_date = format_date(date_str)
    content = f"""# Email: {subject}
- **From:** {sender}
- **Date:** {clean_date}
- **Status:** Unread

## Summary
{snippet}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True


def fetch_unread_emails(service):
    """Fetch latest unread emails and save as Markdown."""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking for unread emails...")

    results = service.users().messages().list(
        userId="me", q="is:unread", maxResults=MAX_EMAILS
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        print("  No unread emails found.")
        return 0

    saved_count = 0
    for msg_info in messages:
        msg_id = msg_info["id"]
        msg = service.users().messages().get(
            userId="me", id=msg_id, format="metadata",
            metadataHeaders=["Subject", "From", "Date"]
        ).execute()

        headers = msg.get("payload", {}).get("headers", [])
        subject = extract_header(headers, "Subject")
        sender = extract_header(headers, "From")
        date_str = extract_header(headers, "Date")
        snippet = msg.get("snippet", "")

        if save_email_as_markdown(msg_id, subject, sender, date_str, snippet):
            print(f"  Saved: {subject[:60]}")
            saved_count += 1
        else:
            print(f"  Skipped (already exists): {subject[:60]}")

    print(f"  Total new: {saved_count} / {len(messages)} unread")
    return saved_count


def main():
    print("=" * 50)
    print("  Gmail Bridge — Silver Tier Watcher")
    print("=" * 50)
    print(f"Vault:    {VAULT_DIR}")
    print(f"Readings: {READINGS_DIR}")
    print()

    service = authenticate()
    print("[OK] Connected to Gmail API.\n")

    # Check for --once flag
    if "--once" in sys.argv:
        fetch_unread_emails(service)
        print("\nDone (single run).")
        return

    # Continuous polling mode
    print(f"[LOOP] Polling every {POLL_INTERVAL}s. Press Ctrl+C to stop.\n")
    while True:
        try:
            fetch_unread_emails(service)
        except KeyboardInterrupt:
            print("\n[STOP] Stopped by user.")
            break
        except Exception as e:
            print(f"  [ERROR] {e} — retrying in {POLL_INTERVAL}s...")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
