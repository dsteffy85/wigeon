# 🦆 Welcome to WIGEON!

**WIGEON** = **W**orkflow **I**ntelligence for **G**athering **E**mail-**O**riginated **N**otifications

A data integration agent built for the Goose platform.

---

## 🚀 Quick Start (30 seconds)

### Option 1: Use with Goose (Easiest!)

Just ask Goose:
```
"Use WIGEON to fetch reports from vendor@acme.com"
```

### Option 2: Use CLI Directly

```bash
cd ~/Desktop/WIGEON

# Ingest a file
python3 wigeon.py ingest \
  --file samples/sales_report.xlsx \
  --third-party "Acme Corp" \
  --email vendor@acme.com

# View results
python3 wigeon.py stats
python3 wigeon.py query --report-id 1 --limit 5
```

---

## 📚 Documentation

1. **START HERE** → `QUICK_START.md` (5-minute tutorial)
2. **Then Read** → `README.md` (comprehensive overview)
3. **Deep Dive** → `docs/USER_GUIDE.md` (detailed guide)
4. **Reference** → `PROJECT_COMPLETE.md` (complete summary)

---

## 🎯 What WIGEON Does

- ✅ Fetches email reports from third-party vendors
- ✅ Parses Excel, XML, ZIP files automatically
- ✅ Stores data in SQLite database
- ✅ Queries consolidated data across sources
- ✅ Exports to CSV, JSON, or Excel

---

## 💡 Common Commands

```bash
# Show all reports
python3 wigeon.py list

# Query data
python3 wigeon.py query --third-party "Acme Corp"

# Export to CSV
python3 wigeon.py export --output data.csv --format csv

# Show statistics
python3 wigeon.py stats

# Get help
python3 wigeon.py --help
```

---

## 🦆 Why "WIGEON"?

Wigeons are social ducks that work well in groups - just like WIGEON consolidates data from multiple sources!

---

## 📞 Need Help?

- Ask Goose: `"Help me use WIGEON"`
- Read docs: `QUICK_START.md`, `README.md`
- Check examples: `samples/` directory

---

**Status:** ✅ Production Ready  
**Version:** 1.0  
**Date:** March 8, 2026

**Happy data integrating! 🦆**
