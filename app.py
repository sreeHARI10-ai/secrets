import streamlit as st
from PIL import Image
from cryptography.fernet import Fernet
import base64
import io

st.set_page_config(page_title="s3cretz", layout="wide")

# Theme-friendly hacker CSS (no forced background)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

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

/* Moving text */
.tagline-1 {
    text-align: center;
    font-size: 1.2em;
    text-shadow: 0 0 5px #ff00ff;
    overflow: hidden;
    white-space: nowrap;
    animation: typing 4s steps(60, end) forwards;
}

.tagline-2 {
    text-align: center;
    font-size: 1em;
    text-shadow: 0 0 5px #00ff00;
    overflow: hidden;
    white-space: nowrap;
    animation: typing 5s steps(50, end) forwards;
}

@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
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
}

/* Inputs */
.stTextInput>div>input,
.stTextArea>div>textarea {
    border: 1px solid #ff00ff;
    border-radius: 5px;
    padding: 10px;
    font-family: 'Courier New', monospace;
}

/* Cards */
.tab-content, .home-content {
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 15px rgba(0,255,0,0.2);
}
</style>
""", unsafe_allow_html=True)


# -------- Encryption -------- #

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
        return None


# -------- Steganography -------- #

def hide_message(image, encrypted_message):
    img = image.convert("RGB")
    pixels = img.load()
    width, height = img.size

    binary_message = ''.join(format(byte, '08b') for byte in encrypted_message)
    message_length = len(binary_message)
    length_prefix = format(message_length, '032b')
    full_binary = length_prefix + binary_message

    index = 0
    for y in range(height):
        for x in range(width):
            if index >= len(full_binary):
                return img
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(full_binary[index])
            pixels[x, y] = (r, g, b)
            index += 1
    return img


def extract_message(image):
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


# -------- Main App -------- #

def main():

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":

        st.markdown('<div class="home-content">', unsafe_allow_html=True)
        st.markdown('<h1 class="custom-title">s3cretz</h1>', unsafe_allow_html=True)
        st.markdown('<p class="tagline-1">Hide your secrets in plain sight.</p>', unsafe_allow_html=True)
        st.markdown('<p class="tagline-2">Encrypt. Encode. Stay Secure.</p>', unsafe_allow_html=True)

        st.button("Get Started", on_click=lambda: st.session_state.update({"page": "app"}))
        st.markdown('</div>', unsafe_allow_html=True)

    else:

        st.markdown('<h1 class="custom-title">s3cretz</h1>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Hide Message", "Extract Message"])

        # Hide Message
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)

            image_file = st.file_uploader("Upload PNG Image", type=["png"])
            message = st.text_area("Enter Secret Message")
            password = st.text_input("Enter Password", type="password")

            if st.button("Hide Message"):
                if image_file and message and password:
                    image = Image.open(image_file)
                    encrypted = encrypt_message(message, password)
                    encoded_img = hide_message(image, encrypted)

                    buffer = io.BytesIO()
                    encoded_img.save(buffer, format="PNG")
                    buffer.seek(0)

                    st.success("Message hidden successfully!")
                    st.download_button(
                        "Download Encoded Image",
                        buffer,
                        file_name="encoded_image.png",
                        mime="image/png"
                    )
                    st.image(encoded_img)

            st.markdown('</div>', unsafe_allow_html=True)

        # Extract Message
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)

            image_file = st.file_uploader("Upload Encoded PNG", type=["png"], key="extract")
            password = st.text_input("Enter Password", type="password", key="extractpass")

            if st.button("Extract Message"):
                if image_file and password:
                    image = Image.open(image_file)
                    extracted = extract_message(image)
                    decrypted = decrypt_message(extracted, password)

                    if decrypted:
                        st.success(f"Decrypted Message: {decrypted}")
                    else:
                        st.error("Wrong password or invalid image.")

            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
