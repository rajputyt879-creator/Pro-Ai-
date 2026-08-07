import os
import streamlit as st
import requests
import io
from PIL import Image
from groq import Groq

# 1. Custom Neon PAi Icon set for Browser Tab
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

# 3. Header & UI Design
st.title("⚡ Pro AI")
st.caption("Now with 4K Photo & 3D Art Generation | Chat & Create")

# --- 4. API Configuration Setup ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY")

if not GROQ_API_KEY:
    st.error(
        "❌ GROQ_API_KEY nahi mili! Kripya environment settings me API Key add karein."
    )
    st.stop()

if not STABILITY_API_KEY:
    st.warning(
        "⚠️ STABILITY_API_KEY nahi mili! Aap Image generate nahi kar payenge. Kripya use Secrets me add karein."
    )

client_groq = Groq(api_key=GROQ_API_KEY)


# --- 5. Image Generation Function ---
def generate_image(prompt, aspect_ratio="16:9", mode="photorealistic"):
    """
    Generates an image using Stability AI's Ultra Model (4K/HD Quality)
    """
    api_host = "https://api.stability.ai"
    # Using the highest quality 'Ultra' model endpoint
    engine_id = "stable-diffusion-ultra"

    # Style modifications based on mode
    enhanced_prompt = prompt
    if mode == "photorealistic":
        enhanced_prompt = (
            f"photorealistic, highly detailed, 4k resolution, professional, natural lighting, sharp focus, stunning quality: {prompt}"
        )
    elif mode == "3d_photo":
        enhanced_prompt = (
            f"3d render, blender render, dramatic neon lighting, depth of field, high contrast, stylized, sharp details: {prompt}"
        )

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {STABILITY_API_KEY}",
    }

    # API Payload for Ultra Model
    payload = {
        "prompt": enhanced_prompt,
        "output_format": "png",
        "aspect_ratio": aspect_ratio,
        "model": engine_id,
    }

    # API Request
    try:
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers=headers,
            files={"none": (None, "")},
            data=payload,
        )

        if response.status_code != 200:
            st.error(f"Stability AI Error: {response.text}")
            return None

        # Process and return image data
        image_bytes = response.content
        return Image.open(io.BytesIO(image_bytes))

    except Exception as e:
        st.error(f"Image generation request failed: {str(e)}")
        return None


# --- 6. Groq Chat Logic & Intent Processing ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! Main **Pro AI** hu. Main high quality 4K photos bana sakta hu. Bolo kya image banaun?",
        }
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. Main Input & Command Handling ---
if prompt := st.chat_input("Pro AI se kuch bhi pucho, ya bolo photo banana hai..."):
    # Clear session if new conversation starts
    if len(st.session_state.messages) > 10:
        st.session_state.messages = st.session_state.messages[-10:]

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # PROCESS CHAT / IMAGE GENERATION INTENT
    with st.chat_message("assistant"):
        with st.spinner("Pro AI soch raha hai..."):
            
            # --- IMAGE GENERATION COMMANDS CHECK ---
            if any(
                keyword in prompt.lower()
                for keyword in ["create image", "create photo", "image create", "image generation"]
            ):
                if not STABILITY_API_KEY:
                    st.error("⚠️ Image generation ke liye API key add karein!")
                else:
                    # Detect 3D Photo or standard photo
                    is_3d = any(keyword in prompt.lower() for keyword in ["3d photo", "3d image"])
                    generation_mode = "3d_photo" if is_3d else "photorealistic"
                    
                    # Generate the image
                    image = generate_image(prompt, aspect_ratio="16:9", mode=generation_mode)
                    
                    if image:
                        # Display the image in the chat
                        st.image(image, caption="Generated by Pro AI", use_column_width=True)
                        
                        # Save the image response to chat history
                        response_content = f"Ye rahi aapki high-quality {'3D photo' if is_3d else 'photo'}:"
                        st.session_state.messages.append({"role": "assistant", "content": response_content})
                        # Add a tiny visual reference to history
                        st.session_state.messages.append({"role": "assistant", "content": "*(Image displayed above)*"})
                        
                    else:
                        st.error("Kuch technical problem hui, image nahi ban payi.")
            
            # --- DEFAULT CHAT RESPONSES ---
            else:
                try:
                    api_messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]

                    chat_completion = client_groq.chat.completions.create(
                        messages=api_messages,
                        model="llama-3.3-70b-versatile",
                        temperature=0.7,
                        max_tokens=1024,
                    )

                    response = chat_completion.choices[0].message.content
                    st.markdown(response)

                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

                except Exception as e:
                    st.error(f"Chat error: {str(e)}")
                    
