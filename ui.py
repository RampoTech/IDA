import streamlit as st
from orhestrate_agent import orhestrate_agent

# Page config
st.set_page_config(page_title="Incident Diagnosis & Orchestration Agent", page_icon="💬")

st.title("Incident Diagnosis & Orchestration Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })


    # Simple bot response (echo / demo logic)
    bot_response = orhestrate_agent(user_input)

    # Show bot message
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # Save bot message
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })
