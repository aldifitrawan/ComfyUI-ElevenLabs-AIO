"""Sound Effects Generation Node"""

import requests
from ..utils.audio import load_audio_from_response, create_empty_audio


class ElevenLabsSoundEffects:
    """Generate sound effects from text descriptions"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Dog barking in the distance"
                }),
                "duration_seconds": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.5,
                    "max": 22.0,
                    "step": 0.5
                }),
                "prompt_influence": ("FLOAT", {
                    "default": 0.3,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
            },
            "optional": {
                "input_text": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "generate_sound_effect"
    CATEGORY = "ElevenLabs"
    
    def generate_sound_effect(self, api_key, text, duration_seconds, prompt_influence, input_text=None):
        """Generate sound effects"""
        final_text = input_text if input_text is not None else text
        
        url = "https://api.elevenlabs.io/v1/sound-generation"
        
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        
        payload = {
            "text": final_text,
            "duration_seconds": duration_seconds,
            "prompt_influence": prompt_influence
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            waveform, sample_rate = load_audio_from_response(response.content)
            
            print(f"✓ Generated sound effect: {duration_seconds}s - '{final_text}'")
            return ({"waveform": waveform, "sample_rate": sample_rate},)
            
        except requests.exceptions.RequestException as e:
            print(f"Error generating sound effect: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return (create_empty_audio(),)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

