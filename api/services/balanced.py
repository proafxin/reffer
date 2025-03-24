import bibtexparser
from bibtexparser import middlewares as mw

text = r"""@book {euler_1748,
	AUTHOR = {Euler, Leonhard},
	TITLE = {Introductio in analysin infinitorum. {T}omus primus $abc=\sum_{i=1}i$},
	NOTE = {Reprint of the 1748 original},
	PUBLISHER = {Sociedad Andaluza de Educaci\'{o}n Matem\'{a}tica ``Thales'', Seville; Real Sociedad Matem\'{a}tica Espa\~{n}ola, Madrid},
	DATE = {2000},
	PAGES = {xvi+320},
	ISBN = {84-923760-2-3},
	MRCLASS = {01A50 (01A75)},
	MRNUMBER = {1841793},
}"""

library = bibtexparser.parse_string(
    text,
    append_middleware=[
        mw.LatexDecodingMiddleware(),
        mw.MonthIntMiddleware(True),
        mw.SeparateCoAuthors(),
        mw.SplitNameParts(),
    ],
)

for entry in library.entries:
    print(entry.fields)
