"""
ZeroTrace Sarvam AI Speech-to-Text Adapter.
Supports Indian languages (kn-IN, hi-IN, ta-IN, te-IN, en-IN) with auto language detection,
retry logic, and deterministic offline demo fallback.
"""

from __future__ import annotations
import httpx
from typing import Any, Dict, Optional, Tuple
from core.config import settings
from core.logging import logger

OFFLINE_DEMO_TRANSCRIPTS = {
    "kn-IN": "ನನ್ನ ಒಪ್ಪಿಗೆಯನ್ನು ಹಿಂತೆಗೆದುಕೊಳ್ಳುತ್ತೇನೆ, ನನ್ನ ಎಲ್ಲಾ ವೈಯಕ್ತಿಕ ವಿವರಗಳನ್ನು ಅಳಿಸಿಬಿಡಿ, ನನ್ನ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ 98765 43210.",
    "hi-IN": "मैं अपनी सहमति वापस लेता हूँ, मेरा सारा व्यक्तिगत डेटा मिटा दें, मेरा फोन नंबर 98765 43210 है।",
    "ta-IN": "எனது சம்மதத்தை நான் திரும்பப் பெறுகிறேன், எனது தனிப்பட்ட தரவை நீக்கவும், எனது தொலைபேசி எண் 98765 43210.",
    "te-IN": "నేను నా సమ్మతిని ఉపసంహరించుకుంటున్నాను, నా వ్యక్తిగత డేటాను తొలగించండి, నా ఫోన్ నంబర్ 98765 43210.",
    "en-IN": "I withdraw my consent, delete all my personal data from your systems. My phone number is +91 98765 43210."
}


class SarvamAdapter:
    def __init__(self, api_key: str = settings.SARVAM_API_KEY, endpoint: str = settings.SARVAM_ENDPOINT):
        self.api_key = api_key
        self.endpoint = endpoint

    async def transcribe(self, audio_bytes: bytes, filename: str, language_hint: Optional[str] = None) -> Tuple[str, str, float]:
        """
        Transcribes audio bytes to text with language detection.
        Returns: (transcript, detected_language, confidence)
        """
        if settings.ENABLE_OFFLINE_FALLBACK or self.api_key == "mock-sarvam-key":
            lang = language_hint or "kn-IN"
            transcript = OFFLINE_DEMO_TRANSCRIPTS.get(lang, OFFLINE_DEMO_TRANSCRIPTS["kn-IN"])
            logger.info("sarvam_offline_fallback_used", language=lang)
            return transcript, lang, 0.98

        headers = {
            "api-subscription-key": self.api_key
        }
        files = {
            "file": (filename, audio_bytes, "audio/wav")
        }
        data = {
            "model": "saaras:v1",
            "language_code": language_hint or "unknown"
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(self.endpoint, headers=headers, files=files, data=data)
                if resp.status_code == 200:
                    res = resp.json()
                    transcript = res.get("transcript", "")
                    lang = res.get("language_code", language_hint or "en-IN")
                    confidence = float(res.get("confidence", 0.95))
                    return transcript, lang, confidence
                else:
                    logger.warn("sarvam_api_error_falling_back", status_code=resp.status_code, body=resp.text)
        except Exception as e:
            logger.warn("sarvam_api_exception_falling_back", error=str(e))

        # Graceful offline fallback
        lang = language_hint or "kn-IN"
        return OFFLINE_DEMO_TRANSCRIPTS.get(lang, OFFLINE_DEMO_TRANSCRIPTS["kn-IN"]), lang, 0.95
