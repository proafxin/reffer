import os
import re

import streamlit as st
from couchbase.cluster import Cluster
from couchbase.options import QueryOptions

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

    return [token.lower() for token in tokens]


def search_by_fields(
    cluster: Cluster,
    title: str,
    author: str,
    year: str | None = None,
    journal: str | None = None,
    publisher: str | None = None,
) -> list[dict[str, str]]:
    tokens = sanitize_text(text=author)
    if len(tokens) < 1:
        st.write(author)

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


def search_by_entry(cluster: Cluster, entry: dict[str, str]) -> list[dict[str, str]]:
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
