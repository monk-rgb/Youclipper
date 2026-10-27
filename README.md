# 🎬 YouTube Video Clipper & Auto-Editor App

An all-in-one desktop application built with **Streamlit**, **OpenAI Whisper**, and **MoviePy** that lets you clip videos, apply anti-copyright transformations, automatically generate styled captions, overlay template videos, and **publish directly to your YouTube channel**.

---

## 🚀 Key Features

1. **🛡️ Anti-Copyright Transformations**:
   - **Horizontal Mirroring (Flip)**: Inverts video layout to bypass automated visual fingerprinting.
   - **Subtle Speed Shift (1.05x)**: Slightly alters video timing and audio pitch.
   - **Smart Border Crop & Zoom**: Crops the outer 5% of the video to remove original frame aspect markers.
   - **Color & Saturation Boost**: Adjusts color grading.

2. **💬 AI Auto-Captioning**:
   - Integrated **OpenAI Whisper AI** to transcribe speech automatically.
   - Position captions at the **Top**, **Center**, or **Bottom** of the screen.
   - Customize font size, text color, and background styles.

3. **🖼️ Template Video Integration**:
   - Upload background frames or reaction overlays.
   - Choose between **Background Mode** (framed split-screens) or **Overlay Mode**.

4. **📤 Direct YouTube Upload**:
   - Secure Google OAuth 2.0 authentication.
   - Upload directly to your channel with custom titles and privacy settings (**Private**, **Unlisted**, or **Public**).

---

## 🛠️ Prerequisites

Before running the app, make sure you have:
- **Python 3.8 or higher** installed on your system.
- **FFmpeg** installed on your system path (required for video processing/rendering).
  - *Windows*: `winget install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/)
  - *Mac*: `brew install ffmpeg`
  - *Linux*: `sudo apt install ffmpeg`

---

## 📦 Installation & Setup

1. **Create the Project Folder**:
   Create a folder named `youtube_clipper_app` containing a subfolder named `utils`.

2. **Add the Code Files**:
   Place your `app.py`, `requirements.txt`, `utils/video_processor.py`, and `utils/youtube_uploader.py` files in their respective directories.

3. **Add your YouTube API Credentials (Optional for Direct Uploads)**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the **YouTube Data API v3**.
   - Create an OAuth 2.0 Client ID (**Desktop app**) under **User data**, and download the JSON file.
   - Rename that file to **`client_secret.json`** and place it directly inside your `youtube_clipper_app/` folder.

4. **Install Dependencies**:
   Open your terminal/command prompt, navigate to the folder, and run:
   ```bash
   cd youtube_clipper_app
   pip install -r requirements.txt