import os
import streamlit as st
from groq import Groq

# 1. Custom Neon PAi Icon set for Browser Tab
ICON_URL = "https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png"

st.set_page_config(
    page_title="Pro AI",
    page_icon=ICON_URL,  # Isse red crown icon hat kar neon icon aayega
    layout="centered",
)

# 2. Inject PWA Manifest Links
st.markdown(
    f"""
    <head>
        <link rel="manifest" href="https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/manifest.json">
        <link rel="apple-touch-icon" sizes="180x180" href="{ICON_URL}">
        <link rel="icon" type="image/png" sizes="32x32" href="{ICON_URL}">
    </head>
    """,
    unsafe_allow_html=True,
)

# 3. Header & UI Design
st.title("⚡ Pro AI")
st.caption("Powered by Advanced AI | Fast & Intelligent Response")

# 4. Groq API Logic Setup
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error(
        "❌ GROQ_API_KEY nahi mili! Kripya environment settings me API Key add karein."
    )
    st.stop()

client = Groq(api_key=api_key)

# 5. Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! Main **Pro AI** hu. Aap mujhse koi bhi sawal pooch sakte hain.",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input & Response Loop
if prompt := st.chat_input("Pro AI se kuch bhi pucho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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

                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
                
