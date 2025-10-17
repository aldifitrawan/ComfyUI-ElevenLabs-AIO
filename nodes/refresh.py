"""Refresh Node - Manually refresh voice and model cache"""

from ..utils.cache import ElevenLabsCache
from ..utils.api import fetch_voices_from_api, fetch_models_from_api


class ElevenLabsRefreshVoices:
    """Node to manually refresh voice and model cache"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "refresh_voices": ("BOOLEAN", {
                    "default": True,
                    "label_on": "Refresh",
                    "label_off": "Skip"
                }),
                "refresh_models": ("BOOLEAN", {
                    "default": True,
                    "label_on": "Refresh",
                    "label_off": "Skip"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "refresh_cache"
    CATEGORY = "ElevenLabs"
    OUTPUT_NODE = True
    
    def refresh_cache(self, api_key, refresh_voices, refresh_models):
        """Force refresh voices and models cache"""
        results = []
        
        if refresh_voices:
            ElevenLabsCache.force_refresh_voices()
            voices = fetch_voices_from_api(api_key)
            results.append(f"✓ Refreshed {len(voices)} voices")
        
        if refresh_models:
            ElevenLabsCache.force_refresh_models()
            models = fetch_models_from_api(api_key)
            results.append(f"✓ Refreshed {len(models)} models")
        
        status = "\n".join(results) if results else "No refresh performed"
        print(status)
        return (status,)

