from __future__ import annotations


class ImportResult:
    """Standard result object for import operations"""

    def __init__(self, success: bool, imported_count: int, errors: list[str]) -> None:
        self.success = success
        self.imported_count = imported_count
        self.errors = errors

    def __repr__(self) -> str:
        return f"ImportResult(success={self.success}, imported_count={self.imported_count}, errors={len(self.errors)})"
