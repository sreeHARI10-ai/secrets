import streamlit as st
from PIL import Image
from cryptography.fernet import Fernet
import base64
import io

# Streamlit page configuration
st.set_page_config(page_title="s3cretz", layout="wide")

# Theme-Friendly Hacker CSS (No forced dark mode)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

/* Container styling */
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
}

/* Taglines */
.tagline-1 {
    text-align: center;
    font-size: 1.2em;
    text-shadow: 0 0 5px #ff00ff;
}

.tagline-2 {
    text-align: center;
    font-size: 1em;
    text-shadow: 0 0 5px #00ff00;
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
}

.stButton>button:hover {
    background-color: #00ff00;
    color: inherit;
}

/* Inputs */
.stTextInput>div>input, 
.stTextArea>div>textarea {
    border: 1px solid #ff00ff;
    border-radius: 5px;
    padding: 10px;
}

/* Cards */
.tab-content, .home-content {
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
}

/* Glitch animation */
@keyframes glitch {
    2%, 64% { transform: translate(2px, 0); }
    4%, 60% { transform: translate(-2px, 0); }
    62% { transform: translate(0, 0) skew(5deg); }
}
</style>
""", unsafe_allow_html=True)


def encrypt_message(message, password):
    try:
        key = base64.urlsafe_b64encode(password.ljust(32)[:32].encode())
        cipher = Fernet(key)
        encrypted = cipher.encrypt(message.encode())
        return encrypted
    except Exception as e:
        st.error(f"Encryption error: {e}")
        return None


def decrypt_message(encrypted_message, password):
    try:
        key = base64.urlsafe_b64encode(password.ljust(32)[:32].encode())
        cipher = Fernet(key)
        decrypted = cipher.decrypt(encrypted_message)
        return decrypted.decode()
    except Exception as e:
        return f"Decryption failed: {e}"


def hide_message(image, encrypted_message):
    try:
        img = image.convert("RGB")
        pixels = img.load()
        width, height = img.size

        binary_message = ''.join(format(byte, '08b') for byte in encrypted_message)
        message_length = len(binary_message)
        length_prefix = format(message_length, '032b')
        full_binary = length_prefix + binary_message + '1' * 16

        if len(full_binary) > width * height:
            raise ValueError("Message too large for image!")

        index = 0
        for y in range(height):
            for x in range(width):
                if index >= len(full_binary):
                    break
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(full_binary[index])
                pixels[x, y] = (r, g, b)
                index += 1

        return img
    except Exception as e:
        st.error(f"Error in hide_message: {e}")
        return None


def extract_message(image):
    try:
        img = image.convert("RGB")
        pixels = img.load()
        width, height = img.size

        binary_data = ""
        for y in range(height):
            for x in range(width):
                r, _, _ = pixels[x, y]
                binary_data += str(r & 1)

        message_length = int(binary_data[:32], 2)
        message_bits = binary_data[32:32 + message_length]
        message_bytes = bytes(
            int(message_bits[i:i + 8], 2)
            for i in range(0, len(message_bits), 8)
        )

        return message_bytes
    except Exception as e:
        st.error(f"Error in extract_message: {e}")
        return None


def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.markdown('<div class="home-content">', unsafe_allow_html=True)
        st.markdown('<h1 class="custom-title">s3cretz</h1>', unsafe_allow_html=True)
        st.markdown('<p class="tagline-1">Hide your secrets in plain sight. Encode messages in images with strong encryption.</p>', unsafe_allow_html=True)
        st.markdown('<p class="tagline-2">Powered by steganography and cryptography.</p>', unsafe_allow_html=True)
        st.button("Get Started", on_click=lambda: st.session_state.update({"page": "app"}))
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<h1 class="custom-title">s3cretz</h1>', unsafe_allow_html=True)
        st.markdown("Encode and decode secret messages in images.")

        tab1, tab2 = st.tabs(["Hide Message", "Extract Message"])

        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            image_file = st.file_uploader("Upload an image (PNG)", type=["png"])
            message = st.text_area("Enter message to hide")
            password = st.text_input("Enter password", type="password")

            if st.button("Hide Message"):
                if image_file and message and password:
                    image = Image.open(image_file)
                    encrypted_message = encrypt_message(message, password)
                    if encrypted_message:
                        encoded_image = hide_message(image, encrypted_message)
                        if encoded_image:
                            buffer = io.BytesIO()
                            encoded_image.save(buffer, format="PNG")
                            buffer.seek(0)
                            st.success("Message hidden successfully!")
                            st.download_button(
                                "Download Encoded Image",
                                buffer,
                                file_name="encoded_image.png",
                                mime="image/png"
                            )
                            st.image(encoded_image, use_column_width=True)
                else:
                    st.error("Please provide image, message, and password.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            image_file = st.file_uploader("Upload encoded image (PNG)", type=["png"], key="extract")
            password = st.text_input("Enter password", type="password", key="extractpass")

            if st.button("Extract Message"):
                if image_file and password:
                    image = Image.open(image_file)
                    extracted = extract_message(image)
                    if extracted:
                        decrypted = decrypt_message(extracted, password)
                        if not decrypted.startswith("Decryption failed"):
                            st.success(f"Decrypted message: {decrypted}")
                        else:
                            st.error(decrypted)
                else:
                    st.error("Please provide image and password.")
            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
