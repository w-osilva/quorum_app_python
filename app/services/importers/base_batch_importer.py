from __future__ import annotations

import csv
import os
from typing import TYPE_CHECKING, Any

from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from .import_result import ImportResult

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class BaseBatchImporter:
    """Base class for batch importers with upsert capabilities"""

    def __init__(
        self,
        session: Session,
        model_class: type,
        batch_size: int = 1000,
    ) -> None:
        self.session = session
        self.model_class = model_class
        self.batch_size = batch_size

    def import_from_file(self, file_path: str) -> ImportResult:
        """Import data from CSV file using batch upsert"""
        errors = []
        imported_count = 0

        if not os.path.exists(file_path):
            return ImportResult(False, 0, [f"File not found: {file_path}"])

        try:
            with open(file_path, encoding="utf-8") as file:
                reader = csv.DictReader(file)

                # Validate required headers
                required_headers = self.get_required_headers()
                if not all(header in reader.fieldnames for header in required_headers):
                    missing = [
                        h for h in required_headers if h not in reader.fieldnames
                    ]
                    return ImportResult(
                        False,
                        0,
                        [f"Missing required headers: {missing}"],
                    )

                # Process data in batches
                batch = []
                row_count = 0
                seen_ids = set()  # Track IDs to detect duplicates within the file

                for row in reader:
                    row_count += 1
                    try:
                        # Transform and validate row
                        transformed_row = self.transform_row(row)
                        validation_error = self.validate_row(transformed_row)

                        # Check for validation errors from transform_row
                        if "_validation_error" in transformed_row:
                            errors.append(
                                f"Row {row_count}: {transformed_row['_validation_error']}",
                            )
                            # Remove the error marker before processing
                            del transformed_row["_validation_error"]

                        if validation_error:
                            errors.append(f"Row {row_count}: {validation_error}")
                            continue

                        # Check for duplicate IDs within the same file
                        row_id = transformed_row.get("id")
                        if row_id in seen_ids:
                            errors.append(
                                f"Row {row_count}: Duplicate ID {row_id} found in file",
                            )
                            continue
                        seen_ids.add(row_id)

                        batch.append(transformed_row)

                        # Process batch when it reaches the batch size
                        if len(batch) >= self.batch_size:
                            batch_imported = self._process_batch(batch)
                            imported_count += batch_imported
                            batch = []

                    except Exception as e:
                        errors.append(f"Row {row_count}: {e}")
                        continue

                # Process remaining batch
                if batch:
                    batch_imported = self._process_batch(batch)
                    imported_count += batch_imported

                self.session.commit()
                success = imported_count > 0 or len(errors) == 0
                return ImportResult(success, imported_count, errors)

        except Exception as e:
            self.session.rollback()
            return ImportResult(False, 0, [f"Import failed: {e}"])

    def _process_batch(self, batch: list[dict[str, Any]]) -> int:
        """Process a batch of records using upsert"""
        if not batch:
            return 0

        try:
            # Use database-specific upsert for PostgreSQL and SQLite only
            dialect_name = self.session.bind.dialect.name if self.session.bind else None

            if dialect_name == "sqlite":
                return self._upsert_sqlite(batch)
            if dialect_name == "postgresql":
                return self._upsert_postgresql(batch)
            # Simple fallback for development/testing
            return self._upsert_simple(batch)

        except Exception:
            # If batch fails, try simple upserts
            return self._upsert_simple(batch)

    def _upsert_sqlite(self, batch: list[dict[str, Any]]) -> int:
        """SQLite-specific upsert using INSERT OR REPLACE"""
        stmt = sqlite_insert(self.model_class.__table__)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                col.name: stmt.excluded[col.name]
                for col in self.model_class.__table__.columns
                if col.name != "id"
            },
        )
        self.session.execute(stmt, batch)
        return len(batch)

    def _upsert_postgresql(self, batch: list[dict[str, Any]]) -> int:
        """PostgreSQL-specific upsert using ON CONFLICT"""
        stmt = postgresql_insert(self.model_class.__table__)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                col.name: stmt.excluded[col.name]
                for col in self.model_class.__table__.columns
                if col.name != "id"
            },
        )
        self.session.execute(stmt, batch)
        return len(batch)

    def _upsert_simple(self, batch: list[dict[str, Any]]) -> int:
        """Simple upsert using individual operations (for development/testing)"""
        imported_count = 0
        for row in batch:
            try:
                # Check if record exists
                existing = (
                    self.session.query(self.model_class).filter_by(id=row["id"]).first()
                )

                if existing:
                    # Update existing record
                    for key, value in row.items():
                        if hasattr(existing, key):
                            setattr(existing, key, value)
                else:
                    # Create new record
                    record = self.model_class(**row)
                    self.session.add(record)

                imported_count += 1

            except Exception:
                continue

        return imported_count

    # Abstract methods to be implemented by subclasses
    def get_required_headers(self) -> list[str]:
        """Return list of required CSV headers"""
        raise NotImplementedError

    def transform_row(self, row: dict[str, str]) -> dict[str, Any]:
        """Transform CSV row to model format"""
        raise NotImplementedError

    def validate_row(self, row: dict[str, Any]) -> str:
        """Validate transformed row, return error message if invalid"""
        return None  # Default: no validation errors
