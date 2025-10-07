import os
import pandas as pd
import json

def create_complete_metadata():
    # Read the clip durations file (mapping between audio files and durations)
    clip_durations_path = 'tests/te/clip_durations.tsv'
    clip_df = pd.read_csv(clip_durations_path, sep='\t')
    
    # Read the other.tsv file (correct mapping between audio files and sentences)
    other_path = 'tests/te/other.tsv'
    other_df = pd.read_csv(other_path, sep='\t')
    
    # Create a dictionary for quick lookup of sentence text by audio file path
    audio_to_sentence = {}
    for _, row in other_df.iterrows():
        audio_file = row['path']  # e.g., "common_voice_te_43371640.mp3"
        sentence_text = row['sentence']
        audio_to_sentence[audio_file] = sentence_text
    
    # Create a list to store our complete metadata
    complete_metadata = []
    
    # Process each clip
    for _, clip_row in clip_df.iterrows():
        clip_name = clip_row['clip']  # e.g., "common_voice_te_43371640.mp3"
        duration_ms = clip_row['duration[ms]']
        
        # Convert MP3 filename to WAV filename
        wav_name = clip_name.replace('.mp3', '.wav')
        
        # Extract the numeric ID from the filename
        # Format: common_voice_te_XXXXXXXX.mp3
        try:
            numeric_id = clip_name.split('_')[-1].replace('.mp3', '')
        except:
            numeric_id = ""
        
        # Look for matching sentence text using the audio file path directly
        sentence_text = audio_to_sentence.get(clip_name, "")
        
        complete_metadata.append({
            'file_name': wav_name,
            'original_file': clip_name,
            'sentence_id': numeric_id,
            'text': sentence_text,
            'duration_ms': duration_ms
        })
    
    # Create DataFrame
    metadata_df = pd.DataFrame(complete_metadata)
    
    # Save to CSV
    metadata_df.to_csv('tests/te/metadata/complete_metadata.csv', index=False)
    
    # Save to JSON
    metadata_df.to_json('tests/te/metadata/complete_metadata.json', orient='records', indent=2)
    
    # Print statistics
    total_files = len(complete_metadata)
    files_with_text = sum(1 for item in complete_metadata if item['text'])
    
    print(f"Created complete metadata for {total_files} audio files")
    print(f"Found text for {files_with_text} files ({files_with_text/total_files*100:.1f}%)")
    
    # Show sample entries
    print("\nSample entries:")
    for i, item in enumerate(complete_metadata[:5]):
        print(f"  {item['file_name']}: {item['text'][:50]}{'...' if len(item['text']) > 50 else ''}")
    
    return complete_metadata

def main():
    print("Creating complete metadata with audio files, durations, and text...")
    metadata = create_complete_metadata()
    print("Complete metadata creation finished!")

if __name__ == "__main__":
    main()