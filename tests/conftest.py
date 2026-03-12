#!/usr/bin/env python3
"""
Shared test fixtures for WIGEON test suite
"""

import csv
import sys
import zipfile
from pathlib import Path

import pytest

# Add project paths so tests can import WIGEON modules
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from database_schema import WigeonDatabase  # noqa: E402

# ---------------------------------------------------------------------------
# Temporary directory / database fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_dir(tmp_path):
    """Provide a clean temporary directory for each test."""
    return tmp_path


@pytest.fixture
def tmp_db(tmp_path):
    """Provide a fresh SQLite database via WigeonDatabase."""
    db_path = tmp_path / "database" / "test_wigeon.db"
    db = WigeonDatabase(str(db_path))
    yield db
    db.close()


# ---------------------------------------------------------------------------
# Sample CSV files
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_csv(tmp_path):
    """Create a simple comma-delimited CSV file."""
    path = tmp_path / "sample.csv"
    rows = [
        {"SKU": "A-SKU-0001", "Description": "Widget Alpha", "Quantity": "100", "Price": "9.99"},
        {"SKU": "A-SKU-0002", "Description": "Widget Beta", "Quantity": "250", "Price": "14.50"},
        {"SKU": "A-SKU-0003", "Description": "Widget Gamma", "Quantity": "50", "Price": "22.00"},
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["SKU", "Description", "Quantity", "Price"])
        writer.writeheader()
        writer.writerows(rows)
    return path


@pytest.fixture
def sample_pipe_csv(tmp_path):
    """Create a pipe-delimited CSV file."""
    path = tmp_path / "pipe_data.csv"
    lines = [
        "Site ID|Item Code|Item Description|Qty",
        "WH-01|A-SKU-0047|Square Reader|500",
        "WH-02|A-SKU-0048|Square Terminal|120",
    ]
    path.write_text("\n".join(lines))
    return path


@pytest.fixture
def sample_tab_csv(tmp_path):
    """Create a tab-delimited CSV file."""
    path = tmp_path / "tab_data.csv"
    lines = [
        "Name\tEmail\tRole",
        "Alice\talice@example.com\tAdmin",
        "Bob\tbob@example.com\tUser",
    ]
    path.write_text("\n".join(lines))
    return path


@pytest.fixture
def empty_csv(tmp_path):
    """Create a CSV with headers but no data rows."""
    path = tmp_path / "empty.csv"
    path.write_text("Col1,Col2,Col3\n")
    return path


# ---------------------------------------------------------------------------
# Sample Excel files (.xlsx)
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_xlsx(tmp_path):
    """Create a minimal .xlsx file with openpyxl."""
    openpyxl = pytest.importorskip("openpyxl")
    path = tmp_path / "sample.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inventory"
    ws.append(["SKU", "Description", "Quantity", "Price"])
    ws.append(["A-SKU-0001", "Widget Alpha", 100, 9.99])
    ws.append(["A-SKU-0002", "Widget Beta", 250, 14.50])
    ws.append(["A-SKU-0003", "Widget Gamma", 50, 22.00])
    wb.save(path)
    return path


@pytest.fixture
def multi_sheet_xlsx(tmp_path):
    """Create an .xlsx file with multiple worksheets."""
    openpyxl = pytest.importorskip("openpyxl")
    path = tmp_path / "multi_sheet.xlsx"
    wb = openpyxl.Workbook()

    ws1 = wb.active
    ws1.title = "Orders"
    ws1.append(["OrderID", "Customer", "Total"])
    ws1.append([1001, "Acme Corp", 500.00])
    ws1.append([1002, "Globex Inc", 1250.75])

    ws2 = wb.create_sheet("Returns")
    ws2.append(["ReturnID", "Reason"])
    ws2.append(["R-001", "Defective"])

    wb.save(path)
    return path


@pytest.fixture
def empty_xlsx(tmp_path):
    """Create an .xlsx file with headers only."""
    openpyxl = pytest.importorskip("openpyxl")
    path = tmp_path / "empty.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Col1", "Col2"])
    wb.save(path)
    return path


# ---------------------------------------------------------------------------
# Sample XML files
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_xml(tmp_path):
    """Create a simple XML data file with repeating elements."""
    path = tmp_path / "sample.xml"
    content = """\
<?xml version="1.0" encoding="UTF-8"?>
<shipments>
    <shipment>
        <tracking>1Z999AA10123456784</tracking>
        <carrier>UPS</carrier>
        <status>Delivered</status>
        <weight>2.5</weight>
    </shipment>
    <shipment>
        <tracking>9400111899223100001</tracking>
        <carrier>USPS</carrier>
        <status>In Transit</status>
        <weight>1.2</weight>
    </shipment>
    <shipment>
        <tracking>7489012345678901234</tracking>
        <carrier>FedEx</carrier>
        <status>Delivered</status>
        <weight>5.0</weight>
    </shipment>
</shipments>
"""
    path.write_text(content)
    return path


@pytest.fixture
def nested_xml(tmp_path):
    """Create an XML file with mixed/nested structure."""
    path = tmp_path / "nested.xml"
    content = """\
<?xml version="1.0" encoding="UTF-8"?>
<report>
    <metadata>
        <title>Monthly Report</title>
        <date>2026-03-01</date>
    </metadata>
    <summary total="1500" currency="USD"/>
</report>
"""
    path.write_text(content)
    return path


@pytest.fixture
def malformed_xml(tmp_path):
    """Create a malformed XML file for error-handling tests."""
    path = tmp_path / "bad.xml"
    path.write_text("<root><unclosed>")
    return path


# ---------------------------------------------------------------------------
# Sample ZIP files
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_zip_with_csv(tmp_path, sample_csv):
    """Create a ZIP containing a CSV file."""
    zip_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(sample_csv, "inner_data.csv")
    return zip_path


@pytest.fixture
def sample_zip_with_xlsx(tmp_path, sample_xlsx):
    """Create a ZIP containing an XLSX file."""
    zip_path = tmp_path / "archive_xlsx.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(sample_xlsx, "report.xlsx")
    return zip_path


@pytest.fixture
def sample_zip_with_xml(tmp_path, sample_xml):
    """Create a ZIP containing an XML file."""
    zip_path = tmp_path / "archive_xml.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(sample_xml, "shipments.xml")
    return zip_path


@pytest.fixture
def empty_zip(tmp_path):
    """Create an empty ZIP archive."""
    zip_path = tmp_path / "empty.zip"
    with zipfile.ZipFile(zip_path, "w"):
        pass  # empty archive
    return zip_path


# ---------------------------------------------------------------------------
# Pre-populated database fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def populated_db(tmp_db, sample_csv):
    """Database pre-loaded with one third-party and one report."""
    tp_id = tmp_db.add_third_party(
        name="Acme Corp",
        email="vendor@acme.com",
        description="Test vendor",
    )
    report_id = tmp_db.add_report(
        third_party_id=tp_id,
        report_type="inventory",
        file_name="sample.csv",
        file_path=str(sample_csv),
        file_format="csv",
        report_date="2026-03-01",
    )
    rows = [
        {"SKU": "A-SKU-0001", "Qty": "100"},
        {"SKU": "A-SKU-0002", "Qty": "250"},
    ]
    tmp_db.add_report_data(
        report_id=report_id,
        third_party_id=tp_id,
        data_rows=rows,
    )
    tmp_db.update_report_status(report_id, "processed", row_count=2)
    return tmp_db, tp_id, report_id
