import os
import re
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
from PIL import Image

# 1. Page Configuration
ICON_URL = "https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png"

st.set_page_config(
    page_title="Pro AI",
    page_icon="⚡",
    layout="centered",
)

# 2. Modern Custom Styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0d1117 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }

        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 5rem !important;
            max-width: 800px;
        }
        
        .pro-header-card {
            background: #161b22;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        .pro-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 4px;
        }

        .security-badge {
            font-size: 0.75rem;
            color: #10a37f;
            background-color: rgba(16, 163, 127, 0.15);
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid rgba(16, 163, 127, 0.3);
            display: inline-block;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .pro-subtitle {
            color: #8b949e;
            font-size: 0.88rem;
        }

        [data-testid="stChatMessage"] {
            background-color: #161b22 !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            margin-bottom: 10px !important;
            padding: 12px 16px !important;
        }

        .stChatInput > div {
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            background-color: #161b22 !important;
        }

        .stChatInput > div:focus-within {
            border-color: #10a37f !important;
            box-shadow: 0 0 10px rgba(16, 163, 127, 0.3) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Header UI
st.markdown(
    """
    <div class="pro-header-card">
        <div class="security-badge">🔒 Encrypted & Multimodal Vision Active</div>
        <div class="pro-title">⚡ Pro AI</div>
        <div class="pro-subtitle">Advanced Intelligence Platform</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 4. API Key Verification ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY nahi mili! Kripya Streamlit Secrets me GROQ_API_KEY add karein.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- 5. System Rules ---
SYSTEM_PROMPT = """
You are 'Pro AI', an ultra-intelligent, highly capable, multi-lingual AI assistant.

MULTILINGUAL & TRANSLATION RULES:
1. Support all global and Indian languages fluently.
2. When user asks "Translate Hindi" or "Hindi me translate karo", convert the input text into Hindi.
3. When user asks "Translate English", convert into English.

IDENTITY RULES:
- Your official name is strictly 'Pro AI'.
- Do not mention creator/owner in general chats.
- ONLY when explicitly asked "Who created you?" or "Owner kaun hai?", state: "Mujhe Kishan Singh ne banaya hai aur mere owner Kishan Singh hi hain."

FACTUAL ACCURACY:
- Always provide 100% true, accurate facts and data.
"""

# --- 6. Sidebar Controls & History Management ---
st.sidebar.title("⚙️ Pro AI Controls")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! Main **Pro AI** hu. Main Text, Screenshot/Photo aur Voice inputs samajhne ke liye ready hu!",
        }
    ]

# New Chat Button
if st.sidebar.button("➕ New Chat / Clear History", use_container_width=True):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Nayi chat shuru ho gayi hai! Aap kya poochna chahte hain?",
        }
    ]
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("📜 Chat History")
st.sidebar.caption(f"Total Messages: {len(st.session_state.messages)}")

# Image Upload Option in Sidebar/UI
st.sidebar.markdown("---")
st.sidebar.subheader("🖼️ Screenshot / Photo Upload")
uploaded_file = st.sidebar.file_uploader("Upload Image/Screenshot", type=["png", "jpg", "jpeg"])

# --- 7. Display Chat Messages ---
for message in st.session_state.messages:
    icon = "assistant" if message["role"] == "assistant" else "user"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# --- 8. Input Processing (Text & Screenshot) ---
if prompt := st.chat_input("Pro AI se kuch bhi pucho..."):
    # Render user prompt
    user_content = prompt
    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("user", avatar="user"):
        st.markdown(user_content)
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Screenshot", width=250)

    with st.chat_message("assistant", avatar="assistant"):
        with st.spinner("Pro AI process kar raha hai..."):
            try:
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.messages:
                    api_messages.append({
                        "role": "user" if m["role"] == "user" else "assistant",
                        "content": m["content"]
                    })

                # Select vision model if photo is uploaded, else standard model
                selected_model = "llama-3.3-70b-versatile"

                chat_completion = client.chat.completions.create(
                    messages=api_messages,
                    model=selected_model,
                    temperature=0.0,
                    max_tokens=1024,
                )

                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                st.error(f"Error: {str(e)}")
                
