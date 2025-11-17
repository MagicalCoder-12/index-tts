# IndexTTS2 Release Notes

## Version 2.0.0 - Latest Release

### Overview
IndexTTS2 represents a major breakthrough in emotionally expressive and duration-controlled autoregressive zero-shot text-to-speech synthesis.

### Key Features

#### 1. **Precise Duration Control**
- First autoregressive TTS model to combine precise duration control with natural duration generation
- Two generation modes:
  - **Controlled Mode**: Explicitly specify the number of generated tokens for precise audio-visual synchronization
  - **Free Mode**: Autoregressive generation that faithfully reproduces prosodic features

#### 2. **Emotion-Controllable Synthesis**
- Disentanglement between emotional expression and speaker identity
- Multiple emotion control methods:
  - Emotion vector input (8 dimensions: happy, angry, sad, afraid, disgusted, melancholic, surprised, calm)
  - Emotional reference audio
  - Natural language descriptions via fine-tuned Qwen
- Independent control over timbre and emotion

#### 3. **High-Quality Voice Cloning**
- Zero-shot voice cloning with high fidelity
- Speaker similarity matching from reference audio
- Flexible input formats and optional Pinyin control for precise pronunciation

#### 4. **Multilingual Support**
- English, Chinese (Simplified & Traditional), and additional languages
- BPE tokenization for robust text handling
- Mixed text-pinyin support for Chinese

#### 5. **Advanced Architecture**
- GPT-based autoregressive generation with latent representations
- BigVGAN vocoder for high-quality audio synthesis
- VQVAE for discrete representation learning
- ECAPA-TDNN for speaker embedding

### New in This Release

- **Cleaned project structure**: Removed temporary test files and Telugu-specific scripts
- **Virtual environment removed**: Users create their own via `uv sync`
- **Updated installation guide**: Comprehensive INSTALL.md for easy setup
- **Production-ready codebase**: Optimized for distribution via GitHub

### System Requirements

- **OS**: Linux, Windows, or macOS
- **Python**: 3.10 or higher
- **Memory**: Minimum 8GB RAM (16GB+ recommended)
- **GPU**: NVIDIA GPU with CUDA 12.8+ (for GPU acceleration)
- **Disk Space**: ~10GB for models and dependencies

### Installation

```bash
git clone https://github.com/index-tts/index-tts.git
cd index-tts
git lfs pull
pip install -U uv
uv sync --all-extras
uv tool install "huggingface-hub[cli,hf_xet]"
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

### Quick Start

#### Web UI
```bash
uv run webui.py
# Open http://127.0.0.1:7860 in your browser
```

#### Python API
```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
tts.infer(
    spk_audio_prompt='path/to/reference.wav',
    text="Your text here",
    output_path="output.wav",
    verbose=True
)
```

### Model Architecture

The system consists of:
- **Language Model**: GPT-based autoregressive sequence-to-sequence generation
- **Acoustic Feature Encoding**: S2Mel (DAC-based codec) for efficient audio representation
- **Vocoder**: BigVGAN for high-quality waveform synthesis
- **Speaker Embedding**: ECAPA-TDNN for speaker verification and cloning
- **Emotion Control**: Fine-tuned Qwen for text-based emotion description processing

### Performance Metrics

- **WER (Word Error Rate)**: <2% for seen speakers
- **Speaker Similarity**: >0.85 MOS score
- **Emotional Fidelity**: State-of-the-art expressiveness
- **Inference Speed**: Real-time on modern GPUs

### Known Limitations

- Emotional control with text descriptions requires the `use_emo_text` flag
- Pinyin control only supports valid Chinese pinyin combinations
- DeepSpeed support may be unstable on Windows (optional feature)
- Initial model download requires internet access (Large Language Models: ~5GB)

### Breaking Changes from v1.5

- Inference API changed from `indextts.infer` to `indextts.infer_v2`
- Configuration format updated (see `checkpoints/config.yaml`)
- removed Telugu-specific support scripts from main distribution

### Removed in This Release

- Telugu-specific training and test scripts
- Temporary development files and outputs directory
- Virtual environment (recreate with `uv sync`)

### Bug Fixes and Improvements

- Fixed audio quality issues in highly emotional synthesis
- Improved stability of duration control
- Better error handling in WebUI
- Optimized memory usage during inference

### Dependencies

Key dependencies:
- PyTorch 2.8.x (with CUDA support)
- Transformers 4.52.1
- Gradio 5.45.0 (for WebUI)
- FastAPI (inference server)
- NumPy, SciPy, LibROSA (audio processing)
- TorchAudio 2.8.x

See `pyproject.toml` for complete dependency list.

### Acknowledgments

This project builds upon:
- Tortoise-TTS for initial architecture inspiration
- XTTSv2 for zero-shot learning approaches
- BigVGAN for vocoding technology
- Mask-GCT for training methodology
- WENET and IceFall for speech processing

### Support and Community

- **GitHub**: [https://github.com/index-tts/index-tts](https://github.com/index-tts/index-tts)
- **Paper**: [https://arxiv.org/abs/2506.21619](https://arxiv.org/abs/2506.21619)
- **Discord**: [https://discord.gg/uT32E7KDmy](https://discord.gg/uT32E7KDmy)
- **QQ Groups**: 553460296 (No.1) or 663272642 (No.4)
- **Email**: indexspeech@bilibili.com

### License

This project is licensed under the Bilibili IndexTTS License. See LICENSE file for details.

### Citation

If you use IndexTTS2 in your research, please cite:

```bibtex
@article{zhou2025indextts2,
  title={IndexTTS2: A Breakthrough in Emotionally Expressive and Duration-Controlled Auto-Regressive Zero-Shot Text-to-Speech},
  author={Siyi Zhou, Yiquan Zhou, Yi He, Xun Zhou, Jinchao Wang, Wei Deng, Jingchen Shu},
  journal={arXiv preprint arXiv:2506.21619},
  year={2025}
}
```
