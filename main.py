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

# 2. Inject PWA Manifest Links
st.markdown(
    f"""
    <head>
        <link rel="manifest" href="https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/manifest.json">
        <link rel="apple-touch-icon" sizes="180x180" href="{ICON_URL}">
        <link rel="icon" type="image/png" sizes="32x32" href="{ICON_URL}">
    </head>
    """,
    unsafe_allow_html=True,
)

# 3. Clean Title & Subtitle
st.title("⚡ Pro AI")
st.caption("Created & Owned by **Kishan Singh** | Fast, Simple & Accurate AI")

# --- 4. API Key Setup ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error(
        "❌ GROQ_API_KEY nahi mili! Kripya Streamlit Secrets mein GROQ_API_KEY add karein."
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- 5. System Rules (Identity & Exact Facts) ---
SYSTEM_PROMPT = """
You are 'Pro AI', an intelligent, polite, and highly accurate AI assistant created and owned by Kishan Singh.

CRITICAL IDENTITY & OWNERSHIP:
- You were created, developed, and owned by Kishan Singh.
- When asked "Who created you?", "Who is your owner?", "Aapko kisne banaya?", "Owner kaun hai?", or any creator inquiry, you MUST reply clearly: "Mujhe Kishan Singh ne banaya hai aur mere owner Kishan Singh hi hain."

FACTUAL ACCURACY RULES:
- Provide 100% exact, verified, and true facts, calculations, and geographical details.
- GEOGRAPHY DATA:
  * Jaipur to Sardarshahar (Churu district, Rajasthan) road distance via NH 52 / State routes is approximately 245 km to 255 km (about 4.5 to 5 hours driving time).
  * Always provide correct and realistic distance figures for routes in Rajasthan and India.
- Keep responses clean, respectful, concise, and helpful in Hindi, Hinglish, or English.
"""

# --- 6. Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Radhe Radhe! Main **Pro AI** hu. Mujhe **Kishan Singh** ne banaya hai. Aap mujhse koi bhi sawal pooch sakte hain!",
        }
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. Simple Input & Response Loop ---
if prompt := st.chat_input("Pro AI se koi bhi sawal pucho..."):
    # Add User Message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process AI Response
    with st.chat_message("assistant"):
        with st.spinner("Pro AI soch raha hai..."):
            try:
                # Prepare Messages List
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

                # Call Groq Llama 3.3 Model with Temperature = 0.0 (Strict Facts Mode)
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
                
