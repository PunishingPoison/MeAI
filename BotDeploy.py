import streamlit as st
from huggingface_hub import InferenceClient
import time

# Initialize the Inference Client with your API key
client = InferenceClient(api_key="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")

# Streamlit app setup
st.set_page_config(page_title="Another Me AI Chatbot", layout="wide", page_icon="🤖")
st.markdown(
    """
    <style>
    body {
        background-color: #f9f9f9;
        color: #333;
    }
    .stApp {
        background-color: #ffffff;
        color: #333;
    }
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }
    .chat-message {
        display: flex;
        align-items: flex-start;
        margin: 10px 0;
    }
    .chat-message.user {
        justify-content: flex-end;
        text-align: right;
    }
    .chat-message.ai {
        justify-content: flex-start;
        text-align: left;
    }
    .message-bubble {
        max-width: 70%;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    .message-bubble.user {
        background-color: #e6f7ff;
        color: #333;
        border: 1px solid #d9edf7;
    }
    .message-bubble.ai {
        background-color: #f0f0f0;
        color: #333;
        border: 1px solid #e0e0e0;
    }
    .message-name {
        font-size: 12px;
        color: #555;
        margin-bottom: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Chat context
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.markdown('<div class="header">Chat with Another Me AI</div>', unsafe_allow_html=True)

# Chat area
chat_container = st.container()
with chat_container:
    for msg in st.session_state["messages"]:
        role = msg["role"]
        content = msg["content"]
        name = "Me" if role == "user" else "Another Me AI"
        alignment_class = "user" if role == "user" else "ai"
        st.markdown(
            f"""
            <div class="chat-message {alignment_class}">
                <div>
                    <div class="message-name">{name}</div>
                    <div class="message-bubble {alignment_class}">{content}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# User input area
with st.form("user_input_form"):
    user_input = st.text_area("Your message:", key="user_input", placeholder="Type your message here...", height=100)
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    # Append user input to the chat context
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Display user message
    with chat_container:
        st.markdown(
            f"""
            <div class="chat-message user">
                <div>
                    <div class="message-name">Me</div>
                    <div class="message-bubble user">{user_input}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Placeholder for AI response
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(
            """
            <div class="chat-message ai">
                <div>
                    <div class="message-name">Another Me AI</div>
                    <div class="message-bubble ai">Another Me AI is typing...</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Call the AI model
    response_chunks = []
    full_response = ""
    stream = client.chat.completions.create(
        model="meta-llama/Llama-3.2-11B-Vision-Instruct",
        messages=[
            {"role": "user", "content": [{"type": "text", "text": user_input}]}
            for msg in st.session_state["messages"]
        ],
        max_tokens=2000,
        stream=True,
    )

    # Collect response dynamically
    for chunk in stream:
        text = chunk.choices[0].delta.content
        response_chunks.append(text)
        full_response += text

    # Replace "Another Me AI is typing..." with the actual response
    placeholder.empty()
    with chat_container:
        st.markdown(
            f"""
            <div class="chat-message ai">
                <div>
                    <div class="message-name">Another Me AI</div>
                    <div class="message-bubble ai">{full_response}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Add response to the chat context
    st.session_state["messages"].append({"role": "assistant", "content": full_response})