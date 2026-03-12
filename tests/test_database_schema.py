#!/usr/bin/env python3
"""
Unit tests for WIGEON WigeonDatabase
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from database_schema import WigeonDatabase

# ===================================================================
# Schema & Initialization
# ===================================================================


class TestDatabaseInit:
    """Tests for database creation and schema."""

    def test_creates_database_file(self, tmp_path):
        db_path = tmp_path / "db" / "test.db"
        db = WigeonDatabase(str(db_path))
        assert db_path.exists()
        db.close()

    def test_creates_parent_directories(self, tmp_path):
        db_path = tmp_path / "deep" / "nested" / "dir" / "test.db"
        db = WigeonDatabase(str(db_path))
        assert db_path.parent.exists()
        db.close()

    def test_tables_exist(self, tmp_db):
        cursor = tmp_db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = {row["name"] for row in cursor.fetchall()}
        assert "third_parties" in tables
        assert "reports" in tables
        assert "report_data" in tables

    def test_indexes_exist(self, tmp_db):
        cursor = tmp_db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = {row["name"] for row in cursor.fetchall()}
        assert "idx_reports_third_party" in indexes
        assert "idx_reports_date" in indexes
        assert "idx_report_data_report" in indexes
        assert "idx_report_data_third_party" in indexes

    def test_idempotent_schema_creation(self, tmp_path):
        """Creating schema twice should not raise."""
        db_path = tmp_path / "test.db"
        db = WigeonDatabase(str(db_path))
        db.create_schema()  # second call
        db.close()


# ===================================================================
# Third-Party CRUD
# ===================================================================


class TestThirdParty:
    """Tests for third-party management."""

    def test_add_third_party(self, tmp_db):
        tp_id = tmp_db.add_third_party(
            name="Acme Corp",
            email="vendor@acme.com",
            description="Test vendor",
        )
        assert tp_id is not None
        assert tp_id > 0

    def test_get_third_party_by_name(self, tmp_db):
        tmp_db.add_third_party(name="Acme Corp", email="vendor@acme.com")
        tp = tmp_db.get_third_party(name="Acme Corp")
        assert tp is not None
        assert tp["name"] == "Acme Corp"
        assert tp["email"] == "vendor@acme.com"

    def test_get_third_party_by_email(self, tmp_db):
        tmp_db.add_third_party(name="Acme Corp", email="vendor@acme.com")
        tp = tmp_db.get_third_party(email="vendor@acme.com")
        assert tp is not None
        assert tp["name"] == "Acme Corp"

    def test_get_nonexistent_third_party(self, tmp_db):
        tp = tmp_db.get_third_party(name="Does Not Exist")
        assert tp is None

    def test_get_third_party_no_args(self, tmp_db):
        result = tmp_db.get_third_party()
        assert result is None

    def test_upsert_third_party(self, tmp_db):
        """Adding same name again should update, not duplicate."""
        tmp_db.add_third_party(name="Acme Corp", email="old@acme.com")
        tmp_db.add_third_party(name="Acme Corp", email="new@acme.com")

        tp = tmp_db.get_third_party(name="Acme Corp")
        assert tp["email"] == "new@acme.com"

    def test_third_party_with_metadata(self, tmp_db):
        meta = {"region": "US", "tier": "gold"}
        tmp_db.add_third_party(
            name="Acme Corp",
            email="vendor@acme.com",
            metadata=meta,
        )
        tp = tmp_db.get_third_party(name="Acme Corp")
        stored_meta = json.loads(tp["metadata"])
        assert stored_meta["region"] == "US"


# ===================================================================
# Report CRUD
# ===================================================================


class TestReports:
    """Tests for report management."""

    def test_add_report(self, tmp_db):
        tp_id = tmp_db.add_third_party(name="Acme", email="a@a.com")
        report_id = tmp_db.add_report(
            third_party_id=tp_id,
            report_type="inventory",
            file_name="report.xlsx",
            file_path="/tmp/report.xlsx",
            file_format="xlsx",
            report_date="2026-03-01",
        )
        assert report_id is not None
        assert report_id > 0

    def test_update_report_status(self, tmp_db):
        tp_id = tmp_db.add_third_party(name="Acme", email="a@a.com")
        report_id = tmp_db.add_report(
            third_party_id=tp_id,
            report_type="sales",
            file_name="sales.csv",
            file_path="/tmp/sales.csv",
            file_format="csv",
        )
        tmp_db.update_report_status(report_id, "processed", row_count=42)

        reports = tmp_db.query_reports()
        assert len(reports) == 1
        assert reports[0]["status"] == "processed"
        assert reports[0]["row_count"] == 42

    def test_update_report_status_failed(self, tmp_db):
        tp_id = tmp_db.add_third_party(name="Acme", email="a@a.com")
        report_id = tmp_db.add_report(
            third_party_id=tp_id,
            report_type="sales",
            file_name="bad.csv",
            file_path="/tmp/bad.csv",
            file_format="csv",
        )
        tmp_db.update_report_status(report_id, "failed", error_message="Parse error")

        reports = tmp_db.query_reports(status="failed")
        assert len(reports) == 1
        assert reports[0]["error_message"] == "Parse error"

    def test_query_reports_by_third_party(self, populated_db):
        db, tp_id, report_id = populated_db
        reports = db.query_reports(third_party_name="Acme Corp")
        assert len(reports) == 1
        assert reports[0]["third_party_name"] == "Acme Corp"

    def test_query_reports_by_status(self, populated_db):
        db, _, _ = populated_db
        reports = db.query_reports(status="processed")
        assert len(reports) == 1

    def test_query_reports_empty_result(self, populated_db):
        db, _, _ = populated_db
        reports = db.query_reports(third_party_name="Nonexistent")
        assert reports == []

    def test_query_reports_by_date_range(self, populated_db):
        db, _, _ = populated_db
        reports = db.query_reports(start_date="2026-01-01", end_date="2026-12-31")
        assert len(reports) == 1

        reports = db.query_reports(start_date="2027-01-01")
        assert len(reports) == 0


# ===================================================================
# Report Data
# ===================================================================


class TestReportData:
    """Tests for report data storage and retrieval."""

    def test_add_and_query_data(self, populated_db):
        db, _, report_id = populated_db
        data = db.query_report_data(report_id=report_id)
        assert len(data) == 2
        assert data[0]["data"]["SKU"] == "A-SKU-0001"
        assert data[1]["data"]["Qty"] == "250"

    def test_query_data_by_third_party(self, populated_db):
        db, _, _ = populated_db
        data = db.query_report_data(third_party_name="Acme Corp")
        assert len(data) == 2

    def test_query_data_with_limit(self, populated_db):
        db, _, report_id = populated_db
        data = db.query_report_data(report_id=report_id, limit=1)
        assert len(data) == 1

    def test_query_data_with_offset(self, populated_db):
        db, _, report_id = populated_db
        data = db.query_report_data(report_id=report_id, limit=1, offset=1)
        assert len(data) == 1
        assert data[0]["data"]["SKU"] == "A-SKU-0002"

    def test_query_data_empty(self, tmp_db):
        data = tmp_db.query_report_data(report_id=999)
        assert data == []

    def test_bulk_insert_many_rows(self, tmp_db):
        tp_id = tmp_db.add_third_party(name="Bulk", email="bulk@test.com")
        report_id = tmp_db.add_report(
            third_party_id=tp_id,
            report_type="big",
            file_name="big.csv",
            file_path="/tmp/big.csv",
            file_format="csv",
        )
        rows = [{"item": f"item_{i}", "qty": str(i)} for i in range(500)]
        count = tmp_db.add_report_data(report_id, tp_id, rows)
        assert count == 500

        data = tmp_db.query_report_data(report_id=report_id, limit=500)
        assert len(data) == 500

    def test_row_numbers_sequential(self, populated_db):
        db, _, report_id = populated_db
        data = db.query_report_data(report_id=report_id)
        row_numbers = [d["row_number"] for d in data]
        assert row_numbers == [1, 2]


# ===================================================================
# Statistics
# ===================================================================


class TestStatistics:
    """Tests for get_statistics."""

    def test_empty_database_stats(self, tmp_db):
        stats = tmp_db.get_statistics()
        assert stats["third_parties"] == 0
        assert stats["total_reports"] == 0
        assert stats["total_data_rows"] == 0

    def test_populated_stats(self, populated_db):
        db, _, _ = populated_db
        stats = db.get_statistics()
        assert stats["third_parties"] == 1
        assert stats["total_reports"] == 1
        assert stats["total_data_rows"] == 2
        assert stats["reports_by_status"]["processed"] == 1
        assert stats["reports_by_third_party"]["Acme Corp"] == 1

    def test_multiple_third_parties(self, tmp_db):
        tmp_db.add_third_party(name="Vendor A", email="a@test.com")
        tmp_db.add_third_party(name="Vendor B", email="b@test.com")
        tmp_db.add_third_party(name="Vendor C", email="c@test.com")
        stats = tmp_db.get_statistics()
        assert stats["third_parties"] == 3
