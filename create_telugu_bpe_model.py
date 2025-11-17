#!/usr/bin/env python3
"""
Create a BPE model for Telugu language from the existing Telugu text data.
This script extracts all Telugu text from the metadata and creates a BPE model.
"""

import os
import pandas as pd
from pathlib import Path
import sentencepiece as spm

def extract_telugu_text():
    """Extract all Telugu text from the metadata files"""
    print("Extracting Telugu text from metadata...")
    
    # Path to the complete metadata file
    metadata_path = Path("tests/te/metadata/complete_metadata.csv")
    
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
    
    # Read the metadata
    df = pd.read_csv(metadata_path)
    
    # Extract all text entries
    telugu_texts = df['text'].tolist()
    
    print(f"Found {len(telugu_texts)} Telugu text entries")
    
    # Write all text to a single file
    output_file = Path("telugu_texts.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for text in telugu_texts:
            if pd.notna(text):  # Check if text is not NaN
                f.write(str(text) + '\n')
    
    print(f"Telugu texts written to {output_file}")
    return output_file

def train_bpe_model(input_file, model_prefix, vocab_size=8000):
    """Train a BPE model using SentencePiece"""
    print(f"Training BPE model with vocab size {vocab_size}...")
    
    # SentencePiece training parameters
    spm.SentencePieceTrainer.train(
        input=str(input_file),
        model_prefix=model_prefix,
        vocab_size=vocab_size,
        character_coverage=1.0,  # Cover all characters for Telugu
        model_type='bpe',  # Use BPE model
        split_by_whitespace=True,
        split_digits=True,
        byte_fallback=True,
        train_extremely_large_corpus=False,
        max_sentence_length=16384,
        shuffle_input_sentence=True,
        unk_id=0,
        bos_id=1,
        eos_id=2,
        pad_id=-1,  # No padding token
        unk_surface='<unk>',
        normalization_rule_name='nmt_nfkc_cf',
        remove_extra_whitespaces=True
    )
    
    print(f"BPE model trained and saved as {model_prefix}.model and {model_prefix}.vocab")

def main():
    print("Creating Telugu BPE model...")
    print("=" * 40)
    
    try:
        # Extract Telugu text
        text_file = extract_telugu_text()
        
        # Train BPE model
        model_prefix = "checkpoints/te_bpe"
        train_bpe_model(text_file, model_prefix, vocab_size=3000)
        
        # Clean up temporary text file
        text_file.unlink()
        
        print("\nTelugu BPE model creation completed!")
        print(f"Model files created:")
        print(f"  - checkpoints/te_bpe.model")
        print(f"  - checkpoints/te_bpe.vocab")
        
        # Test the model
        print("\nTesting the model...")
        sp = spm.SentencePieceProcessor(model_file='checkpoints/te_bpe.model')
        test_text = "ఈ వ్యవస్థ తెలుగు భాషను మద్దతు ఇస్తుంది"
        encoded = sp.encode(test_text, out_type=str)
        print(f"Test text: {test_text}")
        print(f"Encoded tokens: {encoded}")
        print(f"Vocabulary size: {sp.get_piece_size()}")
        
    except Exception as e:
        print(f"Error creating Telugu BPE model: {str(e)}")
        raise

if __name__ == "__main__":
    main()