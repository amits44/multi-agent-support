import streamlit as st

st.title("Multi agent customer support")
st.markdown("a multi agent system for customer support")

st.header("whats your issue")
issue = st.text_area("your issue",)

if st.button("Search", type ="primary") and issue:
    st.spinner("helping you with your issue")