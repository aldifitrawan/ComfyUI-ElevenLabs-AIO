"""Speech-to-Text Node"""

import requests
from ..utils.audio import tensor_to_wav_buffer


class ElevenLabsSpeechToText:
    """Speech-to-Text transcription using Scribe v1 model"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "audio": ("AUDIO",),
                "model": (["scribe_v1"], {
                    "default": "scribe_v1"
                }),
                "language": (["auto", "en", "es", "fr", "de", "it", "pt", "ja", "zh", "ko", "ru", "ar", "hi"], {
                    "default": "auto"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("transcription",)
    FUNCTION = "transcribe_audio"
    CATEGORY = "ElevenLabs"
    
    def transcribe_audio(self, api_key, audio, model, language):
        """Transcribe audio to text"""
        url = "https://api.elevenlabs.io/v1/speech-to-text"
        
        # Convert audio tensor to WAV
        wav_buffer = tensor_to_wav_buffer(audio["waveform"], audio["sample_rate"])
        
        headers = {
            "xi-api-key": api_key
        }
        
        files = {
            "audio": ("audio.wav", wav_buffer, "audio/wav")
        }
        
        data = {
            "model_id": model
        }
        
        if language != "auto":
            data["language"] = language
        
        try:
            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            transcription = result.get("text", "")
            
            print(f"✓ Transcribed audio: {len(transcription)} characters")
            return (transcription,)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error in speech-to-text: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return (error_msg,)

