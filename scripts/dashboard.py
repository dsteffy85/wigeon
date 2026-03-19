#!/usr/bin/env python3
"""
WIGEON Dashboard - Interactive Report Viewer
Shows available reports with filtering, sorting, and statistics
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database_schema import WigeonDatabase


class WigeonDashboard:
    """Interactive dashboard for viewing WIGEON reports"""

    def __init__(self, db_path="database/wigeon.db"):
        """Initialize dashboard with database connection"""
        self.db = WigeonDatabase(db_path)

    def print_header(self):
        """Print dashboard header"""
        print("\n" + "=" * 80)
        print("🦆 WIGEON DASHBOARD - Report Overview")
        print("=" * 80 + "\n")

    def print_summary_stats(self):
        """Print summary statistics"""
        stats = self.db.get_statistics()

        print("📊 SUMMARY STATISTICS")
        print("-" * 80)
        print(f"  Third Parties:     {stats.get('third_parties', 0)}")
        print(f"  Total Reports:     {stats.get('total_reports', 0)}")
        print(f"  Total Data Rows:   {stats.get('total_data_rows', 0):,}")
        print()

    def print_third_party_breakdown(self):
        """Print breakdown by third party"""
        cursor = self.db.conn.cursor()

        # Get reports by third party
        cursor.execute("""
            SELECT
                tp.name,
                tp.email,
                COUNT(r.id) as report_count,
                SUM(r.row_count) as total_rows,
                MIN(r.report_date) as first_report,
                MAX(r.report_date) as last_report
            FROM third_parties tp
            LEFT JOIN reports r ON tp.id = r.third_party_id
            GROUP BY tp.id
            ORDER BY report_count DESC
        """)

        results = cursor.fetchall()

        if results:
            print("📋 THIRD PARTY BREAKDOWN")
            print("-" * 80)
            for row in results:
                name, email, count, rows, first, last = row
                print(f"\n  {name}")
                print(f"    Email:        {email}")
                print(f"    Reports:      {count}")
                print(f"    Total Rows:   {rows:,}" if rows else "    Total Rows:   0")
                print(f"    First Report: {first if first else 'N/A'}")
                print(f"    Last Report:  {last if last else 'N/A'}")
            print()

    def print_report_types(self):
        """Print breakdown by report type"""
        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT
                report_type,
                COUNT(*) as count,
                SUM(row_count) as total_rows
            FROM reports
            WHERE report_type IS NOT NULL
            GROUP BY report_type
            ORDER BY count DESC
        """)

        results = cursor.fetchall()

        if results:
            print("📊 REPORT TYPES")
            print("-" * 80)
            for report_type, count, rows in results:
                print(f"  {report_type:40s} {count:3d} reports  {rows:8,} rows")
            print()

    def print_recent_reports(self, limit=10):
        """Print most recent reports"""
        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                r.id,
                tp.name,
                r.file_name,
                r.report_type,
                r.report_date,
                r.row_count,
                r.status,
                r.created_at
            FROM reports r
            JOIN third_parties tp ON r.third_party_id = tp.id
            ORDER BY r.created_at DESC
            LIMIT ?
        """,
            (limit,),
        )

        results = cursor.fetchall()

        if results:
            print(f"📅 RECENT REPORTS (Last {limit})")
            print("-" * 80)
            print(f"{'ID':4s} {'Third Party':20s} {'Report Type':30s} {'Date':12s} {'Rows':8s} {'Status':10s}")
            print("-" * 80)

            for row in results:
                report_id, name, filename, report_type, report_date, row_count, status, created = row

                # Truncate long names
                name_short = name[:18] + ".." if len(name) > 20 else name
                type_short = (
                    (report_type or "Unknown")[:28] + ".."
                    if report_type and len(report_type) > 30
                    else (report_type or "Unknown")
                )

                print(
                    f"{report_id:4d} {name_short:20s} {type_short:30s} {report_date or 'N/A':12s} {row_count:8,} {status:10s}"
                )
            print()

    def print_reports_by_date(self, days=7):
        """Print reports from last N days"""
        cursor = self.db.conn.cursor()

        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        cursor.execute(
            """
            SELECT
                DATE(r.created_at) as date,
                COUNT(*) as count,
                SUM(r.row_count) as total_rows
            FROM reports r
            WHERE r.created_at >= ?
            GROUP BY DATE(r.created_at)
            ORDER BY date DESC
        """,
            (cutoff_date,),
        )

        results = cursor.fetchall()

        if results:
            print(f"📆 REPORTS BY DATE (Last {days} days)")
            print("-" * 80)
            print(f"{'Date':12s} {'Reports':10s} {'Total Rows':12s}")
            print("-" * 80)

            for date, count, rows in results:
                print(f"{date:12s} {count:10d} {rows:12,}")
            print()
        else:
            print(f"📆 REPORTS BY DATE (Last {days} days)")
            print("-" * 80)
            print(f"  No reports found in the last {days} days")
            print()

    def print_status_breakdown(self):
        """Print breakdown by status"""
        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT
                status,
                COUNT(*) as count
            FROM reports
            GROUP BY status
            ORDER BY count DESC
        """)

        results = cursor.fetchall()

        if results:
            print("✅ STATUS BREAKDOWN")
            print("-" * 80)
            for status, count in results:
                print(f"  {status:15s} {count:5d} reports")
            print()

    def search_reports(self, search_term):
        """Search reports by filename or type"""
        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                r.id,
                tp.name,
                r.file_name,
                r.report_type,
                r.report_date,
                r.row_count,
                r.status
            FROM reports r
            JOIN third_parties tp ON r.third_party_id = tp.id
            WHERE r.file_name LIKE ? OR r.report_type LIKE ?
            ORDER BY r.created_at DESC
        """,
            (f"%{search_term}%", f"%{search_term}%"),
        )

        results = cursor.fetchall()

        if results:
            print(f"\n🔍 SEARCH RESULTS for '{search_term}'")
            print("-" * 80)
            print(f"{'ID':4s} {'Third Party':20s} {'Report Type':30s} {'Date':12s} {'Rows':8s}")
            print("-" * 80)

            for row in results:
                report_id, name, filename, report_type, report_date, row_count, status = row

                name_short = name[:18] + ".." if len(name) > 20 else name
                type_short = (
                    (report_type or "Unknown")[:28] + ".."
                    if report_type and len(report_type) > 30
                    else (report_type or "Unknown")
                )

                print(f"{report_id:4d} {name_short:20s} {type_short:30s} {report_date or 'N/A':12s} {row_count:8,}")
            print(f"\nFound {len(results)} matching reports\n")
        else:
            print(f"\n🔍 No reports found matching '{search_term}'\n")

    def show_report_detail(self, report_id):
        """Show detailed information about a specific report"""
        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                r.id,
                tp.name,
                tp.email,
                r.file_name,
                r.file_path,
                r.report_type,
                r.report_date,
                r.row_count,
                r.status,
                r.created_at
            FROM reports r
            JOIN third_parties tp ON r.third_party_id = tp.id
            WHERE r.id = ?
        """,
            (report_id,),
        )

        result = cursor.fetchone()

        if result:
            report_id, name, email, filename, filepath, report_type, report_date, row_count, status, created = result

            print(f"\n📄 REPORT DETAILS - ID {report_id}")
            print("-" * 80)
            print(f"  Third Party:   {name}")
            print(f"  Email:         {email}")
            print(f"  File Name:     {filename}")
            print(f"  File Path:     {filepath or 'N/A'}")
            print(f"  Report Type:   {report_type or 'Unknown'}")
            print(f"  Report Date:   {report_date or 'N/A'}")
            print(f"  Row Count:     {row_count:,}")
            print(f"  Status:        {status}")
            print(f"  Ingested:      {created}")

            # Get sample data
            cursor.execute(
                """
                SELECT data
                FROM report_data
                WHERE report_id = ?
                LIMIT 3
            """,
                (report_id,),
            )

            samples = cursor.fetchall()
            if samples:
                print("\n  Sample Data (first 3 rows):")
                for i, (data,) in enumerate(samples, 1):
                    print(f"    Row {i}: {data[:100]}..." if len(data) > 100 else f"    Row {i}: {data}")

            print()
        else:
            print(f"\n❌ Report ID {report_id} not found\n")

    def print_available_exports(self):
        """Print available export files and actions"""
        print("📥 AVAILABLE EXPORTS & ACTIONS")
        print("-" * 80)

        # Check exports directory
        exports_dir = Path("exports")
        if exports_dir.exists():
            export_files = list(exports_dir.glob("*"))
            if export_files:
                print("\n  📁 Available Export Files:")
                for f in sorted(export_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                    size = f.stat().st_size
                    size_str = f"{size:,} bytes" if size < 1024 * 1024 else f"{size / (1024 * 1024):.1f} MB"
                    mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    print(f"    • {f.name:40s} {size_str:15s} {mtime}")
            else:
                print("\n  📁 No export files yet")
        else:
            print("\n  📁 No export files yet")

        # Show available actions
        print("\n  🎯 Available Actions:")
        print("    1. Export to CSV       → python3 wigeon.py export --output data.csv --format csv")
        print("    2. Export to Excel     → python3 wigeon.py export --output data.xlsx --format excel")
        print("    3. Export to JSON      → python3 wigeon.py export --output data.json --format json")
        print("    4. Export by vendor    → python3 wigeon.py export --third-party 'Vendor Name' --output vendor.csv")
        print("    5. Query specific data → python3 wigeon.py query --report-id 8 --limit 100")
        print("    6. List all reports    → python3 wigeon.py list")
        print("    7. Search reports      → python3 wigeon.py dashboard --search 'inventory'")

        # Show SQL export info
        print("\n  🗄️  SQL Export Options:")
        print("    • Database location: database/wigeon.db")
        print("    • Direct SQL access: sqlite3 database/wigeon.db")
        print("    • Export to SQL:     sqlite3 database/wigeon.db .dump > wigeon_backup.sql")
        print("    • View schema:       sqlite3 database/wigeon.db .schema")

        # Show data stats for exports
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM report_data")
        total_rows = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT report_id) FROM report_data")
        total_reports = cursor.fetchone()[0]

        print("\n  📊 Export Data Available:")
        print(f"    • Total data rows: {total_rows:,}")
        print(f"    • Reports with data: {total_reports}")
        print(f"    • Database size: {self._get_db_size()}")
        print()

    def _get_db_size(self):
        """Get database file size"""
        db_path = Path("database/wigeon.db")
        if db_path.exists():
            size = db_path.stat().st_size
            if size < 1024:
                return f"{size} bytes"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        return "Unknown"

    def show_full_dashboard(self):
        """Show complete dashboard"""
        self.print_header()
        self.print_summary_stats()
        self.print_third_party_breakdown()
        self.print_report_types()
        self.print_status_breakdown()
        self.print_reports_by_date(days=7)
        self.print_recent_reports(limit=10)
        self.print_available_exports()

    def interactive_mode(self):
        """Interactive dashboard mode"""
        while True:
            print("\n" + "=" * 80)
            print("🦆 WIGEON DASHBOARD - Interactive Mode")
            print("=" * 80)
            print("\nOptions:")
            print("  1. Show full dashboard")
            print("  2. Show summary statistics")
            print("  3. Show recent reports")
            print("  4. Show reports by third party")
            print("  5. Show reports by type")
            print("  6. Show reports by date")
            print("  7. Search reports")
            print("  8. View report details")
            print("  9. Exit")

            choice = input("\nSelect option (1-9): ").strip()

            if choice == "1":
                self.show_full_dashboard()
            elif choice == "2":
                self.print_header()
                self.print_summary_stats()
            elif choice == "3":
                limit = input("How many reports? (default 10): ").strip()
                limit = int(limit) if limit.isdigit() else 10
                self.print_header()
                self.print_recent_reports(limit=limit)
            elif choice == "4":
                self.print_header()
                self.print_third_party_breakdown()
            elif choice == "5":
                self.print_header()
                self.print_report_types()
            elif choice == "6":
                days = input("How many days? (default 7): ").strip()
                days = int(days) if days.isdigit() else 7
                self.print_header()
                self.print_reports_by_date(days=days)
            elif choice == "7":
                search_term = input("Enter search term: ").strip()
                if search_term:
                    self.search_reports(search_term)
            elif choice == "8":
                report_id = input("Enter report ID: ").strip()
                if report_id.isdigit():
                    self.show_report_detail(int(report_id))
            elif choice == "9":
                print("\n👋 Goodbye!\n")
                break
            else:
                print("\n❌ Invalid option. Please select 1-9.\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="WIGEON Dashboard - Interactive Report Viewer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show full dashboard
  python3 dashboard.py

  # Interactive mode
  python3 dashboard.py --interactive

  # Show recent reports
  python3 dashboard.py --recent 20

  # Search reports
  python3 dashboard.py --search "Block Open Orders"

  # Show report details
  python3 dashboard.py --detail 5

  # Show reports from last 14 days
  python3 dashboard.py --days 14
        """,
    )

    parser.add_argument(
        "--db", default="database/wigeon.db", help="Path to database file (default: database/wigeon.db)"
    )
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode")
    parser.add_argument("--recent", type=int, metavar="N", help="Show N most recent reports")
    parser.add_argument("--search", metavar="TERM", help="Search reports by filename or type")
    parser.add_argument("--detail", type=int, metavar="ID", help="Show details for report ID")
    parser.add_argument("--days", type=int, metavar="N", help="Show reports from last N days")

    args = parser.parse_args()

    # Initialize dashboard
    dashboard = WigeonDashboard(args.db)

    # Handle different modes
    if args.interactive:
        dashboard.interactive_mode()
    elif args.recent:
        dashboard.print_header()
        dashboard.print_recent_reports(limit=args.recent)
    elif args.search:
        dashboard.search_reports(args.search)
    elif args.detail:
        dashboard.show_report_detail(args.detail)
    elif args.days:
        dashboard.print_header()
        dashboard.print_reports_by_date(days=args.days)
    else:
        # Default: show full dashboard
        dashboard.show_full_dashboard()


if __name__ == "__main__":
    main()
