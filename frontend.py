
import streamlit as st
import requests
import os

st.title("RAG Application")

question = st.text_input("Ask a question:")

if st.button("Submit"):
    if question:
        try:
            backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
            response = requests.post(f"{backend_url}/ask", json={"question": question})
            response.raise_for_status()  # Raise an exception for bad status codes
            answer = response.json().get("answer")
            st.write("**Answer:**")
            st.write(answer)
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the backend: {e}")
    else:
        st.warning("Please enter a question.")
