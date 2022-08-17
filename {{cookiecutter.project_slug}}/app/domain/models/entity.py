import uuid
from typing import Union, NoReturn
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from core.base.model import Base
from core.exceptions.base import BadRequestException


class Entity(Base):
    __tablename__ = "entity"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    value = Column(String(30))

    def __repr__(self):
        return f"Entity(id={self.id!r}, value={self.value!r})"

    @classmethod
    def create(
        cls,
        value: str,
    ) -> Union["User", NoReturn]:
        if not value:
            raise BadRequestException

        return cls(value=value)
