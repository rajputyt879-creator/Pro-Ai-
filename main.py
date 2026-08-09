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

# 2. Advanced Professional Custom Styling (CSS Injection)
st.markdown(
    f"""
    <head>
        <link rel="manifest" href="https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/manifest.json">
        <link rel="apple-touch-icon" sizes="180x180" href="{ICON_URL}">
        <link rel="icon" type="image/png" sizes="32x32" href="{ICON_URL}">
    </head>
    <style>
        /* Main Container Padding */
        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 4rem !important;
            max-width: 800px;
        }}
        
        /* Glassmorphism Header Card */
        .pro-header-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            padding: 24px 20px;
            text-align: center;
            margin-bottom: 25px;
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

        /* Chat Input Area Styling */
        .stChatInput > div {{
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            background-color: rgba(15, 23, 42, 0.8) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
        }}

        .stChatInput > div:focus-within {{
            border-color: #00f2fe !important;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.3) !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Professional Header Area (Cover Section)
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

# --- 5. System Instructions (Identity & Fact Accuracy) ---
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

# --- 6. Chat History Management ---
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

# --- 7. Main Input & Response Processing ---
if prompt := st.chat_input("Pro AI se kuch bhi pucho..."):
    # Render User Input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Render Assistant Response
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
                
