"""Voice Changer Node - Transform voices in audio"""

import requests
from ..utils.api import fetch_voices_from_api
from ..utils.audio import tensor_to_wav_buffer, load_audio_from_response, create_empty_audio
from ..utils.cache import ElevenLabsCache


class ElevenLabsVoiceChanger:
    """
    Voice Changer - Transform the voice in audio to a different voice
    Also known as Speech-to-Speech (STS)
    """
    
    _last_api_key = None
    
    @classmethod
    def INPUT_TYPES(cls):
        voices = fetch_voices_from_api()
        
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "tooltip": "Your ElevenLabs API key - voices auto-refresh when changed"
                }),
                "audio": ("AUDIO",),
                "target_voice": (voices,),
                "model": (["eleven_english_sts_v2", "eleven_multilingual_sts_v2", "eleven_turbo_v2"], {
                    "default": "eleven_english_sts_v2"
                }),
                "stability": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "similarity_boost": ("FLOAT", {
                    "default": 0.75,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
            },
            "optional": {
                "style": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "use_speaker_boost": ("BOOLEAN", {
                    "default": True,
                }),
            }
        }
    
    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "change_voice"
    CATEGORY = "ElevenLabs"
    
    def change_voice(self, api_key, audio, target_voice, model, stability, similarity_boost, 
                    style=0.0, use_speaker_boost=True):
        """Transform voice in audio to target voice"""
        
        # Auto-refresh voices when API key changes
        if api_key and api_key != self.__class__._last_api_key:
            print(f"\n🔄 New API key detected - Auto-refreshing voices...")
            ElevenLabsCache.force_refresh_voices()
            fetch_voices_from_api(api_key, force_refresh=True)
            self.__class__._last_api_key = api_key
            print("✓ Voices refreshed! Reload node to see updates\n")
        
        voice_id = target_voice.split("(")[-1].strip(")")
        voice_name = target_voice.split("(")[0].strip()
        
        url = f"https://api.elevenlabs.io/v1/speech-to-speech/{voice_id}"
        
        # Convert audio tensor to WAV
        wav_buffer = tensor_to_wav_buffer(audio["waveform"], audio["sample_rate"])
        
        headers = {
            "xi-api-key": api_key,
        }
        
        # Data payload
        data = {
            "model_id": model,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": use_speaker_boost
            }
        }
        
        files = {
            "audio": ("input.wav", wav_buffer, "audio/wav")
        }
        
        # Log request details
        print("\n" + "="*60)
        print("🎭 ELEVENLABS VOICE CHANGER (STS)")
        print("="*60)
        print(f"Target Voice: {voice_name}")
        print(f"Voice ID: {voice_id}")
        print(f"Model: {model}")
        print(f"Settings: stability={stability}, similarity={similarity_boost}, style={style}")
        print("="*60 + "\n")
        
        try:
            # Note: speech-to-speech uses multipart/form-data, not JSON
            response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
            response.raise_for_status()
            
            waveform, sample_rate = load_audio_from_response(response.content)
            
            print(f"✓ Changed voice to {voice_name}")
            print(f"  Audio: {sample_rate}Hz, {waveform.shape}")
            return ({"waveform": waveform, "sample_rate": sample_rate},)
            
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Error in voice changer: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Status Code: {e.response.status_code}")
                print(f"   Response: {e.response.text[:500]}")
            print(f"   Target Voice: {voice_name}")
            print(f"   Voice ID: {voice_id}")
            print(f"   Model: {model}")
            return (create_empty_audio(audio["sample_rate"]),)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

