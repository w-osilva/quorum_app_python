from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class VoteResultBase(BaseModel):
    legislator_id: int
    vote_id: int
    vote_type: int  # 1=Yea, 2=Nay


class VoteResultCreate(VoteResultBase):
    @field_validator("vote_type")
    @classmethod
    def validate_vote_type(cls, v: int) -> int:
        if v not in [1, 2]:
            msg = "Vote type must be 1 (Yea) or 2 (Nay)"
            raise ValueError(msg)
        return v


class VoteResultResponse(VoteResultBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None = None


class VoteResultDetail(VoteResultResponse):
    legislator_name: str | None = None
    bill_title: str | None = None
    vote_type_str: str


class VoteResultList(BaseModel):
    vote_results: list[VoteResultDetail]
    total: int
