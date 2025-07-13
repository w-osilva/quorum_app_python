from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.models.legislator import Legislator

from .base_batch_importer import BaseBatchImporter

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class LegislatorImporter(BaseBatchImporter):
    def __init__(self, session: Session, batch_size: int = 1000) -> None:
        super().__init__(session, Legislator, batch_size)

    def get_required_headers(self) -> list[str]:
        """Return list of required CSV headers"""
        return ["id", "name"]

    def transform_row(self, row: dict[str, str]) -> dict[str, Any]:
        """Transform CSV row to model format"""
        return {"id": int(row["id"]), "name": row["name"].strip()}

    def validate_row(self, row: dict[str, Any]) -> str:
        """Validate transformed row, return error message if invalid"""
        if not row.get("name"):
            return "Name cannot be empty"
        return None
