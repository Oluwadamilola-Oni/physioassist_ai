import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="PhysioAssist AI", page_icon="🦴", layout="centered")

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/physiotherapy.png", width=80)
    st.title("PhysioAssist AI")
    st.markdown("""
    **Your AI-powered physiotherapy assistant.**
    
    I can help with:
    - 🦴 Joint & muscle pain
    - 🏃 Sports injuries
    - 🧍 Posture problems
    - 🔄 Recovery & rehab exercises
    - ❓ General physio questions
    """)
    st.divider()
    st.warning("⚠️ This app does not replace professional physiotherapy advice. Always consult a licensed physiotherapist for diagnosis and treatment.")
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main Area ---
st.title("🦴 PhysioAssist AI")
st.caption("Physiotherapy guidance, available anytime.")

# --- Welcome message on empty chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.markdown("""
    👋 **Welcome! I'm PhysioAssist AI.**
    
    I'm here to help you with physiotherapy-related questions and concerns.
    Whether you're dealing with pain, recovering from an injury, or looking for 
    exercise guidance — just ask me anything!
    
    **Here are some things you can ask me:**
    - *"I have lower back pain after sitting all day, what should I do?"*
    - *"What exercises help with a sprained ankle recovery?"*
    - *"My knee clicks when I walk, is that normal?"*
    - *"How do I improve my posture?"*
    
    > ⚠️ I provide general guidance only. For diagnosis and treatment, please see a licensed physiotherapist.
    """)

# --- Display chat history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat function ---
def chat(user_input):
    messages = [
        {
            "role": "system",
            "content": """
            You are PhysioAssist AI, a professional and friendly physiotherapy assistant 
            for the general public. You specialize in musculoskeletal and orthopedic rehab.
            
            Your goal is to provide safe, simple, and helpful physiotherapy guidance.
            You do NOT replace a licensed physiotherapist — always remind users to seek 
            professional help for diagnosis and treatment.
            
            If a question is completely unrelated to physiotherapy or health, politely 
            let the user know that you only handle physiotherapy-related questions.
            
            Always respond in this format:

            **Possible Cause:**
            ...

            **What To Do:**
            ...

            **What To Avoid:**
            ...

            **When To See a Physiotherapist:**
            ...

            Keep responses simple, clear, and patient-friendly.
            """
        }
    ]

    for msg in st.session_state.messages[-5:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    return response.choices[0].message.content

# --- Chat input ---
if prompt := st.chat_input("Describe your pain or ask a physiotherapy question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})