import os
import pandas as pd
from pydub import AudioSegment
from tqdm import tqdm
import json

def convert_mp3_to_wav(input_dir, output_dir):
    """
    Convert MP3 files to WAV format
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of MP3 files
    mp3_files = [f for f in os.listdir(input_dir) if f.endswith('.mp3')]
    
    print(f"Converting {len(mp3_files)} MP3 files to WAV format...")
    
    # Convert each MP3 file to WAV
    converted_files = []
    for mp3_file in tqdm(mp3_files):
        try:
            # Load MP3 file
            mp3_path = os.path.join(input_dir, mp3_file)
            audio = AudioSegment.from_mp3(mp3_path)
            
            # Convert to WAV
            wav_file = mp3_file.replace('.mp3', '.wav')
            wav_path = os.path.join(output_dir, wav_file)
            audio.export(wav_path, format='wav')
            
            converted_files.append({
                'original_file': mp3_file,
                'converted_file': wav_file,
                'duration_ms': len(audio)
            })
        except Exception as e:
            print(f"Error converting {mp3_file}: {e}")
    
    return converted_files

def create_metadata_files(converted_files, clips_dir, validated_sentences_path, output_dir):
    """
    Create metadata files for the converted dataset
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read validated sentences
    try:
        validated_sentences = pd.read_csv(validated_sentences_path, sep='\t')
    except Exception as e:
        print(f"Error reading validated sentences: {e}")
        validated_sentences = pd.DataFrame()
    
    # Create a mapping from sentence_id to sentence (if possible)
    sentence_map = {}
    if not validated_sentences.empty:
        try:
            sentence_map = dict(zip(validated_sentences['sentence_id'], validated_sentences['sentence']))
        except KeyError:
            print("Could not find sentence_id or sentence columns in validated_sentences.tsv")
    
    # Create metadata list
    metadata = []
    
    # Process each converted file
    for file_info in converted_files:
        original_file = file_info['original_file']
        converted_file = file_info['converted_file']
        duration_ms = file_info['duration_ms']
        
        # Extract sentence_id from filename (common_voice_te_43371640.mp3 -> 43371640)
        # The format seems to be common_voice_te_{sentence_id}.mp3
        sentence_id = original_file.replace('common_voice_te_', '').replace('.mp3', '')
        
        # Look up sentence text
        sentence_text = ""
        if sentence_map:
            for sid, text in sentence_map.items():
                if sentence_id in str(sid):
                    sentence_text = text
                    break
        
        metadata.append({
            'file_name': converted_file,
            'sentence_id': sentence_id,
            'text': sentence_text,
            'duration_ms': duration_ms
        })
    
    # Create train/validation splits (80/20 split)
    train_metadata = metadata[:int(len(metadata) * 0.8)] if metadata else []
    val_metadata = metadata[int(len(metadata) * 0.8):] if metadata else []
    
    # Save metadata files
    if train_metadata:
        train_df = pd.DataFrame(train_metadata)
        val_df = pd.DataFrame(val_metadata)
        
        train_df.to_csv(os.path.join(output_dir, 'train_metadata.csv'), index=False)
        val_df.to_csv(os.path.join(output_dir, 'val_metadata.csv'), index=False)
    
    # Create a simple JSON metadata file as well
    metadata_json = {
        'train_files': len(train_metadata),
        'val_files': len(val_metadata),
        'total_files': len(metadata),
        'files': metadata
    }
    
    with open(os.path.join(output_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata_json, f, ensure_ascii=False, indent=2)
    
    print(f"Created metadata files:")
    print(f"- Train files: {len(train_metadata)}")
    print(f"- Validation files: {len(val_metadata)}")
    print(f"- Total files: {len(metadata)}")
    
    return metadata

def main():
    # Define paths
    te_clips_dir = 'tests/te/clips'
    validated_sentences_path = 'tests/te/validated_sentences.tsv'
    output_wav_dir = 'tests/te/wav_clips'
    metadata_output_dir = 'tests/te/metadata'
    
    # Convert MP3 to WAV
    print("Step 1: Converting MP3 files to WAV format...")
    converted_files = convert_mp3_to_wav(te_clips_dir, output_wav_dir)
    print(f"Successfully converted {len(converted_files)} files")
    
    # Create metadata files
    print("\nStep 2: Creating metadata files...")
    metadata = create_metadata_files(converted_files, te_clips_dir, validated_sentences_path, metadata_output_dir)
    print("Metadata files created successfully")
    
    print("\nConversion and metadata generation completed!")
    print(f"Converted files are in: {output_wav_dir}")
    print(f"Metadata files are in: {metadata_output_dir}")

if __name__ == "__main__":
    main()