"""Text-to-Speech Node"""

import requests
from ..utils.api import fetch_voices_from_api, fetch_models_from_api
from ..utils.audio import load_audio_from_response, create_empty_audio
from ..utils.cache import ElevenLabsCache


class ElevenLabsTTS:
    """Enhanced Text-to-Speech node with all parameters"""
    
    _last_api_key = None
    
    @classmethod
    def INPUT_TYPES(cls):
        voices = fetch_voices_from_api()
        models = fetch_models_from_api()
        
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "tooltip": "Your ElevenLabs API key - voices auto-refresh when changed"
                }),
                "text": ("STRING", {
                    "multiline": True,
                    "default": "Hello, how are you?",
                    "tooltip": "Text to convert to speech. Note: eleven_v3 has 3K char limit, other models 10K-40K"
                }),
                "voice": (voices,),
                "model": (models,),
                "stability": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "similarity_boost": ("FLOAT", {
                    "default": 0.75,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "style": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Style exaggeration (0-1). For eleven_v3: controls emotional expressiveness and dramatic delivery"
                }),
                "use_speaker_boost": ("BOOLEAN", {
                    "default": True,
                }),
            },
            "optional": {
                "input_text": ("STRING", {"forceInput": True}),
                "language_code": (["auto", "en", "es", "fr", "de", "it", "pt", "pl", "ru", "nl", "ja", "zh", "ko", "hi", "ar"], {
                    "default": "auto"
                }),
                "output_format": (["mp3_44100_128", "mp3_44100_192", "pcm_16000", "pcm_22050", "pcm_24000", "pcm_44100"], {
                    "default": "mp3_44100_128"
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 4294967295
                }),
            }
        }
    
    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "generate_speech"
    CATEGORY = "ElevenLabs"
    
    def generate_speech(self, api_key, text, voice, model, stability, similarity_boost, style, use_speaker_boost, 
                       input_text=None, language_code="auto", output_format="mp3_44100_128", seed=-1):
        
        # Auto-refresh voices when API key changes
        if api_key and api_key != self.__class__._last_api_key:
            print(f"\n🔄 New API key detected - Auto-refreshing voices...")
            ElevenLabsCache.force_refresh_voices()
            ElevenLabsCache.force_refresh_models()
            fetch_voices_from_api(api_key, force_refresh=True)
            fetch_models_from_api(api_key, force_refresh=True)
            self.__class__._last_api_key = api_key
            print("✓ Voices and models refreshed! Reload node to see updates\n")
        
        # Use input_text if provided, otherwise use the text from the textbox
        final_text = input_text if input_text is not None else text
        
        if not final_text or final_text.strip() == "":
            print("❌ Error: No text provided for TTS")
            return (create_empty_audio(),)
        
        voice_id = voice.split("(")[-1].strip(")")
        voice_name = voice.split("(")[0].strip()
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": final_text,
            "model_id": model,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": use_speaker_boost
            }
        }
        
        # Add optional parameters
        if language_code != "auto":
            payload["language_code"] = language_code
        
        if seed >= 0:
            payload["seed"] = seed
        
        # Add output format as query parameter
        url_with_params = f"{url}?output_format={output_format}"
        
        # Log request details for API workflow conversion
        print("\n" + "="*60)
        print("🎤 ELEVENLABS TTS REQUEST")
        print("="*60)
        print(f"Voice: {voice_name}")
        print(f"Voice ID: {voice_id}")
        print(f"Model: {model}")
        print(f"Language: {language_code}")
        print(f"Text length: {len(final_text)} chars")
        print(f"Output format: {output_format}")
        print(f"Settings: stability={stability}, similarity={similarity_boost}, style={style}")
        if seed >= 0:
            print(f"Seed: {seed}")
        print("="*60 + "\n")
        
        try:
            response = requests.post(url_with_params, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            waveform, sample_rate = load_audio_from_response(response.content)
            
            print(f"✓ Generated speech: {len(final_text)} chars, {waveform.shape[2]/sample_rate:.2f}s")
            print(f"  Audio: {sample_rate}Hz, {waveform.shape}")
            return ({"waveform": waveform, "sample_rate": sample_rate},)
            
        except requests.exceptions.RequestException as e:
            print(f"\n❌ Error in text-to-speech: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Status Code: {e.response.status_code}")
                print(f"   Response: {e.response.text[:500]}")
            print(f"   Voice: {voice_name}")
            print(f"   Voice ID: {voice_id}")
            print(f"   Model: {model}")
            print(f"   Text length: {len(final_text)} characters")
            print(f"   URL: {url_with_params}")
            return (create_empty_audio(),)
    
    @classmethod
    def IS_CHANGED(cls, api_key, text, voice, model, stability, similarity_boost, style, use_speaker_boost, 
                   input_text=None, language_code="auto", output_format="mp3_44100_128", seed=-1):
        # Always regenerate
        return (api_key, text, voice, model, stability, similarity_boost, style, use_speaker_boost, 
                input_text, language_code, output_format, seed)

