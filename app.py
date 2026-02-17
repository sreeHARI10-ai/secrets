import streamlit as st
from PIL import Image
from cryptography.fernet import Fernet
import base64
import io

st.set_page_config(page_title="s3cretz", layout="wide")

# Hacker CSS (Theme Friendly - No forced dark background)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

/* DO NOT override body or .stApp background */

.main .block-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px 20px 20px;
    font-family: 'Orbitron', sans-serif;
}

/* Title */
.custom-title {
    color: #00ff00;
    text-align: center;
    font-size: 2.5em;
    text-shadow: 0 0 10px #00ff00;
    animation: glitch 2s linear infinite;
    margin-top: 0;
}

/* Moving typing effect */
.tagline-1 {
    text-align: center;
    font-size: 1.2em;
    text-shadow: 0 0 5px #ff00ff;
    overflow: hidden;
    white-space: nowrap;
    animation: typing 4s steps(60, end) forwards, glow 2s infinite alternate;
}

.tagline-2 {
    text-align: center;
    font-size: 1em;
    text-shadow: 0 0 5px #00ff00;
    overflow: hidden;
    white-space: nowrap;
    animation: typing-slow 5s steps(40, end) forwards, glow-green 2.5s infinite alternate;
}

/* Animations */
@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}

@keyframes typing-slow {
    from { width: 0; }
    to { width: 100%; }
}

@keyframes glow {
    from { text-shadow: 0 0 5px #ff00ff; }
    to { text-shadow: 0 0 15px #ff00ff; }
}

@keyframes glow-green {
    from { text-shadow: 0 0 5px #00ff00; }
    to { text-shadow: 0 0 15px #00ff00; }
}

@keyframes glitch {
    2%, 64% { transform: translate(2px, 0); }
    4%, 60% { transform: translate(-2px, 0); }
    62% { transform: translate(0, 0) skew(5deg); }
}

/* Buttons */
.stButton {
    display: flex;
    justify-content: center;
}

.stButton>button {
    background-color: transparent;
    color: #00ff00;
    border: 2px solid #00ff00;
    padding: 10px 20px;
    border-radius: 5px;
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    transition: all 0.3s;
    box-shadow: 0 0 10px #00ff00;
}

.stButton>button:hover {
    background-color: #00ff00;
    color: inherit;
    box-shadow: 0 0 20px #00ff00;
}

/* Inputs - no forced background */
.stTextInput>div>input, 
.stTextArea>div>textarea {
    border: 1px solid #ff00ff;
    border-radius: 5px;
    padding: 10px;
    font-family: 'Courier New', monospace;
}

.stTextInput>div>input:focus, 
.stTextArea>div>textarea:focus {
    box-shadow: 0 0 10px #ff00ff;
}

/* Cards */
.tab-content, .home-content {
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ---------------- #

def encrypt_message(message, password):
    key = base64.urlsafe_b64encode(password.ljust(32)[:32].encode())
    cipher = Fernet(key)
    return cipher.encrypt(message.encode())

def decrypt_message(encrypted_message, password):
    try:
        key = base64.urlsafe_b64encode(password.ljust(32)[:32].encode())
        cipher = Fernet(key)
        return cipher.decrypt(encrypted_message).decode()
    except:
        return "Decryption failed"

# ---------------- MAIN APP ---------------- #

def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.markdown('<div class="home-content">', unsafe_allow_html=True)
        st.markdown('<h1 class="custom-title">s3cretz</h1>', unsafe_allow_html=True)
        st.markdown('<p class="tagline-1">Hide your secrets in plain sight. Encode messages in images with unbreakable encryption.</p>', unsafe_allow_html=True)
        st.markdown('<p class="tagline-2">Stay anonymous. Stay secure. Powered by advanced steganography.</p>', unsafe_allow_html=True)
        st.button("Get Started", on_click=lambda: st.session_state.update({"page": "app"}))
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<h1 class="custom-title">s3cretz</h1>', unsafe_allow_html=True)
        st.markdown("Encode and decode secret messages in images.")

        tab1, tab2 = st.tabs(["Hide Message", "Extract Message"])

        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            message = st.text_area("Enter message")
            password = st.text_input("Enter password", type="password")
            if st.button("Encrypt"):
                if message and password:
                    encrypted = encrypt_message(message, password)
                    st.success("Encrypted:")
                    st.code(encrypted)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            encrypted_text = st.text_area("Enter encrypted text")
            password = st.text_input("Enter password", type="password", key="dec")
            if st.button("Decrypt"):
                if encrypted_text and password:
                    try:
                        decrypted = decrypt_message(encrypted_text.encode(), password)
                        st.success(decrypted)
                    except:
                        st.error("Invalid data")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
