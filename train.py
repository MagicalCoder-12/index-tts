#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path
from types import SimpleNamespace

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import torch
import yaml
import argparse


def dict_to_namespace(d):
    if not isinstance(d, dict):
        return d
    result = SimpleNamespace()
    for k, v in d.items():
        if isinstance(v, dict):
            setattr(result, k, dict_to_namespace(v))
        else:
            setattr(result, k, v)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train IndexTTS model')
    parser.add_argument('--config', type=str, required=True)
    parser.add_argument('--exp_name', type=str, default='default_exp')
    parser.add_argument('--checkpoint', type=str, default=None)
    parser.add_argument('--resume_type', type=str, default=None)
    
    cmd_args = parser.parse_args()
    
    print('=' * 60)
    print('IndexTTS Telugu Training')
    print('=' * 60)
    
    config_path = cmd_args.config
    if not Path(config_path).exists():
        print(f'ERROR: Config not found: {config_path}')
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f) if config_path.endswith('.yaml') else json.load(f)
    
    cfg = dict_to_namespace(cfg)
    
    print(f'Config: {config_path}')
    print(f'Dataset: {cfg.dataset}')
    print(f'Batch: {cfg.train.batch_size}, Epochs: {cfg.train.max_epoch}')
    print()
    
    sys.path.insert(0, os.path.join(os.getcwd(), 'indextts', 'utils', 'maskgct'))
    sys.path.insert(0, os.path.join(os.getcwd(), 'indextts', 'utils'))
    
    try:
        from models.codec.facodec.facodec_trainer import FAcodecTrainer
        
        args = SimpleNamespace()
        args.exp_name = cmd_args.exp_name
        args.log_level = 'INFO'
        args.checkpoint = cmd_args.checkpoint
        args.resume_type = cmd_args.resume_type
        
        print('Initializing trainer...')
        trainer = FAcodecTrainer(args, cfg)
        
        print('Starting training...')
        trainer.train_loop()
        
        print('Training complete!')
        print(f'Checkpoints: {trainer.checkpoint_dir}')
        
    except Exception as e:
        print(f'ERROR: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
