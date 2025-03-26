import os
from datetime import timedelta

import streamlit as st
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, ClusterTimeoutOptions, QueryOptions

username = os.environ["MONGO_USER"]
password = os.environ["MONGO_PASSWORD"]
host = os.environ["MONGO_HOST"]
dbname = os.environ["MONGO_DBNAME"]
collection = os.environ["MONGO_COLLECTION"]


if "cluster" not in st.session_state:
    endpoint = host
    bucket_name = dbname
    auth = PasswordAuthenticator(username, password)
    timeout_opts = ClusterTimeoutOptions(kv_timeout=timedelta(seconds=10))
    cluster = Cluster(endpoint, ClusterOptions(auth, timeout_options=timeout_opts))
    cluster.wait_until_ready(timedelta(seconds=5))
    st.session_state.cluster = cluster


if "couch" not in st.session_state:
    cluster = st.session_state.cluster
    cb = cluster.bucket(dbname)
    cb_coll = cb.scope(dbname).collection(collection)
    st.session_state.couch = cb_coll

authors = set()
n_author = st.number_input(
    label="Number of authors", min_value=1, max_value=100, value=1
)


def clean_author(author: str) -> list[str]:
    tokens = author.split(",")
    author = "".join(tokens)
    tokens = author.split(" ")

    return [token.strip().lower() for token in tokens if len(token) > 0]


for i in range(n_author):
    author = st.text_input(label=f"Author {i + 1}")
    if author.count(",") > 1:
        st.write("Invalid author name")
    elif "," not in author:
        tokens = author.split(" ")
        author = tokens[-1].strip() + ", " + " ".join(tokens[:-1])

    author = " ".join([token.strip() for token in author.split(" ")])
    if len(author) < 4:
        st.write("Invalid author name")
    else:
        clean = clean_author(author=author)
        authors.update(clean)


title = st.text_input(label="Title")


with st.sidebar:
    add_journal = st.checkbox(label="Add Journal")
    add_publisher = st.checkbox(label="Add Publisher")
    add_year = st.checkbox(label="Add Year")

if add_journal:
    journal = st.text_input(label="Journal")

if add_publisher:
    publisher = st.text_input(label="Publisher")

if add_year:
    year = st.number_input(label="Year", min_value=1500)


search_bt = st.button(label="Search")
if search_bt:
    if len(authors) < 1:
        st.stop()

    tokens = list(authors)
    query = f"SELECT * FROM default:`{dbname}`.{dbname}.{collection} l"
    query += f" WHERE CONTAINS(LOWER(l.author), '{tokens[0]}')"
    for token in tokens[1:]:
        query += f" AND CONTAINS(LOWER(l.author), '{token}')"
    if title and len(title) > 0:
        query += f" AND CONTAINS(LOWER(l.title), '{title.lower()}')"
    if add_journal:
        query += f" AND CONTAINS(LOWER(l.journal), '{journal.lower()}')"
    if add_publisher:
        query += f" AND CONTAINS(LOWER(l.publisher), '{publisher.lower()}')"
    if add_year:
        query += f" AND year = '{str(year)}'"
    cluster = st.session_state.cluster
    results = cluster.query(query, QueryOptions(metrics=True))
    data: list[dict[str, str]] = []
    for result in results:
        data.append(result["l"])
    st.session_state.data = data


def form_citekey(entry: dict[str, str], index: int) -> str:
    cite_key = "_".join(clean_author(author=entry["author"]))
    if "year" in entry:
        cite_key += "_" + entry["year"]
    cite_key += "_" + str(index)

    return cite_key


def export_entry(entry: dict[str, str], index: int) -> str:
    cite_key = form_citekey(entry=entry, index=index)
    bibtex = f"@{entry['entry_type']}{{{cite_key},\n"
    for key, value in entry.items():
        if key not in ["entry_type", "ID"]:
            bibtex += f"    {key.upper()} = {{{value}}},\n"
    bibtex = bibtex.rstrip(",\n") + "\n}\n\n"

    return bibtex


if "data" in st.session_state:
    data = st.session_state.data
    st.dataframe(data=data)
    data = st.session_state.data
    indices = st.multiselect(
        label="Select entries to export",
        options=range(1, len(data) + 1),
        default=range(1, len(data) + 1),
    )
    if len(indices) > 0:
        export_bt = st.button(label="Export")
        entries: list[str] = []
        if export_bt:
            export = [data[i - 1] for i in indices]
            for i, entry in enumerate(export):
                entries.append(export_entry(entry=entry, index=i + 1))
            bib = "\n".join(entries)
            st.text_area(label="Bib content", value=bib)
            st.download_button(
                label="Download as bib file",
                data=bib,
                mime="text",
                file_name="export.bib",
            )
