#!/bin/bash

# WIGEON - Fully Automated CEVA Report Fetcher
# Downloads CEVA reports from Gmail and processes them automatically

set -e

WIGEON_DIR="$HOME/Desktop/WIGEON"
DOWNLOADS_DIR="$HOME/Downloads"

echo "🦆 WIGEON - Fully Automated CEVA Report Fetcher"
echo "=============================================="
echo ""

# Step 1: Download reports from Gmail
echo "📥 Step 1: Downloading CEVA reports from Gmail..."
cd "$WIGEON_DIR"
python3 scripts/auto_download_ceva.py

# Wait a moment for downloads to complete
sleep 3

# Step 2: Find all recently downloaded CEVA/Block files
echo ""
echo "🔍 Step 2: Detecting downloaded files..."
RECENT_FILES=$(find "$DOWNLOADS_DIR" -type f -mmin -5 \( -iname "*ceva*" -o -iname "*block*" \) -not -name "*.crdownload")

if [ -z "$RECENT_FILES" ]; then
    echo "❌ No CEVA files found in Downloads from the last 5 minutes"
    echo ""
    echo "💡 Alternative: Manually download files from Gmail, then run:"
    echo "   cd $WIGEON_DIR && ./fetch_ceva.sh"
    exit 1
fi

echo "✅ Found $(echo "$RECENT_FILES" | wc -l | tr -d ' ') file(s)"
echo "$RECENT_FILES" | while read file; do
    echo "   📄 $(basename "$file")"
done

# Step 3: Process each file with WIGEON
echo ""
echo "🔄 Step 3: Processing files with WIGEON..."
echo ""

PROCESSED=0
FAILED=0

echo "$RECENT_FILES" | while read file; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    FILENAME=$(basename "$file")
    echo "Processing: $FILENAME"
    
    # Determine report type from filename
    REPORT_TYPE="Unknown Report"
    if [[ $FILENAME == *"Open Order"* ]]; then
        REPORT_TYPE="Block Open Orders"
    elif [[ $FILENAME == *"Service Level"* ]]; then
        REPORT_TYPE="Block Service Level Detail"
    elif [[ $FILENAME == *"Inventory"* ]]; then
        REPORT_TYPE="Block Inventory Transaction Detail"
    elif [[ $FILENAME == *"Return"* ]]; then
        REPORT_TYPE="Block SRL Returns"
    elif [[ $FILENAME == *"Cancel"* ]]; then
        REPORT_TYPE="Block Open Orders - BKO WMS Cancel"
    fi
    
    # Ingest into WIGEON
    python3 wigeon.py ingest \
        --file "$file" \
        --third-party "CEVA Logistics" \
        --email "ops_reporting@example.com" \
        --report-type "$REPORT_TYPE" \
        2>&1 | grep -E "(Successfully|Error|rows)"
    
    if [ $? -eq 0 ]; then
        PROCESSED=$((PROCESSED + 1))
        echo "✅ Processed successfully"
    else
        FAILED=$((FAILED + 1))
        echo "❌ Failed to process"
    fi
    echo ""
done

# Step 4: Show summary
echo ""
echo "=============================================="
echo "📊 WIGEON Processing Complete"
echo "=============================================="

python3 wigeon.py stats

echo ""
echo "✅ Automation complete!"
echo ""
echo "💡 Next steps:"
echo "   • View reports: python3 wigeon.py list"
echo "   • Query data: python3 wigeon.py query --third-party 'CEVA Logistics'"
echo "   • Export data: python3 wigeon.py export --output ceva_data.csv"
echo ""
