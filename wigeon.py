#!/usr/bin/env python3
"""
🦆 WIGEON v2.0.0
Workflow Intelligence for Gathering Email-Originated Notifications

A universal agent for collecting email report attachments from any
third-party provider and storing the data for easy analysis.
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from wigeon_processor import WigeonProcessor
from wigeon_config import (
    load_config,
    save_config,
    add_provider,
    remove_provider,
    list_providers,
    interactive_setup,
)

VERSION = "2.0.0"
PROJECT_ROOT = Path(__file__).parent


def print_banner():
    print(f"""
    🦆 WIGEON v{VERSION}
    Workflow Intelligence for Gathering Email-Originated Notifications
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)


# ─── Setup Command ────────────────────────────────────────────────

def cmd_setup(args):
    """First-time setup or provider management."""
    config = load_config(PROJECT_ROOT)

    if args.add_provider:
        name = input("  Provider name: ").strip()
        email = input("  Provider email: ").strip()
        subject = input("  Subject filter (optional): ").strip()
        if name and email:
            add_provider(config, name=name, email=email, subject_filter=subject)
            save_config(config, PROJECT_ROOT)
            print(f"\n  ✅ Added provider: {name} ({email})")
        else:
            print("\n  ❌ Name and email are required.")
        return 0

    if args.remove_provider:
        providers = list_providers(config)
        if not providers:
            print("  No providers configured.")
            return 0
        print("\n  Current providers:")
        for i, p in enumerate(providers):
            print(f"    {i + 1}. {p['name']} ({p['email']})")
        choice = input("\n  Enter email to remove: ").strip()
        remove_provider(config, choice)
        save_config(config, PROJECT_ROOT)
        print(f"  ✅ Removed provider: {choice}")
        return 0

    if args.list_providers:
        providers = list_providers(config)
        if not providers:
            print("  No providers configured. Run: python3 wigeon.py setup")
            return 0
        print("\n  📧 Configured Providers:")
        for p in providers:
            filt = f" (filter: {p['subject_filter']})" if p.get("subject_filter") else ""
            print(f"    • {p['name']} — {p['email']}{filt}")
        print()
        return 0

    if args.show:
        print(f"\n  📋 Current Configuration ({PROJECT_ROOT / 'config.json'}):\n")
        print(json.dumps(config, indent=2))
        print()
        return 0

    # Default: run interactive setup
    config = interactive_setup()
    save_config(config, PROJECT_ROOT)
    print(f"  Config saved to {PROJECT_ROOT / 'config.json'}")
    return 0


# ─── Refresh Command ──────────────────────────────────────────────

def cmd_refresh(args):
    """Refresh: download new reports from inbox/ and ingest them."""
    config = load_config(PROJECT_ROOT)
    providers = list_providers(config)

    if not providers:
        print("  ⚠️  No providers configured. Run: python3 wigeon.py setup")
        return 1

    inbox = PROJECT_ROOT / config.get("inbox_dir", "inbox")
    if not inbox.exists():
        inbox.mkdir(parents=True)

    # Find files in inbox
    extensions = {".xlsx", ".xlsm", ".xls", ".csv", ".xml", ".zip"}
    files = sorted(f for f in inbox.iterdir() if f.is_file() and f.suffix.lower() in extensions)

    if not files:
        print("  📭 No report files found in inbox/")
        print("  Download files from Google Drive first, or place files in inbox/")
        return 0

    print(f"\n  📥 Found {len(files)} file(s) in inbox/\n")

    processor = WigeonProcessor(config.get("database_path", "database/wigeon.db"))
    success_count = 0
    fail_count = 0

    for f in files:
        # Try to match file to a provider by filename patterns
        # Default to first provider if only one configured
        provider = _match_provider(f.name, providers)

        print(f"  Processing: {f.name}")
        print(f"    Provider: {provider['name']} ({provider['email']})")

        result = processor.process_file(
            file_path=str(f),
            third_party_name=provider["name"],
            third_party_email=provider["email"],
        )

        if result["success"]:
            print(f"    ✅ {result['row_count']} rows ingested (Report #{result['report_id']})")
            success_count += 1
        else:
            print(f"    ❌ Failed: {result['error']}")
            fail_count += 1
        print()

    processor.close()

    print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  ✅ Ingested: {success_count}  ❌ Failed: {fail_count}")
    print(f"  Run 'python3 wigeon.py stats' to see updated totals.")
    print(f"  Run 'python3 wigeon.py dashboard' for the full view.\n")
    return 0 if fail_count == 0 else 1


def _match_provider(filename, providers):
    """Try to match a filename to a provider. Falls back to first provider."""
    fn_lower = filename.lower()
    for p in providers:
        # Match by provider name appearing in filename
        if p["name"].lower().replace(" ", "_") in fn_lower:
            return p
        if p["name"].lower().replace(" ", "-") in fn_lower:
            return p
        # Match by subject filter
        if p.get("subject_filter") and p["subject_filter"].lower() in fn_lower:
            return p
    return providers[0]


# ─── Ingest Command ───────────────────────────────────────────────

def cmd_ingest(args):
    """Ingest a single report file."""
    processor = WigeonProcessor()

    print(f"\n  📥 INGESTING REPORT")
    print(f"     File: {args.file}")
    print(f"     Provider: {args.third_party}")
    print(f"     Email: {args.email}")

    result = processor.process_file(
        file_path=args.file,
        third_party_name=args.third_party,
        third_party_email=args.email,
        report_type=args.report_type,
        report_date=args.report_date,
        email_subject=args.subject,
        email_date=args.email_date,
        metadata={"notes": args.notes} if args.notes else None,
    )

    if result["success"]:
        print(f"\n  ✅ SUCCESS — {result['row_count']} rows stored (Report #{result['report_id']})")
    else:
        print(f"\n  ❌ FAILED: {result['error']}")

    processor.close()
    return 0 if result["success"] else 1


# ─── List Command ─────────────────────────────────────────────────

def cmd_list(args):
    """List reports."""
    processor = WigeonProcessor()

    reports = processor.query_reports(
        third_party_name=args.third_party,
        report_type=args.report_type,
        start_date=args.start_date,
        end_date=args.end_date,
        status=args.status,
    )

    if not reports:
        print("\n  No reports found.\n")
        processor.close()
        return 0

    print(f"\n  📋 {len(reports)} report(s)\n")
    print(f"  {'ID':>4}  {'Provider':<22} {'Type':<28} {'Date':<12} {'Rows':>8}  {'Status'}")
    print(f"  {'─' * 4}  {'─' * 22} {'─' * 28} {'─' * 12} {'─' * 8}  {'─' * 10}")

    for r in reports:
        name = (r["third_party_name"][:20] + "..") if len(r["third_party_name"]) > 22 else r["third_party_name"]
        rtype = (r["report_type"][:26] + "..") if r["report_type"] and len(r["report_type"]) > 28 else (r["report_type"] or "—")
        print(f"  {r['id']:>4}  {name:<22} {rtype:<28} {r['report_date'] or '—':<12} {r['row_count']:>8,}  {r['status']}")

    print()
    processor.close()
    return 0


# ─── Query Command ────────────────────────────────────────────────

def cmd_query(args):
    """Query report data."""
    processor = WigeonProcessor()

    data = processor.query_data(
        report_id=args.report_id,
        third_party_name=args.third_party,
        limit=args.limit,
        offset=args.offset,
    )

    if not data:
        print("\n  No data found.\n")
        processor.close()
        return 0

    print(f"\n  🔍 {len(data)} row(s)\n")

    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        for idx, row in enumerate(data, 1):
            print(f"  Row {idx}: Report #{row['report_id']} | {row['third_party_name']} | {row['report_type']}")
            print(f"    {json.dumps(row['data'], indent=4)}")
            print()

    processor.close()
    return 0


# ─── Export Command ───────────────────────────────────────────────

def cmd_export(args):
    """Export data to file."""
    processor = WigeonProcessor()

    print(f"\n  📤 Exporting → {args.output} ({args.format})")

    success = processor.export_data(
        output_path=args.output,
        report_id=args.report_id,
        third_party_name=args.third_party,
        format=args.format,
    )

    processor.close()
    return 0 if success else 1


# ─── Stats Command ────────────────────────────────────────────────

def cmd_stats(args):
    """Show statistics."""
    processor = WigeonProcessor()
    stats = processor.get_statistics()

    print(f"\n  📊 WIGEON DATABASE")
    print(f"  {'─' * 40}")
    print(f"  Providers:       {stats['third_parties']}")
    print(f"  Total reports:   {stats['total_reports']}")
    print(f"  Total data rows: {stats['total_data_rows']:,}")

    if stats["reports_by_status"]:
        print(f"\n  By status:")
        for status, count in stats["reports_by_status"].items():
            print(f"    {status}: {count}")

    if stats["reports_by_third_party"]:
        print(f"\n  By provider:")
        for name, count in stats["reports_by_third_party"].items():
            print(f"    {name}: {count}")

    print()
    processor.close()
    return 0


# ─── Dashboard Command ───────────────────────────────────────────

def cmd_dashboard(args):
    """Show dashboard."""
    from dashboard import WigeonDashboard

    dashboard = WigeonDashboard()

    if args.interactive:
        dashboard.interactive_mode()
    elif args.recent:
        dashboard.print_header()
        dashboard.print_recent_reports(limit=args.recent)
    elif args.search:
        dashboard.search_reports(args.search)
    elif args.days:
        dashboard.print_header()
        dashboard.print_reports_by_date(days=args.days)
    elif args.export_json:
        _export_dashboard_json()
    else:
        dashboard.show_full_dashboard()

    return 0


def _export_dashboard_json():
    """Export dashboard data as JSON for the web dashboard."""
    processor = WigeonProcessor()
    stats = processor.get_statistics()
    reports = processor.query_reports()

    dashboard_data = {
        "generated_at": __import__("datetime").datetime.now().isoformat(),
        "version": VERSION,
        "stats": stats,
        "reports": reports,
    }

    out_path = PROJECT_ROOT / "web-dashboard" / "dashboard-data.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(dashboard_data, f, indent=2, default=str)

    print(f"\n  ✅ Dashboard data exported to {out_path}")
    print(f"     Open web-dashboard/index.html in a browser to view.\n")
    processor.close()


# ─── Argument Parser ──────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        description="🦆 WIGEON — Email Report Data Integration Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quick Start:
  python3 wigeon.py setup                  # First-time setup
  python3 wigeon.py refresh                # Ingest files from inbox/
  python3 wigeon.py stats                  # View database stats
  python3 wigeon.py dashboard              # Full dashboard view
  python3 wigeon.py dashboard --export-json # Export for web dashboard

Examples:
  python3 wigeon.py ingest --file report.xlsx --third-party "Acme" --email vendor@acme.com
  python3 wigeon.py list --third-party "Acme"
  python3 wigeon.py export --output data.csv --format csv
        """,
    )
    parser.add_argument("--version", action="version", version=f"WIGEON {VERSION}")

    sub = parser.add_subparsers(dest="command", help="Commands")

    # setup
    sp = sub.add_parser("setup", help="Configure WIGEON (providers, settings)")
    sp.add_argument("--add-provider", action="store_true", help="Add a new provider")
    sp.add_argument("--remove-provider", action="store_true", help="Remove a provider")
    sp.add_argument("--list-providers", action="store_true", help="List configured providers")
    sp.add_argument("--show", action="store_true", help="Show full config")

    # refresh
    sp = sub.add_parser("refresh", help="Ingest all files from inbox/")

    # ingest
    sp = sub.add_parser("ingest", help="Ingest a single report file")
    sp.add_argument("--file", required=True, help="Path to report file")
    sp.add_argument("--third-party", required=True, help="Provider name")
    sp.add_argument("--email", required=True, help="Provider email")
    sp.add_argument("--report-type", help="Report type/category")
    sp.add_argument("--report-date", help="Report date (YYYY-MM-DD)")
    sp.add_argument("--subject", help="Email subject line")
    sp.add_argument("--email-date", help="Email date")
    sp.add_argument("--notes", help="Additional notes")

    # list
    sp = sub.add_parser("list", help="List reports")
    sp.add_argument("--third-party", help="Filter by provider")
    sp.add_argument("--report-type", help="Filter by report type")
    sp.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    sp.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    sp.add_argument("--status", choices=["pending", "processed", "failed"])

    # query
    sp = sub.add_parser("query", help="Query report data")
    sp.add_argument("--report-id", type=int)
    sp.add_argument("--third-party")
    sp.add_argument("--limit", type=int, default=100)
    sp.add_argument("--offset", type=int, default=0)
    sp.add_argument("--format", choices=["table", "json"], default="table")

    # export
    sp = sub.add_parser("export", help="Export data to file")
    sp.add_argument("--output", required=True)
    sp.add_argument("--report-id", type=int)
    sp.add_argument("--third-party")
    sp.add_argument("--format", choices=["csv", "json", "excel"], default="csv")

    # stats
    sub.add_parser("stats", help="Show statistics")

    # dashboard
    sp = sub.add_parser("dashboard", help="Dashboard view")
    sp.add_argument("--interactive", "-i", action="store_true")
    sp.add_argument("--recent", type=int, metavar="N")
    sp.add_argument("--search", metavar="TERM")
    sp.add_argument("--days", type=int, metavar="N")
    sp.add_argument("--export-json", action="store_true", help="Export JSON for web dashboard")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        return 0

    print_banner()

    commands = {
        "setup": cmd_setup,
        "refresh": cmd_refresh,
        "ingest": cmd_ingest,
        "list": cmd_list,
        "query": cmd_query,
        "export": cmd_export,
        "stats": cmd_stats,
        "dashboard": cmd_dashboard,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
