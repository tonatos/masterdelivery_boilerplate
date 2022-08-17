from typing import Any
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr


Base: Any = declarative_base()


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime, default=func.now(), onupdate=func.now(), nullable=False,
        )
