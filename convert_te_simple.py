import os
import soundfile as sf
import librosa
from tqdm import tqdm
import pandas as pd

def convert_mp3_to_wav(input_dir, output_dir):
    """
    Convert MP3 files to WAV format using librosa
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
            y, sr = librosa.load(mp3_path, sr=None)
            
            # Convert to WAV
            wav_file = mp3_file.replace('.mp3', '.wav')
            wav_path = os.path.join(output_dir, wav_file)
            sf.write(wav_path, y, sr)
            
            converted_files.append({
                'original_file': mp3_file,
                'converted_file': wav_file,
                'duration_ms': len(y) * 1000 // sr
            })
        except Exception as e:
            print(f"Error converting {mp3_file}: {e}")
    
    return converted_files

def create_metadata_files(converted_files, validated_sentences_path, output_dir):
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
    
    # Create metadata list
    metadata = []
    
    # Process each converted file
    for file_info in converted_files:
        original_file = file_info['original_file']
        converted_file = file_info['converted_file']
        duration_ms = file_info['duration_ms']
        
        # Extract sentence_id from filename
        sentence_id = original_file.replace('common_voice_te_', '').replace('.mp3', '')
        
        # Look up sentence text
        sentence_text = ""
        if not validated_sentences.empty:
            # Try to find matching sentence
            matching_rows = validated_sentences[validated_sentences['sentence_id'].str.contains(sentence_id, na=False)]
            if not matching_rows.empty:
                sentence_text = matching_rows.iloc[0]['sentence']
        
        metadata.append({
            'file_name': converted_file,
            'sentence_id': sentence_id,
            'text': sentence_text,
            'duration_ms': duration_ms
        })
    
    # Save metadata
    if metadata:
        df = pd.DataFrame(metadata)
        df.to_csv(os.path.join(output_dir, 'metadata.csv'), index=False)
        
        # Also save as JSON
        df.to_json(os.path.join(output_dir, 'metadata.json'), orient='records', indent=2)
        
        print(f"Created metadata file with {len(metadata)} entries")
    else:
        print("No metadata to save")

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
    create_metadata_files(converted_files, validated_sentences_path, metadata_output_dir)
    
    print("\nConversion and metadata generation completed!")
    print(f"Converted files are in: {output_wav_dir}")
    print(f"Metadata files are in: {metadata_output_dir}")

if __name__ == "__main__":
    main()