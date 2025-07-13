from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class LegislatorBase(BaseModel):
    name: str


class LegislatorCreate(LegislatorBase):
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            msg = "Name cannot be empty"
            raise ValueError(msg)
        return v.strip()


class LegislatorResponse(LegislatorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None = None


class LegislatorDetail(LegislatorResponse):
    model_config = ConfigDict(from_attributes=True)

    sponsored_bills_count: int
    supported_bills_count: int
    opposed_bills_count: int


class LegislatorList(BaseModel):
    legislators: list[LegislatorDetail]
    total: int
