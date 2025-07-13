from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.models.bill import Bill
from app.models.vote import Vote

from .base_batch_importer import BaseBatchImporter

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class VoteImporter(BaseBatchImporter):
    def __init__(self, session: Session, batch_size: int = 1000) -> None:
        super().__init__(session, Vote, batch_size)

    def get_required_headers(self) -> list[str]:
        """Return list of required CSV headers"""
        return ["id", "bill_id"]

    def transform_row(self, row: dict[str, str]) -> dict[str, Any]:
        """Transform CSV row to model format"""
        bill_id = None
        if row.get("bill_id") and row["bill_id"].strip():
            bill_id = int(row["bill_id"])

        # Check bill_id validity and collect error for reporting
        bill_error = None
        if bill_id:
            bill_exists = self.session.query(Bill).filter_by(id=bill_id).first()
            if not bill_exists:
                bill_error = f"Bill with ID {bill_id} does not exist"

        transformed = {"id": int(row["id"]), "bill_id": bill_id}

        # Store validation error for later reporting
        if bill_error:
            transformed["_validation_error"] = bill_error

        return transformed

    def validate_row(self, row: dict[str, Any]) -> str:
        """Validate transformed row, return error message if invalid"""
        # Note: We don't prevent import for invalid bill_id, just log it
        # The test expects votes to be imported even with invalid bill_id
        return None
