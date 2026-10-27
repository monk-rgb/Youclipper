import streamlit as st
import os
import tempfile
from utils.video_processor import VideoClipper
from utils.youtube_uploader import upload_video_to_youtube

st.set_page_config(page_title="AI YouTube Clip & Anti-Copyright Tool", layout="wide", page_icon="🎬")

st.title("🎬 YouTube Video Clipper & Auto-Editor")
st.markdown("""
Transform uploaded videos into YouTube-ready clips with:
- **Anti-Copyright Modifications** (Speed shift, frame cropping, color grading, horizontal flipping)
- **AI Auto-Captioning** with customizable position & styles
- **Custom Template Video Integration**
- **Direct YouTube Publishing** via OAuth 2.0
""")

st.sidebar.header("⚙️ Editing & Anti-Copyright Settings")

# 1. Subtitle & Caption Settings
st.sidebar.subheader("💬 Caption Options")
caption_pos = st.sidebar.selectbox("Caption Position", ["bottom", "center", "top"], index=0)
font_size = st.sidebar.slider("Font Size", 20, 60, 36)
font_color = st.sidebar.color_picker("Text Color", "#FFFFFF")
bg_color_option = st.sidebar.selectbox("Background Style", ["black", "none", "blue", "red"])

# 2. Anti-Copyright & Effects Settings
st.sidebar.subheader("🛡️ Anti-Copyright Effects")
apply_flip = st.sidebar.checkbox("Flip Horizontally (Mirror)", value=True)
apply_speed = st.sidebar.checkbox("Subtle Speed Change (1.05x)", value=True)
apply_zoom = st.sidebar.checkbox("Smart Border Crop & Zoom (5%)", value=True)
apply_color = st.sidebar.checkbox("Color Boost & Saturation Shift", value=True)

selected_effects = []
if apply_flip: selected_effects.append("flip_horizontal")
if apply_speed: selected_effects.append("speed_change")
if apply_zoom: selected_effects.append("zoom_in")
if apply_color: selected_effects.append("color_boost")

# Main Interface
col1, col2 = st.columns(2)

with col1:
    st.header("1. Source Video")
    uploaded_video = st.file_uploader("Upload video to clip (.mp4, .mov, .mkv)", type=["mp4", "mov", "mkv"])
    
    start_time = st.number_input("Clip Start Time (seconds)", min_value=0.0, value=0.0, step=1.0)
    end_time = st.number_input("Clip End Time (seconds, 0 for full video)", min_value=0.0, value=0.0, step=1.0)

with col2:
    st.header("2. Template Video (Optional)")
    uploaded_template = st.file_uploader("Upload background/frame template video", type=["mp4", "mov"])
    template_mode = st.selectbox("Template Mode", ["background", "overlay"], help="Background puts target clip over template; Overlay places template over target video.")

if uploaded_video is not None:
    st.divider()
    if st.button("🚀 Process & Generate YouTube-Ready Clip", type="primary"):
        with st.spinner("Processing video, applying anti-copyright transformations, and generating auto-captions..."):
            temp_dir = tempfile.mkdtemp()
            input_path = os.path.join(temp_dir, "input_video.mp4")
            output_path = os.path.join(temp_dir, "youtube_ready_clip.mp4")

            with open(input_path, "wb") as f:
                f.write(uploaded_video.read())

            template_path = None
            if uploaded_template is not None:
                template_path = os.path.join(temp_dir, "template_video.mp4")
                with open(template_path, "wb") as f:
                    f.write(uploaded_template.read())

            try:
                clipper = VideoClipper()
                clipper.process_video(
                    input_path=input_path,
                    output_path=output_path,
                    start_time=start_time,
                    end_time=end_time if end_time > 0 else None,
                    caption_pos=caption_pos,
                    custom_fontsize=font_size,
                    custom_fontcolor=font_color,
                    custom_bg_color=bg_color_option,
                    effects=selected_effects,
                    template_path=template_path,
                    template_mode=template_mode
                )

                st.session_state["processed_video_path"] = output_path
                st.success("✅ Video processing complete!")

            except Exception as e:
                st.error(f"Error processing video: {str(e)}")

# Display Download & YouTube Upload section if processed video exists
if "processed_video_path" in st.session_state and os.path.exists(st.session_state["processed_video_path"]):
    st.divider()
    st.header("📥 Download & Publish")
    
    st.video(st.session_state["processed_video_path"])

    with open(st.session_state["processed_video_path"], "rb") as file:
        st.download_button(
            label="📥 Download YouTube-Ready Video",
            data=file,
            file_name="ready_for_youtube.mp4",
            mime="video/mp4"
        )

    st.subheader("📤 Direct YouTube Upload")
    yt_title = st.text_input("YouTube Video Title", value="My Clipped Video")
    yt_privacy = st.selectbox("Privacy Status", ["private", "unlisted", "public"])

    if st.button("🚀 Upload Directly to YouTube"):
        if os.path.exists("client_secret.json"):
            with st.spinner("Authenticating with Google & uploading video..."):
                try:
                    video_id = upload_video_to_youtube(
                        video_path=st.session_state["processed_video_path"],
                        title=yt_title,
                        privacy_status=yt_privacy
                    )
                    st.success(f"🎉 Successfully uploaded! Watch it here: https://youtu.be/{video_id}")
                except Exception as e:
                    st.error(f"Upload failed: {str(e)}")
        else:
            st.warning("⚠️ `client_secret.json` not found in the app folder. Please add your Google Cloud OAuth client secret file to enable direct uploads.")