# OllamaBot

# Ollama Chat Bot with Streamlit

This project demonstrates a chatbot built using Streamlit and the Ollama API. The bot allows users to interact with a selected Ollama model and receive real-time responses. The conversation history is maintained, and the responses from the bot are streamed as they are generated.

## Features

- **Model Selection**: Users can select an Ollama model from the sidebar.
- **Real-Time Chat**: Messages are sent to the Ollama API, and responses are streamed back and displayed in real-time.
- **Chat History**: The conversation history is maintained throughout the session.

## Requirements

- **Python 3.x**
- **Streamlit**: Used for the frontend to display the chat interface.
- **Ollama**: The API service that provides the chatbot model.
- **Requests**: Used to send HTTP requests to the Ollama API.

To install the required dependencies, you can use `pip`:

```bash
pip install streamlit requests ollama
```



## Running the Streamlit App

To start the Streamlit app, use the following command:

```bash
streamlit run app.py
```



Start Ollama: To start the Ollama service, run the following command:

```bash
ollama start
```

Pull a Model: You can pull a model from Ollama's repository, such as the Mistral or Llama 3.1 models:

```bash
ollama pull mistral
ollama pull llama3.1
```

Run a Model: Once the model is pulled, you can run the model with the following command:

```bash
ollama run mistral
ollama pull llama3.1
```

Stop the Model: If you want to stop the model, use the following command:
```bash
ollama stop mistral
ollama stop llama3.1
```


## Ollama useful function

### List

```python
ollama.list()
```

### Show

```python
ollama.show('llama3.1')
```

### Delete

```python
ollama.delete('llama3.1')
```

### Pull

```python
ollama.pull('llama3.1')
```


## How It Works

1. Model Selection:
    - The user selects a model from the list of available models from Ollama, which are fetched dynamically using the ollama.list() API call.
2. Chat Interface:
    - The user can type their message in the input box, and the chat interface updates in real-time.
    - The bot's response is streamed back to the user using the stream_chat() function.
3. Streaming Responses:
    - The chatbot sends a POST request to the Ollama API with the user's message and conversation history.
    - The response is streamed back line by line and displayed as it is received. The stream parameter is set to True in the request to enable this behavior.
4. Maintaining Conversation History:
    - The conversation history is stored in the st.session_state object, allowing the bot to remember previous messages during the current session.
