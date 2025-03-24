import polars as pl
import streamlit as st

from api.services.parser import parse_bibtext

bib_file = st.file_uploader(label="Upload bib file", type=["bib"])
process = st.button(label="Submit")

if process and bib_file:
    file_bytes = bib_file.read()
    text = file_bytes.decode()

    bibentries = parse_bibtext(text=text)
    data = pl.DataFrame(bibentries)
    for column in data.columns:
        if data[column].null_count() == data.shape[0]:
            data = data.drop(column)
    st.dataframe(data, use_container_width=True)
