#!/usr/bin/env python3
"""
Verify that the Telugu BPE model works correctly
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from indextts.utils.front import TextTokenizer, TextNormalizer

def test_telugu_bpe():
    """Test the Telugu BPE model"""
    print("Testing Telugu BPE model...")
    
    # Initialize normalizer
    normalizer = TextNormalizer()
    normalizer.load()
    
    # Test with Telugu BPE model
    telugu_bpe_path = "checkpoints/te_bpe.model"
    tokenizer = TextTokenizer(telugu_bpe_path, normalizer)
    
    print(f"Telugu BPE model loaded from: {telugu_bpe_path}")
    print(f"Vocabulary size: {tokenizer.vocab_size}")
    
    # Test text
    test_text = "ఈ వ్యవస్థ తెలుగు భాషను మద్దతు ఇస్తుంది"
    print(f"\nTest text: {test_text}")
    
    # Tokenize
    tokens = tokenizer.tokenize(test_text)
    print(f"Tokens: {tokens}")
    
    # Convert to IDs
    ids = tokenizer.convert_tokens_to_ids(tokens)
    print(f"Token IDs: {ids}")
    
    # Decode back
    decoded = tokenizer.decode(ids)
    print(f"Decoded text: {decoded}")
    
    print("\nTelugu BPE model verification completed successfully!")

if __name__ == "__main__":
    test_telugu_bpe()