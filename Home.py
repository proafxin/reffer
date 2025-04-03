import os
from datetime import timedelta

import streamlit as st
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, ClusterTimeoutOptions

from api.services.search import collection, dbname

username = os.environ["MONGO_USER"]
password = os.environ["MONGO_PASSWORD"]
host = os.environ["MONGO_HOST"]

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

__VERSION__ = "1.2"

st.set_page_config(layout="wide", page_title="Reffer")
st.title("Reffer")
st.subheader("A community based open source reference solution.")
st.write(
    "Reffer is a community based open source reference solution that allows you to store, search and add your references."
)
st.subheader(
    ":green[The database only has 8GB storage. Please be responsible in using this]"
)

st.subheader("How Does Parsing Work?")
st.text(
    "Reffer uses the `bibtextparser` python package internally to parse your bib file. It then stores the parsed data in a NoSQL database. You can then search for your references."
)
st.text(
    "Now, the work is not done after the parsing. To make the bibliography entries retrieved from the file searchable, we need to clean it first."
)
st.subheader("How Does Cleaning Work?")
st.text(
    "After the bib file is parsed, we get a list of objects. Each object represents a bibliography entry. However, the title or author or journal or publisher may contain undesirable or harmful characters for database searching."
)
st.text(
    "For example, a common occurence is that the title contains LaTeX expressions. Sometimes the author names contain single apostrophe which is harmful for query language commands (the database used internally is Couchbase Capella, a NoSQL database with a syntax called SQL++ which essentially is very similar to SQL in nature). Both must be removed to make the entry searchable."
)
st.text(
    "Therefore, we clean and tokenize the title, string into a list of tokens. So, during a search, we will check if all of the tokens are contained within the title of any entry."
)
st.text(
    "The same procedure is repeated for journal, publisher and authors. This way, we make sure we won't burn down the system."
)
st.text(
    "This approach presented a big problem initially. Every query would take a long time. Now during a search, we are searching only one entry."
)
st.text(
    "This application supports uploading multiple entries during which first it is checked if any of them are already within the database. If so, they are not uploaded again and only new entries are uploaded."
)
st.text(
    "This way database does not have any duplicate entries, storage is saved and search also remains faster."
)
st.text(
    "Now imagine you have a bib file of 150 entries (mine had close to 200). If you upload it, most of the entries will have at least 2/3 of the 4 fields: author, journal, title, publisher."
)
st.text(
    "Now author string may contain more than 1 tokens and more so if there are multiple authors. Same for journal, publisher and title."
)
st.text(
    "Then in each search we will have to check if all the title tokens are contained in an entry title, all author tokens are contained in the author token and so on."
)
st.text(
    "As you can guess this search will be VERY slow. In fact it was that slow. And for a file with 100+ bib entries, it will be 100+ times slower."
)
st.text(
    "You may notice that the search and upload functionality is to the contrary, lightning fast. That's because I did something to solve the problem we just saw above. I am not going into details. I just wanted to point out how the search works so you have an idea how duplicate entries are identified during search or upload."
)
