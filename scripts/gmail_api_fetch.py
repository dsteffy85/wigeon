#!/usr/bin/env python3
"""
WIGEON - Gmail API Fetcher (Alternative to Extension)
Uses direct Gmail API access to download attachments
"""

import subprocess
import time
from pathlib import Path


def get_gmail_messages_via_applescript():
    """
    Alternative approach: Use AppleScript to interact with Mail.app
    if Gmail is synced there
    """
    script = """
    tell application "Mail"
        set cevaMessages to {}
        repeat with theAccount in accounts
            repeat with theMailbox in mailboxes of theAccount
                set theMessages to (every message of theMailbox whose sender contains "na_ops_reporting")
                repeat with theMessage in theMessages
                    set messageDate to date received of theMessage
                    set daysDiff to (current date) - messageDate
                    if daysDiff < (7 * days) then
                        set end of cevaMessages to {subject:(subject of theMessage), date:(date received of theMessage)}
                    end if
                end repeat
            end repeat
        end repeat
        return cevaMessages
    end tell
    """

    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=30)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"


def download_via_selenium():
    """
    Use Selenium WebDriver for more reliable browser automation
    This requires: pip3 install selenium
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
        from selenium.webdriver.support.ui import WebDriverWait

        print("🌐 Using Selenium for reliable browser automation...")

        # Use existing Chrome profile to avoid login
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"user-data-dir={Path.home()}/Library/Application Support/Google/Chrome")
        chrome_options.add_argument("profile-directory=Default")

        driver = webdriver.Chrome(options=chrome_options)

        # Open Gmail search
        gmail_url = "https://mail.google.com/mail/u/0/#search/from%3Aops_reporting%40example.com+newer_than%3A7d+has%3Aattachment"
        driver.get(gmail_url)

        # Wait for emails to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.zA")))

        # Find all email rows
        emails = driver.find_elements(By.CSS_SELECTOR, "tr.zA")
        print(f"📧 Found {len(emails)} emails")

        downloaded = []

        for i, email in enumerate(emails[:5]):  # Process first 5
            try:
                email.click()
                time.sleep(2)

                # Find and click download button
                download_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-tooltip='Download']"))
                )
                download_btn.click()
                time.sleep(3)

                downloaded.append(f"Email {i + 1}")

                # Go back
                driver.execute_script("window.history.back()")
                time.sleep(2)

            except Exception as e:
                print(f"⚠️  Error processing email {i + 1}: {e}")
                continue

        driver.quit()
        return downloaded

    except ImportError:
        print("❌ Selenium not installed")
        print("💡 Install with: pip3 install selenium")
        return []
    except Exception as e:
        print(f"❌ Selenium error: {e}")
        return []


def main():
    print("🦆 WIGEON - Alternative Gmail Fetcher")
    print("=" * 60)

    # Try Selenium approach
    print("\n🔄 Attempting Selenium-based download...")
    result = download_via_selenium()

    if result:
        print(f"✅ Downloaded {len(result)} files")
        return True
    else:
        print("❌ Selenium approach failed")
        print("\n💡 Manual workaround needed:")
        print("   1. Open Gmail in Chrome")
        print("   2. Search: from:ops_reporting@example.com newer_than:7d")
        print("   3. Download attachments manually")
        print("   4. Run: cd ~/Desktop/WIGEON && ./fetch_ceva.sh")
        return False


if __name__ == "__main__":
    main()
