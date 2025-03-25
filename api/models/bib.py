from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.models.base import Base

MAX_LENGTH = 256


class BibEntry(Base):
    __tablename__ = "library"
    entry_type: Mapped[str] = mapped_column(String(length=MAX_LENGTH))
    author: Mapped[str] = mapped_column(String(length=MAX_LENGTH))
    address: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    annote: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    booktitle: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    chapter: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    date: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    doi: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    edition: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    editor: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    howpublished: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    institution: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    isbn: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    issn: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    journal: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    language: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    month: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    mrclass: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    mrnumber: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    mrreviewer: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    mrreviewnumber: Mapped[str] = mapped_column(
        String(length=MAX_LENGTH), nullable=True
    )
    note: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    number: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    organization: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    pages: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    publisher: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    school: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    series: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    title: Mapped[str] = mapped_column(String(length=MAX_LENGTH))
    type: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    url: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    volume: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    year: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    zbl: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)
    zbmath: Mapped[str] = mapped_column(String(length=MAX_LENGTH), nullable=True)

    def __repr__(self):
        return f"{self.entry_type} {self.author} {self.title} {self.year}"
