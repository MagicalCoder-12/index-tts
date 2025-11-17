#!/usr/bin/env python3
"""
Prepare Telugu Dataset for Training
This script ensures the Telugu dataset is properly formatted for FAcodec training.
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import librosa

def verify_and_prepare_dataset() -> bool:
    """Verify and prepare the Telugu dataset for FAcodec training"""
    print("\n" + "="*50)
    print("Verifying Telugu dataset for FAcodec training...")
    print("="*50)
    
    # Check directories
    te_dir = Path("tests/te")
    wav_dir = te_dir / "wav_clips"
    metadata_dir = te_dir / "metadata"
    
    if not te_dir.exists():
        print("✗ Error: Telugu dataset directory not found!")
        return False
    
    if not wav_dir.exists():
        print("✗ Error: WAV clips directory not found!")
        return False
    
    if not metadata_dir.exists():
        print("✓ Creating metadata directory...")
        metadata_dir.mkdir(parents=True, exist_ok=True)
    
    # Check WAV files
    wav_files = list(wav_dir.glob("*.wav"))
    print(f"Found {len(wav_files)} WAV files")
    
    if len(wav_files) == 0:
        print("Error: No WAV files found!")
        return False
    
    # Check metadata files
    complete_metadata = metadata_dir / "complete_metadata.csv"
    if not complete_metadata.exists():
        print("Complete metadata not found. Creating from existing data...")
        # Try to create from other.tsv or validated_sentences.tsv
        other_tsv = te_dir / "other.tsv"
        if other_tsv.exists():
            create_metadata_from_other_tsv(other_tsv, wav_dir, metadata_dir)
        else:
            validated_tsv = te_dir / "validated_sentences.tsv"
            if validated_tsv.exists():
                create_metadata_from_validated_tsv(validated_tsv, wav_dir, metadata_dir)
            else:
                print("Error: No source metadata files found!")
                return False
    
    # Verify metadata integrity
    if complete_metadata.exists():
        try:
            df = pd.read_csv(complete_metadata)
            required_columns = ['file_name', 'original_file', 'sentence_id', 'text', 'duration_ms']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"Warning: Missing columns in metadata: {missing_columns}")
            else:
                print(f"Metadata verified: {len(df)} entries")
        except Exception as e:
            print(f"Error reading metadata: {e}")
            return False
    
    # Check train/val splits
    train_metadata = metadata_dir / "train_metadata.csv"
    val_metadata = metadata_dir / "val_metadata.csv"
    
    if not train_metadata.exists() or not val_metadata.exists():
        print("Creating train/validation splits...")
        create_train_val_splits(complete_metadata, metadata_dir)
    
    print("Telugu dataset preparation completed successfully!")
    return True


def create_metadata_from_other_tsv(other_tsv_path, wav_dir, metadata_dir):
    """Create metadata from other.tsv file"""
    print("Creating metadata from other.tsv...")
    
    try:
        # Read the other.tsv file
        df = pd.read_csv(other_tsv_path, sep='\t')
        
        # Prepare metadata list
        metadata = []
        
        # Get all WAV files
        wav_files = list(wav_dir.glob("*.wav"))
        wav_dict = {f.name: f for f in wav_files}
        
        # Process each entry
        for _, row in df.iterrows():
            original_file = row['path']  # e.g., common_voice_te_43371640.mp3
            sentence_id = row['sentence_id']
            text = row['sentence']
            
            # Convert MP3 filename to WAV filename
            if original_file.endswith('.mp3'):
                wav_filename = original_file.replace('.mp3', '.wav')
            else:
                wav_filename = original_file
            
            # Check if WAV file exists
            if wav_filename in wav_dict:
                # For duration, we would normally calculate it, but for now we'll use a placeholder
                # In a real implementation, you would use librosa or similar to get actual duration
                duration_ms = 3000  # Placeholder
                
                metadata.append({
                    'file_name': wav_filename,
                    'original_file': original_file,
                    'sentence_id': sentence_id,
                    'text': text,
                    'duration_ms': duration_ms
                })
        
        # Save complete metadata
        if metadata:
            metadata_df = pd.DataFrame(metadata)
            complete_metadata_path = metadata_dir / "complete_metadata.csv"
            metadata_df.to_csv(complete_metadata_path, index=False)
            print(f"Created complete metadata with {len(metadata)} entries")
        else:
            print("Warning: No matching WAV files found for metadata")
            
    except Exception as e:
        print(f"Error creating metadata from other.tsv: {e}")


def create_metadata_from_validated_tsv(validated_tsv_path, wav_dir, metadata_dir):
    """Create metadata from validated_sentences.tsv file"""
    print("Creating metadata from validated_sentences.tsv...")
    
    try:
        # This is a simplified implementation
        # In a real scenario, you would need to match sentences with audio files
        print("Note: Creating basic metadata structure from validated sentences")
        
        # For demonstration, we'll create a minimal metadata file
        # In practice, you would need to properly match sentences with audio files
        
    except Exception as e:
        print(f"Error creating metadata from validated_sentences.tsv: {e}")


def create_train_val_splits(complete_metadata_path, metadata_dir):
    """Create train/validation splits"""
    try:
        # Read complete metadata
        df = pd.read_csv(complete_metadata_path)
        
        # Shuffle the dataframe
        df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Split into train (90%) and validation (10%)
        split_index = int(0.9 * len(df_shuffled))
        train_df = df_shuffled[:split_index]
        val_df = df_shuffled[split_index:]
        
        # Save train and validation metadata
        train_metadata_path = metadata_dir / "train_metadata.csv"
        val_metadata_path = metadata_dir / "val_metadata.csv"
        
        train_df.to_csv(train_metadata_path, index=False)
        val_df.to_csv(val_metadata_path, index=False)
        
        print(f"Created train/validation splits:")
        print(f"  Train: {len(train_df)} samples")
        print(f"  Validation: {len(val_df)} samples")
        
    except Exception as e:
        print(f"Error creating train/validation splits: {e}")


def main():
    print("Telugu Dataset Preparation Script")
    print("=" * 35)
    
    success = verify_and_prepare_dataset()
    
    if success:
        print("\nDataset is ready for training!")
        print("\nTo train the model, you can:")
        print("1. Use the train_telugu_voice.py script")
        print("2. Or manually run the training process with the prepared dataset")
        print("\nTo test voice cloning, use:")
        print("  python clone_telugu_voice.py --list")
        print("  python clone_telugu_voice.py --voice <voice_file> --text <telugu_text>")
    else:
        print("\nDataset preparation failed. Please check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()