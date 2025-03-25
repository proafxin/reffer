import os
from datetime import timedelta

import streamlit as st
from bson import ObjectId
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, ClusterTimeoutOptions
from couchbase.result import MultiMutationResult

from api.services.parser import parse_bibtext

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
    cluster = Cluster(endpoint, ClusterOptions(auth, timeout_options=timeout_opts))
    cluster.wait_until_ready(timedelta(seconds=5))

    cb = cluster.bucket(dbname)
    cb_coll = cb.scope(dbname).collection(collection)
    st.session_state.couch = cb_coll


bib_file = st.file_uploader(label="Upload bib file", type=["bib"])


def write_entries(bibentries: list[dict[str, str]]):
    documents: dict[str, dict[str, str]] = {}
    for entry in bibentries:
        objectid = str(ObjectId())
        documents[objectid] = entry

    cb_coll = st.session_state.couch
    insert_results: MultiMutationResult = cb_coll.insert_multi(documents)

    written = 0
    for key in documents:
        if key in insert_results.results:
            written += 1

    st.write(f"Successfully uploaded {written} entries!")


upload = st.button(label="Upload")

if upload and bib_file:
    client = st.session_state.couch
    file_bytes = bib_file.read()
    text = file_bytes.decode()

    bibentries = parse_bibtext(text=text)
    write_entries(bibentries)
