#!/usr/bin/env python3
"""
Data import script for Quorum App
Imports CSV data into the database using batch processing
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session

from app import create_app, db
from app.services.importers import (
    BillImporter,
    LegislatorImporter,
    VoteImporter,
    VoteResultImporter,
)

if TYPE_CHECKING:
    from app.services.importers.base_batch_importer import BaseBatchImporter


def import_entity(
    data_dir: Path,
    session: Session,
    batch_size: int,
    entity_name: str,
    filename: str,
    importer_class: type[BaseBatchImporter],
) -> bool:
    """Import a single entity type from CSV file"""
    file_path = data_dir / filename

    if not file_path.exists():
        print(f"❌ {filename} not found, skipping...")
        return False

    print(f"Importing {entity_name}...")
    importer = importer_class(session, batch_size)
    result = importer.import_from_file(str(file_path))

    print(f"✅ Imported {result.imported_count} {entity_name}")

    if result.errors:
        print(f"⚠️  {len(result.errors)} errors occurred")
        for error in result.errors[:5]:  # Show first 5 errors
            print(f"   - {error}")
        if len(result.errors) > 5:
            print(f"   ... and {len(result.errors) - 5} more errors")

    return True


def import_data() -> None:
    """Import all CSV data into the database using batch processing"""
    print("Starting batch data import...")

    # Ensure data directory exists
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    # Create Flask app
    app = create_app()

    with app.app_context():
        if not data_dir.exists():
            print(f"Data directory not found: {data_dir}")
            print("Please ensure the data directory exists with CSV files:")
            print("- data/legislators.csv")
            print("- data/bills.csv")
            print("- data/votes.csv")
            print("- data/vote_results.csv")
            return

        try:
            # Use a single session for all imports with larger batch sizes
            session = db.session
            batch_size = 1000  # Adjust based on memory and performance needs

            # Define import order and configurations (order matters due to foreign keys)
            import_configs = [
                ("legislators", "legislators.csv", LegislatorImporter),
                ("bills", "bills.csv", BillImporter),
                ("votes", "votes.csv", VoteImporter),
                ("vote results", "vote_results.csv", VoteResultImporter),
            ]

            # Import entities in order
            for entity_name, filename, importer_class in import_configs:
                import_entity(
                    data_dir,
                    session,
                    batch_size,
                    entity_name,
                    filename,
                    importer_class,
                )

            print("🎉 Batch data import completed successfully!")

        except Exception as e:
            print(f"❌ Error during import: {e}")
            db.session.rollback()
            raise


if __name__ == "__main__":
    import_data()
