import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from llm import conversational_llm_from_settings, Settings

# Load environment variables
load_dotenv()

# Initialize settings and LLM
settings = Settings()
chat_llm = conversational_llm_from_settings(settings)

# Initialize message history
msgs = StreamlitChatMessageHistory(key="langchain_messages")

# Streamlit page configuration
st.set_page_config(page_title="Simple Chatbot", page_icon="💬")
st.title("Simple Chatbot 💬")

# Display existing chat messages
for msg in msgs.messages:
    with st.chat_message(msg.type):
        st.write(msg.content)

# Handle new user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to the history and display it
    user_message = HumanMessage(content=prompt)
    msgs.add_message(user_message)
    with st.chat_message("user"):
        st.write(prompt)

    # Generate AI response
    def generate_reply(prompt: str) -> str:
        response = chat_llm.generate(prompt)  # Adjust according to your LLM's API
        return response.strip()

    response = generate_reply(prompt)

    # Add AI message to the history and display it
    ai_message = AIMessage(content=response)
    msgs.add_message(ai_message)
    with st.chat_message("ai"):
        st.write(response)

# Option to reset the chat
if st.sidebar.button("Reset Chat"):
    msgs.clear()
    st.session_state["messages"] = []
    st.write("Chat history has been cleared.")

# This will ensure messages are displayed correctly in the UI
if "messages" in st.session_state:
    for msg in st.session_state["messages"]:
        with st.chat_message(msg.type):
            st.write(msg.content)
else:
    st.session_state["messages"] = []

# Handle chat history updates
for msg in msgs.messages:
    st.session_state["messages"].append(msg)
