from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class BillBase(BaseModel):
    title: str
    sponsor_id: int


class BillCreate(BillBase):
    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            msg = "Title cannot be empty"
            raise ValueError(msg)
        return v.strip()


class BillResponse(BillBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None = None


class BillDetail(BillResponse):
    sponsor_name: str | None = None
    votes_count: int = 0


class BillList(BaseModel):
    bills: list[BillDetail]
    total: int
