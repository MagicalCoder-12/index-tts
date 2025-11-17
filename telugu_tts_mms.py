#!/usr/bin/env python3
"""
Telugu Text-to-Speech using Meta's MMS-TTS
This WILL generate actual Telugu speech (not Chinese!)
"""

import torch
import scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer
import argparse


def generate_telugu_speech(text, output_file="telugu_output.wav"):
    """
    Generate Telugu speech using Meta's Massively Multilingual Speech model.
    
    Args:
        text (str): Telugu text to synthesize
        output_file (str): Output WAV file path
    """
    print("=" * 60)
    print("Telugu TTS with Meta MMS-TTS")
    print("=" * 60)
    print(f"Text: {text}")
    print(f"Output: {output_file}\n")
    
    # Load model and tokenizer
    print("Loading Meta MMS-TTS Telugu model...")
    model = VitsModel.from_pretrained("facebook/mms-tts-tel")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-tel")
    print("✓ Model loaded\n")
    
    # Tokenize input text
    print("Tokenizing text...")
    inputs = tokenizer(text=text, return_tensors="pt")
    
    # Generate speech
    print("Generating Telugu speech...")
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Save to file
    waveform = outputs.waveform[0].cpu().numpy()
    sampling_rate = model.config.sampling_rate
    
    scipy.io.wavfile.write(
        output_file,
        rate=sampling_rate,
        data=waveform
    )
    
    print(f"✓ Telugu audio saved to: {output_file}")
    print(f"  Sample rate: {sampling_rate} Hz")
    print(f"  Duration: {len(waveform) / sampling_rate:.2f} seconds\n")
    
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate Telugu speech using Meta MMS-TTS"
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Telugu text to synthesize"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="telugu_output.wav",
        help="Output WAV file path"
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Generate example Telugu speech samples"
    )
    
    args = parser.parse_args()
    
    if args.examples:
        # Generate multiple examples
        example_texts = [
            "నమస్కారం, నేను తెలుగు మాట్లాడతాను",
            "తెలుగు భాష చాలా అందంగా ఉంది",
            "కృత్రిమ మేధస్సు భవిష్యత్తు సాంకేతికత",
            "ఈ రోజు మంచి రోజు",
        ]
        
        for i, text in enumerate(example_texts, 1):
            output = f"telugu_example_{i}.wav"
            print(f"\n[Example {i}/{len(example_texts)}]")
            generate_telugu_speech(text, output)
        
        print("=" * 60)
        print(f"✓ Generated {len(example_texts)} Telugu audio samples")
        print("=" * 60)
        
    elif args.text:
        # Generate from user input
        generate_telugu_speech(args.text, args.output)
    else:
        # Default example
        print("Running with default Telugu example...\n")
        default_text = "నమస్కారం, ఇది తెలుగు వాయిస్ సింథసిస్ టెస్ట్"
        generate_telugu_speech(default_text, args.output)
        
        print("\nTo use your own Telugu text:")
        print('  python telugu_tts_mms.py --text "మీ తెలుగు వచనం"\n')
        print("To generate example samples:")
        print("  python telugu_tts_mms.py --examples\n")


if __name__ == "__main__":
    main()
