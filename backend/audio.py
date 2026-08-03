from gtts import gTTS
from deep_translator import GoogleTranslator
import tempfile
import hashlib
import os

# Cache folder
CACHE_DIR = "audio_cache"

os.makedirs(CACHE_DIR, exist_ok=True)


def generate_audio(text, language="English"):
    """
    Generate English or Hindi speech.

    Hindi:
        English -> Hindi translation -> gTTS

    English:
        Original text -> gTTS
    """

    if language == "Hindi":

        try:
            text = GoogleTranslator(
                source="auto",
                target="hi"
            ).translate(text)

        except Exception:
            # fallback if translation fails
            pass

        lang = "hi"

    else:

        lang = "en"

    # Create unique filename
    file_hash = hashlib.md5(
        (language + text).encode()
    ).hexdigest()

    filename = os.path.join(
        CACHE_DIR,
        f"{file_hash}.mp3"
    )

    # Don't regenerate existing audio
    if not os.path.exists(filename):

        tts = gTTS(
            text=text,
            lang=lang,
            slow=False
        )

        tts.save(filename)

    return filename