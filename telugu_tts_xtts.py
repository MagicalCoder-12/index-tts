#!/usr/bin/env python3
"""
Telugu Text-to-Speech with Voice Cloning using Coqui XTTS
This supports BOTH Telugu language AND voice cloning!
"""

import os
import argparse
from pathlib import Path


def generate_telugu_with_voice_cloning(
    text,
    reference_audio,
    output_file="telugu_xtts_output.wav"
):
    """
    Generate Telugu speech with voice cloning using Coqui XTTS.
    
    Args:
        text (str): Telugu text to synthesize
        reference_audio (str): Path to reference audio for voice cloning
        output_file (str): Output WAV file path
    """
    try:
        from TTS.api import TTS
    except ImportError:
        print("ERROR: TTS library not installed!")
        print("Install it with: pip install TTS")
        print("OR: uv pip install TTS")
        return None
    
    print("=" * 60)
    print("Telugu TTS with Voice Cloning (Coqui XTTS)")
    print("=" * 60)
    print(f"Text: {text}")
    print(f"Reference Audio: {reference_audio}")
    print(f"Output: {output_file}\n")
    
    # Initialize XTTS model
    print("Loading Coqui XTTS model (this may take a minute)...")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    print("✓ Model loaded\n")
    
    # Generate speech with voice cloning
    print("Generating Telugu speech with your voice...")
    tts.tts_to_file(
        text=text,
        file_path=output_file,
        speaker_wav=reference_audio,
        language="te"  # Telugu language code
    )
    
    print(f"✓ Telugu audio saved to: {output_file}\n")
    
    return output_file


def batch_generate(reference_dir="tests/te/wav_clips", output_dir="telugu_xtts_outputs"):
    """Generate multiple Telugu samples with different voices."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Example Telugu texts
    telugu_texts = [
        "నమస్కారం, నేను తెలుగు మాట్లాడతాను",
        "తెలుగు భాష చాలా అందంగా ఉంది",
        "కృత్రిమ మేధస్సు భవిష్యత్తు సాంకేతికత",
        "ఈ రోజు మంచి రోజు",
    ]
    
    # Get reference audio files
    ref_dir = Path(reference_dir)
    if not ref_dir.exists():
        print(f"ERROR: Reference directory not found: {reference_dir}")
        return
    
    reference_files = list(ref_dir.glob("*.wav"))[:len(telugu_texts)]
    
    if not reference_files:
        print(f"ERROR: No WAV files found in {reference_dir}")
        return
    
    print(f"Found {len(reference_files)} reference audio files")
    print(f"Will generate {len(telugu_texts)} samples\n")
    
    # Generate with different voices
    for i, (text, ref_audio) in enumerate(zip(telugu_texts, reference_files), 1):
        output_path = os.path.join(output_dir, f"telugu_xtts_sample_{i}.wav")
        print(f"\n[{i}/{len(telugu_texts)}] Generating...")
        generate_telugu_with_voice_cloning(text, str(ref_audio), output_path)
    
    print("=" * 60)
    print(f"✓ All samples generated in: {output_dir}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Telugu speech with voice cloning using Coqui XTTS"
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Telugu text to synthesize"
    )
    parser.add_argument(
        "--reference",
        type=str,
        help="Path to reference audio for voice cloning"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="telugu_xtts_output.wav",
        help="Output WAV file path"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Generate batch samples with different voices"
    )
    
    args = parser.parse_args()
    
    if args.batch:
        # Generate multiple samples
        batch_generate()
    elif args.text and args.reference:
        # Single synthesis
        generate_telugu_with_voice_cloning(args.text, args.reference, args.output)
    else:
        # Demo with example
        print("Running demo with example Telugu text...\n")
        
        # Find a reference audio
        ref_audio = "tests/te/wav_clips/common_voice_te_43371640.wav"
        if not os.path.exists(ref_audio):
            wav_files = list(Path("tests/te/wav_clips").glob("*.wav"))
            if wav_files:
                ref_audio = str(wav_files[0])
            else:
                print("ERROR: No Telugu reference audio found!")
                print("Please provide --reference argument")
                return
        
        # Example Telugu text
        text = "నమస్కారం, ఇది తెలుగు వాయిస్ క్లోనింగ్ టెస్ట్"
        
        generate_telugu_with_voice_cloning(text, ref_audio, args.output)
        
        print("\nTo use your own text and voice:")
        print(f'  python telugu_tts_xtts.py --text "మీ తెలుగు వచనం" --reference path/to/audio.wav')
        print("\nTo generate multiple samples:")
        print(f"  python telugu_tts_xtts.py --batch")
        print("\nNote: First run will download the XTTS model (~2GB)")


if __name__ == "__main__":
    main()
