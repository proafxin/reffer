from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.models.base import Base


class BibEntry(Base):
    entry_type: Mapped[str] = mapped_column(String(length=100))
