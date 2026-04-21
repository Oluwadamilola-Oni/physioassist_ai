import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="PhysioAssist AI", page_icon="🧠", layout="centered")

st.title("🧠 PhysioAssist AI")
st.caption("Your AI-powered physiotherapy assistant")

st.warning("⚠️ This chatbot provides general physiotherapy guidance and is not a substitute for professional medical advice.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to call OpenAI
def chat(user_input):
    messages = [
        {
            "role": "system",
            "content": """
            You are a professional physiotherapy assistant.
            You specialize in musculoskeletal and orthopedic rehab.
            Use the conversation history to give more relevant and personalized answers.
            Always respond in this format:

            Possible Cause:
            ...

            What To Do:
            ...

            What To Avoid:
            ...

            When To See a Physiotherapist:
            ...

            Keep it simple, safe, and patient-friendly.
            Always remind users to consult a licensed physiotherapist for proper diagnosis.
            """
        }
    ]

    # Add past messages for memory
    for msg in st.session_state.messages[-5:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add current user message
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    return response.choices[0].message.content

# Chat input
if prompt := st.chat_input("Describe your pain or ask a question..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display thinking spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat(prompt)
            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})