"""API helper functions for ElevenLabs"""

import requests
from .cache import ElevenLabsCache


def fetch_voices_from_api(api_key=None, force_refresh=False):
    """
    Fetch voices from ElevenLabs API with caching
    
    Args:
        api_key: Optional API key for authenticated requests
        force_refresh: Force bypass cache
        
    Returns:
        List of voice strings in format "Name (voice_id)"
    """
    if not force_refresh and ElevenLabsCache.is_voices_cache_valid():
        return ElevenLabsCache.get_voices()
    
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {}
    if api_key:
        headers["xi-api-key"] = api_key
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        voices = response.json()["voices"]
        voice_list = [f"{voice['name']} ({voice['voice_id']})" for voice in voices]
        
        if not voice_list:
            voice_list = ["No voices available"]
        
        ElevenLabsCache.set_voices(voice_list)
        print(f"✓ Fetched {len(voice_list)} voices from ElevenLabs")
        return voice_list
        
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Error fetching voices: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f"\n   Status Code: {e.response.status_code}"
            error_msg += f"\n   Response: {e.response.text[:200]}"
        print(error_msg)
        
        cached = ElevenLabsCache.get_voices()
        if cached is None:
            return ["Error: Cannot fetch voices - check API key"]
        return cached


def fetch_models_from_api(api_key=None, force_refresh=False):
    """
    Fetch models from ElevenLabs API with caching
    
    According to ElevenLabs docs, models are built into the TTS endpoint
    There's no separate /v1/models endpoint, so we use known model list
    
    Args:
        api_key: Optional API key for authenticated requests
        force_refresh: Force bypass cache
        
    Returns:
        List of model IDs
    """
    # Known models from ElevenLabs documentation
    # Source: https://elevenlabs.io/docs/models
    known_models = [
        "eleven_v3",                        # NEW: Most emotionally expressive (70+ langs, 3K char limit)
        "eleven_ttv_v3",                    # NEW: Voice design model v3
        "eleven_multilingual_v2",           # 29 languages, 10K char limit
        "eleven_turbo_v2_5",                # Low latency, 32 languages, 40K char limit
        "eleven_turbo_v2",                  # English only, 40K char limit
        "eleven_flash_v2_5",                # Ultra-low latency, 32 languages, 40K char limit
        "eleven_flash_v2",                  # Ultra-low latency, English only
        "eleven_english_sts_v2",            # Speech-to-Speech English
        "eleven_multilingual_sts_v2",       # Speech-to-Speech Multilingual
        "eleven_multilingual_ttv_v2",       # Voice design model v2
        "eleven_monolingual_v1",            # DEPRECATED (but still works)
        "eleven_multilingual_v1"            # DEPRECATED (but still works)
    ]
    
    if not force_refresh and ElevenLabsCache.is_models_cache_valid():
        return ElevenLabsCache.get_models()
    
    # ElevenLabs doesn't have a models list endpoint
    # Models are specified directly in TTS requests
    # Use the known models from documentation
    ElevenLabsCache.set_models(known_models)
    
    if force_refresh and api_key:
        print(f"✓ Using {len(known_models)} models from ElevenLabs documentation")
    
    return known_models


def make_api_request(method, url, headers, **kwargs):
    """
    Make an API request with comprehensive error handling and logging
    
    Args:
        method: HTTP method (GET, POST, etc.)
        url: API endpoint URL
        headers: Request headers
        **kwargs: Additional arguments for requests
        
    Returns:
        Response object or None if error
    """
    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        print(f"❌ API Request Timeout: {url}")
        print(f"   The request took too long to complete")
        return None
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else "Unknown"
        print(f"❌ API HTTP Error {status_code}: {url}")
        if e.response is not None:
            print(f"   Response: {e.response.text[:500]}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"❌ API Connection Error: {url}")
        print(f"   Could not connect to ElevenLabs API")
        print(f"   Check your internet connection")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Status: {e.response.status_code}")
            print(f"   Response: {e.response.text[:500]}")
        return None

