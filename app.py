import streamlit as st
import subprocess
import os
import tempfile
import imageio_ffmpeg

# --- Config ---
st.set_page_config(layout="wide", page_title="MKV to MP4 Converter")

# --- Style ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans&display=swap');
    html, body, [class*="css"] {
        font-family: 'Nunito Sans', sans-serif !important;
    }
    .block-container {
        padding-top: 3rem;
    }
    .custom-text-label {
        font-size: 28px;
        font-weight: bold;
        color: #000000;
        margin-bottom: 8px;
    }
    div.stButton > button {
        background-color: #5378b3 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        font-size: 16px !important;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #405f91 !important;
        cursor: pointer;
    }
    div.stDownloadButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        font-size: 16px !important;
        width: 100%;
        margin-top: 10px;
        transition: background-color 0.3s ease;
    }
    div.stDownloadButton > button:hover {
        background-color: #388E3C !important;
        cursor: pointer;
    div.stImage > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()

def convert_mkv_to_mp4(input_path, output_path):
    command = [
        FFMPEG_PATH,
        "-i", input_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-strict", "experimental",
        output_path,
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode()
        raise RuntimeError(f"FFmpeg error:\n{error_msg}")

def main():
    st.image("assets/image.png")
    st.title("MKV to MP4 Converter")

    st.markdown('<div class="custom-text-label">Upload your MKV file:</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["mkv"], label_visibility="collapsed")

    if uploaded_file:
        st.write(f"📄 File ready: **{uploaded_file.name}**")

        convert_clicked = st.button("Convert to MP4")

        if convert_clicked:
            temp_input_path = None
            output_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mkv") as temp_input:
                    temp_input.write(uploaded_file.read())
                    temp_input_path = temp_input.name

                output_path = temp_input_path.rsplit(".", 1)[0] + ".mp4"

                with st.spinner("Converting..."):
                    convert_mkv_to_mp4(temp_input_path, output_path)

                st.success("✅ Conversion completed!")

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
                try:
                    if temp_input_path and os.path.exists(temp_input_path):
                        os.remove(temp_input_path)
                    if output_path and os.path.exists(output_path):
                        os.remove(output_path)
                except Exception:
                    pass

    # Horizontal separator
    st.markdown("---")

    # Footer with author and Streamlit link
    col_left, col_right = st.columns([8, 2])
    with col_left:
        st.markdown("**Built by Shashank H P**", unsafe_allow_html=True)
    with col_right:
        st.markdown(
            '<div style="text-align: right;">Powered by '
            '<a href="https://streamlit.io" target="_blank" '
            'style="color: #5378b3; font-weight: bold; text-decoration: none;">Streamlit</a></div>',
            unsafe_allow_html=True,
        )

if __name__ == "__main__":
    main()
