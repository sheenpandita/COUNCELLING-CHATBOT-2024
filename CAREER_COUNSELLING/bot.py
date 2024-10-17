
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
# Load environment variables
load_dotenv()

# Configure Streamlit page settings with blue-themed elements
st.set_page_config(
    page_title="Career Counseling Bot",
    page_icon="🎓",  # Graduation cap icon to suit the student/career theme
    layout="centered",
)

# Get Google API Key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session and history in Streamlit
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Stores only user inputs

# Sidebar for user input history (student-only input)
with st.sidebar:
    st.header("📚 Your Questions")
    st.write("Here are your past queries about your career:")
    
    # Show user input history in the sidebar
    if st.session_state.chat_history:
        for idx, message in enumerate(st.session_state.chat_history):
            st.markdown(f"**Query {idx+1}:** {message}")
    else:
        st.write("No queries yet.")
    
    # Clear history button
    if st.button("Clear Questions"):
        # Clear both chat session and user input history
        st.session_state.chat_history = []  # Clear user inputs
        st.session_state.chat_session.history = []  # Clear entire chat session
        st.experimental_set_query_params()  # Refresh the app to apply changes

# Main chatbot interface
st.title("🎓 Career Counseling Bot")
st.subheader("Helping you plan your career with confidence 💼")
st.write(
    """
    Welcome to your Career Counseling Bot! Feel free to ask any questions regarding your career, 
    education path, or skill development. Let’s build your future together!
    """
)

# Blue-themed styling for the chatbot area
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f8ff;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage.user {
        background-color: #d0e7ff;  /* Light blue for user */
    }
    .stChatMessage.assistant {
        background-color: #a0c4ff;  /* Darker blue for assistant */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the current chat session (assistant's responses only in the main chat)
for message in st.session_state.chat_session.history:
    if translate_role_for_streamlit(message.role) == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message.parts[0].text)

# User input box
user_prompt = st.chat_input("Ask about your career, education, or skills...")

if user_prompt:
    # Show user's question in the main chat area and store it in session state
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append(user_prompt)  # Store only user inputs

    # Get response from Gemini-Pro
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    
    # Show Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text) 
