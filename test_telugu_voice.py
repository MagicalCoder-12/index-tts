#!/usr/bin/env python3
"""
Simple test script for Telugu voice cloning
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def test_telugu_voice_cloning():
    """Test Telugu voice cloning with a simple example"""
    print("Testing Telugu voice cloning...")
    
    # Check if we have the required files
    te_dir = Path("tests/te")
    wav_dir = te_dir / "wav_clips"
    metadata_dir = te_dir / "metadata"
    
    if not te_dir.exists():
        print("Error: Telugu dataset directory not found!")
        return False
        
    if not wav_dir.exists():
        print("Error: WAV clips directory not found!")
        return False
        
    # Get a sample voice file
    wav_files = list(wav_dir.glob("*.wav"))
    if not wav_files:
        print("Error: No WAV files found!")
        return False
    
    sample_voice = wav_files[0]
    print(f"Using sample voice: {sample_voice.name}")
    
    # Test text in Telugu
    telugu_text = "ఈ వ్యవస్థ తెలుగు భాషను మద్దతు ఇస్తుంది"  # "This system supports the Telugu language"
    print(f"Text to synthesize: {telugu_text}")
    
    # Check if BPE model exists
    bpe_model = Path("checkpoints/te_bpe.model")
    if not bpe_model.exists():
        print("Error: Telugu BPE model not found!")
        return False
    
    print("All required files found. Telugu voice cloning is ready!")
    print("\nTo clone a Telugu voice, run:")
    print(f"  python clone_telugu_voice.py --voice \"{sample_voice}\" --text \"{telugu_text}\" --output telugu_output.wav")
    
    return True

if __name__ == "__main__":
    test_telugu_voice_cloning()