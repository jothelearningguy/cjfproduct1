import streamlit as st
import pandas as pd
import requests
import json
from io import StringIO
import time

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
st.write("Upload a CSV file and ask questions about its contents!")
st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'session_id' not in st.session_state:
    st.session_state.session_id = None

# File uploader
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    try:
        # Upload file to server
        files = {"file": uploaded_file}
        response = requests.post(f"{API_URL}/upload", files=files)
        response.raise_for_status()
        
        data = response.json()
        st.session_state.session_id = data["session_id"]
        
        # Display the preview
        st.markdown('<div class="data-preview">', unsafe_allow_html=True)
        st.subheader("Preview of your data")
        st.dataframe(pd.DataFrame(data["preview"]))
        
        st.subheader("Columns in your dataset")
        st.write(data["columns"])
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")

# Chat interface
if st.session_state.session_id is not None:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.subheader("Ask questions about your data")
    
    # Agent status indicators
    st.markdown('<div class="agent-status">', unsafe_allow_html=True)
    st.markdown("""
        <div class="agent">
            <div class="agent-icon coordinator"></div>
            <span>Coordinator</span>
        </div>
        <div class="agent">
            <div class="agent-icon extractor"></div>
            <span>Extractor</span>
        </div>
        <div class="agent">
            <div class="agent-icon researcher"></div>
            <span>Researcher</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your data"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Show processing state
        st.session_state.processing = True
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 Thinking...")

            try:
                # Send question to server
                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": prompt,
                        "session_id": st.session_state.session_id
                    }
                )
                response.raise_for_status()
                
                data = response.json()
                final_response = data["response"]

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                message_placeholder.markdown(final_response)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please make sure the server is running and accessible.")
            
            finally:
                st.session_state.processing = False

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Please upload a CSV file to start asking questions!") 