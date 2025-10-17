"""Voice Isolator Node"""

import requests
from ..utils.audio import tensor_to_wav_buffer, load_audio_from_response


class ElevenLabsVoiceIsolator:
    """Isolate voice from background noise"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "audio": ("AUDIO",),
            }
        }
    
    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "isolate_voice"
    CATEGORY = "ElevenLabs"
    
    def isolate_voice(self, api_key, audio):
        """Remove background noise and isolate voice"""
        url = "https://api.elevenlabs.io/v1/audio-isolation"
        
        # Convert audio tensor to WAV
        wav_buffer = tensor_to_wav_buffer(audio["waveform"], audio["sample_rate"])
        
        headers = {
            "xi-api-key": api_key
        }
        
        files = {
            "audio": ("audio.wav", wav_buffer, "audio/wav")
        }
        
        try:
            response = requests.post(url, headers=headers, files=files, timeout=60)
            response.raise_for_status()
            
            waveform, sample_rate = load_audio_from_response(response.content)
            
            print(f"✓ Isolated voice from audio")
            return ({"waveform": waveform, "sample_rate": sample_rate},)
            
        except requests.exceptions.RequestException as e:
            print(f"Error isolating voice: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return (audio,)  # Return original audio on error
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

