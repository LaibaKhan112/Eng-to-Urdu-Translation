import streamlit as st
from dotenv import load_dotenv
import os
from ai71 import AI71 

# Load environment variables from .env file
load_dotenv()

# Set up AI71 API key
AI71_API_KEY = os.getenv("AI71_API_KEY")

# Initialize the AI71 client
client = AI71(AI71_API_KEY)

# OpenAI interaction function
def translate_to_urdu(text):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Translate the following text to Urdu: {text}"},
    ]
    translation = ""
    try:
        for chunk in client.chat.completions.create(
            model="tiiuae/falcon-180b-chat",
            messages=messages,
            stream=True,
        ):
            if chunk.choices[0].delta.content:
                translation += chunk.choices[0].delta.content
        return translation.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit app interface
st.title("English to Urdu")

input_text = st.text_area("Enter any Text")

if st.button("Translate"):
    if input_text:
        urdu_translation = translate_to_urdu(input_text)
        st.write("Urdu Translation:")
        st.write(urdu_translation)
    else:
        st.warning("Empty Text")
