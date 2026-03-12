#!/usr/bin/env python3
"""
🦆 WIGEON - Workflow Intelligence for Gathering Email-Originated Notifications

Main command-line interface for WIGEON agent
Users invoke this through Goose to process email reports
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from wigeon_processor import WigeonProcessor


def print_banner():
    """Print WIGEON banner"""
    print("""
    🦆 WIGEON v1.2.0
    Workflow Intelligence for Gathering Email-Originated Notifications
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)


def cmd_ingest(args):
    """Ingest a report file"""
    processor = WigeonProcessor()
    
    print(f"\n📥 INGESTING REPORT")
    print(f"   File: {args.file}")
    print(f"   Third-party: {args.third_party}")
    print(f"   Email: {args.email}")
    
    result = processor.process_file(
        file_path=args.file,
        third_party_name=args.third_party,
        third_party_email=args.email,
        report_type=args.report_type,
        report_date=args.report_date,
        email_subject=args.subject,
        email_date=args.email_date,
        metadata={'notes': args.notes} if args.notes else None
    )
    
    if result['success']:
        print(f"\n✅ SUCCESS!")
        print(f"   Report ID: {result['report_id']}")
        print(f"   Rows stored: {result['row_count']}")
        print(f"   Format: {result['file_format']}")
    else:
        print(f"\n❌ FAILED: {result['error']}")
    
    processor.close()
    return 0 if result['success'] else 1


def cmd_list(args):
    """List reports"""
    processor = WigeonProcessor()
    
    print(f"\n📋 REPORTS")
    
    reports = processor.query_reports(
        third_party_name=args.third_party,
        report_type=args.report_type,
        start_date=args.start_date,
        end_date=args.end_date,
        status=args.status
    )
    
    if not reports:
        print("   No reports found")
        processor.close()
        return 0
    
    print(f"   Found {len(reports)} report(s)\n")
    
    for report in reports:
        print(f"   Report ID: {report['id']}")
        print(f"   Third-party: {report['third_party_name']} ({report['third_party_email']})")
        print(f"   Type: {report['report_type']}")
        print(f"   Date: {report['report_date']}")
        print(f"   File: {report['file_name']}")
        print(f"   Status: {report['status']}")
        print(f"   Rows: {report['row_count']}")
        if report['email_subject']:
            print(f"   Email: {report['email_subject']}")
        print(f"   Created: {report['created_at']}")
        print()
    
    processor.close()
    return 0


def cmd_query(args):
    """Query report data"""
    processor = WigeonProcessor()
    
    print(f"\n🔍 QUERYING DATA")
    
    data = processor.query_data(
        report_id=args.report_id,
        third_party_name=args.third_party,
        limit=args.limit,
        offset=args.offset
    )
    
    if not data:
        print("   No data found")
        processor.close()
        return 0
    
    print(f"   Found {len(data)} row(s)\n")
    
    if args.format == 'json':
        print(json.dumps(data, indent=2))
    else:
        # Table format
        for idx, row in enumerate(data, 1):
            print(f"   Row {idx}:")
            print(f"     Report ID: {row['report_id']}")
            print(f"     Third-party: {row['third_party_name']}")
            print(f"     Report Type: {row['report_type']}")
            print(f"     Report Date: {row['report_date']}")
            print(f"     Data: {json.dumps(row['data'], indent=6)}")
            print()
    
    processor.close()
    return 0


def cmd_export(args):
    """Export data to file"""
    processor = WigeonProcessor()
    
    print(f"\n📤 EXPORTING DATA")
    print(f"   Output: {args.output}")
    print(f"   Format: {args.format}")
    
    success = processor.export_data(
        output_path=args.output,
        report_id=args.report_id,
        third_party_name=args.third_party,
        format=args.format
    )
    
    processor.close()
    return 0 if success else 1


def cmd_stats(args):
    """Show statistics"""
    processor = WigeonProcessor()
    
    print(f"\n📊 WIGEON STATISTICS")
    
    stats = processor.get_statistics()
    
    print(f"\n   Third-parties: {stats['third_parties']}")
    print(f"   Total reports: {stats['total_reports']}")
    print(f"   Total data rows: {stats['total_data_rows']}")
    
    if stats['reports_by_status']:
        print(f"\n   Reports by status:")
        for status, count in stats['reports_by_status'].items():
            print(f"     {status}: {count}")
    
    if stats['reports_by_third_party']:
        print(f"\n   Reports by third-party:")
        for name, count in stats['reports_by_third_party'].items():
            print(f"     {name}: {count}")
    
    print()
    processor.close()
    return 0


def cmd_dashboard(args):
    """Show dashboard"""
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
    else:
        # Default: show full dashboard
        dashboard.show_full_dashboard()
    
    return 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='🦆 WIGEON - Email Report Data Integration Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ingest a report
  python wigeon.py ingest --file report.xlsx --third-party "Acme Corp" --email vendor@acme.com
  
  # List all reports
  python wigeon.py list
  
  # List reports from specific third-party
  python wigeon.py list --third-party "Acme Corp"
  
  # Query data from a report
  python wigeon.py query --report-id 1
  
  # Export data to CSV
  python wigeon.py export --output data.csv --third-party "Acme Corp"
  
  # Show statistics
  python wigeon.py stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest a report file')
    ingest_parser.add_argument('--file', required=True, help='Path to report file')
    ingest_parser.add_argument('--third-party', required=True, help='Third-party company name')
    ingest_parser.add_argument('--email', required=True, help='Third-party email address')
    ingest_parser.add_argument('--report-type', help='Report type/category')
    ingest_parser.add_argument('--report-date', help='Report date (YYYY-MM-DD)')
    ingest_parser.add_argument('--subject', help='Email subject line')
    ingest_parser.add_argument('--email-date', help='Email received date (YYYY-MM-DD)')
    ingest_parser.add_argument('--notes', help='Additional notes')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List reports')
    list_parser.add_argument('--third-party', help='Filter by third-party name')
    list_parser.add_argument('--report-type', help='Filter by report type')
    list_parser.add_argument('--start-date', help='Filter by start date (YYYY-MM-DD)')
    list_parser.add_argument('--end-date', help='Filter by end date (YYYY-MM-DD)')
    list_parser.add_argument('--status', choices=['pending', 'processed', 'failed'], help='Filter by status')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query report data')
    query_parser.add_argument('--report-id', type=int, help='Filter by report ID')
    query_parser.add_argument('--third-party', help='Filter by third-party name')
    query_parser.add_argument('--limit', type=int, default=100, help='Limit results (default: 100)')
    query_parser.add_argument('--offset', type=int, default=0, help='Offset results (default: 0)')
    query_parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to file')
    export_parser.add_argument('--output', required=True, help='Output file path')
    export_parser.add_argument('--report-id', type=int, help='Filter by report ID')
    export_parser.add_argument('--third-party', help='Filter by third-party name')
    export_parser.add_argument('--format', choices=['csv', 'json', 'excel'], default='csv', help='Output format')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Show interactive dashboard')
    dashboard_parser.add_argument('--interactive', '-i', action='store_true',
                                  help='Start interactive mode')
    dashboard_parser.add_argument('--recent', type=int, metavar='N',
                                  help='Show N most recent reports')
    dashboard_parser.add_argument('--search', metavar='TERM',
                                  help='Search reports')
    dashboard_parser.add_argument('--days', type=int, metavar='N',
                                  help='Show reports from last N days')
    
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        parser.print_help()
        return 0
    
    print_banner()
    
    # Route to command handler
    if args.command == 'ingest':
        return cmd_ingest(args)
    elif args.command == 'list':
        return cmd_list(args)
    elif args.command == 'query':
        return cmd_query(args)
    elif args.command == 'export':
        return cmd_export(args)
    elif args.command == 'stats':
        return cmd_stats(args)
    elif args.command == 'dashboard':
        return cmd_dashboard(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
