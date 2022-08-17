from uuid import UUID, uuid1
from pydantic import BaseModel


class EntityResponse(BaseModel):
    id: UUID
    value: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": uuid1(),
                "value": "test value",
            }
        }
