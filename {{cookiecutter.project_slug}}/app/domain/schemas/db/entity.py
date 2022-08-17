from uuid import UUID
from pydantic import BaseModel, Field


class EntityDBSchema(BaseModel):
    id: UUID = Field(..., description='Id')
    value: str = Field(..., description='Value')

    class Config:
        orm_mode = True
