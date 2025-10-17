"""Caching system for ElevenLabs API data"""

import time


class ElevenLabsCache:
    """Shared cache for voices and models across all nodes"""
    
    voices_cache = None
    models_cache = None
    voices_last_fetch = 0
    models_last_fetch = 0
    cache_duration = 3600  # 1 hour in seconds
    
    @classmethod
    def force_refresh_voices(cls):
        """Force refresh voices cache"""
        cls.voices_cache = None
        cls.voices_last_fetch = 0
        print("🔄 Voice cache invalidated")
    
    @classmethod
    def force_refresh_models(cls):
        """Force refresh models cache"""
        cls.models_cache = None
        cls.models_last_fetch = 0
        print("🔄 Model cache invalidated")
    
    @classmethod
    def is_voices_cache_valid(cls):
        """Check if voices cache is still valid"""
        current_time = time.time()
        return (cls.voices_cache is not None and 
                (current_time - cls.voices_last_fetch) < cls.cache_duration)
    
    @classmethod
    def is_models_cache_valid(cls):
        """Check if models cache is still valid"""
        current_time = time.time()
        return (cls.models_cache is not None and 
                (current_time - cls.models_last_fetch) < cls.cache_duration)
    
    @classmethod
    def set_voices(cls, voices):
        """Set voices cache"""
        cls.voices_cache = voices
        cls.voices_last_fetch = time.time()
    
    @classmethod
    def set_models(cls, models):
        """Set models cache"""
        cls.models_cache = models
        cls.models_last_fetch = time.time()
    
    @classmethod
    def get_voices(cls):
        """Get cached voices"""
        return cls.voices_cache
    
    @classmethod
    def get_models(cls):
        """Get cached models"""
        return cls.models_cache

