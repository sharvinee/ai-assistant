import streamlit as st
from api_utils import get_api_response

def display_chat_interface():
    # displays the chat interface for user and AI assistant interaction

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Your message"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Generating response..."):
            response = get_api_response(prompt, st.session_state.session_id, st.session_state.model)
            
            # check if response was received from API
            if response:
                st.session_state.session_id = response.get('session_id')
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})  # append assistant's response to session state
                
                with st.chat_message("assistant"):  #display AI assistant's response in chat interface
                    st.markdown(response['answer'])
                    
            else:  # display error message if API response fails
                st.error("Failed to get a response from the API. Please try again.")