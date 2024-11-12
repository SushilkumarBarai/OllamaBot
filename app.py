
"""
Author: Sushilkumar Barai
Email: sushilkumarbarai123456@gmail.com
Date: 12-11-2024
Description: This project demonstrates a chatbot built using Streamlit and the Ollama API. 
The bot allows users to interact with a selected Ollama models and receive real-time responses.
 The conversation history is maintained, and the responses from the bot are streamed as they are generated.

Version: 1.0.0
"""

import streamlit as st
import requests
import json
import ollama
import time

# Streamlit page configuration

st.set_page_config(layout="wide", page_title="🦙💬 Llama 2 Chatbot", page_icon="🦙")

# Sidebar configuration
st.sidebar.title("Ollama Chat Model 🦙")

# Fetch the available models from Ollama
try:
    OLLAMA_MODELS = ollama.list()["models"]
except Exception as e:
    st.warning("It seems that Ollama is not installed on your system. Please make sure Ollama is installed first. "
               "You can find more details on how to install Ollama here: [https://ollama.ai](https://ollama.ai).")
    st.stop()

# Dropdown function to select model
def select_model():
    model_options = [model['name'] for model in OLLAMA_MODELS]
    selected_model = st.sidebar.selectbox("Select a model:", model_options)
    return selected_model

# Select model from sidebar
selected_model = select_model()

# Function to stream chatbot response from Ollama API
def stream_chat(user_input, selected_model, conversation_history):
    url = "http://localhost:11434/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": selected_model,  # Use the selected model in the request body
        "stream": True,
        "messages": conversation_history + [
              {"role": "assistant", "content": "Your name is Alexa. You are a helpful assistant. Greet the user first time. You can provide solutions to any question. Provide any solution, max 20 words only. With your extensive knowledge, you can assist with a wide range of topics, from everyday tasks to complex problems. Whether it's finding information, troubleshooting issues, or offering recommendations, you're here to help. Your goal is to make users' lives easier and more efficient by providing accurate and timely assistance."},
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        
        if response.status_code == 200:
            bot_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        message = json.loads(line.decode('utf-8'))
                        if 'message' in message and 'content' in message['message']:
                            bot_response += message['message']['content']
                            yield bot_response
                    except json.JSONDecodeError:
                        continue
        else:
            st.error(f"Error: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        st.error(f"Request error: {e}")

# Initialize session state to keep track of chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello, I am Alia. How can I help you?"}
    ]

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(message["content"])
    elif message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])

# Input box for the user to type their message
user_query = st.chat_input("Type your message here...")
if user_query:
    # Append the user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # Display the user message in chat interface
    with st.chat_message("user"):
        st.markdown(user_query)

    # Prepare to display the AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # Placeholder for streaming response

        # Stream the bot's response in real-time
        bot_response = ""
        for partial_response in stream_chat(user_query, selected_model, st.session_state.chat_history):
            bot_response = partial_response
            response_placeholder.markdown(bot_response)
            time.sleep(0.1)  # Adjust speed of streaming if needed

        # Add the complete bot response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
