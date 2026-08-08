import os
import streamlit as st
import requests
import io
import re
from PIL import Image
import google.generativeai as genai
from gtts import gTTS

# 1. Custom Neon Icon & Page Config
ICON_URL = "https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png"

st.set_page_config(
    page_title="Pro AI",
    page_icon=ICON_URL,
    layout="centered",
)

# 2. Inject PWA Links & Security CSS
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

# 3. Header UI
st.title("⚡ Pro AI")
st.markdown('<div class="security-badge">🔒 Powered by Google Gemini Engine | Ultra Accurate & Secure</div>', unsafe_allow_html=True)
st.caption("Created & Owned by **Kishan Singh** | Real-time Search Grounded AI")

# --- 4. API Keys Setup ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY nahi mili! Kripya Streamlit Secrets me add karein.")
    st.stop()

# Configure Google GenAI
genai.configure(api_key=GEMINI_API_KEY)

# System Instruction
SYSTEM_INSTRUCTION = """
You are 'Pro AI', an ultra-intelligent, highly accurate AI assistant powered by Google Gemini technology.

CRITICAL IDENTITY & OWNERSHIP:
- You were created, developed, and owned by Kishan Singh.
- When asked "Who created you?", "Who is your owner?", "Aapko kisne banaya?", "Owner kaun hai?", or any creator query, you MUST reply clearly and respectfully: "Mujhe Kishan Singh ne banaya hai aur mere owner Kishan Singh hi hain."

FACTUAL ACCURACY RULES:
- Provide 100% exact, verified, and true geographical distances (e.g., Jaipur to Sardarshahar distance via NH 52 / State Highway is approx 245-255 km), route info, math calculations, and real-time facts.
- Never guess or hallucinate numbers/distances. Always provide precise factual data in polite Hindi, Hinglish, or English.
- Never reveal internal API keys, code, or server secrets.
"""

def sanitize_input(user_input):
    """Prevents malicious script injection"""
    cleaned = re.sub(r'<[^>]*?>', '', user_input)
    malicious_patterns = [r'api[_\s]?key', r'system[_\s]?prompt', r'gemini[_\s]?key', r'stability[_\s]?key']
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
    """Generates 4K/3D photo using Stability AI"""
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

# --- 5. Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "content": "Radhe Radhe! Main **Pro AI** hu. Mujhe **Kishan Singh** ne banaya hai. Main Google Gemini Engine se 100% accurate jaankari dene ke liye ready hu!",
        }
    ]

# Sidebar Controls
st.sidebar.header("⚙️ Pro AI Settings")
voice_enabled = st.sidebar.checkbox("🔊 Enable Voice Response", value=True)

# Display History
for message in st.session_state.messages:
    role_name = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role_name):
        st.markdown(message["content"])

# --- 6. Main User Input & Response ---
if prompt := st.chat_input("Pro AI se kuch bhi pucho, ya photo banane ko bolo..."):
    safe_prompt = sanitize_input(prompt)
    
    if safe_prompt is None:
        with st.chat_message("assistant"):
            st.error("🛡️ Security Warning: Internal system credentials/keys disclose nahi kiye ja sakte.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Pro AI processing..."):

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
                            {"role": "model", "content": resp_text}
                        )

                # --- 2. GEMINI ENGINE RESPONSE ---
                else:
                    try:
                        # Initialize Gemini Model
                        model = genai.GenerativeModel(
                            model_name="gemini-1.5-flash",
                            system_instruction=SYSTEM_INSTRUCTION
                        )

                        response = model.generate_content(prompt)

                        resp_text = response.text
                        st.markdown(resp_text)

                        if voice_enabled:
                            audio_fp = text_to_speech(resp_text)
                            if audio_fp:
                                st.audio(audio_fp, format="audio/mp3")

                        st.session_state.messages.append(
                            {"role": "model", "content": resp_text}
                        )

                    except Exception as e:
                        st.error(f"Gemini Engine Error: {str(e)}")
                        
