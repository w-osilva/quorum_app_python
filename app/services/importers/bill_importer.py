from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.models.bill import Bill
from app.models.legislator import Legislator

from .base_batch_importer import BaseBatchImporter

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class BillImporter(BaseBatchImporter):
    def __init__(self, session: Session, batch_size: int = 1000) -> None:
        super().__init__(session, Bill, batch_size)

    def get_required_headers(self) -> list[str]:
        """Return list of required CSV headers"""
        return ["id", "title", "sponsor_id"]

    def transform_row(self, row: dict[str, str]) -> dict[str, Any]:
        """Transform CSV row to model format"""
        sponsor_id = None
        if row.get("sponsor_id") and row["sponsor_id"].strip():
            sponsor_id = int(row["sponsor_id"])

        return {
            "id": int(row["id"]),
            "title": row["title"].strip(),
            "sponsor_id": sponsor_id,
        }

    def validate_row(self, row: dict[str, Any]) -> str:
        """Validate transformed row, return error message if invalid"""
        if not row.get("title"):
            return "Title cannot be empty"

        # Note: We don't prevent import for invalid sponsor_id, just log it
        # The test expects bills to be imported even with invalid sponsor_id
        return None

    def transform_row(self, row: dict[str, str]) -> dict[str, Any]:
        """Transform CSV row to model format"""
        sponsor_id = None
        if row.get("sponsor_id") and row["sponsor_id"].strip():
            sponsor_id = int(row["sponsor_id"])

        # Check sponsor_id validity and collect error for reporting
        sponsor_error = None
        if sponsor_id:
            sponsor_exists = (
                self.session.query(Legislator).filter_by(id=sponsor_id).first()
            )
            if not sponsor_exists:
                sponsor_error = f"Sponsor with ID {sponsor_id} does not exist"

        transformed = {
            "id": int(row["id"]),
            "title": row["title"].strip(),
            "sponsor_id": sponsor_id,
        }

        # Store validation error for later reporting
        if sponsor_error:
            transformed["_validation_error"] = sponsor_error

        return transformed
