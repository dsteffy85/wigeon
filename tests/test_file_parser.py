#!/usr/bin/env python3
"""
Unit tests for WIGEON FileParser and normalize_data
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from file_parser import FileParser, normalize_data


# ===================================================================
# CSV Parser Tests
# ===================================================================

class TestCSVParser:
    """Tests for CSV file parsing."""

    def test_parse_simple_csv(self, sample_csv):
        parser = FileParser(sample_csv)
        result = parser.parse()

        assert result["format"] == "csv"
        assert result["total_rows"] == 3
        assert result["sheet_count"] == 1
        assert "Sheet1" in result["sheets"]

        rows = result["sheets"]["Sheet1"]["rows"]
        assert len(rows) == 3
        assert rows[0]["SKU"] == "A-SKU-0001"
        assert rows[2]["Price"] == "22.00"

    def test_parse_pipe_delimited(self, sample_pipe_csv):
        parser = FileParser(sample_pipe_csv)
        result = parser.parse()

        assert result["format"] == "csv"
        assert result["total_rows"] == 2
        rows = result["sheets"]["Sheet1"]["rows"]
        assert rows[0]["Item Code"] == "A-SKU-0047"
        assert rows[1]["Qty"] == "120"

    def test_parse_tab_delimited(self, sample_tab_csv):
        parser = FileParser(sample_tab_csv)
        result = parser.parse()

        assert result["format"] == "csv"
        assert result["total_rows"] == 2
        rows = result["sheets"]["Sheet1"]["rows"]
        assert rows[0]["Name"] == "Alice"
        assert rows[1]["Email"] == "bob@example.com"

    def test_parse_empty_csv(self, empty_csv):
        parser = FileParser(empty_csv)
        result = parser.parse()

        assert result["format"] == "csv"
        assert result["total_rows"] == 0
        assert result["sheets"]["Sheet1"]["headers"] == ["Col1", "Col2", "Col3"]

    def test_csv_headers_preserved(self, sample_csv):
        parser = FileParser(sample_csv)
        result = parser.parse()
        headers = result["sheets"]["Sheet1"]["headers"]
        assert headers == ["SKU", "Description", "Quantity", "Price"]


# ===================================================================
# Excel (.xlsx) Parser Tests
# ===================================================================

class TestXLSXParser:
    """Tests for Excel .xlsx file parsing."""

    def test_parse_simple_xlsx(self, sample_xlsx):
        parser = FileParser(sample_xlsx)
        result = parser.parse()

        assert result["format"] == "xlsx"
        assert result["total_rows"] == 3
        assert "Inventory" in result["sheets"]

        rows = result["sheets"]["Inventory"]["rows"]
        assert len(rows) == 3
        assert rows[0]["SKU"] == "A-SKU-0001"
        assert rows[1]["Quantity"] == 250

    def test_parse_multi_sheet_xlsx(self, multi_sheet_xlsx):
        parser = FileParser(multi_sheet_xlsx)
        result = parser.parse()

        assert result["format"] == "xlsx"
        assert result["sheet_count"] == 2
        assert "Orders" in result["sheets"]
        assert "Returns" in result["sheets"]
        assert result["sheets"]["Orders"]["row_count"] == 2
        assert result["sheets"]["Returns"]["row_count"] == 1
        assert result["total_rows"] == 3

    def test_parse_empty_xlsx(self, empty_xlsx):
        parser = FileParser(empty_xlsx)
        result = parser.parse()

        assert result["format"] == "xlsx"
        assert result["total_rows"] == 0

    def test_xlsx_numeric_values(self, sample_xlsx):
        parser = FileParser(sample_xlsx)
        result = parser.parse()
        row = result["sheets"]["Inventory"]["rows"][0]
        assert row["Quantity"] == 100
        assert row["Price"] == 9.99


# ===================================================================
# XML Parser Tests
# ===================================================================

class TestXMLParser:
    """Tests for XML file parsing."""

    def test_parse_repeating_elements(self, sample_xml):
        parser = FileParser(sample_xml)
        result = parser.parse()

        assert result["format"] == "xml"
        assert result["root_tag"] == "shipments"
        assert result["row_count"] == 3

        rows = result["rows"]
        assert rows[0]["tracking"]["_text"] == "1Z999AA10123456784"
        assert rows[1]["carrier"]["_text"] == "USPS"

    def test_parse_nested_xml(self, nested_xml):
        parser = FileParser(nested_xml)
        result = parser.parse()

        assert result["format"] == "xml"
        assert result["row_count"] == 1
        data = result["rows"][0]
        assert "metadata" in data
        assert "summary" in data

    def test_malformed_xml_raises(self, malformed_xml):
        parser = FileParser(malformed_xml)
        with pytest.raises(Exception):
            parser.parse()

    def test_xml_attributes_captured(self, nested_xml):
        parser = FileParser(nested_xml)
        result = parser.parse()
        summary = result["rows"][0]["summary"]
        assert summary["total"] == "1500"
        assert summary["currency"] == "USD"


# ===================================================================
# ZIP Parser Tests
# ===================================================================

class TestZIPParser:
    """Tests for ZIP archive parsing."""

    def test_parse_zip_with_csv(self, sample_zip_with_csv):
        parser = FileParser(sample_zip_with_csv)
        result = parser.parse()

        assert result["format"] == "zip"
        assert result["file_count"] >= 1
        # CSV inside ZIP is not parsed by default (only xlsx/xml are)
        # but the file should be listed
        assert "inner_data.csv" in result["files"]

    def test_parse_zip_with_xlsx(self, sample_zip_with_xlsx):
        parser = FileParser(sample_zip_with_xlsx)
        result = parser.parse()

        assert result["format"] == "zip"
        assert "report.xlsx" in result["files"]
        inner = result["files"]["report.xlsx"]
        assert inner["format"] == "xlsx"
        assert inner["total_rows"] == 3

    def test_parse_zip_with_xml(self, sample_zip_with_xml):
        parser = FileParser(sample_zip_with_xml)
        result = parser.parse()

        assert result["format"] == "zip"
        assert "shipments.xml" in result["files"]
        inner = result["files"]["shipments.xml"]
        assert inner["format"] == "xml"
        assert inner["row_count"] == 3

    def test_parse_empty_zip(self, empty_zip):
        parser = FileParser(empty_zip)
        result = parser.parse()

        assert result["format"] == "zip"
        assert result["file_count"] == 0

    def test_zip_cleanup(self, sample_zip_with_xlsx):
        """Verify extracted temp directory is cleaned up."""
        parent = sample_zip_with_xlsx.parent
        parser = FileParser(sample_zip_with_xlsx)
        parser.parse()

        extracted_dirs = [d for d in parent.iterdir() if d.is_dir() and d.name.startswith("_extracted_")]
        assert len(extracted_dirs) == 0, "Temp extraction directory was not cleaned up"


# ===================================================================
# FileParser edge cases
# ===================================================================

class TestFileParserEdgeCases:
    """Edge cases and error handling."""

    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            FileParser(tmp_path / "nonexistent.csv")

    def test_unsupported_format(self, tmp_path):
        path = tmp_path / "data.parquet"
        path.write_text("fake")
        parser = FileParser(path)
        with pytest.raises(ValueError, match="Unsupported file format"):
            parser.parse()

    def test_get_summary(self, sample_csv):
        parser = FileParser(sample_csv)
        summary = parser.get_summary()

        assert summary["file_name"] == "sample.csv"
        assert summary["file_format"] == ".csv"
        assert summary["file_size"] > 0
        assert "modified_date" in summary


# ===================================================================
# normalize_data Tests
# ===================================================================

class TestNormalizeData:
    """Tests for the normalize_data helper."""

    def test_normalize_csv_data(self, sample_csv):
        parser = FileParser(sample_csv)
        parsed = parser.parse()
        rows = normalize_data(parsed, "TestVendor")

        assert len(rows) == 3
        assert rows[0]["_third_party"] == "TestVendor"
        assert rows[0]["_sheet"] == "Sheet1"
        assert rows[0]["SKU"] == "A-SKU-0001"

    def test_normalize_xlsx_data(self, sample_xlsx):
        parser = FileParser(sample_xlsx)
        parsed = parser.parse()
        rows = normalize_data(parsed, "ExcelVendor")

        assert len(rows) == 3
        assert all(r["_third_party"] == "ExcelVendor" for r in rows)

    def test_normalize_multi_sheet(self, multi_sheet_xlsx):
        parser = FileParser(multi_sheet_xlsx)
        parsed = parser.parse()
        rows = normalize_data(parsed, "MultiVendor")

        assert len(rows) == 3  # 2 orders + 1 return
        sheets = {r["_sheet"] for r in rows}
        assert "Orders" in sheets
        assert "Returns" in sheets

    def test_normalize_xml_data(self, sample_xml):
        parser = FileParser(sample_xml)
        parsed = parser.parse()
        rows = normalize_data(parsed, "XMLVendor")

        assert len(rows) == 3
        assert rows[0]["_third_party"] == "XMLVendor"

    def test_normalize_zip_with_xlsx(self, sample_zip_with_xlsx):
        parser = FileParser(sample_zip_with_xlsx)
        parsed = parser.parse()
        rows = normalize_data(parsed, "ZipVendor")

        assert len(rows) == 3
        assert all(r.get("_source_file") == "report.xlsx" for r in rows)

    def test_normalize_empty_data(self, empty_csv):
        parser = FileParser(empty_csv)
        parsed = parser.parse()
        rows = normalize_data(parsed, "EmptyVendor")

        assert rows == []
