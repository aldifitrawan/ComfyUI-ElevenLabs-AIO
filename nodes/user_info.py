"""User Info Node - Check account status and credits"""

import requests


class ElevenLabsUserInfo:
    """Node to check ElevenLabs account info, credits, and balance"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "refresh": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Refresh Now",
                    "label_off": "Use Cache"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("user_info",)
    FUNCTION = "get_user_info"
    CATEGORY = "ElevenLabs"
    OUTPUT_NODE = True
    
    def get_user_info(self, api_key, refresh):
        """Fetch user subscription info and credits"""
        if not api_key or api_key.strip() == "":
            return ("Error: API key is required",)
        
        url = "https://api.elevenlabs.io/v1/user"
        headers = {
            "xi-api-key": api_key,
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract key information
            subscription = data.get("subscription", {})
            
            info_text = f"""
╔══════════════════════════════════════╗
║     ELEVENLABS ACCOUNT INFO         ║
╚══════════════════════════════════════╝

👤 User: {data.get('email', 'N/A')}

📊 SUBSCRIPTION:
   Tier: {subscription.get('tier', 'N/A')}
   Status: {subscription.get('status', 'N/A')}

💳 CHARACTER USAGE:
   Used: {subscription.get('character_count', 0):,}
   Limit: {subscription.get('character_limit', 0):,}
   Remaining: {subscription.get('character_limit', 0) - subscription.get('character_count', 0):,}

🔄 Reset Date: {subscription.get('next_character_count_reset_unix', 'N/A')}

🎙️ Voice Cloning:
   Can use Instant Voice Cloning: {subscription.get('can_use_instant_voice_cloning', False)}
   Can use Professional Voice Cloning: {subscription.get('professional_voice_limit', 0)}

🌐 API Access: {subscription.get('can_use_api', 'N/A')}
"""
            
            print(info_text)
            return (info_text,)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error fetching user info: {str(e)}"
            print(error_msg)
            return (error_msg,)

