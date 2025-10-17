"""Voice Manager Node - Manage and inspect voices"""

import requests
from ..utils.api import fetch_voices_from_api


class ElevenLabsVoiceManager:
    """Manage voices - view details, add, edit"""
    
    @classmethod
    def INPUT_TYPES(cls):
        voices = fetch_voices_from_api()
        
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "voice": (voices,),
                "action": (["Get Info", "Get Settings"], {
                    "default": "Get Info"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("voice_info",)
    FUNCTION = "manage_voice"
    CATEGORY = "ElevenLabs"
    OUTPUT_NODE = True
    
    def manage_voice(self, api_key, voice, action):
        """Manage voice operations"""
        voice_id = voice.split("(")[-1].strip(")")
        
        if action == "Get Info":
            url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
        elif action == "Get Settings":
            url = f"https://api.elevenlabs.io/v1/voices/{voice_id}/settings"
        else:
            return ("Unknown action",)
        
        headers = {
            "xi-api-key": api_key,
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if action == "Get Info":
                info_text = f"""
╔══════════════════════════════════════╗
║         VOICE INFORMATION           ║
╚══════════════════════════════════════╝

🎙️ Name: {data.get('name', 'N/A')}
🆔 ID: {data.get('voice_id', 'N/A')}
📝 Description: {data.get('description', 'N/A')}
🏷️ Category: {data.get('category', 'N/A')}
👤 Created by: {data.get('created_by', 'N/A')}

⚙️ SETTINGS:
   Stability: {data.get('settings', {}).get('stability', 'N/A')}
   Similarity Boost: {data.get('settings', {}).get('similarity_boost', 'N/A')}
   Style: {data.get('settings', {}).get('style', 'N/A')}
   Speaker Boost: {data.get('settings', {}).get('use_speaker_boost', 'N/A')}

🏷️ Labels: {', '.join([f"{k}: {v}" for k, v in data.get('labels', {}).items()]) if data.get('labels') else 'None'}
"""
            else:
                settings = data
                info_text = f"""
⚙️ VOICE SETTINGS:
   Stability: {settings.get('stability', 'N/A')}
   Similarity Boost: {settings.get('similarity_boost', 'N/A')}
   Style: {settings.get('style', 'N/A')}
   Speaker Boost: {settings.get('use_speaker_boost', 'N/A')}
"""
            
            print(info_text)
            return (info_text,)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error managing voice: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return (error_msg,)

