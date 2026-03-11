#!/usr/bin/env python3
"""
WIGEON - Fetch CEVA CLS NORTAM Reports
Automated script to download CEVA reports from Gmail using browser automation
"""
import subprocess
import time
import os
import glob
from datetime import datetime

def run_applescript(script):
    """Execute AppleScript and return result"""
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return None, str(e)

def open_gmail_ceva_search():
    """Open Gmail with CEVA search"""
    script = '''
    tell application "Google Chrome"
        activate
        delay 1
        
        -- Open Gmail search for CEVA reports with attachments
        set newURL to "https://mail.google.com/mail/u/0/#search/from%3Aops_reporting%40example.com+subject%3A%22CEVA+CLS+NORTAM%22+newer_than%3A7d+has%3Aattachment"
        
        try
            set URL of active tab of window 1 to newURL
        on error
            make new tab at window 1 with properties {URL:newURL}
        end try
        
        delay 5
    end tell
    
    return "Opened Gmail CEVA search"
    '''
    
    stdout, stderr = run_applescript(script)
    return stdout

def download_attachments_from_gmail():
    """
    Guide user through downloading attachments from Gmail
    This is a semi-automated approach that works without Gmail API
    """
    script = '''
    tell application "System Events"
        display dialog "WIGEON will now help you download CEVA reports.\\n\\nSteps:\\n1. Click on each CEVA email\\n2. Click the download button for each attachment\\n3. Files will save to ~/Downloads/\\n\\nClick OK when you've downloaded all files, or Cancel to do it manually." buttons {"Cancel", "OK"} default button "OK"
        
        if button returned of result is "OK" then
            return "User will download files"
        else
            return "User cancelled"
        end if
    end tell
    '''
    
    stdout, stderr = run_applescript(script)
    return stdout

def get_recent_downloads(minutes=10):
    """Get files downloaded in the last N minutes"""
    downloads_dir = os.path.expanduser("~/Downloads")
    cutoff_time = time.time() - (minutes * 60)
    
    recent_files = []
    for file in glob.glob(os.path.join(downloads_dir, "*")):
        if os.path.isfile(file):
            mtime = os.path.getmtime(file)
            if mtime > cutoff_time:
                recent_files.append(file)
    
    return sorted(recent_files, key=os.path.getmtime, reverse=True)

def process_with_wigeon(file_path, report_type):
    """Process a file with WIGEON"""
    wigeon_dir = os.path.expanduser("~/Desktop/WIGEON")
    
    cmd = [
        'python3',
        os.path.join(wigeon_dir, 'wigeon.py'),
        'ingest',
        '--file', file_path,
        '--third-party', 'CEVA Logistics',
        '--email', 'ops_reporting@example.com',
        '--report-type', report_type
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🦆 WIGEON - CEVA Report Fetcher")
    print("=" * 70)
    print()
    
    # Step 1: Open Gmail search
    print("📧 Step 1: Opening Gmail with CEVA search...")
    result = open_gmail_ceva_search()
    print(f"   ✓ {result}")
    print()
    
    # Step 2: Wait for user to download files
    print("📥 Step 2: Download attachments from Gmail")
    print("   → Chrome should now show CEVA emails with attachments")
    print("   → Click on each email and download the attachments")
    print()
    
    input("   Press ENTER when you've downloaded all files...")
    print()
    
    # Step 3: Find recently downloaded files
    print("🔍 Step 3: Finding recently downloaded files...")
    recent_files = get_recent_downloads(minutes=10)
    
    if not recent_files:
        print("   ⚠️  No recent downloads found in ~/Downloads/")
        print("   Please download the CEVA attachments and run this script again")
        return
    
    print(f"   ✓ Found {len(recent_files)} recent file(s):")
    for f in recent_files:
        print(f"     - {os.path.basename(f)}")
    print()
    
    # Step 4: Process each file with WIGEON
    print("⚙️  Step 4: Processing files with WIGEON...")
    print()
    
    processed = 0
    failed = 0
    
    for file_path in recent_files:
        filename = os.path.basename(file_path)
        
        # Skip non-data files
        if not any(file_path.endswith(ext) for ext in ['.xlsx', '.xls', '.xml', '.zip', '.csv', '.txt']):
            print(f"   ⊘ Skipping {filename} (not a supported format)")
            continue
        
        # Determine report type from filename
        report_type = "Unknown"
        if "Open Orders" in filename:
            report_type = "Block Open Orders"
        elif "Service Level" in filename:
            report_type = "Block Service Level Detail"
        elif "Returns Disposition" in filename:
            report_type = "Block SRL Returns Disposition"
        elif "Inventory Transaction" in filename:
            report_type = "Block Inventory Transaction Detail"
        elif "Return Receipts" in filename:
            report_type = "Block SRL Return Receipts"
        
        print(f"   Processing: {filename}")
        print(f"   Report Type: {report_type}")
        
        success, stdout, stderr = process_with_wigeon(file_path, report_type)
        
        if success:
            print(f"   ✓ Successfully processed")
            processed += 1
        else:
            print(f"   ✗ Failed to process")
            if stderr:
                print(f"   Error: {stderr}")
            failed += 1
        print()
    
    # Step 5: Summary
    print("=" * 70)
    print("📊 Summary:")
    print(f"   ✓ Processed: {processed} file(s)")
    if failed > 0:
        print(f"   ✗ Failed: {failed} file(s)")
    print()
    
    # Show WIGEON stats
    print("📈 WIGEON Database Stats:")
    stats_cmd = ['python3', os.path.expanduser('~/Desktop/WIGEON/wigeon.py'), 'stats']
    result = subprocess.run(stats_cmd, capture_output=True, text=True)
    print(result.stdout)
    
    print("=" * 70)
    print("🦆 WIGEON fetch complete!")
    print()
    print("Next steps:")
    print("  • View reports: python3 ~/Desktop/WIGEON/wigeon.py list")
    print("  • Query data: python3 ~/Desktop/WIGEON/wigeon.py query --limit 10")
    print("  • Export data: python3 ~/Desktop/WIGEON/wigeon.py export --output ceva_data.csv")

if __name__ == "__main__":
    main()
