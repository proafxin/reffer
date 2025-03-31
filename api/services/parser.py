# Parse bib files
import bibtexparser
from bibtexparser import middlewares as mw


def parse_bibtext(text: str) -> list[dict[str, str]]:
    library = bibtexparser.parse_string(
        text,
        append_middleware=[mw.LatexDecodingMiddleware(), mw.MonthIntMiddleware(True)],
    )

    bibentries: list[dict[str, str]] = []
    for entry in library.entries:
        bibentry = {}
        bibentry["entry_type"] = entry.entry_type
        keys = [field.key.lower() for field in entry.fields]

        if "author" not in keys:
            continue

        if "title" not in keys:
            continue

        for field in entry.fields:
            key = field.key.lower()
            value = field.value

            bibentry[key] = value

        bibentries.append(bibentry)

    return bibentries
