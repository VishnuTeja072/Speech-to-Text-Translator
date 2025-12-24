# src/speech_to_text.py
import shutil

_model = None

def _load_model():
    try:
        import whisper
    except Exception as e:
        raise ImportError(
            "Missing dependency: install the package 'openai-whisper' (pip install openai-whisper)"
        ) from e
    return whisper.load_model("base")

def _ensure_ffmpeg():
    """Ensure ffmpeg is available on PATH. Whisper relies on ffmpeg for audio I/O."""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "ffmpeg executable not found. Install ffmpeg and add it to your PATH. "
            "On Windows you can use Chocolatey: `choco install ffmpeg -y`, or winget: "
            "`winget install --id Gyan.FFmpeg -e`, or download from https://ffmpeg.org/download.html"
        )

def convert_speech_to_text(audio_path):
    """Convert an audio file to text using Whisper.

    The Whisper model is loaded lazily on first use to avoid heavy imports
    and downloads at module import time. This function verifies ffmpeg is
    available so the user receives a clear error message instead of a
    low-level FileNotFoundError from subprocess.
    """
    global _model
    # ensure ffmpeg present before attempting to load/convert audio
    _ensure_ffmpeg()

    if _model is None:
        _model = _load_model()

    result = _model.transcribe(audio_path)
    return result.get("text", "")
