from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VoteBase(BaseModel):
    bill_id: int


class VoteCreate(VoteBase):
    pass


class VoteResponse(VoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None = None


class VoteDetail(VoteResponse):
    bill_title: str | None = None
    vote_results_count: int = 0


class VoteList(BaseModel):
    votes: list[VoteDetail]
    total: int
