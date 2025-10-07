import os
import pandas as pd

def verify_dataset():
    print("Verifying Telugu voice dataset...")
    
    # Check directories
    wav_dir = "tests/te/wav_clips"
    metadata_dir = "tests/te/metadata"
    
    if not os.path.exists(wav_dir):
        print(f"Error: WAV directory not found: {wav_dir}")
        return False
        
    if not os.path.exists(metadata_dir):
        print(f"Error: Metadata directory not found: {metadata_dir}")
        return False
    
    # Check WAV files
    wav_files = [f for f in os.listdir(wav_dir) if f.endswith('.wav')]
    print(f"Found {len(wav_files)} WAV files")
    
    # Check metadata files
    required_files = [
        "metadata.csv",
        "complete_metadata.csv",
        "train_metadata.csv",
        "val_metadata.csv"
    ]
    
    for file in required_files:
        file_path = os.path.join(metadata_dir, file)
        if not os.path.exists(file_path):
            print(f"Error: Required metadata file not found: {file}")
            return False
        print(f"Found metadata file: {file}")
    
    # Check content of complete metadata
    complete_metadata_path = os.path.join(metadata_dir, "complete_metadata.csv")
    df = pd.read_csv(complete_metadata_path)
    
    print(f"Complete metadata contains {len(df)} entries")
    
    # Verify all entries have text
    missing_text = df[df['text'].isnull() | (df['text'] == '')]
    if len(missing_text) > 0:
        print(f"Warning: {len(missing_text)} entries missing text content")
    else:
        print("All entries have text content")
    
    # Verify train/val split
    train_metadata_path = os.path.join(metadata_dir, "train_metadata.csv")
    val_metadata_path = os.path.join(metadata_dir, "val_metadata.csv")
    
    train_df = pd.read_csv(train_metadata_path)
    val_df = pd.read_csv(val_metadata_path)
    
    print(f"Training set: {len(train_df)} samples")
    print(f"Validation set: {len(val_df)} samples")
    print(f"Total: {len(train_df) + len(val_df)} samples")
    
    # Verify file existence
    missing_files = []
    for _, row in df.iterrows():
        wav_file = row['file_name']
        wav_path = os.path.join(wav_dir, wav_file)
        if not os.path.exists(wav_path):
            missing_files.append(wav_file)
    
    if missing_files:
        print(f"Error: {len(missing_files)} WAV files missing")
        return False
    else:
        print("All WAV files present")
    
    print("\nDataset verification completed successfully!")
    print(f"Summary:")
    print(f"- Total audio files: {len(wav_files)}")
    print(f"- Training samples: {len(train_df)} ({len(train_df)/len(df)*100:.1f}%)")
    print(f"- Validation samples: {len(val_df)} ({len(val_df)/len(df)*100:.1f}%)")
    print(f"- All files have text content: {'Yes' if len(missing_text) == 0 else 'No'}")
    
    return True

def main():
    success = verify_dataset()
    if success:
        print("\n✅ Dataset is ready for use!")
    else:
        print("\n❌ Dataset verification failed!")

if __name__ == "__main__":
    main()