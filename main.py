import os
import re
import streamlit as st
from groq import Groq

# 1. Page Configuration & Custom Icon
ICON_URL = "https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png"

st.set_page_config(
    page_title="Pro AI",
    page_icon=ICON_URL,
    layout="centered",
)

# 2. Advanced Professional Custom Styling
st.markdown(
    f"""
    <head>
        <link rel="manifest" href="https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/manifest.json">
        <link rel="apple-touch-icon" sizes="180x180" href="{ICON_URL}">
        <link rel="icon" type="image/png" sizes="32x32" href="{ICON_URL}">
    </head>
    <style>
        .block-container {{
            padding-top: 1.8rem !important;
            padding-bottom: 6rem !important;
            max-width: 800px;
        }}
        
        /* Glassmorphism Cover Card */
        .pro-header-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            padding: 22px 18px;
            text-align: center;
            margin-bottom: 22px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}

        .pro-title {{
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }}

        .security-badge {{
            font-size: 0.78rem;
            color: #00ff88;
            background-color: rgba(0, 255, 136, 0.1);
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid rgba(0, 255, 136, 0.3);
            display: inline-block;
            margin-bottom: 10px;
            font-weight: 600;
            letter-spacing: 0.3px;
        }}

        .pro-subtitle {{
            color: #a0aec0;
            font-size: 0.9rem;
            margin-top: 4px;
        }}

        /* Custom Input Container at Bottom */
        .input-box-container {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #0e1117;
            padding: 10px 15px;
            z-index: 999;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Header Cover Area
st.markdown(
    """
    <div class="pro-header-card">
        <div class="security-badge">🔒 End-to-End Encrypted & Verified Accuracy</div>
        <div class="pro-title">⚡ Pro AI</div>
        <div class="pro-subtitle">Created & Owned by <b>Kishan Singh</b> | Advanced Intelligence Platform</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 4. API Key Setup ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error(
        "❌ GROQ_API_KEY nahi mili! Kripya Streamlit Secrets mein GROQ_API_KEY add karein."
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- 5. System Instructions ---
SYSTEM_PROMPT = """
You are 'Pro AI', an intelligent, polite, highly professional, and accurate AI assistant created and owned by Kishan Singh.

CRITICAL IDENTITY & OWNERSHIP INSTRUCTIONS:
- You were created, developed, and owned by Kishan Singh.
- When asked "Who created you?", "Who is your owner?", "Aapko kisne banaya?", "Owner kaun hai?", or any creator query, reply clearly and proudly: "Mujhe Kishan Singh ne banaya hai aur mere owner Kishan Singh hi hain."

FACTUAL ACCURACY INSTRUCTIONS:
- Always provide 100% accurate, verified facts, calculations, and route/distance details.
- GEOGRAPHY DATA:
  * Jaipur to Sardarshahar (Churu district, Rajasthan) road distance via NH 52 is approximately 245 km to 255 km.
  * Always state correct, accurate road distances for routes in India.
- Keep tone polite, clean, respectful, and helpful in Hindi, Hinglish, or English.
"""

# --- 6. Chat History Session ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Radhe Radhe! Main **Pro AI** hu. Mujhe **Kishan Singh** ne banaya hai. Main aapke kisi bhi sawal ka sahi aur accurate jawab dene ke liye ready hu!",
        }
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. Separate Input & Send Button Handling ---
# Textarea allows Keyboard Enter (↵) to add a NEW LINE
with st.container():
    user_input = st.text_area(
        "Pro AI",
        placeholder="Pro AI se kuch bhi pucho...",
        key="user_text",
        height=80,
        label_visibility="collapsed",
    )
    send_clicked = st.button("🚀 Send Message", use_container_width=True)

if send_clicked and user_input.strip():
    prompt = user_input.strip()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
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
                
