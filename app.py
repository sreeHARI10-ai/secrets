import streamlit as st
from PIL import Image
from cryptography.fernet import Fernet
import base64
import io

# Streamlit page configuration
st.set_page_config(page_title="s3cretz", layout="wide")

# Custom CSS for hacker/Anonymous vibe
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

/* Override Streamlit's default background and margins */
body, .stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%) !important;
    color: #ffffff;
    font-family: 'Orbitron', sans-serif;
    margin: 0 !important;
    padding: 0 !important;
}

/* Main app container with extra padding to avoid overlap */
.main .block-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px 20px 20px; /* Extra top padding */
    background: transparent;
}

/* Hide Streamlit's header and toolbar more aggressively */
.st-emotion-cache-1y4p8pa, 
.st-emotion-cache-ue6h4q, 
.st-emotion-cache-1r4qj8v, 
.st-emotion-cache-1wmy9hl {
    display: none !important;
}

/* Custom title styling */
.custom-title {
    color: #00ff00;
    text-align: center;
    font-size: 2.5em;
    text-shadow: 0 0 10px #00ff00;
    animation: glitch 2s linear infinite;
    margin-top: 0;
}

/* First tagline with typing animation and neon glow */
.tagline-1 {
    color: #cccccc;
    font-size: 1.2em;
    text-align: center;
    text-shadow: 0 0 5px #ff00ff;
    overflow: hidden;
    white-space: nowrap;
    animation: typing 4s steps(60, end) forwards, glow 2s infinite alternate;
}

/* Second tagline with slower typing and different glow */
.tagline-2 {
    color: #cccccc;
    font-size: 1em;
    text-align: center;
    text-shadow: 0 0 5px #00ff00;
    overflow: hidden;
    white-space: nowrap;
    animation: typing-slow 5s steps(40, end) forwards, glow-green 2.5s infinite alternate;
}

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
    to { text-shadow: 0 0 10px #ff00ff, 0 0 15px #ff00ff; }
}
@keyframes glow-green {
    from { text-shadow: 0 0 5px #00ff00; }
    to { text-shadow: 0 0 10px #00ff00, 0 0 15px #00ff00; }
}

/* Center buttons */
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
    font-size: 16px;
    font-weight: 700;
    text-transform: uppercase;
    transition: all 0.3s;
    box-shadow: 0 0 10px #00ff00;
}
.stButton>button:hover {
    background-color: #00ff00;
    color: #0a0a0a;
    box-shadow: 0 0 20px #00ff00;
}

/* Input fields */
.stTextInput>div>input, .stTextArea>div>textarea {
    background-color: #1a1a1a;
    color: #ffffff;
    border: 1px solid #ff00ff;
    border-radius: 5px;
    padding: 10px;
    font-family: 'Courier New', monospace;
}
.stTextInput>div>input:focus, .stTextArea>div>textarea:focus {
    box-shadow: 0 0 10px #ff00ff;
}
.stFileUploader>div {
    background-color: #1a1a1a;
    border: 1px solid #ff00ff;
    border-radius: 5px;
    padding: 10px;
}

/* Success and error messages */
.stSuccess, .stError {
    padding: 10px;
    border-radius: 5px;
    margin-top: 10px;
    font-family: 'Courier New', monospace;
}
.stSuccess {
    background-color: #002200;
    color: #00ff00;
    border: 1px solid #00ff00;
}
.stError {
    background-color: #220022;
    color: #ff00ff;
    border: 1px solid #ff00ff;
}

/* Content cards */
.tab-content, .home-content {
    background-color: rgba(10, 10, 10, 0.8);
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
}

/* Glitch animation for title */
@keyframes glitch {
    2%, 64% {
        transform: translate(2px, 0) skew(0deg);
    }
    4%, 60% {
        transform: translate(-2px, 0) skew(0deg);
    }
    62% {
        transform: translate(0, 0) skew(5deg);
    }
}

/* Remove Streamlit's default branding and margins */
.st-emotion-cache-uf99v8 {
    background: transparent !important;
}
.st-emotion-cache-1vzeuhh {
    background: transparent !important;
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
            raise ValueError(f"Message too large for image! Binary length: {len(full_binary)}, Image capacity: {width * height}")

        index = 0
        pixel_positions = [(x, y) for y in range(height) for x in range(width)]
        for x, y in pixel_positions:
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
        pixel_positions = [(x, y) for y in range(height) for x in range(width)]
        total_pixels = width * height

        binary_data = ""
        for i in range(min(32, total_pixels)):
            x, y = pixel_positions[i]
            r, _, _ = pixels[x, y]
            binary_data += str(r & 1)

        if len(binary_data) < 32:
            st.error(f"Not enough bits to read length prefix. Got {len(binary_data)} bits.")
            return None

        message_length = int(binary_data, 2)
        total_bits_needed = 32 + message_length + 16
        if total_bits_needed > total_pixels:
            st.error(f"Not enough pixels to extract message. Need {total_bits_needed}, have {total_pixels}.")
            return None

        binary_data = ""
        for i in range(total_bits_needed):
            x, y = pixel_positions[i]
            r, _, _ = pixels[x, y]
            binary_data += str(r & 1)

        message_bits = binary_data[32:32 + message_length]
        end_marker = binary_data[32 + message_length:32 + message_length + 16]
        if end_marker != '1' * 16:
            st.error(f"End marker not found. Got: {end_marker}")
            return None

        if len(message_bits) != message_length:
            st.error(f"Extracted {len(message_bits)} bits, expected {message_length} bits.")
            return None

        if len(message_bits) % 8 != 0:
            st.error(f"Message bits not a multiple of 8. Got {len(message_bits)} bits.")
            return None

        message_bytes = bytes(int(message_bits[i:i + 8], 2) for i in range(0, len(message_bits), 8))
        return message_bytes
    except Exception as e:
        st.error(f"Error in extract_message: {e}")
        return None

def main():
    # Session state to toggle between home and app
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.markdown('<div class="home-content">', unsafe_allow_html=True)
        # Custom title
        st.markdown('<h1 class="custom-title">s3cretz</h1>', unsafe_allow_html=True)
        # First tagline with typing and purple glow
        st.markdown('<p class="tagline-1">Hide your secrets in plain sight. Encode messages in images with unbreakable encryption. Stay anonymous. Stay secure.</p>', unsafe_allow_html=True)
        # Second tagline with slower typing and green glow
        st.markdown('<p class="tagline-2">Powered by advanced steganography and cryptography. Perfect for covert communication in a digital world.</p>', unsafe_allow_html=True)
        st.button("Get Started", key="get_started", on_click=lambda: st.session_state.update({"page": "app"}))
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="custom-title">s3cretz</h1>', unsafe_allow_html=True)
        st.markdown("Encode and decode secret messages in images.")

        # Tabs for Hide and Extract
        tab1, tab2 = st.tabs(["Hide Message", "Extract Message"])

        # Hide Message Tab
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("Hide a Secret Message")
            image_file = st.file_uploader("Upload an image (PNG)", type=["png"], key="hide_image")
            message = st.text_area("Enter message to hide", height=100)
            password = st.text_input("Enter password", type="password")
            if st.button("Hide Message"):
                if image_file and message and password:
                    try:
                        image = Image.open(image_file)
                        encrypted_message = encrypt_message(message, password)
                        if encrypted_message:
                            encoded_image = hide_message(image, encrypted_message)
                            if encoded_image:
                                img_buffer = io.BytesIO()
                                encoded_image.save(img_buffer, format="PNG")
                                img_buffer.seek(0)
                                st.success("Message hidden successfully!")
                                st.download_button(
                                    label="Download Encoded Image",
                                    data=img_buffer,
                                    file_name="encoded_image.png",
                                    mime="image/png"
                                )
                                st.image(encoded_image, caption="Encoded Image Preview", use_column_width=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Please provide an image, message, and password.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Extract Message Tab
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("Extract a Secret Message")
            image_file = st.file_uploader("Upload an encoded image (PNG)", type=["png"], key="extract_image")
            password = st.text_input("Enter password", type="password", key="extract_password")
            if st.button("Extract Message"):
                if image_file and password:
                    try:
                        image = Image.open(image_file)
                        extracted_bytes = extract_message(image)
                        if extracted_bytes:
                            decrypted_message = decrypt_message(extracted_bytes, password)
                            if not decrypted_message.startswith("Decryption failed"):
                                st.success(f"Decrypted message: {decrypted_message}")
                            else:
                                st.error(decrypted_message)
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Please provide an image and password.")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

