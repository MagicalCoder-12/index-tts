import os
import pandas as pd
import json

def update_metadata_with_text():
    # Read the validated sentences file
    validated_sentences_path = 'tests/te/validated_sentences.tsv'
    validated_df = pd.read_csv(validated_sentences_path, sep='\t')
    
    # Read the existing metadata
    metadata_path = 'tests/te/metadata/metadata.csv'
    metadata_df = pd.read_csv(metadata_path)
    
    # Create a mapping from sentence_id to text
    sentence_map = {}
    for _, row in validated_df.iterrows():
        sentence_id = row['sentence_id']
        sentence_text = row['sentence']
        sentence_map[sentence_id] = sentence_text
    
    # Update metadata with text
    updated_rows = []
    for _, row in metadata_df.iterrows():
        file_name = row['file_name']
        sentence_id = row['sentence_id']
        
        # Extract the numeric part of the sentence_id to match with validated sentences
        # The audio files have names like common_voice_te_42973996.wav
        # The sentence_id in validated_sentences.tsv might be a hash
        
        # For now, let's try to match by looking for the numeric part in the sentence_id
        text = ""
        for sid, sentence_text in sentence_map.items():
            if str(sentence_id) in str(sid) or str(sid) in str(sentence_id):
                text = sentence_text
                break
        
        updated_rows.append({
            'file_name': file_name,
            'sentence_id': sentence_id,
            'text': text,
            'duration_ms': row['duration_ms']
        })
    
    # Create updated DataFrame
    updated_df = pd.DataFrame(updated_rows)
    
    # Save updated metadata
    updated_df.to_csv(metadata_path, index=False)
    
    # Also save as JSON
    updated_df.to_json('tests/te/metadata/metadata.json', orient='records', indent=2)
    
    # Print some statistics
    text_count = sum(1 for row in updated_rows if row['text'])
    print(f"Updated metadata with {text_count} text entries out of {len(updated_rows)} total entries")
    
    # Show some examples
    print("\nSample entries with text:")
    count = 0
    for row in updated_rows:
        if row['text'] and count < 5:
            print(f"  {row['file_name']}: {row['text'][:50]}...")
            count += 1

def main():
    print("Updating metadata with text from validated sentences...")
    update_metadata_with_text()
    print("Metadata update completed!")

if __name__ == "__main__":
    main()