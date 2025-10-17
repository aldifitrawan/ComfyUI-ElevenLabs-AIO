"""History Node - View generation history"""

import requests


class ElevenLabsHistory:
    """View and manage generation history"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "page_size": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 100
                }),
                "refresh": ("BOOLEAN", {
                    "default": False
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("history",)
    FUNCTION = "get_history"
    CATEGORY = "ElevenLabs"
    OUTPUT_NODE = True
    
    def get_history(self, api_key, page_size, refresh):
        """Get generation history"""
        url = f"https://api.elevenlabs.io/v1/history?page_size={page_size}"
        
        headers = {
            "xi-api-key": api_key,
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            history_items = data.get("history", [])
            
            if not history_items:
                return ("No history items found",)
            
            history_text = "═══════════════════════════════════\n"
            history_text += "   ELEVENLABS GENERATION HISTORY\n"
            history_text += "═══════════════════════════════════\n\n"
            
            for i, item in enumerate(history_items, 1):
                history_text += f"{i}. {item.get('text', 'N/A')[:50]}...\n"
                history_text += f"   Voice: {item.get('voice_name', 'N/A')}\n"
                history_text += f"   Date: {item.get('date_unix', 'N/A')}\n"
                history_text += f"   Character Count: {item.get('character_count_change_from', 0)}\n"
                history_text += "   " + "─" * 35 + "\n"
            
            print(history_text)
            return (history_text,)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error fetching history: {str(e)}"
            print(error_msg)
            return (error_msg,)

