#!/bin/bash

# WIGEON - Complete Automated CEVA Fetcher
# Opens Gmail, watches for downloads, auto-ingests

set -e

WIGEON_DIR="$HOME/Desktop/WIGEON"

echo "🦆 WIGEON - Complete Automated CEVA Report Fetcher"
echo "=========================================================="
echo ""
echo "This script will:"
echo "  1. Open Gmail with CEVA search"
echo "  2. Give you 2 minutes to click download on attachments"
echo "  3. Automatically detect and ingest downloaded files"
echo "  4. Show you the consolidated results"
echo ""
echo "Ready? Press Enter to start..."
read

# Step 1: Open Gmail with CEVA search
echo "📧 Opening Gmail with CEVA search..."
osascript <<EOF
tell application "Google Chrome"
    activate
    set searchURL to "https://mail.google.com/mail/u/0/#search/from%3Aops_reporting%40example.com+newer_than%3A7d+has%3Aattachment+CEVA"
    open location searchURL
end tell
EOF

echo "✅ Gmail opened"
echo ""
echo "📥 Please download the CEVA report attachments now"
echo "   (You have 2 minutes - the script is watching for downloads)"
echo ""

# Step 2: Watch for downloads and auto-ingest
cd "$WIGEON_DIR"
python3 scripts/watch_and_ingest.py --watch --duration 120

echo ""
echo "=========================================================="
echo "✅ Complete! All CEVA reports have been processed"
echo "=========================================================="
echo ""
echo "💡 Next steps:"
echo "   • View all reports: python3 wigeon.py list"
echo "   • Query CEVA data: python3 wigeon.py query --third-party 'CEVA Logistics'"
echo "   • Export to CSV: python3 wigeon.py export --output ceva_consolidated.csv"
echo ""
