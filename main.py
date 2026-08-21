import os
import re
import time
import urllib.parse
import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Pro AI", page_icon="⚡", layout="centered", initial_sidebar_state="collapsed")

# 2. CSS - Ultra Clean Interface
st.markdown("""
    <style>
        [data-testid="stSidebar"], footer, header, #MainMenu { display: none !important; }
        .stApp { background-color: #0d1117 !important; color: #ffffff !important; }
        .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; max-width: 800px !important; }
        .pro-header { background: #161b22; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 20px; border: 1px solid #30363d; }
        [data-testid="stChatMessage"] { background-color: #161b22 !important; border: 1px solid #30363d !important; border-radius: 12px !important; }
        .stChatInput > div { border-radius: 12px !important; background-color: #161b22 !important; border: 1px solid #30363d !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown('<div class="pro-header"><h2 style="color:white">⚡ Pro AI</h2><p style="color:#8b949e">System: Online & Stable</p></div>', unsafe_allow_html=True)

# 4. API Client with Error Handling
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("API Key missing!")
    st.stop()
client = Groq(api_key=GROQ_API_KEY)

# 5. Logic to generate response with Fallbacks
def get_ai_response(messages):
    models = ["llama-3.1-8b-instant", "gemma2-9b-it", "llama3-70b-8192"]
    for model in models:
        try:
            chat = client.chat.completions.create(messages=messages, model=model, temperature=0.7, max_tokens=1024)
            return chat.choices[0].message.content
        except Exception:
            continue # Try next model if one fails
    return "❌ Server busy hai, kripya 5 seconds baad dobara puchein."

# 6. Session Logic
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste! Main Pro AI hu. Main aapki kya madad kar sakta hu?"}]

for msg in st.session_state.messages:
    avatar = "⚡" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if "image_url" in msg: st.image(msg["image_url"], use_column_width=True)

# 7. Chat Input
if prompt := st.chat_input("Ask ProAi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="⚡"):
        # Image Generation Logic
        if any(kw in prompt.lower() for kw in ["image", "photo", "pic", "banao"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
            st.image(url, use_column_width=True)
            st.session_state.messages.append({"role": "assistant", "content": "Ye rahi image:", "image_url": url})
        else:
            # Robust Text Logic
            with st.spinner("Processing..."):
                formatted_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                response = get_ai_response(formatted_msgs)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
