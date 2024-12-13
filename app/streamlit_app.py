import streamlit as st

home = st.Page("./home.py", title="Home", icon=":material/home:")
asr = st.Page("./asr.py", title="ASR", icon=":material/mic:")

pg = st.navigation([home, asr])

pg.run()