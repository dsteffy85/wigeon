#!/usr/bin/env python3
"""
WIGEON - Fully Automated CEVA Report Downloader
Downloads all CEVA attachments from Gmail automatically using browser automation
"""

import subprocess
import time
from pathlib import Path


def run_applescript(script):
    """Execute AppleScript and return result"""
    process = subprocess.Popen(["osascript", "-e", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode("utf-8").strip(), stderr.decode("utf-8").strip()


def open_gmail_ceva_search():
    """Open Gmail with CEVA search in Chrome"""
    script = """
    tell application "Google Chrome"
        activate
        set searchURL to "https://mail.google.com/mail/u/0/#search/CEVA+newer_than%3A7d"
        open location searchURL
        delay 3
    end tell
    """
    print("🔍 Opening Gmail CEVA search...")
    run_applescript(script)
    time.sleep(3)


def click_first_email():
    """Click on the first email in the list"""
    script = """
    tell application "System Events"
        tell process "Google Chrome"
            -- Click on first email (approximate position)
            click at {500, 300}
            delay 2
        end tell
    end tell
    """
    print("📧 Opening first email...")
    run_applescript(script)
    time.sleep(2)


def download_attachment_via_keyboard():
    """Download attachment using keyboard shortcuts"""
    script = """
    tell application "System Events"
        tell process "Google Chrome"
            -- Tab to the attachment
            key code 48 -- Tab key
            delay 0.5
            key code 48 -- Tab again
            delay 0.5
            -- Press Enter to download
            key code 36 -- Enter/Return
            delay 2
        end tell
    end tell
    """
    print("⬇️  Downloading attachment...")
    run_applescript(script)
    time.sleep(2)


def download_attachment_direct():
    """Try direct click on download area"""
    script = """
    tell application "System Events"
        tell process "Google Chrome"
            -- Scroll down to see attachment
            key code 125 -- down arrow
            delay 0.5
            key code 125 -- down arrow
            delay 1

            -- Click on attachment area (where download icon should be)
            click at {310, 490}
            delay 1

            -- Try clicking download icon (typically appears on right side)
            click at {360, 490}
            delay 2
        end tell
    end tell
    """
    print("⬇️  Attempting direct download...")
    run_applescript(script)
    time.sleep(3)


def go_back_to_list():
    """Go back to email list"""
    script = """
    tell application "System Events"
        tell process "Google Chrome"
            -- Press Escape or click back
            key code 53 -- Escape
            delay 1
        end tell
    end tell
    """
    print("⬅️  Returning to email list...")
    run_applescript(script)
    time.sleep(1)


def get_recent_downloads():
    """Get list of recently downloaded files"""
    downloads_dir = Path.home() / "Downloads"
    cutoff_time = time.time() - 300  # Last 5 minutes

    recent_files = []
    for file in downloads_dir.iterdir():
        if (
            file.is_file()
            and file.stat().st_mtime > cutoff_time
            and ("ceva" in file.name.lower() or "block" in file.name.lower())
        ):
            recent_files.append(file)

    return sorted(recent_files, key=lambda x: x.stat().st_mtime, reverse=True)


def main():
    print("🦆 WIGEON - Fully Automated CEVA Report Downloader")
    print("=" * 60)

    # Track downloads before we start
    downloads_before = set(get_recent_downloads())

    # Open Gmail CEVA search
    open_gmail_ceva_search()

    # Try to download first 5 emails
    max_emails = 5
    for i in range(max_emails):
        print(f"\n📨 Processing email {i + 1}/{max_emails}...")

        if i == 0:
            # First email - click on it
            click_first_email()
        else:
            # Navigate to next email
            script = """
            tell application "System Events"
                tell process "Google Chrome"
                    key code 125 -- down arrow to next email
                    delay 0.5
                    key code 36 -- Enter to open
                    delay 2
                end tell
            end tell
            """
            run_applescript(script)
            time.sleep(2)

        # Try to download attachment
        download_attachment_direct()

        # Check if something downloaded
        downloads_after = set(get_recent_downloads())
        new_downloads = downloads_after - downloads_before

        if new_downloads:
            print(f"✅ Downloaded: {[f.name for f in new_downloads]}")
            downloads_before = downloads_after
        else:
            print("⚠️  No new download detected")

        # Go back to list
        go_back_to_list()

    # Final check of all downloads
    print("\n" + "=" * 60)
    all_downloads = get_recent_downloads()

    if all_downloads:
        print(f"✅ Total files downloaded: {len(all_downloads)}")
        for file in all_downloads:
            print(f"   📄 {file.name}")

        print("\n🔄 Now processing with WIGEON...")
        return list(all_downloads)
    else:
        print("❌ No files were downloaded")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure you're logged into Gmail in Chrome")
        print("   2. Check if Chrome has accessibility permissions")
        print("   3. Try running the fetch_ceva.sh script for manual download")
        return []


if __name__ == "__main__":
    downloaded_files = main()

    if downloaded_files:
        print("\n" + "=" * 60)
        print("Next: Run WIGEON ingestion on these files")
        print("=" * 60)
