import os
import urllib.parse
import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Pro AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. CSS - Responsive Layout & High-Contrast Text
st.markdown(
    """
    <style>
        [data-testid="stSidebar"], [data-testid="collapsedControl"], footer, header, #MainMenu { display: none !important; }
        .stApp { background-color: #0d1117 !important; color: #ffffff !important; }
        .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; max-width: 800px !important; }
        
        /* Mobile-Friendly Table Fix */
        table { width: 100% !important; table-layout: fixed !important; }
        th, td { word-wrap: break-word !important; white-space: normal !important; overflow-wrap: break-word !important; }
        
        .pro-header-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 15px; }
        [data-testid="stChatMessage"] { background-color: #161b22 !important; border: 1px solid #30363d !important; border-radius: 12px !important; }
        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div { color: #ffffff !important; font-size: 1.05rem !important; }
        .stChatInput > div { border-radius: 12px !important; background-color: #161b22 !important; border: 1px solid #30363d !important; }
        .stChatInput textarea { color: white !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Header
st.markdown('<div class="pro-header-card"><h2 style="color:white">⚡ Pro AI</h2><p style="color:#8b949e">Accuracy: High | Mode: Stable</p></div>', unsafe_allow_html=True)

# 4. API Client
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY: st.error("API Key missing!")
client = Groq(api_key=GROQ_API_KEY)

# 5. Session Setup
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste! Main Pro AI hu. Main aapki kya madad kar sakta hu?"}]

for message in st.session_state.messages:
    avatar = "⚡" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "image_url" in message: st.image(message["image_url"], use_container_width=True)

# 6. Logic with Language Perfection Prompt
if prompt := st.chat_input("Ask ProAi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="⚡"):
        if any(kw in prompt.lower() for kw in ["image", "photo", "pic", "banao"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
            st.image(url, use_container_width=True)
            st.session_state.messages.append({"role": "assistant", "content": "Ye rahi image:", "image_url": url})
        else:
            with st.spinner("Processing..."):
                # Professional Language Prompt
                system_prompt = (
                    "You are Pro AI, a precise expert linguist. "
                    "When answering in Hindi or English, ensure perfect grammar, formal yet natural tone, and high cultural accuracy. "
                    "Do not use casual slang. For tables or lists, keep text concise so it fits on mobile devices."
                )
                
                msgs = [{"role": "system", "content": system_prompt}] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                
                try:
                    # Fetching models dynamically
                    models = [m.id for m in client.models.list().data if "whisper" not in m.id]
                    response = client.chat.completions.create(messages=msgs, model=models[0], temperature=0.5).choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error: {e}")
                    
