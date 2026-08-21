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

# 2. Responsive UI & Mobile Overflow Fix
st.markdown(
    """
    <style>
        [data-testid="stSidebar"], [data-testid="collapsedControl"], footer, header, #MainMenu {
            display: none !important;
        }

        .stApp {
            background-color: #0d1117 !important;
            color: #ffffff !important;
        }

        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 5rem !important;
            max-width: 800px !important;
        }
        
        .pro-header-card {
            background: #161b22;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 18px;
            text-align: center;
            margin-bottom: 16px;
        }

        .pro-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff !important;
            margin-bottom: 2px;
        }

        .security-badge {
            font-size: 0.75rem;
            color: #10a37f !important;
            background-color: rgba(16, 163, 127, 0.15);
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid rgba(16, 163, 127, 0.3);
            display: inline-block;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .pro-subtitle {
            color: #c9d1d9 !important;
            font-size: 1.05rem;
            font-weight: 700;
            margin-top: 2px;
        }

        /* Message Bubble & Text Contrast */
        [data-testid="stChatMessage"] {
            background-color: #161b22 !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            margin-bottom: 10px !important;
            padding: 12px 16px !important;
        }

        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div, [data-testid="stChatMessage"] span, [data-testid="stChatMessage"] li {
            color: #ffffff !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }

        /* Responsive Tables & Lists */
        table {
            width: 100% !important;
            table-layout: auto !important;
            border-collapse: collapse !important;
            margin: 10px 0 !important;
        }

        th, td {
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            padding: 8px !important;
            word-break: normal !important;
            white-space: normal !important;
            color: #ffffff !important;
        }

        /* Input Bar */
        .stChatInput > div {
            border-radius: 14px !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            background-color: #161b22 !important;
        }

        .stChatInput textarea {
            color: #ffffff !important;
            font-size: 1rem !important;
        }

        .stChatInput textarea::placeholder {
            color: #8b949e !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Header Card
st.markdown(
    """
    <div class="pro-header-card">
        <div class="security-badge">🔏 Enterprise AI Engine Active</div>
        <div class="pro-title">⚡ Pro AI</div>
        <div class="pro-subtitle">Ask ProAi</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 4. API Client Setup ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY missing hai. Kripya Streamlit secrets check karein.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- 5. System Prompt (High Quality Hindi + English) ---
SYSTEM_PROMPT = """
You are 'Pro AI', an ultra-intelligent, highly capable AI assistant created by Kishan Singh.
Language Guidelines:
1. Hindi / Hinglish: Speak with natural, highly accurate, and fluent Hindi (pure Devanagari or clean Hinglish depending on user prompt).
2. English: Deliver clear, grammatically perfect, and professional English.
3. Mobile Layout: Avoid excessively wide tables. Prefer clean bullet points or compact tables so mobile screens do not break.
4. Provide direct, helpful, and culturally accurate responses without unnecessary meta-announcements.
"""

# --- 6. Session State Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! Main **Pro AI** hu. Main aapki kya madad kar sakta hu?"}
    ]

# Display Messages
for message in st.session_state.messages:
    avatar_icon = "⚡" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])
        if "image_url" in message:
            st.image(message["image_url"], caption="Generated by Pro AI", use_container_width=True)

# --- 7. Chat Execution Pipeline ---
if prompt := st.chat_input("Ask ProAi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        prompt_lower = prompt.lower()

        # Image Generation Branch
        if any(kw in prompt_lower for kw in ["image", "photo", "pic", "picture", "draw", "banao"]):
            with st.spinner("🎨 Pro AI Image Render kar raha hai..."):
                try:
                    clean_query = prompt
                    encoded_prompt = urllib.parse.quote(clean_query)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed=42&nologo=true"
                    
                    msg_text = "✨ **Aapki AI Image ready hai:**"
                    st.markdown(msg_text)
                    st.image(image_url, caption="Generated by Pro AI", use_container_width=True)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": msg_text,
                        "image_url": image_url
                    })
                except Exception as e:
                    st.error(f"Image Error: {str(e)}")

        # Chat LLM Generation Branch (Direct Chat Models Only)
        else:
            with st.spinner("Pro AI reply taiyar kar raha hai..."):
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                
                # Take last 6 conversational turns
                for m in st.session_state.messages[-6:]:
                    if "content" in m and m["content"]:
                        api_messages.append({
                            "role": m["role"],
                            "content": m["content"]
                        })

                # Explicitly target ONLY Generative Chat models (never moderation/classification)
                chat_models = [
                    "llama-3.3-70b-versatile",
                    "llama3-70b-8192",
                    "llama3-8b-8192"
                ]

                response_text = None
                last_error = ""

                for model_id in chat_models:
                    try:
                        chat_completion = client.chat.completions.create(
                            messages=api_messages,
                            model=model_id,
                            temperature=0.5,
                            max_tokens=1500,
                        )
                        response_text = chat_completion.choices[0].message.content
                        if response_text:
                            break
                    except Exception as err:
                        last_error = str(err)
                        continue

                if response_text:
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    st.error(f"⚠️ Error: {last_error}")
                    
