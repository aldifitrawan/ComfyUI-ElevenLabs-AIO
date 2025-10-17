"""Music Generation Node"""

import requests
from ..utils.audio import load_audio_from_response, create_empty_audio


class ElevenLabsMusic:
    """
    Music Generation - Generate music from text prompts
    Note: This feature may require specific subscription tiers
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Upbeat electronic music with synthesizers"
                }),
                "duration_seconds": ("FLOAT", {
                    "default": 10.0,
                    "min": 1.0,
                    "max": 300.0,
                    "step": 1.0
                }),
                "model": (["music_gen_medium", "music_gen_large"], {
                    "default": "music_gen_medium"
                }),
            },
            "optional": {
                "input_prompt": ("STRING", {"forceInput": True}),
                "temperature": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 2.0,
                    "step": 0.1
                }),
            }
        }
    
    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "generate_music"
    CATEGORY = "ElevenLabs"
    
    def generate_music(self, api_key, prompt, duration_seconds, model, input_prompt=None, temperature=1.0):
        """Generate music from text prompt"""
        
        final_prompt = input_prompt if input_prompt is not None else prompt
        
        # Note: This endpoint might not be publicly available yet
        # Using a placeholder URL - check ElevenLabs docs for actual endpoint
        url = "https://api.elevenlabs.io/v1/music-generation"
        
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        
        payload = {
            "text": final_prompt,
            "duration": duration_seconds,
            "model_id": model,
            "temperature": temperature,
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=max(60, int(duration_seconds * 2)))
            response.raise_for_status()
            
            waveform, sample_rate = load_audio_from_response(response.content)
            
            print(f"✓ Generated music: {duration_seconds}s - '{final_prompt}'")
            return ({"waveform": waveform, "sample_rate": sample_rate},)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"""
❌ Error generating music: {str(e)}

Note: Music generation may not be available in the 
current API version or may require a specific 
subscription tier.

Check the ElevenLabs documentation for:
- Feature availability
- Subscription requirements
- API endpoint updates
"""
            print(error_msg)
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return (create_empty_audio(),)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

