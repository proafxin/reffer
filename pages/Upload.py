import os
from datetime import timedelta

import streamlit as st
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.collection import Collection
from couchbase.options import ClusterOptions, ClusterTimeoutOptions
from couchbase.result import MultiGetResult, MultiMutationResult

from api.services.parser import parse_bibtext
from api.services.search import form_key

username = os.environ["MONGO_USER"]
password = os.environ["MONGO_PASSWORD"]
host = os.environ["MONGO_HOST"]
dbname = os.environ["MONGO_DBNAME"]
collection = os.environ["MONGO_COLLECTION"]


if "couch" not in st.session_state:
    endpoint = host
    bucket_name = dbname
    auth = PasswordAuthenticator(username, password)
    timeout_opts = ClusterTimeoutOptions(kv_timeout=timedelta(seconds=10))
    if "cluster" in st.session_state:
        cluster = st.session_state.cluster
    else:
        cluster = Cluster(endpoint, ClusterOptions(auth, timeout_options=timeout_opts))
        cluster.wait_until_ready(timedelta(seconds=5))
        st.session_state.cluster = cluster

    cb = cluster.bucket(dbname)
    cb_coll: Collection = cb.scope(dbname).collection(collection)
    st.session_state.couch = cb_coll


bib_file = st.file_uploader(label="Upload bib file", type=["bib"])


def write_entries(bibentries: list[dict[str, str]]) -> None:
    documents: dict[str, dict[str, str]] = {}
    for entry in bibentries:
        key = form_key(entry=entry)
        documents[key] = entry

    cb_coll: Collection = st.session_state.couch

    results: MultiGetResult = cb_coll.get_multi(list(documents.keys())).results
    for key in results:
        if key in documents:
            documents.pop(key)

    insert_results: MultiMutationResult = cb_coll.insert_multi(documents)
    written = len(insert_results.results.keys())
    if written > 0:
        st.write(f"Added {written} documents in the database.")

    existing = len(bibentries) - written
    if existing > 0:
        st.write(
            f"Skipped writing {existing} entries because they already exist in the database."
        )


upload = st.button(label="Upload")

if upload and bib_file:
    client = st.session_state.couch
    file_bytes = bib_file.read()
    text = file_bytes.decode()

    bibentries = parse_bibtext(text=text)
    write_entries(bibentries)
