"""ElevenLabs ComfyUI Nodes"""

# Import all nodes
from .tts import ElevenLabsTTS
from .stt import ElevenLabsSpeechToText
from .sound_effects import ElevenLabsSoundEffects
from .voice_isolator import ElevenLabsVoiceIsolator
from .voice_changer import ElevenLabsVoiceChanger
from .dubbing import ElevenLabsDubbing
from .voice_design import ElevenLabsVoiceDesign
from .voice_clone import ElevenLabsVoiceClone
from .music import ElevenLabsMusic
from .user_info import ElevenLabsUserInfo
from .refresh import ElevenLabsRefreshVoices
from .history import ElevenLabsHistory
from .voice_manager import ElevenLabsVoiceManager

# Export all node classes
NODE_CLASS_MAPPINGS = {
    "ElevenLabsTTS": ElevenLabsTTS,
    "ElevenLabsSpeechToText": ElevenLabsSpeechToText,
    "ElevenLabsSoundEffects": ElevenLabsSoundEffects,
    "ElevenLabsVoiceIsolator": ElevenLabsVoiceIsolator,
    "ElevenLabsVoiceChanger": ElevenLabsVoiceChanger,
    "ElevenLabsDubbing": ElevenLabsDubbing,
    "ElevenLabsVoiceDesign": ElevenLabsVoiceDesign,
    "ElevenLabsVoiceClone": ElevenLabsVoiceClone,
    "ElevenLabsMusic": ElevenLabsMusic,
    "ElevenLabsUserInfo": ElevenLabsUserInfo,
    "ElevenLabsRefreshVoices": ElevenLabsRefreshVoices,
    "ElevenLabsHistory": ElevenLabsHistory,
    "ElevenLabsVoiceManager": ElevenLabsVoiceManager,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ElevenLabsTTS": "ElevenLabs Text-to-Speech",
    "ElevenLabsSpeechToText": "ElevenLabs Speech-to-Text",
    "ElevenLabsSoundEffects": "ElevenLabs Sound Effects",
    "ElevenLabsVoiceIsolator": "ElevenLabs Voice Isolator",
    "ElevenLabsVoiceChanger": "ElevenLabs Voice Changer",
    "ElevenLabsDubbing": "ElevenLabs Dubbing",
    "ElevenLabsVoiceDesign": "ElevenLabs Voice Design",
    "ElevenLabsVoiceClone": "ElevenLabs Voice Clone",
    "ElevenLabsMusic": "ElevenLabs Music Generation",
    "ElevenLabsUserInfo": "ElevenLabs User Info (Credits)",
    "ElevenLabsRefreshVoices": "ElevenLabs Refresh Voices",
    "ElevenLabsHistory": "ElevenLabs History",
    "ElevenLabsVoiceManager": "ElevenLabs Voice Manager",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

