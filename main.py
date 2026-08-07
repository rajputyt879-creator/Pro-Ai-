import os
import streamlit as st
from groq import Groq

# --- 1. Page Configuration (Icon aur Title) ---
st.set_page_config(
    page_title="Pro AI",
    page_icon="⚡",  # Yahan browser tab me lightning icon dikhega
    layout="centered",
)

# --- 2. Custom Neon Pro AI Icon & PWA Setup ---
# Yeh code aapke custom neon "PAi" icon ko mobile home screen par layega
# Aur Streamlit header me bhi display karega
st.markdown(
    """
    <style>
        /* Mobile Install-able App Naam */
        @media (display-mode: standalone) {
            body::before {
                content: "Pro AI";
                display: none;
            }
        }
    </style>
    
    <!-- Neon Pro AI Icon Links -->
    <link rel="apple-touch-icon" sizes="180x180" href="https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png">
    
    <!-- Streamlit Header me Custom Icon -->
    <script>
        const observer = new MutationObserver((mutations) => {
            const header = document.querySelector('header');
            if (header && !header.querySelector('.pro-ai-icon')) {
                const iconContainer = document.createElement('div');
                iconContainer.className = 'pro-ai-icon';
                iconContainer.style = 'display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; margin-left: 1rem;';
                
                const icon = document.createElement('img');
                icon.src = 'https://raw.githubusercontent.com/rajputyt879-creator/Pro-AI-/main/pro_ai_neon_icon.png';
                icon.style = 'width: 30px; height: 30px; border-radius: 6px;';
                
                iconContainer.appendChild(icon);
                header.prepend(iconContainer);
            }
        });
        observer.observe(document.body, { childList: True, subtree: True });
    </script>
    """,
    unsafe_allow_html=True,
)

# --- 3. App UI Content ---
st.title("⚡ Pro AI")
st.caption("Powered by Advanced AI | Fast & Intelligent Response")

# --- 4. Core Logic & API Setup ---
# Fetch API Key from environment
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error(
        "❌ GROQ_API_KEY nahi mili! Kripya environment settings me API Key add karein."
    )
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Namaste! Main **Pro AI** hu. Aap mujhse koi bhi sawal pooch sakte hain.",
        }
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Pro AI se kuch bhi pucho..."):
    # Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Pro AI soch raha hai..."):
            try:
                api_messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]

                chat_completion = client.chat.completions.create(
                    messages=api_messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=1024,
                )

                response = chat_completion.choices[0].message.content
                st.markdown(response)

                # Save AI response
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
                
