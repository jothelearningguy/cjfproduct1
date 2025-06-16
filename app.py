import streamlit as st
import requests
import json
import pandas as pd
import io

# Set page config
st.set_page_config(
    page_title="CSV Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# API configuration
API_URL = "http://localhost:8000"

# Sidebar
with st.sidebar:
    st.title("About")
    st.write("""
    This application uses three specialized AI agents to analyze your CSV data:
    
    🤖 **Coordinator Agent**: Manages the workflow and synthesizes responses
    
    📊 **Information Extractor**: Analyzes and extracts data insights
    
    🔍 **Researcher**: Provides deeper context and interpretations
    """)
    
    st.write("---")
    st.write("Made with ❤️ using Streamlit and OpenAI")

# Main content
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("CSV Chatbot 🤖")
st.write("Upload a CSV file and ask questions about your data!")
st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Upload file to server
        files = {'file': uploaded_file}
        response = requests.post(f"{API_URL}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.session_id = data['session_id']
            st.success("File uploaded successfully!")
        else:
            st.error(f"Error uploading file: {response.json().get('error', 'Unknown error')}")
            
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")

# Chat interface
if st.session_state.session_id:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your data"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        try:
            # Send question to server
            response = requests.post(
                f"{API_URL}/ask",
                json={
                    'question': prompt,
                    'session_id': st.session_state.session_id
                }
            )
            
            if response.status_code == 200:
                answer = response.json()['response']
                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.write(answer)
            else:
                error_msg = response.json().get('error', 'Unknown error')
                st.error(f"Error: {error_msg}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload a CSV file to start asking questions!") 