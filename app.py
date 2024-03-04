import streamlit as st
from prediction import search_location

st.set_page_config(page_title="Job search location", page_icon="📍", layout="wide")
st.title("Job search location")

search_key = "City, state, zip code"

text_search = st.text_input("Enter location", value="", key=search_key)

change_event_script = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.querySelector('input[data-testid="stSessionState"]'); // Find the text input field
    textInput.addEventListener('input', function() {
        const value = textInput.value; // Get the current value of the input field
        const event = new Event('change'); // Create a change event
        textInput.dispatchEvent(event); // Dispatch the change event
    });
});
</script>
"""

st.markdown(change_event_script, unsafe_allow_html=True)

@st.cache_data
def search_and_display_results(text):
    if text:
<<<<<<< Updated upstream
        results = search_location(text)
        for result in results:
            st.write(result['entity_name'])
=======
        try:
            if submit_button:
                results = search_location(text, 15)
                for result in results:
                    st.write(result['entity_name'])
        except:
            st.error('No location found.')
>>>>>>> Stashed changes

search_and_display_results(text_search)