"""Voice Design Node - Create custom voices from descriptions"""

import requests
from ..utils.api import fetch_models_from_api
from ..utils.audio import load_audio_from_response, create_empty_audio


class ElevenLabsVoiceDesign:
    """
    Voice Design - Generate custom voices from text descriptions
    Create unique voices by describing their characteristics
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "voice_description": ("STRING", {
                    "multiline": True,
                    "default": "A deep, authoritative male voice with a slight British accent"
                }),
                "sample_text": ("STRING", {
                    "multiline": True,
                    "default": "Hello, this is a test of the voice design feature."
                }),
                "gender": (["male", "female", "neutral"], {
                    "default": "male"
                }),
                "age": (["young", "middle_aged", "old"], {
                    "default": "middle_aged"
                }),
                "accent": (["american", "british", "australian", "indian", "african", "neutral"], {
                    "default": "american"
                }),
                "accent_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.5,
                    "max": 2.0,
                    "step": 0.1
                }),
            }
        }
    
    RETURN_TYPES = ("AUDIO", "STRING")
    RETURN_NAMES = ("preview_audio", "voice_info")
    FUNCTION = "design_voice"
    CATEGORY = "ElevenLabs"
    
    def design_voice(self, api_key, voice_description, sample_text, gender, age, accent, accent_strength):
        """
        Design a custom voice from description
        Note: This uses the voice generation preview endpoint
        """
        url = "https://api.elevenlabs.io/v1/voice-generation/generate-voice"
        
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        
        payload = {
            "text": sample_text,
            "voice_description": voice_description,
            "gender": gender,
            "age": age,
            "accent": accent,
            "accent_strength": accent_strength,
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            waveform, sample_rate = load_audio_from_response(response.content)
            
            info = f"""
╔══════════════════════════════════════╗
║       VOICE DESIGN PREVIEW          ║
╚══════════════════════════════════════╝

Description: {voice_description}
Gender: {gender}
Age: {age}
Accent: {accent} (strength: {accent_strength})

Sample Text: {sample_text}

✓ Voice preview generated successfully!

Note: To save this voice permanently, you'll need
to use the voice cloning feature with multiple
samples or the ElevenLabs web interface.
"""
            
            print("✓ Voice design preview generated")
            return (
                {"waveform": waveform, "sample_rate": sample_rate},
                info
            )
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error in voice design: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return (
                create_empty_audio(),
                error_msg
            )
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

