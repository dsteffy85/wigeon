#!/usr/bin/env python3
"""
Integration tests for WIGEON WigeonProcessor
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from wigeon_processor import WigeonProcessor


@pytest.fixture
def processor(tmp_path):
    """Create a WigeonProcessor with a temp database."""
    db_path = str(tmp_path / "database" / "test.db")
    proc = WigeonProcessor(db_path=db_path)
    yield proc
    proc.close()


# ===================================================================
# File Processing (end-to-end)
# ===================================================================

class TestProcessFile:
    """Integration tests for process_file."""

    def test_process_csv(self, processor, sample_csv):
        result = processor.process_file(
            file_path=str(sample_csv),
            third_party_name="CSV Vendor",
            third_party_email="csv@vendor.com",
        )
        assert result["success"] is True
        assert result["row_count"] == 3
        assert result["file_format"] == "csv"
        assert result["report_id"] > 0
        assert result["third_party_id"] > 0

    def test_process_xlsx(self, processor, sample_xlsx):
        result = processor.process_file(
            file_path=str(sample_xlsx),
            third_party_name="Excel Vendor",
            third_party_email="excel@vendor.com",
        )
        assert result["success"] is True
        assert result["row_count"] == 3
        assert result["file_format"] == "xlsx"

    def test_process_xml(self, processor, sample_xml):
        result = processor.process_file(
            file_path=str(sample_xml),
            third_party_name="XML Vendor",
            third_party_email="xml@vendor.com",
        )
        assert result["success"] is True
        assert result["row_count"] == 3
        assert result["file_format"] == "xml"

    def test_process_zip_with_xlsx(self, processor, sample_zip_with_xlsx):
        result = processor.process_file(
            file_path=str(sample_zip_with_xlsx),
            third_party_name="Zip Vendor",
            third_party_email="zip@vendor.com",
        )
        assert result["success"] is True
        assert result["row_count"] == 3
        assert result["file_format"] == "zip"

    def test_process_nonexistent_file(self, processor):
        result = processor.process_file(
            file_path="/nonexistent/file.csv",
            third_party_name="Bad Vendor",
            third_party_email="bad@vendor.com",
        )
        assert result["success"] is False
        assert "not found" in result["error"].lower() or "File not found" in result["error"]

    def test_process_with_optional_fields(self, processor, sample_csv):
        result = processor.process_file(
            file_path=str(sample_csv),
            third_party_name="Full Vendor",
            third_party_email="full@vendor.com",
            report_type="inventory_snapshot",
            report_date="2026-03-11",
            email_subject="Daily Inventory Report",
            email_date="2026-03-11T08:00:00",
            metadata={"source": "automated"},
        )
        assert result["success"] is True
        assert result["row_count"] == 3

    def test_process_empty_csv(self, processor, empty_csv):
        result = processor.process_file(
            file_path=str(empty_csv),
            third_party_name="Empty Vendor",
            third_party_email="empty@vendor.com",
        )
        assert result["success"] is True
        assert result["row_count"] == 0

    def test_reuses_existing_third_party(self, processor, sample_csv, sample_xlsx):
        """Processing two files from the same vendor should reuse the third-party record."""
        r1 = processor.process_file(
            file_path=str(sample_csv),
            third_party_name="Repeat Vendor",
            third_party_email="repeat@vendor.com",
        )
        r2 = processor.process_file(
            file_path=str(sample_xlsx),
            third_party_name="Repeat Vendor",
            third_party_email="repeat@vendor.com",
        )
        assert r1["success"] and r2["success"]
        assert r1["third_party_id"] == r2["third_party_id"]

    def test_auto_report_type(self, processor, sample_csv):
        """When report_type is not given, it should be auto-generated from format."""
        result = processor.process_file(
            file_path=str(sample_csv),
            third_party_name="Auto Vendor",
            third_party_email="auto@vendor.com",
        )
        assert result["success"] is True
        # Verify the report was stored with auto-generated type
        reports = processor.query_reports(third_party_name="Auto Vendor")
        assert len(reports) == 1
        assert "csv" in reports[0]["report_type"]


# ===================================================================
# Query & Export
# ===================================================================

class TestQueryAndExport:
    """Tests for querying and exporting data."""

    def test_query_reports(self, processor, sample_csv):
        processor.process_file(
            file_path=str(sample_csv),
            third_party_name="Query Vendor",
            third_party_email="query@vendor.com",
            report_type="test_report",
        )
        reports = processor.query_reports(third_party_name="Query Vendor")
        assert len(reports) == 1
        assert reports[0]["report_type"] == "test_report"

    def test_query_data(self, processor, sample_csv):
        processor.process_file(
            file_path=str(sample_csv),
            third_party_name="Data Vendor",
            third_party_email="data@vendor.com",
        )
        data = processor.query_data(third_party_name="Data Vendor")
        assert len(data) == 3
        assert data[0]["data"]["SKU"] == "A-SKU-0001"

    def test_query_data_with_limit(self, processor, sample_csv):
        processor.process_file(
            file_path=str(sample_csv),
            third_party_name="Limit Vendor",
            third_party_email="limit@vendor.com",
        )
        data = processor.query_data(third_party_name="Limit Vendor", limit=2)
        assert len(data) == 2

    def test_export_csv(self, processor, sample_csv, tmp_path):
        processor.process_file(
            file_path=str(sample_csv),
            third_party_name="Export Vendor",
            third_party_email="export@vendor.com",
        )
        output = tmp_path / "export.csv"
        result = processor.export_data(str(output), third_party_name="Export Vendor", format="csv")
        assert result is True
        assert output.exists()
        lines = output.read_text().strip().split("\n")
        assert len(lines) == 4  # header + 3 rows

    def test_export_json(self, processor, sample_csv, tmp_path):
        processor.process_file(
            file_path=str(sample_csv),
            third_party_name="JSON Vendor",
            third_party_email="json@vendor.com",
        )
        output = tmp_path / "export.json"
        result = processor.export_data(str(output), third_party_name="JSON Vendor", format="json")
        assert result is True
        data = json.loads(output.read_text())
        assert len(data) == 3

    def test_export_no_data(self, processor, tmp_path):
        output = tmp_path / "empty_export.csv"
        result = processor.export_data(str(output), third_party_name="Nobody")
        assert result is False

    def test_export_unsupported_format(self, processor, sample_csv, tmp_path):
        processor.process_file(
            file_path=str(sample_csv),
            third_party_name="Bad Format",
            third_party_email="bad@format.com",
        )
        output = tmp_path / "export.parquet"
        result = processor.export_data(str(output), third_party_name="Bad Format", format="parquet")
        assert result is False


# ===================================================================
# Statistics
# ===================================================================

class TestProcessorStats:
    """Tests for get_statistics via processor."""

    def test_empty_stats(self, processor):
        stats = processor.get_statistics()
        assert stats["third_parties"] == 0
        assert stats["total_reports"] == 0
        assert stats["total_data_rows"] == 0

    def test_stats_after_processing(self, processor, sample_csv, sample_xlsx):
        processor.process_file(
            file_path=str(sample_csv),
            third_party_name="Stats Vendor A",
            third_party_email="a@stats.com",
        )
        processor.process_file(
            file_path=str(sample_xlsx),
            third_party_name="Stats Vendor B",
            third_party_email="b@stats.com",
        )
        stats = processor.get_statistics()
        assert stats["third_parties"] == 2
        assert stats["total_reports"] == 2
        assert stats["total_data_rows"] == 6  # 3 + 3
