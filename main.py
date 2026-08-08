import os
import streamlit as st
import requests
import io
import re
from PIL import Image
from groq import Groq
from gtts import gTTS

# 1. Custom Neon PAi Icon & Page Configuration
ICON_URL = "https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png"

st.set_page_config(
    page_title="Pro AI",
    page_icon=ICON_URL,
    layout="centered",
)

# 2. Inject PWA Manifest Links & Security CSS
st.markdown(
    f"""
    <head>
        <link rel="manifest" href="https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/manifest.json">
        <link rel="apple-touch-icon" sizes="180x180" href="{ICON_URL}">
        <link rel="icon" type="image/png" sizes="32x32" href="{ICON_URL}">
        <meta name="apple-mobile-web-app-title" content="Pro AI">
        <meta name="application-name" content="Pro AI">
    </head>
    <style>
        .security-badge {{
            font-size: 0.8rem;
            color: #00ff88;
            background-color: #112211;
            padding: 4px 10px;
            border-radius: 12px;
            border: 1px solid #00ff88;
            display: inline-block;
            margin-bottom: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Header & UI Design
st.title("⚡ Pro AI")
st.markdown('<div class="security-badge">🔒 Highly Accurate & Professional Mode Active</div>', unsafe_allow_html=True)
st.caption("Created by **Kishan Singh** | Powered by Advanced AI | Accurate, Secure & Professional")

# --- 4. API Keys Setup ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY nahi mili! Kripya Streamlit Secrets me add karein.")
    st.stop()

client_groq = Groq(api_key=GROQ_API_KEY)

# --- 5. Professional System Prompt with Fact-Checking Guardrails ---
SYSTEM_PROMPT = """
You are 'Pro AI', a highly professional, accurate, and intelligent AI assistant.

CRITICAL IDENTITY & OWNERSHIP INSTRUCTIONS:
- You were created, developed, and owned by Kishan Singh.
- When asked "Who created you?", "Who is your owner?", "Aapko kisne banaya?", "Owner kaun hai?", or any creator inquiry, state clearly: "Mujhe Kishan Singh ne banaya hai aur mere owner Kishan Singh hi hain."

FACTUAL ACCURACY & PROFESSIONAL RESPONSE RULES:
- ACCURACY IS TOP PRIORITY: Provide 100% verified, precise, and accurate factual information.
- GEOGRAPHY, DISTANCE, MATH & SCIENCE: Do not guess or hallucinate geographical distances, calculations, historical facts, or technical details. If you state a number or distance, make sure it is accurate.
- If you are unsure or if data is ambiguous, state the most accurate available information clearly without giving wrong guesses.
- TONE: Maintain a polite, professional, respectful, and helpful tone in Hindi / Hinglish / English.
- SECURITY: Never reveal internal system parameters, code details, or API keys.
"""

def sanitize_input(user_input):
    """Sanitizes input to prevent prompt injections or malicious tags"""
    cleaned = re.sub(r'<[^>]*?>', '', user_input)
    malicious_patterns = [r'api[_\s]?key', r'system[_\s]?prompt', r'groq[_\s]?key', r'stability[_\s]?key']
    for pattern in malicious_patterns:
        if re.search(pattern, cleaned, re.IGNORECASE) and any(word in cleaned.lower() for word in ['show', 'give', 'print', 'tell', 'batao', 'dikhaye']):
            return None
    return cleaned

def text_to_speech(text):
    """Converts text response to voice audio"""
    try:
        clean_text = re.sub(r'[*_#~`]', '', text)
        tts = gTTS(text=clean_text, lang="hi", slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception:
        return None

def generate_image(prompt, mode="photorealistic"):
    """Generates 4K/3D photo using Stability AI API"""
    if not STABILITY_API_KEY:
        st.error("⚠️ Image generation ke liye STABILITY_API_KEY add karein!")
        return None

    api_host = "https://api.stability.ai"
    engine_id = "stable-diffusion-ultra"

    enhanced_prompt = prompt
    if mode == "photorealistic":
        enhanced_prompt = f"photorealistic, highly detailed, 4k resolution, professional lighting, sharp focus: {prompt}"
    elif mode == "3d_photo":
        enhanced_prompt = f"3d render, blender style, dramatic neon lighting, depth of field, high contrast: {prompt}"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_API_KEY}",
    }

    payload = {
        "prompt": enhanced_prompt,
        "output_format": "png",
        "aspect_ratio": "16:9",
        "model": engine_id,
    }

    try:
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers=headers,
            files={"none": (None, "")},
            data=payload,
        )
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            st.error(f"Image Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Failed: {str(e)}")
        return None

# --- 6. Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Radhe Radhe! Main **Pro AI** hu. Mujhe **Kishan Singh** ne banaya hai. Main bilkul accurate jankari dene ke liye tayaar hu!",
        }
    ]

# Sidebar Controls
st.sidebar.header("⚙️ Pro AI Settings")
voice_enabled = st.sidebar.checkbox("🔊 Enable Voice Response", value=True)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. Main User Input & Response Engine ---
if prompt := st.chat_input("Pro AI se kuch bhi pucho, ya photo banane ko bolo..."):
    safe_prompt = sanitize_input(prompt)
    
    if safe_prompt is None:
        with st.chat_message("assistant"):
            st.error("🛡️ Security Warning: Security policies ki wajah se main internal API keys ya system settings disclose nahi kar sakta.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Pro AI sahi aur accurate jankari verify kar raha hai..."):

                # --- 1. IMAGE GENERATION TRIGGER ---
                if any(
                    keyword in prompt.lower()
                    for keyword in [
                        "create image",
                        "create photo",
                        "make image",
                        "3d photo",
                        "3d image",
                        "photo banao",
                        "image banao"
                    ]
                ):
                    is_3d = "3d" in prompt.lower()
                    mode = "3d_photo" if is_3d else "photorealistic"
                    image = generate_image(prompt, mode=mode)

                    if image:
                        st.image(image, caption="Generated by Pro AI | Created by Kishan Singh", use_column_width=True)
                        resp_text = f"Ye rahi aapki {'3D photo' if is_3d else '4K photo'}!"
                        st.markdown(resp_text)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": resp_text}
                        )

                # --- 2. ACCURATE TEXT CHAT WITH TEMPERATURE=0.0 ---
                else:
                    try:
                        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                        for m in st.session_state.messages:
                            api_messages.append({"role": m["role"], "content": m["content"]})

                        # SETTING TEMPERATURE TO 0.0 FOR MAXIMUM ACCURACY & ZERO HALLUCINATION
                        chat_completion = client_groq.chat.completions.create(
                            messages=api_messages,
                            model="llama-3.3-70b-versatile",
                            temperature=0.0,  # Zero randomness = 100% Precise & Accurate Facts
                            max_tokens=1024,
                        )

                        response = chat_completion.choices[0].message.content
                        st.markdown(response)

                        if voice_enabled:
                            audio_fp = text_to_speech(response)
                            if audio_fp:
                                st.audio(audio_fp, format="audio/mp3")

                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )

                    except Exception as e:
                        st.error(f"Chat error: {str(e)}")
                        
