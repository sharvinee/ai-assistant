import streamlit as st
from chat_interface import display_chat_interface

#Configure streamlit app
st.set_page_config(page_title="Horizon Internal Medicine Clinic", page_icon="⚕", layout = "centered")


# Custom CSS to align the title
st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="title">🩺 Horizon Internal Medicine Clinic AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<h5 class="title">"Access All the Clinic Information You Need - No Wait, No Hassle"</h5>', unsafe_allow_html=True)


# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for session_id and model if not already set
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "model" not in st.session_state:
    st.session_state.model = "gpt-4o-mini"  

# Display the chat interface
display_chat_interface()