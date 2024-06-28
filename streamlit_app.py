import streamlit as st
import requests

st.title("ChatGPT-style Chatbot with Perplexity")

# Initialize 'messages' in session_state if not already present
if 'messages' not in st.session_state:
    st.session_state.messages = []

url = "https://api.perplexity.ai/chat/completions"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer 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"
}

def send_message(user_input):
    payload = {
        "model": "llama-3-sonar-small-32k-online",
        "messages": [
            {
                "content": user_input,
                "role": "user"
            }
        ],
        "max_tokens": 300,
        "temperature": 0.2,
        "top_p": 0.9,
        "return_citations": False,
        "return_images": False,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return "An error occurred while contacting the API."

# Streamlit chat interface
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("", value=message["content"], key=message["content"], disabled=True)
    else:
        st.text_area("", value=message["content"], key=message["content"] + "resp", disabled=True)

# Input for new messages
user_input = st.text_input("Type your message:", key="new_user_input")

# Send button to submit new message
if st.button("Send"):
    if user_input:
        # Append the user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        # Get the model's response
        model_response = send_message(user_input)
        # Append the model response
        st.session_state.messages.append({"role": "system", "content": model_response})
        # Clear the input box by rerunning the script
        st.experimental_rerun()
