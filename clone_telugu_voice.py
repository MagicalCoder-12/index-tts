#!/usr/bin/env python3
"""
Telugu Voice Cloning Inference Script
This script demonstrates how to use the IndexTTS model for Telugu voice cloning.
"""

import os
import sys
import argparse
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from indextts.infer_v2 import IndexTTS2


def list_telugu_voices():
    """List available Telugu voice samples"""
    te_dir = Path("tests/te/wav_clips")
    if not te_dir.exists():
        print("Error: Telugu dataset not found. Please run convert_te_dataset.py first.")
        return []
    
    wav_files = list(te_dir.glob("*.wav"))
    print(f"Found {len(wav_files)} Telugu voice samples:")
    for i, wav_file in enumerate(wav_files[:10]):  # Show first 10
        print(f"  {i+1}. {wav_file.name}")
    
    if len(wav_files) > 10:
        print(f"  ... and {len(wav_files) - 10} more")
    
    return [str(f) for f in wav_files]


def clone_telugu_voice(voice_path, text, output_path, use_emo=False):
    """Clone Telugu voice using IndexTTS2"""
    try:
        print("Initializing IndexTTS2 model...")
        
        # Initialize the model
        tts = IndexTTS2(
            model_dir="checkpoints",
            cfg_path="checkpoints/config.yaml",
            use_fp16=False,
            use_deepspeed=False,
            use_cuda_kernel=False
        )
        
        print(f"Using voice reference: {voice_path}")
        print(f"Text to synthesize: {text}")
        
        # Set emotion parameters if needed
        if use_emo:
            print("Using emotional voice cloning...")
            # You can specify emotion parameters here
            emo_alpha = 0.6
            tts.infer(
                spk_audio_prompt=voice_path,
                text=text,
                output_path=output_path,
                emo_alpha=emo_alpha,
                use_emo_text=True,
                emo_text="తెలుగు భాషకు సంబంధించిన సందేశం",  # Telugu related message
                verbose=True
            )
        else:
            print("Using standard voice cloning...")
            tts.infer(
                spk_audio_prompt=voice_path,
                text=text,
                output_path=output_path,
                verbose=True
            )
        
        print(f"Voice cloning completed! Output saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error during voice cloning: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Clone Telugu voices using IndexTTS")
    parser.add_argument("--voice", type=str, help="Path to voice reference WAV file")
    parser.add_argument("--text", type=str, default="ఈ వ్యవస్థ తెలుగు భాషను మద్దతు ఇస్తుంది", 
                        help="Text to synthesize in Telugu (default: 'ఈ వ్యవస్థ తెలుగు భాషను మద్దతు ఇస్తుంది')")
    parser.add_argument("--output", type=str, default="telugu_clone_output.wav",
                        help="Output WAV file path")
    parser.add_argument("--emo", action="store_true",
                        help="Use emotional voice cloning")
    parser.add_argument("--list", action="store_true",
                        help="List available Telugu voice samples")
    
    args = parser.parse_args()
    
    print("Telugu Voice Cloning Demo")
    print("=" * 30)
    
    # List voices if requested
    if args.list:
        list_telugu_voices()
        return
    
    # Check if voice file is provided
    if not args.voice:
        print("No voice reference provided. Listing available Telugu voices...")
        voices = list_telugu_voices()
        if voices:
            print(f"\nExample usage:")
            print(f"  python clone_telugu_voice.py --voice \"{voices[0]}\" --text \"మీ కోసం తెలుగు టెక్స్ట్-టు-స్పీచ్ సింథసైజర్\" --output output.wav")
        return
    
    # Check if voice file exists
    if not os.path.exists(args.voice):
        print(f"Error: Voice file not found: {args.voice}")
        return
    
    # Clone the voice
    success = clone_telugu_voice(
        voice_path=args.voice,
        text=args.text,
        output_path=args.output,
        use_emo=args.emo
    )
    
    if success:
        print(f"\nSuccess! Generated Telugu voice clone saved to: {args.output}")
    else:
        print("\nVoice cloning failed. Please check the error messages above.")


if __name__ == "__main__":
    main()