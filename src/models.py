from enum import Enum

from pydantic import BaseModel, Field


class PolicyType(str, Enum):
    ARUPA = "Arupa"
    FRISCO = "Frisco"


class PolicyModel(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=32,
        pattern=r'^[a-zA-Z0-9_]+$'
    )
    description: str
    type: PolicyType


class PolicyResponse(PolicyModel):
    policy_id: str
