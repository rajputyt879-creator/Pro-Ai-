import os
import re
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# 1. Page Configuration
ICON_URL = "https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png"

st.set_page_config(
    page_title="Pro AI",
    page_icon="⚡",
    layout="centered",
)

# 2. ChatGPT-Style Modern Clean UI Styling (CSS)
st.markdown(
    f"""
    <head>
        <link rel="manifest" href="https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/manifest.json">
        <link rel="apple-touch-icon" sizes="180x180" href="{ICON_URL}">
        <link rel="icon" type="image/png" sizes="32x32" href="{ICON_URL}">
    </head>
    <style>
        .stApp {{
            background-color: #0d1117 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        }}

        .block-container {{
            padding-top: 1.8rem !important;
            padding-bottom: 5rem !important;
            max-width: 800px;
        }}
        
        /* ChatGPT Cover Header Card */
        .pro-header-card {{
            background: #161b22;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            padding: 24px 20px;
            text-align: center;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }}

        .pro-title {{
            font-size: 2.3rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }}

        .security-badge {{
            font-size: 0.78rem;
            color: #10a37f;
            background-color: rgba(16, 163, 127, 0.12);
            padding: 4px 14px;
            border-radius: 20px;
            border: 1px solid rgba(16, 163, 127, 0.3);
            display: inline-block;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        .pro-subtitle {{
            color: #8b949e;
            font-size: 0.9rem;
            margin-top: 4px;
        }}

        /* ChatGPT Style Chat Bubbles */
        [data-testid="stChatMessage"] {{
            background: #161b22 !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            margin-bottom: 12px !important;
            padding: 14px 18px !important;
        }}

        /* Avatar Styling Fix */
        [data-testid="stChatMessageAvatar"] {{
            background-color: #21262d !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}

        /* Input Bar Styling */
        .stChatInput > div {{
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            background-color: #161b22 !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
        }}

        .stChatInput > div:focus-within {{
            border-color: #10a37f !important;
            box-shadow: 0 0 12px rgba(16, 163, 127, 0.3) !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. JavaScript Handler
components.html(
    """
    <script>
    const doc = window.parent.document;
    doc.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            const activeElem = doc.activeElement;
            if (activeElem && activeElem.tagName === 'TEXTAREA') {
                e.stopPropagation();
                e.stopImmediatePropagation();
            }
        }
    }, true);
    </script>
    """,
    height=0,
    width=0,
)

# 4. Header Section
st.markdown(
    """
    <div class="pro-header-card">
        <div class="security-badge">🔒 Encrypted & Verified Accuracy Mode</div>
        <div class="pro-title">⚡ Pro AI</div>
        <div class="pro-subtitle">Advanced Intelligence Platform</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 5. API Key Setup ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY nahi mili! Kripya Streamlit Secrets mein GROQ_API_KEY add karein.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- 6. Strict System Instructions ---
SYSTEM_PROMPT = """
You are 'Pro AI', an intelligent, polite, highly professional, and accurate AI assistant. Your name is strictly 'Pro AI'.

IDENTITY & OWNERSHIP RULES:
- Your name is Pro AI.
- In general, normal conversations, greetings, or answering queries, DO NOT mention your creator or owner's name. Speak normally as Pro AI.
- ONLY when a user explicitly asks about your creator, developer, or owner (e.g., "Aapko kisne banaya?", "Aapka owner kaun hai?", "Who created you?", "Who is your developer?"), you must state clearly and respectfully: "Mujhe Kishan Singh ne banaya hai aur mere owner Kishan Singh hi hain."

FACTUAL ACCURACY INSTRUCTIONS:
- Always provide 100% accurate, verified facts, calculations, and route/distance details.
- Maintain a clean, respectful, helpful tone in Hindi, Hinglish, or English.
"""

# --- 7. Chat History Session ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! Main **Pro AI** hu. Main aapki kya madad kar sakta hu?",
        }
    ]

# ChatGPT Style Crisp Avatars ("⚡" for Pro AI, "👤" for User)
for message in st.session_state.messages:
    avatar_icon = "⚡" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# --- 8. Input & Response Loop ---
if prompt := st.chat_input("Pro AI se kuch bhi pucho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Pro AI soch raha hai..."):
            try:
                api_messages = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + [
                    {
                        "role": ("user" if m["role"] == "user" else "assistant"),
                        "content": m["content"],
                    }
                    for m in st.session_state.messages
                ]

                chat_completion = client.chat.completions.create(
                    messages=api_messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.0,
                    max_tokens=1024,
                )

                response = chat_completion.choices[0].message.content

                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
                
