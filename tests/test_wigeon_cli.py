#!/usr/bin/env python3
"""
Tests for WIGEON CLI argument parsing and command routing
"""

import subprocess
import sys
from pathlib import Path

WIGEON_PY = str(Path(__file__).parent.parent / "wigeon.py")


def run_wigeon(*args, cwd=None):
    """Helper to invoke wigeon.py as a subprocess."""
    cmd = [sys.executable, WIGEON_PY] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd or str(Path(__file__).parent.parent),
        timeout=30,
    )
    return result


# ===================================================================
# Help & Banner
# ===================================================================


class TestCLIHelp:
    """Tests for help output and banner."""

    def test_no_args_shows_help(self):
        result = run_wigeon()
        assert result.returncode == 0
        assert "WIGEON" in result.stdout
        assert "ingest" in result.stdout
        assert "list" in result.stdout
        assert "query" in result.stdout
        assert "export" in result.stdout
        assert "stats" in result.stdout

    def test_help_flag(self):
        result = run_wigeon("--help")
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower() or "WIGEON" in result.stdout

    def test_ingest_help(self):
        result = run_wigeon("ingest", "--help")
        assert result.returncode == 0
        assert "--file" in result.stdout
        assert "--third-party" in result.stdout
        assert "--email" in result.stdout

    def test_list_help(self):
        result = run_wigeon("list", "--help")
        assert result.returncode == 0
        assert "--third-party" in result.stdout
        assert "--status" in result.stdout

    def test_query_help(self):
        result = run_wigeon("query", "--help")
        assert result.returncode == 0
        assert "--report-id" in result.stdout
        assert "--limit" in result.stdout
        assert "--format" in result.stdout

    def test_export_help(self):
        result = run_wigeon("export", "--help")
        assert result.returncode == 0
        assert "--output" in result.stdout
        assert "--format" in result.stdout

    def test_stats_help(self):
        result = run_wigeon("stats", "--help")
        assert result.returncode == 0

    def test_dashboard_help(self):
        result = run_wigeon("dashboard", "--help")
        assert result.returncode == 0
        assert "--interactive" in result.stdout
        assert "--recent" in result.stdout
        assert "--search" in result.stdout


# ===================================================================
# Ingest Command
# ===================================================================


class TestCLIIngest:
    """Tests for the ingest subcommand."""

    def test_ingest_csv(self, sample_csv, tmp_path):
        result = run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "Test Vendor",
            "--email",
            "test@vendor.com",
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert "SUCCESS" in result.stdout
        assert "3" in result.stdout  # 3 rows

    def test_ingest_with_all_options(self, sample_csv, tmp_path):
        result = run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "Full Vendor",
            "--email",
            "full@vendor.com",
            "--report-type",
            "inventory",
            "--report-date",
            "2026-03-11",
            "--subject",
            "Daily Report",
            "--notes",
            "Test run",
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert "SUCCESS" in result.stdout

    def test_ingest_missing_file(self, tmp_path):
        result = run_wigeon(
            "ingest",
            "--file",
            "/nonexistent/file.csv",
            "--third-party",
            "Bad Vendor",
            "--email",
            "bad@vendor.com",
            cwd=str(tmp_path),
        )
        assert result.returncode == 1
        assert "FAILED" in result.stdout

    def test_ingest_missing_required_args(self):
        result = run_wigeon("ingest", "--file", "test.csv")
        assert result.returncode != 0  # argparse error


# ===================================================================
# List Command
# ===================================================================


class TestCLIList:
    """Tests for the list subcommand."""

    def test_list_empty(self, tmp_path):
        result = run_wigeon("list", cwd=str(tmp_path))
        assert result.returncode == 0
        assert "No reports found" in result.stdout or "REPORTS" in result.stdout

    def test_list_after_ingest(self, sample_csv, tmp_path):
        run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "List Vendor",
            "--email",
            "list@vendor.com",
            cwd=str(tmp_path),
        )
        result = run_wigeon("list", cwd=str(tmp_path))
        assert result.returncode == 0
        assert "List Vendor" in result.stdout

    def test_list_with_filter(self, sample_csv, tmp_path):
        run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "Filter Vendor",
            "--email",
            "filter@vendor.com",
            cwd=str(tmp_path),
        )
        result = run_wigeon("list", "--third-party", "Filter Vendor", cwd=str(tmp_path))
        assert result.returncode == 0
        assert "Filter Vendor" in result.stdout

    def test_list_filter_no_match(self, sample_csv, tmp_path):
        run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "Real Vendor",
            "--email",
            "real@vendor.com",
            cwd=str(tmp_path),
        )
        result = run_wigeon("list", "--third-party", "Nonexistent", cwd=str(tmp_path))
        assert result.returncode == 0
        assert "No reports found" in result.stdout


# ===================================================================
# Query Command
# ===================================================================


class TestCLIQuery:
    """Tests for the query subcommand."""

    def test_query_empty(self, tmp_path):
        result = run_wigeon("query", cwd=str(tmp_path))
        assert result.returncode == 0
        assert "No data found" in result.stdout or "QUERYING" in result.stdout

    def test_query_after_ingest(self, sample_csv, tmp_path):
        run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "Query Vendor",
            "--email",
            "query@vendor.com",
            cwd=str(tmp_path),
        )
        result = run_wigeon(
            "query",
            "--third-party",
            "Query Vendor",
            "--limit",
            "2",
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert "2 row(s)" in result.stdout or "Row" in result.stdout

    def test_query_json_format(self, sample_csv, tmp_path):
        run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "JSON Vendor",
            "--email",
            "json@vendor.com",
            cwd=str(tmp_path),
        )
        result = run_wigeon(
            "query",
            "--third-party",
            "JSON Vendor",
            "--format",
            "json",
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        # Should contain valid JSON in the output
        assert "A-SKU-0001" in result.stdout


# ===================================================================
# Stats Command
# ===================================================================


class TestCLIStats:
    """Tests for the stats subcommand."""

    def test_stats_shows_output(self, tmp_path):
        result = run_wigeon("stats", cwd=str(tmp_path))
        assert result.returncode == 0
        assert "STATISTICS" in result.stdout
        assert "Third-parties:" in result.stdout
        assert "Total reports:" in result.stdout
        assert "Total data rows:" in result.stdout

    def test_stats_after_ingest(self, sample_csv, tmp_path):
        run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "Stats Vendor",
            "--email",
            "stats@vendor.com",
            cwd=str(tmp_path),
        )
        result = run_wigeon("stats", cwd=str(tmp_path))
        assert result.returncode == 0
        assert "STATISTICS" in result.stdout
        assert "Stats Vendor" in result.stdout


# ===================================================================
# Export Command
# ===================================================================


class TestCLIExport:
    """Tests for the export subcommand."""

    def test_export_csv(self, sample_csv, tmp_path):
        run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "ExportCSV Vendor",
            "--email",
            "exportcsv@vendor.com",
            cwd=str(tmp_path),
        )
        output = tmp_path / "output.csv"
        result = run_wigeon(
            "export",
            "--output",
            str(output),
            "--third-party",
            "ExportCSV Vendor",
            "--format",
            "csv",
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert output.exists()
        lines = output.read_text().strip().split("\n")
        assert len(lines) >= 4  # header + at least 3 rows
        # Verify header contains expected columns
        assert "SKU" in lines[0]
        assert "report_id" in lines[0]

    def test_export_json(self, sample_csv, tmp_path):
        run_wigeon(
            "ingest",
            "--file",
            str(sample_csv),
            "--third-party",
            "JSON Export",
            "--email",
            "jsonexport@vendor.com",
            cwd=str(tmp_path),
        )
        output = tmp_path / "output.json"
        result = run_wigeon(
            "export",
            "--output",
            str(output),
            "--format",
            "json",
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert output.exists()

    def test_export_no_data(self, tmp_path):
        output = tmp_path / "empty.csv"
        result = run_wigeon(
            "export",
            "--output",
            str(output),
            "--third-party",
            "Nobody",
            cwd=str(tmp_path),
        )
        assert result.returncode == 1
