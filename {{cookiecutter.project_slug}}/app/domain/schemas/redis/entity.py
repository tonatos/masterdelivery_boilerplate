from uuid import UUID
from pydantic import BaseModel, Field


class EntityRedisSchema(BaseModel):
    id: UUID = Field(..., description='Id')
    value: str = Field(..., description='Value')
