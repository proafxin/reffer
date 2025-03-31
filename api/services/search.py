import os
import re

import streamlit as st
from couchbase.cluster import Cluster
from couchbase.collection import Collection
from couchbase.options import QueryOptions
from couchbase.result import MultiGetResult

dbname = os.environ["MONGO_DBNAME"]

collection = os.environ["MONGO_COLLECTION"]


def remove_latex_expression(text: str) -> str:
    return "".join(re.sub(r"\$.*?\$", " ", text))


def tokenize_author(author: str) -> list[str]:
    author = re.sub(r"\b\w*'\w*\b", "", author)
    tokens = author.split(",")
    author = "".join(tokens)
    tokens = author.split(" ")

    return [token.strip().lower() for token in tokens if len(token) > 0]


def sanitize_text(text: str) -> list[str]:
    text = remove_latex_expression(text=text)
    text = re.sub(r"\b\w*'\w*\b", " ", text)
    tokens = re.findall(r"\b\w+\b", text)

    return sorted([token.lower() for token in tokens])


def form_key(entry: dict[str, str]) -> str:
    author = entry.get("author")
    title = entry.get("title")
    year = entry.get("year")
    journal = entry.get("journal")
    publisher = entry.get("publisher")
    fields = author, year, title, journal, publisher

    key = ""
    for field in fields:
        if field:
            tokens = sanitize_text(text=field)
            if len(tokens) > 0:
                key += "".join(tokens)

    return str(hash(key))


def search_by_fields(
    cluster: Cluster,
    title: str,
    author: str,
    year: str | None = None,
    journal: str | None = None,
    publisher: str | None = None,
) -> list[dict[str, str]]:
    tokens = sanitize_text(text=author)

    query = f"SELECT * FROM default:`{dbname}`.{dbname}.{collection} l"
    query += f" WHERE CONTAINS(LOWER(l.author), '{tokens[0]}')"
    for token in tokens[1:]:
        query += f" AND CONTAINS(LOWER(l.author), '{token}')"
    if title and len(title) > 0:
        tokens = sanitize_text(text=title)
        for token in tokens:
            query += f" AND CONTAINS(LOWER(l.title), '{token.lower()}')"
    if journal and len(journal) > 0:
        tokens = sanitize_text(text=journal)
        for token in tokens:
            query += f" AND CONTAINS(LOWER(l.journal), '{token.lower()}')"
    if publisher and len(publisher) > 0:
        tokens = sanitize_text(text=publisher)
        for token in tokens:
            query += f" AND CONTAINS(LOWER(l.publisher), '{token.lower()}')"
    if year:
        query += f" AND year = '{str(year)}'"

    results = cluster.query(query, QueryOptions(metrics=True))
    data: list[dict[str, str]] = []
    for result in results:
        data.append(result["l"])

    return data


def search_by_key(cluster: Cluster, key: str) -> list[dict[str, str]]:
    cb_coll: Collection = st.session_state.couch
    result: MultiGetResult = cb_coll.get_multi(
        ["67e257c274f537222c366422", "67e257c274f537222c366423", "A"]
    )
    st.write(result.results)

    return []


def search_by_entry(cluster: Cluster, entry: dict[str, str]) -> list[dict[str, str]]:
    key = form_key(entry=entry)
    search_by_key(cluster=cluster, key=key)
    author = entry["author"]
    title = entry["title"]
    journal = entry.get("journal")
    year = entry.get("year")
    publisher = entry.get("publisher")

    return search_by_fields(
        cluster=cluster,
        title=title,
        author=author,
        year=year,
        journal=journal,
        publisher=publisher,
    )
