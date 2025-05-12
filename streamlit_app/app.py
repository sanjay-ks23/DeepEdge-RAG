import streamlit as st
import requests
import json

st.set_page_config(
    page_title="RAG Search Assistant",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1E88E5;
    }
    .sub-header {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: #424242;
    }
    .response-container {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">LLM-based RAG Search Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask me anything and I\'ll search and scrape the information from the web for you!</p>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user query
query = st.chat_input("Ask the LLM...")

# Flask API endpoint
FLASK_ENDPOINT = "http://localhost:5001/query"

# Reset conversation button
if st.sidebar.button("Reset Conversation"):
    # Clear chat history in session state
    st.session_state.messages = []
    
    # Call reset endpoint
    try:
        reset_response = requests.post("http://localhost:5001/reset")
        if reset_response.status_code == 200:
            st.sidebar.success("Conversation history cleared!")
        else:
            st.sidebar.error(f"Error: {reset_response.status_code}")
    except Exception as e:
        st.sidebar.error(f"Could not connect to server: {e}")
    
    # Rerun the app to refresh the UI
    st.rerun()

# Process user query when submitted
if query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(query)
    
    # GUI feedback while waiting for the response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Searching the web and generating response...")
        
        try:
            # Make a POST request to the Flask API
            response = requests.post(
                FLASK_ENDPOINT,
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                # Extract the answer from the response
                answer = response.json().get('answer', "No answer received.")
                
                message_placeholder.markdown(answer)

                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                message_placeholder.markdown(f"Error: {response.status_code}")
                st.error(f"Server error: {response.status_code}")
        except Exception as e:
            message_placeholder.markdown(f"Connection error: {e}")
            st.error(f"Could not connect to server: {e}")

with st.sidebar:
    st.markdown("## About")
    st.markdown("""
    This RAG (Retrieval-Augmented Generation) system:
    1. Searches the web for your query
    2. Retrieves relevant articles
    3. Extracts key information
    4. Generates an informative answer
    
    The system maintains conversation memory to provide contextual responses.
    """)
