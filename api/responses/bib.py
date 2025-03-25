from enum import Enum

from pydantic import field_validator

from api.responses.base import Base


class EntryType(str, Enum):
    ARTICLE = "article"
    BOOK = "book"
    BOOKLET = "booklet"
    CONFERENCE = "conference"
    INBOOK = "inbook"
    INCOLLECTION = "incollection"
    INPROCEEDINGS = "inproceedings"
    MANUAL = "manual"
    MASTERTHESIS = "masterthesis"
    MISC = "misc"
    PHDTHESIS = "phdthesis"
    PROCEEDINGS = "proceedings"
    TECHREPORT = "techreport"
    UNPUBLISHED = "unpublished"


class BibField(str, Enum):
    ADDRESS = "address"
    ARXIV = "arXiv"
    ANNOTE = "annote"
    AUTHOR = "author"
    BOOKTITLE = "booktitle"
    CHAPTER = "chapter"
    CITEKEY = "citekey"
    DATE = "date"
    DOI = "doi"
    EDITION = "edition"
    EDITOR = "editor"
    ENTRY_TYPE = "entry_type"
    HOWPUBLISHED = "howpublished"
    INSTITUTION = "institution"
    ISBN = "isbn"
    ISSN = "issn"
    JOURNAL = "journal"
    MONTH = "month"
    MRCLASS = "mrclass"
    MRNUMBER = "mrnumber"
    MRREVIEWER = "mrreviewer"
    MRREVIEWNUMBER = "mrreviewnumber"
    NOTE = "note"
    NUMBER = "number"
    ORGANIZATION = "organization"
    PAGES = "pages"
    PUBLISHER = "publisher"
    SCHOOL = "school"
    SERIES = "series"
    TITLE = "title"
    TYPE = "type"
    URL = "url"
    VOLUME = "volume"
    YEAR = "year"


class BibEntry(Base):
    arXiv: str | None = None
    author: list[str]
    address: str | None = None
    annote: str | None = None
    booktitle: str | None = None
    chapter: str | None = None
    date: str | None = None
    doi: str | None = None
    edition: str | None = None
    editor: str | None = None
    entry_type: str
    howpublished: str | None = None
    institution: str | None = None
    isbn: str | None = None
    issn: str | None = None
    journal: str | None = None
    language: str | None = None
    month: str | None = None
    mrclass: str | None = None
    mrnumber: str | None = None
    mrreviewer: str | None = None
    mrreviewnumber: str | None = None
    note: str | None = None
    number: str | None = None
    organization: str | None = None
    pages: str | None = None
    publisher: str | None = None
    school: str | None = None
    series: str | None = None
    title: str | None = None
    type: str | None = None
    url: str | None = None
    volume: str | None = None
    year: str | None = None
    zbl: str | None = None
    zbmath: str | None = None

    @field_validator("entry_type", mode="before")
    @classmethod
    def validate_entry_type(cls, entry_type: str):
        if entry_type not in EntryType:
            raise ValueError("Invalid entry type")
        return entry_type
