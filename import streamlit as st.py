import streamlit as st
import requests

st.title("ChatGPT-style Chatbot with Perplexity")

# Configure the API endpoint and API key
API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = "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"  # Replace with your actual API key

# Initialize session state for storing chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

def send_message(prompt):
    # Define the payload for the API request
    payload = {
        "model": "llama-3-sonar-small-32k-online",
        "messages": [
            {"content": m['content'], "role": m['role']} for m in st.session_state.messages
        ] + [{"content": prompt, "role": "user"}],
        "max_tokens": 250,  # Adjust token limit as needed
        "temperature": 0.5,
        "top_p": 0.9,
        "return_citations": False,
        "return_images": False,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0.5
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }

    # Make a POST request to the Perplexity API
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    response_data = response.json()

    # Extract the text from the response
    return response_data["choices"][0]["message"]["content"]

# Streamlit chat interface
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("", value=message["content"], key=message["content"], disabled=True)
    else:
        st.text_area("", value=message["content"], key=message["content"] + "resp", disabled=True, style={"background-color": "#F0F2F6"})

# Input for new messages
user_input = st.text_input("Type your message:", key="user_input")

# Send button to submit new message
if st.button("Send"):
    if user_input:
        # Append the user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Get the model's response
        model_response = send_message(user_input)
        # Append the model response
        st.session_state.messages.append({"role": "system", "content": model_response})
        # Clear the input box
        st.session_state.user_input = ""
