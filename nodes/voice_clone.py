"""Voice Clone Node - Clone voices from audio samples"""

import requests


class ElevenLabsVoiceClone:
    """
    Voice Clone - Create a cloned voice from audio samples
    Requires multiple audio samples for best results (Instant Voice Cloning)
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "voice_name": ("STRING", {
                    "multiline": False,
                    "default": "My Cloned Voice"
                }),
                "audio_sample": ("AUDIO",),
                "voice_description": ("STRING", {
                    "multiline": True,
                    "default": "A clear, friendly voice"
                }),
            },
            "optional": {
                "labels": ("STRING", {
                    "multiline": True,
                    "default": "accent: american, age: young, gender: female"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "clone_voice"
    CATEGORY = "ElevenLabs"
    OUTPUT_NODE = True
    
    def clone_voice(self, api_key, voice_name, audio_sample, voice_description, labels=""):
        """
        Clone a voice from audio sample
        This creates an instant voice clone (IVC)
        """
        from ..utils.audio import tensor_to_wav_buffer
        
        url = "https://api.elevenlabs.io/v1/voices/add"
        
        # Convert audio tensor to WAV
        wav_buffer = tensor_to_wav_buffer(audio_sample["waveform"], audio_sample["sample_rate"])
        
        headers = {
            "xi-api-key": api_key,
        }
        
        # Prepare data
        data = {
            "name": voice_name,
            "description": voice_description,
        }
        
        # Parse labels if provided
        if labels and labels.strip():
            labels_dict = {}
            for label in labels.split(","):
                if ":" in label:
                    key, value = label.split(":", 1)
                    labels_dict[key.strip()] = value.strip()
            if labels_dict:
                data["labels"] = str(labels_dict)
        
        # Files - the API expects files with specific field names
        files = {
            "files": ("sample.wav", wav_buffer, "audio/wav")
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            voice_id = result.get("voice_id")
            
            status_msg = f"""
╔══════════════════════════════════════╗
║       VOICE CLONE SUCCESSFUL        ║
╚══════════════════════════════════════╝

✓ Voice cloned successfully!

Voice Name: {voice_name}
Voice ID: {voice_id}
Description: {voice_description}

This voice is now available in your account
and can be used with the TTS node.

💡 Tip: Use the "Refresh Voices" node to 
see your new cloned voice in the voice list.
"""
            
            print(f"✓ Voice cloned: {voice_name} ({voice_id})")
            return (status_msg,)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"""
❌ Error cloning voice: {str(e)}

Common issues:
- Insufficient subscription tier
- Audio quality too low
- Audio too short (need 30s+ for best results)
- Hit voice clone limit for your plan

Check your ElevenLabs subscription and audio quality.
"""
            print(f"Error cloning voice: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
                error_msg += f"\n\nAPI Response: {e.response.text}"
            return (error_msg,)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

