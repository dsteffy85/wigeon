#!/usr/bin/env python3
"""
WIGEON Configuration Manager
Handles provider setup, config persistence, and first-run experience.
"""

from __future__ import annotations

import json
from pathlib import Path

CONFIG_FILENAME = "config.json"
DEFAULT_CONFIG = {
    "version": "2.0.0",
    "providers": [],
    "google_drive_folder_id": "",
    "google_drive_folder_name": "WIGEON_Reports",
    "inbox_dir": "inbox",
    "database_path": "database/wigeon.db",
    "retention": {
        "max_copies_per_report": 2,
        "days_to_search": 7,
    },
}


def _config_path(project_root: Path | None = None) -> Path:
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent
    return project_root / CONFIG_FILENAME


def load_config(project_root: Path | None = None) -> dict:
    """Load config.json or return defaults if missing."""
    path = _config_path(project_root)
    if path.exists():
        with open(path) as f:
            cfg = json.load(f)
        # Merge with defaults so new keys are always present
        merged = {**DEFAULT_CONFIG, **cfg}
        merged["retention"] = {**DEFAULT_CONFIG["retention"], **cfg.get("retention", {})}
        return merged
    return dict(DEFAULT_CONFIG)


def save_config(config: dict, project_root: Path | None = None) -> Path:
    """Persist config to config.json."""
    path = _config_path(project_root)
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    return path


def add_provider(
    config: dict,
    name: str,
    email: str,
    subject_filter: str = "",
    description: str = "",
) -> dict:
    """Add a provider to the config (idempotent by email)."""
    for p in config["providers"]:
        if p["email"].lower() == email.lower():
            # Update existing
            p["name"] = name
            p["subject_filter"] = subject_filter
            p["description"] = description
            return config

    config["providers"].append(
        {
            "name": name,
            "email": email,
            "subject_filter": subject_filter,
            "description": description,
        }
    )
    return config


def remove_provider(config: dict, email: str) -> dict:
    """Remove a provider by email."""
    config["providers"] = [p for p in config["providers"] if p["email"].lower() != email.lower()]
    return config


def list_providers(config: dict) -> list[dict]:
    """Return the list of configured providers."""
    return config.get("providers", [])


def get_provider_emails(config: dict) -> list[str]:
    """Return just the email addresses."""
    return [p["email"] for p in config.get("providers", [])]


def interactive_setup() -> dict:
    """Run the first-time interactive setup wizard."""
    print()
    print("=" * 60)
    print("🦆 WIGEON — First-Time Setup")
    print("=" * 60)
    print()
    print("WIGEON collects email report attachments from your vendors")
    print("and stores the data in a local database for easy analysis.")
    print()

    config = dict(DEFAULT_CONFIG)

    # Provider setup
    print("Let's add your first report provider.\n")
    name = input("  Provider name (e.g. Acme Logistics): ").strip()
    email = input("  Provider email address: ").strip()
    subject = input("  Email subject filter (optional, press Enter to skip): ").strip()

    if name and email:
        add_provider(config, name=name, email=email, subject_filter=subject)
        print(f"\n  ✅ Added provider: {name} ({email})")
    else:
        print("\n  ⚠️  Skipped — you can add providers later with: python3 wigeon.py setup --add-provider")

    # Google Drive folder
    print()
    folder_id = input("  Google Drive folder ID for reports (optional, Enter to skip): ").strip()
    if folder_id:
        config["google_drive_folder_id"] = folder_id

    print()
    print("=" * 60)
    print("🦆 Setup complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Deploy the Google Apps Script (see SETUP.md)")
    print("  2. Run:  python3 wigeon.py refresh")
    print("  3. View: python3 wigeon.py dashboard")
    print()

    return config


if __name__ == "__main__":
    cfg = interactive_setup()
    path = save_config(cfg)
    print(f"Config saved to {path}")
