import streamlit as st
import subprocess
import os
import tempfile

FFMPEG_PATH = "ffmpeg"

def convert_mkv_to_mp4(input_path, output_path):
    command = [
        FFMPEG_PATH,
        "-i", input_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        output_path
    ]
    try:
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        # Decode ffmpeg error message and raise
        error_msg = e.stderr.decode()
        raise RuntimeError(f"FFmpeg error:\n{error_msg}")

# Page config
st.set_page_config(page_title="MKV to MP4 Converter", layout="wide")

# --- Custom CSS to style buttons and label ---
st.markdown("""
    <style>
    /* Style for all Streamlit buttons */
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 0.5em 1em;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #155d8b;
    }
    /* Style for download button */
    .stDownloadButton > button {
        background-color: #2ca02c;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 0.5em 1em;
        font-size: 16px;
        cursor: pointer;
    }
    .stDownloadButton > button:hover {
        background-color: #1f7a1f;
    }
    /* Upload label font size */
    .custom-upload-label {
        font-size: 25px !important;
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI ---
st.image("image.png")
st.markdown('<label class="custom-upload-label">Upload your MKV file</label>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📥 Please upload an MKV file to enable conversion", type=["mkv"])

if uploaded_file:
    st.write(f"📄 File ready: **{uploaded_file.name}**")

    convert_clicked = st.button("Convert to MP4")

    if convert_clicked:
        temp_input_path = None
        output_path = None
        try:
            # Save uploaded MKV file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mkv") as temp_input:
                temp_input.write(uploaded_file.read())
                temp_input_path = temp_input.name

            # Define output path with .mp4 extension
            output_path = temp_input_path.rsplit('.', 1)[0] + ".mp4"

            with st.spinner("Converting..."):
                convert_mkv_to_mp4(temp_input_path, output_path)

            st.success("✅ Conversion completed!")

            # Offer download button for MP4
            with open(output_path, "rb") as f:
                st.download_button(
                    label="Download MP4",
                    data=f,
                    file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.mp4",
                    mime="video/mp4",
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")

        finally:
            # Clean up temp files safely
            try:
                if temp_input_path and os.path.exists(temp_input_path):
                    os.remove(temp_input_path)
                if output_path and os.path.exists(output_path):
                    os.remove(output_path)
            except Exception:
                pass
# End of app.py
# This code is a Streamlit app that allows users to upload an MKV file and convert it to MP4 using FFmpeg.
