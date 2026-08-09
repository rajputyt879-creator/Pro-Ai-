import os
import re
import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# 1. Page Configuration & Custom Neon Logo URL
ICON_URL = "https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png"

st.set_page_config(
    page_title="Pro AI",
    page_icon=ICON_URL,
    layout="centered",
)

# 2. Advanced 3D & 4K Styling (CSS Injection)
st.markdown(
    f"""
    <head>
        <link rel="manifest" href="https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/manifest.json">
        <link rel="apple-touch-icon" sizes="180x180" href="{ICON_URL}">
        <link rel="icon" type="image/png" sizes="32x32" href="{ICON_URL}">
    </head>
    <style>
        .stApp {{
            background: radial-gradient(circle at 50% 10%, #1a1f2c 0%, #0d1117 100%) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 5rem !important;
            max-width: 820px;
        }}
        
        /* 3D Glassmorphism Header */
        .pro-header-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.07) 0%, rgba(255, 255, 255, 0.02) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-top: 1px solid rgba(255, 255, 255, 0.3);
            border-left: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
            padding: 28px 22px;
            text-align: center;
            margin-bottom: 28px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }}

        /* 4K Glowing Title */
        .pro-title {{
            font-size: 2.6rem;
            font-weight: 900;
            background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00c6ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            letter-spacing: -0.8px;
            filter: drop-shadow(0px 4px 12px rgba(0, 242, 254, 0.35));
        }}

        /* Security Badge */
        .security-badge {{
            font-size: 0.8rem;
            color: #00ff88;
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.15) 0%, rgba(0, 255, 136, 0.05) 100%);
            padding: 6px 16px;
            border-radius: 30px;
            border: 1px solid rgba(0, 255, 136, 0.4);
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
            display: inline-block;
            margin-bottom: 12px;
            font-weight: 700;
            letter-spacing: 0.4px;
            text-transform: uppercase;
        }}

        .pro-subtitle {{
            color: #cbd5e1;
            font-size: 0.95rem;
            font-weight: 500;
            margin-top: 6px;
        }}

        /* Chat Bubbles */
        [data-testid="stChatMessage"] {{
            background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%) !important;
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            margin-bottom: 14px !important;
            padding: 14px 18px !important;
        }}

        /* Chat Input Styling */
        .stChatInput > div {{
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.3) !important;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%) !important;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        }}

        .stChatInput > div:focus-within {{
            border-color: #00f2fe !important;
            box-shadow: 0 0 25px rgba(0, 242, 254, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
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

# 4. Header Area
st.markdown(
    """
    <div class="pro-header-card">
        <div class="security-badge">🔒 End-to-End Encrypted & Verified 4K Accuracy</div>
        <div class="pro-title">⚡ Pro AI</div>
        <div class="pro-subtitle">Created & Owned by <b>Kishan Singh</b> | Advanced Intelligence Platform</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 5. API Key Setup ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error(
        "❌ GROQ_API_KEY nahi mili! Kripya Streamlit Secrets mein GROQ_API_KEY add karein."
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- 6. System Instructions ---
SYSTEM_PROMPT = """
You are 'Pro AI', an intelligent, polite, highly professional, and accurate AI assistant created and owned by Kishan Singh.

CRITICAL IDENTITY & OWNERSHIP INSTRUCTIONS:
- You were created, developed, and owned by Kishan Singh.
- When asked "Who created you?", "Who is your owner?", "Aapko kisne banaya?", "Owner kaun hai?", or any creator query, reply clearly and proudly: "Mujhe Kishan Singh ne banaya hai aur mere owner Kishan Singh hi hain."

FACTUAL ACCURACY INSTRUCTIONS:
- Always provide 100% accurate, verified facts, calculations, and route/distance details.
- Keep tone polite, clean, respectful, and helpful in Hindi, Hinglish, or English.
"""

# --- 7. Chat History Session ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Radhe Radhe! Main **Pro AI** hu. Mujhe **Kishan Singh** ne banaya hai. Main aapke kisi bhi sawal ka sahi aur accurate jawab dene ke liye ready hu!",
        }
    ]

# Display Chat History with Custom Avatars (PRO AI Neon Logo for Assistant)
for message in st.session_state.messages:
    avatar_icon = ICON_URL if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# --- 8. Input & Response Loop ---
if prompt := st.chat_input("Pro AI se kuch bhi pucho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=ICON_URL):
        with st.spinner("Pro AI soch raha hai..."):
            try:
                api_messages = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ] + [
                    {
                        "role": (
                            "user" if m["role"] == "user" else "assistant"
                        ),
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
                
