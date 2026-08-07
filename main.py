import os
import streamlit as st
from groq import Groq

# Page Config & Title - App Name set to Pro AI
st.set_page_config(page_title="Pro AI", page_icon="⚡", layout="centered")

st.title("⚡ Pro AI")
st.caption("Powered by Advanced AI | Fast & Intelligent Response")

# Fetch API Key from environment
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error(
        "❌ GROQ_API_KEY nahi mili! Kripya environment settings me API Key add karein."
    )
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! Main **Pro AI** hu. Aap mujhse koi bhi sawal pooch sakte hain.",
        }
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Pro AI se kuch bhi pucho..."):
    # Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Pro AI soch raha hai..."):
            try:
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                chat_completion = client.chat.completions.create(
                    messages=api_messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=1024,
                )

                response = chat_completion.choices[0].message.content
                st.markdown(response)

                # Save AI response
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
              
