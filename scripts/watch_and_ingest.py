#!/usr/bin/env python3
"""
WIGEON - Smart File Watcher & Auto-Ingest
Watches Downloads folder and automatically ingests CEVA reports
"""

import subprocess
import time
from datetime import datetime
from pathlib import Path


class WigeonWatcher:
    def __init__(self, watch_dir=None):
        self.watch_dir = Path(watch_dir or Path.home() / "Downloads")
        self.processed_files = set()
        self.wigeon_dir = Path.home() / "Desktop" / "WIGEON"

    def is_ceva_file(self, filename):
        """Check if file is a CEVA report"""
        filename_lower = filename.lower()
        keywords = ["ceva", "block open order", "block service level", "block inventory", "block srl", "nortam"]
        return any(keyword in filename_lower for keyword in keywords)

    def get_report_type(self, filename):
        """Determine report type from filename"""
        filename_lower = filename.lower()

        if "open order" in filename_lower and "cancel" in filename_lower:
            return "Block Open Orders - BKO WMS Cancel"
        elif "open order" in filename_lower:
            return "Block Open Orders"
        elif "service level" in filename_lower:
            return "Block Service Level Detail"
        elif "inventory transaction" in filename_lower:
            return "Block Inventory Transaction Detail"
        elif "return" in filename_lower and "disposition" in filename_lower:
            return "Block SRL Returns Disposition"
        elif "return" in filename_lower and "receipt" in filename_lower:
            return "Block SRL Return Receipts"
        else:
            return "CEVA Report"

    def ingest_file(self, filepath):
        """Ingest file into WIGEON"""
        filename = filepath.name
        report_type = self.get_report_type(filename)

        print(f"\n📥 Ingesting: {filename}")
        print(f"   Type: {report_type}")

        cmd = [
            "python3",
            str(self.wigeon_dir / "wigeon.py"),
            "ingest",
            "--file",
            str(filepath),
            "--third-party",
            "CEVA Logistics",
            "--email",
            "ops_reporting@example.com",
            "--report-type",
            report_type,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.wigeon_dir)

            if result.returncode == 0:
                print("✅ Successfully ingested")
                # Show relevant output
                for line in result.stdout.split("\n"):
                    if "Successfully" in line or "rows" in line or "Report ID" in line:
                        print(f"   {line}")
                return True
            else:
                print(f"❌ Error: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Exception: {e}")
            return False

    def scan_existing_files(self):
        """Scan for existing CEVA files in Downloads"""
        print("🔍 Scanning for existing CEVA files...")

        cutoff_time = time.time() - (7 * 24 * 60 * 60)  # 7 days ago
        found_files = []

        for filepath in self.watch_dir.iterdir():
            if not filepath.is_file():
                continue

            # Check if it's a CEVA file, recent, and not already processed
            if (
                self.is_ceva_file(filepath.name)
                and filepath.stat().st_mtime > cutoff_time
                and filepath not in self.processed_files
            ):
                found_files.append(filepath)

        return sorted(found_files, key=lambda x: x.stat().st_mtime, reverse=True)

    def watch_mode(self, duration_seconds=300):
        """Watch for new files for specified duration"""
        print(f"\n👀 Watching {self.watch_dir} for new CEVA files...")
        print(f"   Duration: {duration_seconds} seconds ({duration_seconds // 60} minutes)")
        print("   Press Ctrl+C to stop early")

        start_time = time.time()
        last_check = {}

        try:
            while time.time() - start_time < duration_seconds:
                # Check all files
                for filepath in self.watch_dir.iterdir():
                    if not filepath.is_file():
                        continue

                    if not self.is_ceva_file(filepath.name):
                        continue

                    # Check if file is new or modified
                    mtime = filepath.stat().st_mtime

                    if (
                        filepath not in self.processed_files
                        and (filepath not in last_check or last_check[filepath] != mtime)
                        and time.time() - mtime < 60  # Modified in last minute
                    ):
                        # New or modified file
                        print(f"\n🆕 New file detected: {filepath.name}")
                        time.sleep(2)  # Wait for download to complete

                        if self.ingest_file(filepath):
                            self.processed_files.add(filepath)
                            last_check[filepath] = mtime

                time.sleep(2)  # Check every 2 seconds

        except KeyboardInterrupt:
            print("\n\n⏹️  Stopped watching")

    def run(self, watch=False, watch_duration=300):
        """Main run method"""
        print("🦆 WIGEON - Smart File Watcher & Auto-Ingest")
        print("=" * 60)

        # First, scan for existing files
        existing_files = self.scan_existing_files()

        if existing_files:
            print(f"\n✅ Found {len(existing_files)} existing CEVA file(s)")

            for filepath in existing_files:
                print(f"\n📄 {filepath.name}")
                print(f"   Modified: {datetime.fromtimestamp(filepath.stat().st_mtime)}")

            response = input("\n❓ Ingest these files? (y/n): ").strip().lower()

            if response == "y":
                print("\n🔄 Processing existing files...")
                success_count = 0

                for filepath in existing_files:
                    if self.ingest_file(filepath):
                        self.processed_files.add(filepath)
                        success_count += 1

                print(f"\n✅ Processed {success_count}/{len(existing_files)} files")
        else:
            print("\n📭 No existing CEVA files found in Downloads")

        # Watch mode
        if watch:
            self.watch_mode(watch_duration)

        # Show final stats
        print("\n" + "=" * 60)
        print("📊 Final Statistics")
        print("=" * 60)

        subprocess.run(["python3", "wigeon.py", "stats"], cwd=self.wigeon_dir)


if __name__ == "__main__":
    import sys

    watcher = WigeonWatcher()

    # Check if watch mode requested
    watch_mode = "--watch" in sys.argv
    watch_duration = 300  # 5 minutes default

    if "--duration" in sys.argv:
        idx = sys.argv.index("--duration")
        if idx + 1 < len(sys.argv):
            watch_duration = int(sys.argv[idx + 1])

    watcher.run(watch=watch_mode, watch_duration=watch_duration)
