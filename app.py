import streamlit as st
from prediction import search_location

st.set_page_config(page_title="Job search location", page_icon="📍", layout="wide", initial_sidebar_state="expanded")
st.title("Job search location")

search_key = "City, state, zip code"

with st.form(key='searchform'):
    text_search = st.text_input("Enter location", value="", key=search_key)
    submit_button = st.form_submit_button(label='Search')

@st.cache_data(ttl=10, show_spinner=False)
def search_and_display_results(text):
    if text:
        try:
            if submit_button:
                results = search_location(text)
                for result in results:
                    st.write(result['entity_name'])
        except:
            st.error('No location found.')

search_and_display_results(text_search)