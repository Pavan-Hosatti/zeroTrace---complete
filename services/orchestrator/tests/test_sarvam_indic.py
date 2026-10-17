"""Unit tests for ZeroTrace Sarvam AI Indic Speech & Voice Adapter."""

import pytest
from src.adapters.sarvam import SarvamAdapter


@pytest.mark.asyncio
async def test_sarvam_adapter_initialization():
    adapter = SarvamAdapter()
    assert adapter.stt_model == "saaras:v4"
    assert adapter.tts_model == "bulbul:v4-flash"
    assert adapter.tts_speaker == "shubh_enhi_ads"
    assert adapter.endpoint is not None


@pytest.mark.asyncio
async def test_sarvam_tts_synthesis():
    adapter = SarvamAdapter()
    audio = await adapter.synthesize_speech(
        text="ZeroTrace verification is complete.",
        target_language_code="en-IN",
    )
    assert len(audio) > 0
    # Valid RIFF / WAV header
    assert audio.startswith(b"RIFF")


@pytest.mark.asyncio
async def test_sarvam_transcription_offline_or_online():
    adapter = SarvamAdapter()
    transcript, lang, conf = await adapter.transcribe(
        audio_bytes=b"dummy-audio-bytes",
        language_hint="kn-IN",
    )
    assert "ಒಪ್ಪಿಗೆ" in transcript or len(transcript) > 0
    assert lang == "kn-IN"
    assert conf >= 0.90
