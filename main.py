import os
import re
import streamlit as st
from groq import Groq

# 1. Page Configuration
ICON_URL = "https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png"

st.set_page_config(
    page_title="Pro AI",
    page_icon="⚡",
    layout="centered",
)

# 2. Modern ChatGPT CSS
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0d1117 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
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

# 3. Header Section
st.markdown(
    """
    <div class="pro-header-card">
        <div class="security-badge">🔒 Encrypted & Multi-Language Active</div>
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

# --- 5. System Rules (Translation Fix, All Languages & India Awareness) ---
SYSTEM_PROMPT = """
You are 'Pro AI', an ultra-intelligent, highly capable, multi-lingual AI assistant.

MULTILINGUAL & TRANSLATION RULES (CRITICAL):
1. You MUST support ALL global and Indian languages fluently (Hindi, English, Hinglish, Marwari, Rajasthani, Tamil, Bengali, French, Spanish, etc.).
2. DIRECT TRANSLATION DIRECTION RULE:
   - When user asks "Translate Hindi", "Translate to Hindi", "Hindi Translation", or "Hindi me translate karo", convert the input INTO HINDI (हिंदी भाषा में अनुवाद करें).
   - When user asks "Translate English", "Translate to English", or "English translation", convert the input INTO ENGLISH.
   - Never confuse the translation target language!

INDIA & GENERAL KNOWLEDGE:
- You have comprehensive knowledge of India, current affairs, sports, culture, geography, and real-time updates.
- GEOGRAPHY: Jaipur to Sardarshahar road distance is approx 245-255 km. Always provide 100% accurate factual data.

IDENTITY & OWNERSHIP RULES:
- Your name is Pro AI.
- Speak naturally as Pro AI. DO NOT mention creator/owner name in routine chats.
- ONLY when explicitly asked "Who created you?", "Who is your owner?", "Aapko kisne banaya?", or "Owner kaun hai?", reply clearly: "Mujhe Kishan Singh ne banaya hai aur mere owner Kishan Singh hi hain."
"""

# --- 6. Session History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! Main **Pro AI** hu. Main sabhi bhashaon (Languages) aur accurate jankari ke saath aapki madad karne ke liye ready hu!",
        }
    ]

# Display Messages
for message in st.session_state.messages:
    icon = "assistant" if message["role"] == "assistant" else "user"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# --- 7. Input Engine ---
if prompt := st.chat_input("Pro AI se kuch bhi pucho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="assistant"):
        with st.spinner("Pro AI process kar raha hai..."):
            try:
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.messages:
                    api_messages.append({
                        "role": "user" if m["role"] == "user" else "assistant",
                        "content": m["content"]
                    })

                chat_completion = client.chat.completions.create(
                    messages=api_messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.0,
                    max_tokens=1024,
                )

                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                st.error(f"Error: {str(e)}")
                
