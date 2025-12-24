# app.py
import os
import sys

# Add FFmpeg to PATH if not already present (fixes winget/choco install not updating session PATH)
ffmpeg_bin = r"C:\Users\VISHNU TEJA\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
if ffmpeg_bin not in os.environ.get('PATH', ''):
    os.environ['PATH'] = ffmpeg_bin + os.pathsep + os.environ.get('PATH', '')

import streamlit as st
from src.speech_to_text import convert_speech_to_text
from src.translator import translate_text
import tempfile

st.set_page_config(
    page_title="Speech to Text Translator",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Speech-to-Text & Language Translator")

# Language selection
languages = {
    "Telugu": "te_IN",
    "Hindi": "hi_IN",
    "Tamil": "ta_IN",
    "Marathi": "mr_IN",
    "Gujarati": "gu_IN",
    "Kannada": "kn_IN",
    "Malayalam": "ml_IN",
}
selected_language = st.selectbox("Select target language:", list(languages.keys()), index=0)
target_lang_code = languages[selected_language]

uploaded_audio = st.file_uploader(
    "Upload an audio file (WAV/MP3)", type=["wav", "mp3"]
)

if uploaded_audio:
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(uploaded_audio.read())
        audio_path = temp_audio.name

    st.audio(uploaded_audio)

    if st.button("🚀 Convert & Translate"):
        with st.spinner("Processing..."):
            try:
                english_text = convert_speech_to_text(audio_path)
            except Exception as e:
                st.error(f"Error converting audio: {e}")
                st.markdown(
                    """**Install ffmpeg (Windows)** — one of the following options:

```
choco install ffmpeg -y
# or
winget install --id Gyan.FFmpeg -e
```

Or download a static build from https://ffmpeg.org/download.html and add the `bin` folder to your PATH.
"""
                )
                english_text = ""

        if english_text:
            translated_text = translate_text(english_text, target_lang_code)

            st.subheader("📝 English Text")
            st.write(english_text)

            st.subheader(f"🌍 Translated Text ({selected_language})")
            st.write(translated_text)
