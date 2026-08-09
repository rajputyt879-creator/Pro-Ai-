import os
import re
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

# 2. Modern Dark Theme, Zero-Margin CSS & Permanent Toolbar Removal
st.markdown(
    """
    <style>
        /* Permanently Hide all Streamlit branding, toolbars, and badges */
        [data-testid="stSidebar"], [data-testid="collapsedControl"], footer, header, #MainMenu, 
        .stAppToolbar, [data-testid="stStatusWidget"], [data-testid="stToolbar"], 
        div[class*="viewerBadge"], div[class*="stDecoration"], div[class*="stActionButton"], 
        div[class*="stAppHeader"], div[class*="stBottom"], .stDeployButton, 
        div[data-baseweb="popover"], a[href*="streamlit.io"],
        div[class*="viewerBadge"] {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
            width: 0px !important;
            pointer-events: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Full Dark Theme with Zero Side Gaps */
        .stApp {
            background-color: #0d1117 !important;
            color: #ffffff !important;
        }

        /* Remove side white margins */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 2rem !important;
            max-width: 800px !important;
        }
        
        /* Header Card */
        .pro-header-card {
            background: #161b22;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }

        .pro-title { font-size: 2.2rem; font-weight: 800; color: #ffffff !important; margin-bottom: 4px; }
        
        .security-badge {
            font-size: 0.75rem; color: #10a37f !important;
            background-color: rgba(16, 163, 127, 0.15);
            padding: 4px 12px; border-radius: 20px;
            border: 1px solid rgba(16, 163, 127, 0.3);
            display: inline-block; margin-bottom: 8px; font-weight: 600;
        }

        .pro-subtitle { color: #c9d1d9 !important; font-size: 1.1rem; font-weight: 700; margin-top: 4px; }

        /* Chat Message High-Contrast */
        [data-testid="stChatMessage"] {
            background-color: #161b22 !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            margin-bottom: 10px !important;
            padding: 12px 16px !important;
        }

        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div {
            color: #ffffff !important;
            font-size: 1.05rem !important;
        }

        /* Input Area Fix */
        .stChatInput > div {
            background-color: #161b22 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Header
st.markdown(
    """
    <div class="pro-header-card">
        <div class="security-badge">🔏 Secure AI Engine Active</div>
        <div class="pro-title">⚡ Pro AI</div>
        <div class="pro-subtitle">Ask ProAi</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Logic (Same as before) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY missing!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Namaste! Main **Pro AI** hu. Main aapki kya madad kar sakta hu?"}]

for message in st.session_state.messages:
    avatar = "⚡" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "image_url" in message: st.image(message["image_url"], use_column_width=True)

if prompt := st.chat_input("Ask ProAi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="⚡"):
        if any(kw in prompt.lower() for kw in ["image", "photo", "banao"]):
            encoded = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"
            st.image(url, use_column_width=True)
            st.session_state.messages.append({"role": "assistant", "content": "Ye rahi aapki image:", "image_url": url})
        else:
            chat = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama-3.3-70b-versatile")
            resp = chat.choices[0].message.content
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp})
            
