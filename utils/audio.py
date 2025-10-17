"""Audio tensor utilities for ComfyUI"""

import io
import torch
import torchaudio


def ensure_3d_tensor(tensor):
    """
    Ensure tensor is 3D for ComfyUI audio format [batch, channels, samples]
    
    Args:
        tensor: Input audio tensor
        
    Returns:
        3D tensor in ComfyUI format
    """
    if tensor.dim() == 1:
        # [samples] -> [1, 1, samples]
        return tensor.unsqueeze(0).unsqueeze(0)
    elif tensor.dim() == 2:
        # [channels, samples] -> [1, channels, samples]
        return tensor.unsqueeze(0)
    elif tensor.dim() > 3:
        # Squeeze extra dimensions
        return tensor.squeeze().unsqueeze(0)
    return tensor


def tensor_to_wav_buffer(waveform, sample_rate):
    """
    Convert audio tensor to WAV buffer
    
    Args:
        waveform: Audio tensor (3D)
        sample_rate: Sample rate of audio
        
    Returns:
        BytesIO buffer containing WAV data
    """
    waveform = ensure_3d_tensor(waveform)
    wav_buffer = io.BytesIO()
    # ComfyUI format is [batch, channels, samples], torchaudio needs [channels, samples]
    torchaudio.save(wav_buffer, waveform.squeeze(0), sample_rate, format="wav")
    wav_buffer.seek(0)
    return wav_buffer


def load_audio_from_response(response_content):
    """
    Load audio from API response content
    
    Args:
        response_content: Raw audio bytes from API response
        
    Returns:
        Tuple of (waveform, sample_rate) in ComfyUI format
    """
    audio_content = io.BytesIO(response_content)
    waveform, sample_rate = torchaudio.load(audio_content)
    
    # Ensure 3D tensor
    waveform = ensure_3d_tensor(waveform)
    
    # Ensure float32
    if waveform.dtype != torch.float32:
        waveform = waveform.float() / torch.iinfo(waveform.dtype).max
    
    # Final check
    if waveform.dim() != 3:
        waveform = waveform.view(1, 1, -1)
    
    return waveform, sample_rate


def create_empty_audio(sample_rate=44100):
    """
    Create empty audio tensor for error cases
    
    Args:
        sample_rate: Sample rate for the empty audio
        
    Returns:
        Dict with empty waveform and sample_rate
    """
    return {
        "waveform": torch.zeros(1, 1, 1).float(),
        "sample_rate": sample_rate
    }

