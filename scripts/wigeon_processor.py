#!/usr/bin/env python3
"""
WIGEON Processor
Main processing engine for email report ingestion
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database_schema import WigeonDatabase
from file_parser import FileParser, normalize_data


class WigeonProcessor:
    """Main WIGEON processing engine"""

    def __init__(self, db_path="database/wigeon.db"):
        self.db = WigeonDatabase(db_path)
        self.project_root = Path(__file__).parent.parent

    def process_file(
        self,
        file_path,
        third_party_name,
        third_party_email,
        report_type=None,
        report_date=None,
        email_subject=None,
        email_date=None,
        metadata=None,
    ):
        """
        Process a single file and store in database

        Args:
            file_path: Path to file to process
            third_party_name: Name of third-party company
            third_party_email: Email address of third-party
            report_type: Type/category of report (optional)
            report_date: Date of report (optional)
            email_subject: Email subject line (optional)
            email_date: Email received date (optional)
            metadata: Additional metadata dictionary (optional)

        Returns:
            dict: Processing results
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return {"success": False, "error": f"File not found: {file_path}"}

        print(f"\n🦆 Processing: {file_path.name}")
        print(f"   Third-party: {third_party_name} ({third_party_email})")

        try:
            # 1. Ensure third-party exists in database
            third_party = self.db.get_third_party(name=third_party_name)
            if not third_party:
                print("   Creating new third-party record...")
                third_party_id = self.db.add_third_party(
                    name=third_party_name, email=third_party_email, description="Auto-created from report ingestion"
                )
            else:
                third_party_id = third_party["id"]
                print(f"   Using existing third-party (ID: {third_party_id})")

            # 2. Parse file
            print("   Parsing file...")
            parser = FileParser(file_path)
            parsed_data = parser.parse()

            # 3. Create report record
            file_format = file_path.suffix.lower().replace(".", "")
            if not report_type:
                report_type = f"{file_format}_report"

            if not report_date:
                # Try to extract date from filename or use today
                report_date = datetime.now().date().isoformat()

            report_id = self.db.add_report(
                third_party_id=third_party_id,
                report_type=report_type,
                file_name=file_path.name,
                file_path=str(file_path.absolute()),
                file_format=file_format,
                report_date=report_date,
                email_subject=email_subject,
                email_date=email_date,
                metadata=metadata,
            )

            print(f"   Created report record (ID: {report_id})")

            # 4. Normalize and store data
            print("   Normalizing data...")
            normalized_rows = normalize_data(parsed_data, third_party_name)

            if normalized_rows:
                print(f"   Storing {len(normalized_rows)} rows...")
                row_count = self.db.add_report_data(
                    report_id=report_id, third_party_id=third_party_id, data_rows=normalized_rows
                )

                # Update report status
                self.db.update_report_status(report_id=report_id, status="processed", row_count=row_count)

                print(f"   ✅ Successfully processed {row_count} rows")
            else:
                self.db.update_report_status(report_id=report_id, status="processed", row_count=0)
                print("   ⚠️  No data rows found in file")

            return {
                "success": True,
                "report_id": report_id,
                "third_party_id": third_party_id,
                "third_party_name": third_party_name,
                "row_count": len(normalized_rows),
                "file_format": file_format,
                "parsed_data_summary": {
                    "format": parsed_data.get("format"),
                    "total_rows": parsed_data.get("total_rows") or parsed_data.get("row_count", 0),
                },
            }

        except Exception as e:
            error_msg = str(e)
            print(f"   ❌ Error: {error_msg}")

            # Update report status if report was created
            if "report_id" in locals():
                self.db.update_report_status(report_id=report_id, status="failed", error_message=error_msg)

            return {"success": False, "error": error_msg}

    def query_reports(self, third_party_name=None, report_type=None, start_date=None, end_date=None, status=None):
        """Query reports with filters"""
        return self.db.query_reports(
            third_party_name=third_party_name,
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            status=status,
        )

    def query_data(self, report_id=None, third_party_name=None, limit=100, offset=0):
        """Query report data"""
        return self.db.query_report_data(
            report_id=report_id, third_party_name=third_party_name, limit=limit, offset=offset
        )

    def export_data(self, output_path, report_id=None, third_party_name=None, format="csv"):
        """
        Export data to file

        Args:
            output_path: Path to output file
            report_id: Filter by report ID (optional)
            third_party_name: Filter by third-party name (optional)
            format: Output format ('csv', 'json', 'excel')
        """
        data = self.query_data(report_id=report_id, third_party_name=third_party_name, limit=None)

        if not data:
            print("⚠️  No data to export")
            return False

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            with open(output_path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✅ Exported {len(data)} rows to {output_path}")
            return True

        elif format == "csv":
            import csv

            # Extract all unique keys from data
            all_keys = set()
            for row in data:
                all_keys.update(row["data"].keys())

            fieldnames = ["report_id", "third_party_name", "report_type", "report_date", "row_number"] + sorted(
                all_keys
            )

            with open(output_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for row in data:
                    flat_row = {
                        "report_id": row["report_id"],
                        "third_party_name": row["third_party_name"],
                        "report_type": row["report_type"],
                        "report_date": row["report_date"],
                        "row_number": row["row_number"],
                    }
                    flat_row.update(row["data"])
                    writer.writerow(flat_row)

            print(f"✅ Exported {len(data)} rows to {output_path}")
            return True

        elif format == "excel":
            try:
                from openpyxl import Workbook

                wb = Workbook()
                ws = wb.active
                ws.title = "WIGEON Export"

                # Extract headers
                all_keys = set()
                for row in data:
                    all_keys.update(row["data"].keys())

                headers = ["report_id", "third_party_name", "report_type", "report_date", "row_number"] + sorted(
                    all_keys
                )
                ws.append(headers)

                # Write data
                for row in data:
                    row_values = [
                        row["report_id"],
                        row["third_party_name"],
                        row["report_type"],
                        row["report_date"],
                        row["row_number"],
                    ]
                    for key in sorted(all_keys):
                        row_values.append(row["data"].get(key, ""))
                    ws.append(row_values)

                wb.save(output_path)
                print(f"✅ Exported {len(data)} rows to {output_path}")
                return True

            except ImportError:
                print("❌ openpyxl required for Excel export. Install: pip install openpyxl")
                return False

        else:
            print(f"❌ Unsupported format: {format}")
            return False

    def get_statistics(self):
        """Get database statistics"""
        return self.db.get_statistics()

    def close(self):
        """Close database connection"""
        self.db.close()


if __name__ == "__main__":
    # Test processor
    processor = WigeonProcessor()

    print("\n🦆 WIGEON Processor - Ready")
    print("\n📊 Current Statistics:")
    stats = processor.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    processor.close()
