# filebundler/ui/confirm.py

# https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog

import streamlit as st


@st.dialog("Confirm")
def confirm(title: str):
    st.write(title)
    if st.button("confirm"):
        return True
    if st.button("cancel"):
        return False
