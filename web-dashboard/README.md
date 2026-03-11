# WIGEON Web Dashboard

## 🦆 Overview

Web-based dashboard for visualizing WIGEON data integration reports. Provides an interactive interface for viewing third-party vendor reports, export files, and database statistics.

## Features

- 📊 **Real-time Statistics**: Third parties, reports, data rows, database size
- 📅 **Recent Reports**: List of latest ingested reports with row counts
- 📋 **Third Party Breakdown**: Vendor-specific statistics and metrics
- 📥 **Export Files**: Available downloads with sizes and dates
- 🗄️ **SQL Export Options**: Direct database access commands
- 📈 **Report Types Chart**: Visual distribution of report types

## Quick Start

### Local Testing
```bash
cd ~/Desktop/WIGEON/web-dashboard
open index.html
```

### Deploy to Blockcell
```bash
# Use Goose with Blockcell extension
blockcell__manage_site(
    action="upload",
    site_name="wigeon-dashboard",
    directory_path="~/WIGEON/web-dashboard"
)
```

## Current Data (2026-03-09)

- **Third Parties**: 2 (CEVA Logistics, Acme Corp)
- **Total Reports**: 8 reports
- **Total Data Rows**: 39,814 rows
- **Database Size**: 31.8 MB

### CEVA Logistics Reports
1. Block Inventory Transaction Detail - MTD: 37,154 rows
2. Block Inventory Transaction Detail - Daily: 1,986 rows
3. Block Open Orders: 249 rows
4. Block Service Level Detail: 50 rows
5. Block SRL Return Receipts: 75 rows
6. Block Inventory Transaction Detail: 150 rows
7. Block Open Orders (sample): 100 rows

### Export Files Available
- `ceva_all_data.csv`: 12.2 MB (39,764 rows)
- `acme_sales.csv`: 6.6 KB (50 rows)

## Dashboard Sections

### 1. Summary Statistics
Four key metrics displayed in card format:
- Third Parties count
- Total Reports processed
- Total Data Rows ingested
- Database Size

### 2. Recent Reports
Scrollable list showing:
- Vendor name
- Report type
- Date ingested
- Row count

### 3. Third Party Breakdown
Vendor cards displaying:
- Email address
- Number of reports
- Total rows
- Last report date

### 4. Available Export Files
List of export files with:
- File name
- Size
- Date created
- Row count

### 5. SQL Export Options
Code snippets for:
- Database location
- Direct SQL access
- Export to SQL dump
- View schema

### 6. Report Types Distribution
Visual bar chart showing:
- Report type names
- Row counts
- Relative distribution

## Action Buttons

- **Export to CSV**: Command to export data to CSV format
- **Export to Excel**: Command to export data to Excel format
- **Export to JSON**: Command to export data to JSON format

## Technical Details

### Technology Stack
- Pure HTML/CSS/JavaScript (no dependencies)
- Responsive design (mobile, tablet, desktop)
- Gradient purple theme matching WIGEON branding

### Data Source
Currently uses embedded sample data. In production, would connect to:
- WIGEON SQLite database (`database/wigeon.db`)
- Real-time API endpoint for live data
- Export files directory for download links

### Browser Compatibility
- Chrome/Edge: ✅ Full support
- Safari: ✅ Full support
- Firefox: ✅ Full support
- Mobile browsers: ✅ Responsive design

## Future Enhancements

### Phase 1 (Current)
- ✅ Static HTML dashboard
- ✅ Embedded sample data
- ✅ Responsive design
- ✅ Export file listing

### Phase 2 (Planned)
- [ ] Live database connection
- [ ] Real-time data updates
- [ ] Download buttons for export files
- [ ] Search and filter functionality
- [ ] Date range picker

### Phase 3 (Future)
- [ ] Interactive charts (Chart.js)
- [ ] Data drill-down views
- [ ] Export scheduling
- [ ] Email notifications
- [ ] Multi-user access control

## Deployment

### Option 1: Blockcell (Recommended)
```bash
# Deploy to internal Block hosting
blockcell__manage_site(
    action="upload",
    site_name="wigeon-dashboard",
    directory_path="~/WIGEON/web-dashboard"
)

# Access at:
# https://your-deployment-url.example.com/
```

### Option 2: Local File
```bash
# Open directly in browser
open ~/Desktop/WIGEON/web-dashboard/index.html
```

### Option 3: Web Server
```bash
# Copy to any web server
cp -r ~/Desktop/WIGEON/web-dashboard /path/to/webroot/wigeon
```

## Updating Data

To update the dashboard with latest WIGEON data:

1. **Ingest new reports** via CLI:
   ```bash
   cd ~/Desktop/WIGEON
   python3 wigeon.py ingest --file report.xlsx --third-party "Vendor Name"
   ```

2. **Export updated data**:
   ```bash
   python3 wigeon.py export --output exports/latest.csv --format csv
   ```

3. **Update dashboard data** (edit `index.html`):
   - Update `dashboardData` object with new statistics
   - Add new reports to `reports` array
   - Update export files in `exports` array

4. **Redeploy** to Blockcell:
   ```bash
   blockcell__manage_site(action="upload", ...)
   ```

## Related Projects

- **WIGEON CLI**: Command-line data integration tool
- **Block Hardware SKUs**: Product database web app
- **Commercial Invoice Generator**: Invoice creation tool
- **Retail Order Tracking**: Shipment tracking dashboard

## Support

For issues or questions:
- Check WIGEON documentation: `~/Desktop/WIGEON/README.md`
- Review CLI guide: `~/Desktop/WIGEON/QUICK_START.md`
- Contact: Project maintainer

## License

Internal Block project - Not for external distribution

---

**Last Updated**: March 9, 2026  
**Version**: 1.0  
**Status**: Production Ready
