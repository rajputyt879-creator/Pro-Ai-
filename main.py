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

# 2. ChatGPT Dark Theme CSS
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

# 3. Header Section
st.markdown(
    """
    <div class="pro-header-card">
        <div class="security-badge">🔏 Anti-Abuse Privacy Shield Active</div>
        <div class="pro-title">⚡ Pro AI</div>
        <div class="pro-subtitle">ChatGPT & Gemini Powered Intelligence Platform</div>
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

# --- 5. Bad Words Filter ---
BAD_WORDS = [
    "bhadwe", "gand", "gandu", "chutiya", "madarchod", "bhenchod", 
    "gaali", "fuck", "bitch", "bastard", "harami", "bsdk"
]

def check_abusive_content(text):
    text_lower = text.lower()
    for word in BAD_WORDS:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            return True
    return False

# --- 6. System Instructions ---
SYSTEM_PROMPT = """
You are 'Pro AI', an ultra-intelligent AI assistant combining the speed and reasoning of ChatGPT and Google Gemini.

MULTILINGUAL & ACCURACY RULES:
1. Support all global and Indian languages fluently.
2. When asked "Translate Hindi", translate input into Hindi.
3. When asked "Translate English", translate input into English.
4. Provide 100% verified factual data without guesswork.

IDENTITY & OWNERSHIP RULES:
- Your name is strictly 'Pro AI'.
- Do not mention owner details in general chats.
- ONLY when explicitly asked "Who created you?", "Who is your owner?", or "Aapko kisne banaya?", reply: "Mujhe Kishan Singh ne banaya hai aur mere owner Kishan Singh hi hain."
"""

# --- 7. Sidebar Controls & Clickable History ---
st.sidebar.title("⚡ Pro AI Controls")

if "is_blocked" not in st.session_state:
    st.session_state.is_blocked = False

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! Main **Pro AI** hu. ChatGPT aur Gemini level intelligence ke saath main aapki madad karne ke liye ready hu!",
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
    st.session_state.is_blocked = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("💬 Active Chat History")

# Interactive Chat History Items in Sidebar
user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]

if user_msgs:
    for idx, msg in enumerate(user_msgs, 1):
        # Shorten message preview
        preview = msg[:25] + "..." if len(msg) > 25 else msg
        st.sidebar.write(f"**{idx}.** {preview}")
else:
    st.sidebar.caption("Abhi koi purani baat nahi hai. Sawal poochna shuru karein!")

st.sidebar.markdown("---")
st.sidebar.caption(f"Security Status: {'🚫 BLOCKED' if st.session_state.is_blocked else '🟢 SECURE'}")

# --- 8. Display Messages ---
for message in st.session_state.messages:
    avatar_icon = "⚡" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# --- 9. Input & Processing ---
if prompt := st.chat_input("Pro AI se kuch bhi pucho..."):
    if st.session_state.is_blocked:
        st.error("🚫 Aapko Pro AI system se block kar diya gaya hai.")
    
    elif check_abusive_content(prompt):
        st.session_state.is_blocked = True
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        block_msg = "🚨 **Policy Violation:** Galat shabd ka use karne ki wajah se aapko BLOCK kar diya gaya hai."
        st.session_state.messages.append({"role": "assistant", "content": block_msg})
        st.rerun()

    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="⚡"):
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
                                          
