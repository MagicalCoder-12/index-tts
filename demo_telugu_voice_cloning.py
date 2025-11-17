#!/usr/bin/env python3
"""
Demo script showing how to use Telugu voice cloning with IndexTTS
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def main():
    print("=== Telugu Voice Cloning Demo ===")
    print()
    
    # 1. Show available Telugu voices
    print("1. Available Telugu Voices:")
    os.system("python clone_telugu_voice.py --list")
    print()
    
    # 2. Verify BPE model
    print("2. Verifying Telugu BPE Model:")
    os.system("python verify_telugu_bpe.py")
    print()
    
    # 3. Show configuration
    print("3. Configuration Summary:")
    config_path = Path("checkpoints/config.yaml")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config_content = f.read()
            # Show only the Telugu-related parts
            lines = config_content.split('\n')
            telugu_lines = []
            in_dataset_section = False
            for line in lines:
                if line.strip() == 'dataset:':
                    in_dataset_section = True
                if in_dataset_section:
                    telugu_lines.append(line)
                    if line.strip() == '' and len(telugu_lines) > 5:  # End of dataset section
                        break
            print("\n".join(telugu_lines[:20]))  # Show first 20 lines
    print()
    
    # 4. Show sample command
    print("4. Sample Usage Command:")
    sample_voice = "tests/te/wav_clips/common_voice_te_43371640.wav"
    sample_text = "ఈ వ్యవస్థ తెలుగు భాషను మద్దతు ఇస్తుంది"
    print(f"   python clone_telugu_voice.py --voice \"{sample_voice}\" --text \"{sample_text}\" --output telugu_demo_output.wav")
    print()
    
    print("=== Demo Complete ===")
    print()
    print("To try voice cloning, run the sample command above!")

if __name__ == "__main__":
    main()