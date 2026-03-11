#!/bin/bash
#
# WIGEON - Fetch CEVA Reports (Automated)
# This script automates downloading CEVA CLS NORTAM reports from Gmail
#

echo "🦆 WIGEON - CEVA Report Fetcher (Automated)"
echo "=================================================================="
echo ""

# Step 1: Open Gmail search in Chrome
echo "📧 Opening Gmail with CEVA search..."
open "https://mail.google.com/mail/u/0/#search/from%3Aops_reporting%40example.com+subject%3A%22CEVA+CLS+NORTAM%22+newer_than%3A7d+has%3Aattachment"
sleep 5

# Step 2: Instructions for user
echo ""
echo "📥 DOWNLOAD INSTRUCTIONS:"
echo "=================================================================="
echo ""
echo "Chrome should now show CEVA emails with attachments."
echo ""
echo "For each email:"
echo "  1. Click on the email to open it"
echo "  2. Scroll down to see attachments"
echo "  3. Click the download icon (⬇) for each attachment"
echo "  4. Files will save to ~/Downloads/"
echo ""
echo "Common CEVA reports you'll see:"
echo "  • Block Open Orders - Daily"
echo "  • Block Service Level Detail - Daily"
echo "  • Block SRL Returns Disposition - MTD"
echo "  • Block Inventory Transaction Detail - MTD"
echo "  • Block SRL Return Receipts - Daily"
echo ""
echo "=================================================================="
echo ""
read -p "Press ENTER when you've downloaded all files..."

# Step 3: Find recently downloaded files
echo ""
echo "🔍 Finding recently downloaded files..."
DOWNLOADS_DIR=~/Downloads
RECENT_FILES=$(find "$DOWNLOADS_DIR" -type f -mmin -10 | grep -E '\.(xlsx?|xml|zip|csv|txt)$')

if [ -z "$RECENT_FILES" ]; then
    echo "⚠️  No recent downloads found in ~/Downloads/"
    echo ""
    echo "Please download the CEVA attachments and run this script again:"
    echo "  cd ~/Desktop/WIGEON && ./fetch_ceva.sh"
    exit 1
fi

echo "✓ Found recent files:"
echo "$RECENT_FILES" | while read file; do
    echo "  - $(basename "$file")"
done
echo ""

# Step 4: Process each file with WIGEON
echo "⚙️  Processing files with WIGEON..."
echo ""

PROCESSED=0
FAILED=0

echo "$RECENT_FILES" | while read file; do
    filename=$(basename "$file")
    
    # Determine report type from filename
    REPORT_TYPE="Unknown"
    if [[ "$filename" == *"Open Orders"* ]]; then
        REPORT_TYPE="Block Open Orders"
    elif [[ "$filename" == *"Service Level"* ]]; then
        REPORT_TYPE="Block Service Level Detail"
    elif [[ "$filename" == *"Returns Disposition"* ]]; then
        REPORT_TYPE="Block SRL Returns Disposition"
    elif [[ "$filename" == *"Inventory Transaction"* ]]; then
        REPORT_TYPE="Block Inventory Transaction Detail"
    elif [[ "$filename" == *"Return Receipts"* ]]; then
        REPORT_TYPE="Block SRL Return Receipts"
    fi
    
    echo "  Processing: $filename"
    echo "  Report Type: $REPORT_TYPE"
    
    # Ingest with WIGEON
    cd ~/Desktop/WIGEON
    python3 wigeon.py ingest \
        --file "$file" \
        --third-party "CEVA Logistics" \
        --email "ops_reporting@example.com" \
        --report-type "$REPORT_TYPE" 2>&1 | grep -E "(Successfully|Error|rows)"
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo "  ✓ Successfully processed"
        ((PROCESSED++))
    else
        echo "  ✗ Failed to process"
        ((FAILED++))
    fi
    echo ""
done

# Step 5: Summary
echo "=================================================================="
echo "📊 Summary:"
echo "  ✓ Processed: $PROCESSED file(s)"
if [ $FAILED -gt 0 ]; then
    echo "  ✗ Failed: $FAILED file(s)"
fi
echo ""

# Show WIGEON stats
echo "📈 WIGEON Database Stats:"
cd ~/Desktop/WIGEON
python3 wigeon.py stats

echo ""
echo "=================================================================="
echo "🦆 WIGEON fetch complete!"
echo ""
echo "Next steps:"
echo "  • View reports: cd ~/Desktop/WIGEON && python3 wigeon.py list"
echo "  • Query data: python3 wigeon.py query --third-party 'CEVA Logistics' --limit 10"
echo "  • Export data: python3 wigeon.py export --output ceva_data.csv --format csv"
echo ""
