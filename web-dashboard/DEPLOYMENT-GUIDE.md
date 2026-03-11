# WIGEON Web Dashboard - Deployment Guide

## 🎯 Quick Deploy to Blockcell

### Step 1: Verify Files
```bash
cd ~/Desktop/WIGEON/web-dashboard
ls -lh
```

Expected files:
- `index.html` (main dashboard)
- `README.md` (documentation)
- `DEPLOYMENT-GUIDE.md` (this file)

### Step 2: Deploy via Goose
```bash
# Use Blockcell extension in Goose
blockcell__manage_site(
    action="upload",
    site_name="wigeon-dashboard",
    directory_path="~/WIGEON/web-dashboard"
)
```

### Step 3: Access Dashboard
After deployment, access at:
```
https://your-deployment-url.example.com/
```

---

## 📊 What You'll See

### Dashboard Overview
The web dashboard displays:

1. **Summary Statistics** (4 cards)
   - Third Parties: 2
   - Total Reports: 8
   - Total Data Rows: 39,814
   - Database Size: 31.8 MB

2. **Recent Reports** (scrollable list)
   - 8 reports from CEVA Logistics and Acme Corp
   - Shows vendor, report type, date, and row count

3. **Third Party Breakdown** (vendor cards)
   - CEVA Logistics: 7 reports, 39,764 rows
   - Acme Corp: 1 report, 50 rows

4. **Available Export Files** (with download info)
   - ceva_all_data.csv: 12.2 MB
   - acme_sales.csv: 6.6 KB

5. **SQL Export Options** (code snippets)
   - Database location
   - Direct SQL access commands
   - Export and schema commands

6. **Report Types Distribution** (visual chart)
   - Bar chart showing data distribution across report types

---

## 🔄 Updating Dashboard Data

### When New Reports Are Ingested

1. **Ingest new CEVA reports**:
   ```bash
   cd ~/Desktop/WIGEON
   python3 wigeon.py ingest --file report.xlsx --third-party "CEVA Logistics" --email ops_reporting@example.com
   ```

2. **Run stats to get new numbers**:
   ```bash
   python3 wigeon.py stats
   ```

3. **Update index.html** with new data:
   - Edit the `dashboardData` object in `index.html`
   - Update statistics, reports, vendors, exports arrays

4. **Redeploy to Blockcell**:
   ```bash
   blockcell__manage_site(action="upload", site_name="wigeon-dashboard", directory_path="~/WIGEON/web-dashboard")
   ```

---

## 🎨 Dashboard Features

### Responsive Design
- ✅ Desktop: Full layout with side-by-side cards
- ✅ Tablet: Adjusted grid layout
- ✅ Mobile: Stacked single-column layout

### Interactive Elements
- ✅ Hover effects on cards and reports
- ✅ Scrollable report list
- ✅ Action buttons with command alerts
- ✅ Visual bar chart for report types

### Color Scheme
- Primary: Purple gradient (#667eea to #764ba2)
- Cards: White with subtle shadows
- Text: Dark gray (#2d3748) with light gray accents
- Accents: Purple, green, blue, orange borders

---

## 📁 File Structure

```
web-dashboard/
├── index.html              # Main dashboard (single file)
├── README.md               # Project documentation
└── DEPLOYMENT-GUIDE.md     # This file
```

### Single-File Architecture
The dashboard is a **single HTML file** with embedded:
- CSS styles (in `<style>` tag)
- JavaScript code (in `<script>` tag)
- Sample data (in `dashboardData` object)

**Benefits**:
- ✅ No external dependencies
- ✅ Easy to deploy (one file)
- ✅ Fast loading (no network requests)
- ✅ Works offline

---

## 🚀 Deployment Options

### Option 1: Blockcell (Recommended)
**Best for**: Team sharing, production use

```bash
blockcell__manage_site(
    action="upload",
    site_name="wigeon-dashboard",
    directory_path="~/WIGEON/web-dashboard"
)
```

**URL**: `https://your-deployment-url.example.com/`

### Option 2: Local File
**Best for**: Quick testing, personal use

```bash
open ~/Desktop/WIGEON/web-dashboard/index.html
```

### Option 3: Web Server
**Best for**: External hosting

```bash
# Copy to web server
scp -r ~/Desktop/WIGEON/web-dashboard user@server:/var/www/html/wigeon
```

---

## 🔧 Customization

### Update Statistics
Edit the `dashboardData.stats` object in `index.html`:

```javascript
stats: {
    thirdParties: 2,      // Update with new count
    totalReports: 8,      // Update with new count
    totalRows: 39814,     // Update with new count
    dbSize: 31.8          // Update with new size
}
```

### Add New Reports
Add to the `dashboardData.reports` array:

```javascript
{
    id: 9,
    vendor: 'CEVA Logistics',
    type: 'New Report Type',
    date: '2026-03-10',
    rows: 1000,
    status: 'processed'
}
```

### Add New Vendors
Add to the `dashboardData.vendors` array:

```javascript
{
    name: 'New Vendor',
    email: 'vendor@example.com',
    reports: 1,
    rows: 500,
    firstReport: '2026-03-10',
    lastReport: '2026-03-10'
}
```

### Add Export Files
Add to the `dashboardData.exports` array:

```javascript
{
    name: 'new_export.csv',
    size: '5.2 MB',
    date: '2026-03-10 10:00',
    rows: 5000
}
```

---

## 🧪 Testing Checklist

Before deploying:

- [ ] Open `index.html` locally
- [ ] Verify all 4 stat cards display correctly
- [ ] Check recent reports list shows 8 reports
- [ ] Verify vendor breakdown shows 2 vendors
- [ ] Check export files section shows 2 files
- [ ] Test action buttons (should show alert with command)
- [ ] Verify SQL commands section displays correctly
- [ ] Check report types chart renders properly
- [ ] Test responsive design (resize browser window)
- [ ] Verify no console errors (F12 Developer Tools)

---

## 📊 Current Data Snapshot

**As of March 9, 2026**:

### Summary
- Third Parties: 2
- Total Reports: 8
- Total Data Rows: 39,814
- Database Size: 31.8 MB

### CEVA Logistics (7 reports, 39,764 rows)
1. Block Inventory Transaction Detail - MTD: 37,154 rows
2. Block Inventory Transaction Detail - Daily: 1,986 rows
3. Block Open Orders: 249 rows
4. Block SRL Return Receipts: 75 rows
5. Block Inventory Transaction Detail: 150 rows
6. Block Service Level Detail: 50 rows
7. Block Open Orders: 100 rows

### Acme Corp (1 report, 50 rows)
1. Sales Report: 50 rows

### Export Files
1. ceva_all_data.csv: 12.2 MB (39,764 rows)
2. acme_sales.csv: 6.6 KB (50 rows)

---

## 🔗 Related Resources

### WIGEON CLI Documentation
- Main README: `~/Desktop/WIGEON/README.md`
- Quick Start: `~/Desktop/WIGEON/QUICK_START.md`
- User Guide: `~/Desktop/WIGEON/docs/USER_GUIDE.md`

### Other Dashboards
- Block Hardware SKUs: `https://your-deployment-url.example.com/`
- Retail Order Tracking: `https://your-deployment-url.example.com/`
- Commercial Invoice Generator: `https://your-deployment-url.example.com/`

---

## 🆘 Troubleshooting

### Dashboard Not Loading
- Check file exists: `ls ~/Desktop/WIGEON/web-dashboard/index.html`
- Try opening in different browser
- Check browser console for errors (F12)

### Data Not Updating
- Verify you edited the `dashboardData` object
- Clear browser cache (Cmd+Shift+R)
- Redeploy to Blockcell

### Blockcell Deploy Fails
- Check Blockcell extension is enabled
- Verify directory path is correct
- Try uploading single file instead of directory

### Styling Issues
- Check browser compatibility (use Chrome/Safari)
- Verify CSS is not being blocked
- Try incognito/private mode

---

## 📞 Quick Reference

### Deploy Command
```bash
blockcell__manage_site(action="upload", site_name="wigeon-dashboard", directory_path="~/WIGEON/web-dashboard")
```

### Local Test
```bash
open ~/Desktop/WIGEON/web-dashboard/index.html
```

### Update Data
1. Edit `index.html`
2. Update `dashboardData` object
3. Save file
4. Redeploy or refresh browser

---

**Last Updated**: March 9, 2026  
**Version**: 1.0  
**Status**: Ready for Deployment
