#!/usr/bin/env python3
"""
WIGEON Database Schema
Creates and manages SQLite database for third-party report data
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

class WigeonDatabase:
    def __init__(self, db_path="database/wigeon.db"):
        """Initialize database connection"""
        self.db_path = Path(__file__).parent.parent / db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.create_schema()
    
    def create_schema(self):
        """Create database schema if not exists"""
        cursor = self.conn.cursor()
        
        # Third-party companies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS third_parties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL,
                description TEXT,
                metadata TEXT,  -- JSON field for flexible data
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Reports table (tracks each ingested report)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                third_party_id INTEGER NOT NULL,
                report_type TEXT NOT NULL,
                report_date DATE,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_format TEXT NOT NULL,  -- xlsx, xml, zip, etc.
                email_subject TEXT,
                email_date TIMESTAMP,
                status TEXT DEFAULT 'pending',  -- pending, processed, failed
                row_count INTEGER DEFAULT 0,
                error_message TEXT,
                metadata TEXT,  -- JSON field for report-specific data
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                FOREIGN KEY (third_party_id) REFERENCES third_parties(id)
            )
        """)
        
        # Report data table (flexible schema for actual report data)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS report_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                third_party_id INTEGER NOT NULL,
                row_number INTEGER,
                data TEXT NOT NULL,  -- JSON field for flexible row data
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (report_id) REFERENCES reports(id),
                FOREIGN KEY (third_party_id) REFERENCES third_parties(id)
            )
        """)
        
        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_reports_third_party 
            ON reports(third_party_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_reports_date 
            ON reports(report_date)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_report_data_report 
            ON report_data(report_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_report_data_third_party 
            ON report_data(third_party_id)
        """)
        
        self.conn.commit()
        print("✅ Database schema created successfully")
    
    def add_third_party(self, name, email, description=None, metadata=None):
        """Add or update a third-party company"""
        cursor = self.conn.cursor()
        
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute("""
            INSERT INTO third_parties (name, email, description, metadata)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                email = excluded.email,
                description = excluded.description,
                metadata = excluded.metadata,
                updated_at = CURRENT_TIMESTAMP
        """, (name, email, description, metadata_json))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_third_party(self, name=None, email=None):
        """Get third-party by name or email"""
        cursor = self.conn.cursor()
        
        if name:
            cursor.execute("SELECT * FROM third_parties WHERE name = ?", (name,))
        elif email:
            cursor.execute("SELECT * FROM third_parties WHERE email = ?", (email,))
        else:
            return None
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def add_report(self, third_party_id, report_type, file_name, file_path, 
                   file_format, report_date=None, email_subject=None, 
                   email_date=None, metadata=None):
        """Add a new report record"""
        cursor = self.conn.cursor()
        
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute("""
            INSERT INTO reports (
                third_party_id, report_type, report_date, file_name, 
                file_path, file_format, email_subject, email_date, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (third_party_id, report_type, report_date, file_name, 
              file_path, file_format, email_subject, email_date, metadata_json))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def update_report_status(self, report_id, status, row_count=None, error_message=None):
        """Update report processing status"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            UPDATE reports 
            SET status = ?, 
                row_count = COALESCE(?, row_count),
                error_message = ?,
                processed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, row_count, error_message, report_id))
        
        self.conn.commit()
    
    def add_report_data(self, report_id, third_party_id, data_rows):
        """Add report data rows (bulk insert)"""
        cursor = self.conn.cursor()
        
        rows = [
            (report_id, third_party_id, idx, json.dumps(row))
            for idx, row in enumerate(data_rows, 1)
        ]
        
        cursor.executemany("""
            INSERT INTO report_data (report_id, third_party_id, row_number, data)
            VALUES (?, ?, ?, ?)
        """, rows)
        
        self.conn.commit()
        return len(rows)
    
    def query_reports(self, third_party_name=None, report_type=None, 
                     start_date=None, end_date=None, status=None):
        """Query reports with filters"""
        cursor = self.conn.cursor()
        
        query = """
            SELECT r.*, tp.name as third_party_name, tp.email as third_party_email
            FROM reports r
            JOIN third_parties tp ON r.third_party_id = tp.id
            WHERE 1=1
        """
        params = []
        
        if third_party_name:
            query += " AND tp.name = ?"
            params.append(third_party_name)
        
        if report_type:
            query += " AND r.report_type = ?"
            params.append(report_type)
        
        if start_date:
            query += " AND r.report_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND r.report_date <= ?"
            params.append(end_date)
        
        if status:
            query += " AND r.status = ?"
            params.append(status)
        
        query += " ORDER BY r.report_date DESC, r.created_at DESC"
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def query_report_data(self, report_id=None, third_party_name=None, 
                         limit=None, offset=0):
        """Query report data with filters"""
        cursor = self.conn.cursor()
        
        query = """
            SELECT rd.*, r.report_type, r.report_date, tp.name as third_party_name
            FROM report_data rd
            JOIN reports r ON rd.report_id = r.id
            JOIN third_parties tp ON rd.third_party_id = tp.id
            WHERE 1=1
        """
        params = []
        
        if report_id:
            query += " AND rd.report_id = ?"
            params.append(report_id)
        
        if third_party_name:
            query += " AND tp.name = ?"
            params.append(third_party_name)
        
        query += " ORDER BY rd.report_id DESC, rd.row_number ASC"
        
        if limit:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Parse JSON data field
        results = []
        for row in rows:
            row_dict = dict(row)
            row_dict['data'] = json.loads(row_dict['data'])
            results.append(row_dict)
        
        return results
    
    def get_statistics(self):
        """Get database statistics"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Count third parties
        cursor.execute("SELECT COUNT(*) as count FROM third_parties")
        stats['third_parties'] = cursor.fetchone()['count']
        
        # Count reports
        cursor.execute("SELECT COUNT(*) as count FROM reports")
        stats['total_reports'] = cursor.fetchone()['count']
        
        # Count by status
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM reports 
            GROUP BY status
        """)
        stats['reports_by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Count data rows
        cursor.execute("SELECT COUNT(*) as count FROM report_data")
        stats['total_data_rows'] = cursor.fetchone()['count']
        
        # Reports by third party
        cursor.execute("""
            SELECT tp.name, COUNT(r.id) as count
            FROM third_parties tp
            LEFT JOIN reports r ON tp.id = r.third_party_id
            GROUP BY tp.name
        """)
        stats['reports_by_third_party'] = {row['name']: row['count'] for row in cursor.fetchall()}
        
        return stats
    
    def close(self):
        """Close database connection"""
        self.conn.close()


if __name__ == "__main__":
    # Test database creation
    db = WigeonDatabase()
    print("\n📊 Database Statistics:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    db.close()
