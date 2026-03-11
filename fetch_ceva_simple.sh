#!/bin/bash

# WIGEON - Simple CEVA Fetcher (Most Reliable)
# Opens Gmail, you download files, WIGEON auto-ingests

WIGEON_DIR="$HOME/Desktop/WIGEON"
DOWNLOADS_DIR="$HOME/Downloads"

echo "🦆 WIGEON - Simple CEVA Report Fetcher"
echo "============================================================"
echo ""
echo "This is the MOST RELIABLE approach:"
echo "  1. I'll open Gmail with CEVA emails"
echo "  2. You click to download the attachments (takes 30 seconds)"
echo "  3. WIGEON automatically detects and ingests them"
echo "  4. You get consolidated data instantly"
echo ""
echo "Press Enter to open Gmail..."
read

# Open Gmail with CEVA search
echo "📧 Opening Gmail..."
open "https://mail.google.com/mail/u/0/#search/from%3Aops_reporting%40example.com+newer_than%3A7d+has%3Aattachment+CEVA"

echo "✅ Gmail opened in your browser"
echo ""
echo "📥 INSTRUCTIONS:"
echo "   1. Click on each CEVA email"
echo "   2. Click the download button on the attachment"
echo "   3. Repeat for all CEVA emails"
echo ""
echo "⏱️  When you're done downloading, press Enter here..."
read

# Now process all downloaded files
echo ""
echo "🔍 Scanning Downloads folder for CEVA files..."

# Find CEVA files from the last 10 minutes
CEVA_FILES=$(find "$DOWNLOADS_DIR" -type f \( -name "*CEVA*" -o -name "*Block Open*" -o -name "*Block Service*" -o -name "*Block Inventory*" -o -name "*Block SRL*" \) -mmin -10 2>/dev/null)

if [ -z "$CEVA_FILES" ]; then
    echo "❌ No CEVA files found in Downloads from the last 10 minutes"
    echo ""
    echo "💡 Make sure you downloaded the attachments"
    echo "   Files should be in: $DOWNLOADS_DIR"
    exit 1
fi

# Count files
FILE_COUNT=$(echo "$CEVA_FILES" | wc -l | tr -d ' ')
echo "✅ Found $FILE_COUNT CEVA file(s)"
echo ""

# Process each file
SUCCESS_COUNT=0
cd "$WIGEON_DIR"

echo "$CEVA_FILES" | while read -r filepath; do
    if [ -f "$filepath" ]; then
        filename=$(basename "$filepath")
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📥 Processing: $filename"
        
        # Determine report type from filename
        REPORT_TYPE="CEVA Report"
        if [[ "$filename" == *"Open Order"* ]] && [[ "$filename" == *"Cancel"* ]]; then
            REPORT_TYPE="Block Open Orders - BKO WMS Cancel"
        elif [[ "$filename" == *"Open Order"* ]]; then
            REPORT_TYPE="Block Open Orders"
        elif [[ "$filename" == *"Service Level"* ]]; then
            REPORT_TYPE="Block Service Level Detail"
        elif [[ "$filename" == *"Inventory Transaction"* ]]; then
            REPORT_TYPE="Block Inventory Transaction Detail"
        elif [[ "$filename" == *"Return"* ]] && [[ "$filename" == *"Disposition"* ]]; then
            REPORT_TYPE="Block SRL Returns Disposition"
        elif [[ "$filename" == *"Return"* ]] && [[ "$filename" == *"Receipt"* ]]; then
            REPORT_TYPE="Block SRL Return Receipts"
        fi
        
        echo "   Type: $REPORT_TYPE"
        
        # Ingest into WIGEON
        python3 wigeon.py ingest \
            --file "$filepath" \
            --third-party "CEVA Logistics" \
            --email "ops_reporting@example.com" \
            --report-type "$REPORT_TYPE" 2>&1 | grep -E "(Successfully|Report ID|rows)"
        
        if [ $? -eq 0 ]; then
            ((SUCCESS_COUNT++))
            echo "   ✅ Ingested successfully"
        else
            echo "   ❌ Failed to ingest"
        fi
    fi
done

echo ""
echo "============================================================"
echo "✅ Processing Complete!"
echo "============================================================"
echo ""
echo "📊 View statistics:"
python3 wigeon.py stats

echo ""
echo "💡 Next steps:"
echo "   • List all reports: python3 wigeon.py list"
echo "   • Query CEVA data: python3 wigeon.py query --third-party 'CEVA Logistics'"
echo "   • Export to CSV: python3 wigeon.py export --output ceva_consolidated.csv"
echo ""
