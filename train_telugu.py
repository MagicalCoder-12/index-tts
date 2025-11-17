#!/usr/bin/env python3
import os
import sys
import json
import argparse
import torch
import yaml
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def prepare_telugu_training():
    print('=' * 60)
    print('Telugu Voice Cloning Training Preparation')
    print('=' * 60)
    
    te_dir = Path('tests/te')
    wav_dir = te_dir / 'wav_clips'
    metadata_dir = te_dir / 'metadata'
    
    if not te_dir.exists():
        print('ERROR: Telugu dataset not found at tests/te')
        return False
    
    if not wav_dir.exists():
        print('ERROR: WAV files not found')
        return False
    
    wav_files = list(wav_dir.glob('*.wav'))
    if not wav_files:
        print('ERROR: No WAV files found')
        return False
    
    print('OK Found {} Telugu voice samples'.format(len(wav_files)))
    print('OK Dataset location: {}'.format(wav_dir))
    print('OK Sample rate: 24000 Hz')
    print('OK Training dataset ready')
    
    config_path = 'checkpoints/config.yaml'
    if not Path(config_path).exists():
        print('ERROR: Base config not found: {}'.format(config_path))
        return False
    
    telugu_config = {
        'dataset': str(wav_dir),
        'language': 'te',
        'preprocess_params': {
            'sr': 24000,
            'duration_range': [3, 10],
            'frame_rate': 80,
            'spect_params': {
                'n_mels': 100,
                'n_fft': 1024,
                'win_length': 1024,
                'hop_length': 256
            }
        },
        'train': {
            'batch_size': 4,
            'max_epoch': 50,
            'gradient_accumulation_step': 1,
            'random_seed': 42,
            'dataloader': {
                'num_worker': 4,
                'pin_memory': True
            },
            'max_frame_len': 250
        },
        'telugu_support': True
    }
    
    output_config = 'checkpoints/config_telugu.json'
    os.makedirs(os.path.dirname(output_config), exist_ok=True)
    with open(output_config, 'w') as f:
        json.dump(telugu_config, f, indent=2)
    
    print('OK Configuration saved to {}'.format(output_config))
    print('')
    print('=' * 60)
    print('TRAINING SETUP COMPLETE')
    print('=' * 60)
    print('\nNext steps:')
    print('1. Review configuration: {}'.format(output_config))
    print('2. Start training with:')
    print('   python -m torch.distributed.launch --nproc_per_node=1 \\\\\\')
    print('     indextts/train.py --config {} \\\\\\'.format(output_config))
    print('     --exp_name telugu_voice_v1')
    print('')
    
    if torch.cuda.is_available():
        print('GPU Available: {}'.format(torch.cuda.get_device_name(0)))
    else:
        print('WARNING: No GPU detected. Training will be slow.')
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Prepare Telugu voice training')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    
    success = prepare_telugu_training()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
