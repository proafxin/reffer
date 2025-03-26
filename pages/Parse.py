import polars as pl
import streamlit as st

from api.services.parser import parse_bibtext

bib_file = st.file_uploader(label="Upload bib file", type=["bib"])

if "parse" not in st.session_state:
    st.session_state.parse = False


def parse() -> None:
    st.session_state.parse = True


def show_entry(entry: dict[str, str | list[str]]) -> None:
    for key, value in entry.items():
        st.write(f"**{key}**: {value}")


st.button("Parse", on_click=parse)

if st.session_state.parse and bib_file:
    file_bytes = bib_file.read()
    text = file_bytes.decode()

    bibentries = parse_bibtext(text=text)
    data = pl.DataFrame(bibentries)
    for column in data.columns:
        if data[column].null_count() == data.shape[0]:
            data = data.drop(column)

    show_data = st.checkbox(label="Show data", value=False)
    if show_data:
        st.dataframe(data)
