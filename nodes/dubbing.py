"""Dubbing Node - Dub audio/video into different languages"""

import requests
import time


class ElevenLabsDubbing:
    """
    Dubbing - Automatically dub audio or video into different languages
    Note: This is an async operation that requires polling for completion
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "audio": ("AUDIO",),
                "target_language": (["es", "fr", "de", "it", "pt", "pl", "ru", "nl", "ja", "zh", "ko", "hi", "ar", "tr"], {
                    "default": "es"
                }),
                "source_language": (["auto", "en", "es", "fr", "de", "it", "pt", "pl", "ru", "nl", "ja", "zh", "ko", "hi", "ar", "tr"], {
                    "default": "auto"
                }),
                "num_speakers": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10
                }),
            },
            "optional": {
                "wait_for_completion": ("BOOLEAN", {
                    "default": True,
                    "label_on": "Wait",
                    "label_off": "Don't Wait"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("dubbing_id_or_status",)
    FUNCTION = "create_dubbing"
    CATEGORY = "ElevenLabs"
    OUTPUT_NODE = True
    
    def create_dubbing(self, api_key, audio, target_language, source_language, num_speakers, wait_for_completion=True):
        """
        Create a dubbing project
        Returns dubbing_id or status message
        """
        from ..utils.audio import tensor_to_wav_buffer
        
        url = "https://api.elevenlabs.io/v1/dubbing"
        
        # Convert audio tensor to WAV
        wav_buffer = tensor_to_wav_buffer(audio["waveform"], audio["sample_rate"])
        
        headers = {
            "xi-api-key": api_key,
        }
        
        data = {
            "target_lang": target_language,
            "mode": "automatic",
            "num_speakers": num_speakers,
        }
        
        if source_language != "auto":
            data["source_lang"] = source_language
        
        files = {
            "file": ("audio.wav", wav_buffer, "audio/wav")
        }
        
        try:
            # Create dubbing project
            response = requests.post(url, headers=headers, data=data, files=files, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            dubbing_id = result.get("dubbing_id")
            
            if not dubbing_id:
                return ("Error: No dubbing_id returned",)
            
            print(f"✓ Dubbing project created: {dubbing_id}")
            
            # If wait for completion, poll the status
            if wait_for_completion:
                return (self._wait_for_dubbing(api_key, dubbing_id),)
            else:
                return (f"Dubbing ID: {dubbing_id}\nStatus: Processing\nUse this ID to check status later.",)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error creating dubbing: {str(e)}"
            print(error_msg)
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return (error_msg,)
    
    def _wait_for_dubbing(self, api_key, dubbing_id, max_wait=300):
        """Poll dubbing status until complete or timeout"""
        url = f"https://api.elevenlabs.io/v1/dubbing/{dubbing_id}"
        headers = {
            "xi-api-key": api_key,
        }
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                result = response.json()
                
                status = result.get("status", "unknown")
                print(f"Dubbing status: {status}")
                
                if status == "dubbed":
                    return (f"✓ Dubbing complete!\nID: {dubbing_id}\nStatus: {status}\n"
                           f"Download URL available in API response.")
                elif status == "dubbing":
                    time.sleep(10)  # Wait 10 seconds before next check
                    continue
                else:
                    return (f"Dubbing ID: {dubbing_id}\nStatus: {status}")
                    
            except requests.exceptions.RequestException as e:
                return (f"Error checking dubbing status: {str(e)}",)
        
        return (f"Dubbing timeout after {max_wait}s\nID: {dubbing_id}\nCheck status manually.",)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

