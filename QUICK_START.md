# IndexTTS2 Quick Start Guide

Get IndexTTS2 up and running in 5 minutes!

## Prerequisites

- **Git & Git LFS**: [Install Git LFS](https://git-lfs.com/)
- **Python 3.10+**: [Install Python](https://www.python.org/)
- **GPU (Optional)**: NVIDIA GPU with CUDA 12.8+ for acceleration

## Installation (5 minutes)

### Step 1: Clone and Download (2 min)

```bash
git clone https://github.com/index-tts/index-tts.git
cd index-tts
git lfs install  # One-time setup
git lfs pull     # Download large files
```

### Step 2: Install Dependencies (2 min)

```bash
pip install -U uv
uv sync --all-extras
```

If download is slow, use a mirror:
```bash
uv sync --all-extras --default-index "https://mirrors.aliyun.com/pypi/simple"
```

### Step 3: Download Models (1 min)

```bash
uv tool install "huggingface-hub[cli,hf_xet]"
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
```

Done! You're ready to use IndexTTS2.

## Using the Web UI

```bash
uv run webui.py
```

Open your browser and visit: **http://127.0.0.1:7860**

### Features:
- **Voice Cloning**: Upload reference audio and generate speech
- **Emotion Control**: Choose from 8 emotion types
- **Text Input**: Plain text, Chinese, or with Pinyin annotations
- **Settings**: FP16 mode, DeepSpeed, CUDA kernels

## Using Python API

```python
from indextts.infer_v2 import IndexTTS2

# Initialize
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")

# Simple voice cloning
tts.infer(
    spk_audio_prompt='path/to/reference.wav',
    text="Hello, this is IndexTTS2!",
    output_path="output.wav"
)
```

### With Emotional Control

```python
# Using emotion vector: [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]
tts.infer(
    spk_audio_prompt='reference.wav',
    text="You surprised me!",
    output_path="output.wav",
    emo_vector=[0, 0, 0, 0, 0, 0, 0.7, 0]  # High surprise
)
```

### With Emotion Reference Audio

```python
tts.infer(
    spk_audio_prompt='reference_voice.wav',
    text="Your text here",
    output_path="output.wav",
    emo_audio_prompt='reference_emotion.wav',  # Emotional reference
    emo_alpha=0.8  # Emotion influence (0.0-1.0)
)
```

## Supported Languages

- **English** ✓
- **Chinese (Simplified & Traditional)** ✓
- **Multilingual** (Partial support)

### Chinese with Pinyin

```python
text = "这是DE5一个PIN2测试。"  # Pinyin-annotated text
tts.infer(spk_audio_prompt='ref.wav', text=text, output_path="output.wav")
```

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Always use `uv run` to ensure correct environment:
```bash
uv run webui.py
```

### Issue: "CUDA out of memory"
**Solution**: Enable FP16 inference:
```bash
uv run webui.py --fp16
```

### Issue: "Port 7860 already in use"
**Solution**: Use a different port:
```bash
uv run webui.py --listen 127.0.0.1 --server-port 7861
```

### Issue: "Model files not found"
**Solution**: Make sure Git LFS files are downloaded:
```bash
git lfs pull
```

### Issue: "CUDA not found"
**Solution**: Install NVIDIA CUDA 12.8+, then restart terminal.

## Performance Tips

1. **Use FP16**: Faster inference with minimal quality loss
   ```bash
   uv run webui.py --fp16
   ```

2. **Batch Processing**: Process multiple texts in sequence
3. **Cache Results**: Reuse outputs for identical inputs
4. **Disable Unnecessary Features**: Use minimal features needed

## Examples

### Example 1: Clone a Celebrity Voice

```python
from indextts.infer_v2 import IndexTTS2

tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")

tts.infer(
    spk_audio_prompt='celebrity_sample.wav',
    text="Hello, this is my synthesized voice!",
    output_path="celebrity_speech.wav"
)
```

### Example 2: Generate Emotional Speech

```python
# Angry version
tts.infer(
    spk_audio_prompt='speaker.wav',
    text="I'm furious about this!",
    output_path="angry.wav",
    emo_vector=[0, 1, 0, 0, 0, 0, 0, 0]  # Angry emotion
)

# Sad version
tts.infer(
    spk_audio_prompt='speaker.wav',
    text="This makes me sad...",
    output_path="sad.wav",
    emo_vector=[0, 0, 1, 0, 0, 0, 0, 0]  # Sad emotion
)
```

### Example 3: Batch Processing

```python
texts = [
    "First sentence here.",
    "Second sentence here.",
    "Third sentence here."
]

for i, text in enumerate(texts):
    tts.infer(
        spk_audio_prompt='reference.wav',
        text=text,
        output_path=f'output_{i:03d}.wav'
    )
```

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|------------|
| Python | 3.10 | 3.11+ |
| RAM | 8GB | 16GB+ |
| Disk | 10GB | 20GB |
| GPU | Optional | NVIDIA (8GB VRAM) |
| CUDA | 12.8+ | 12.8+ |

## Next Steps

- **Learn More**: Read [INSTALL.md](INSTALL.md) for detailed setup
- **Production Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing**: Check [CONTRIBUTING.md](CONTRIBUTING.md)
- **Community**: Join our [Discord](https://discord.gg/uT32E7KDmy)

## Getting Help

- **Documentation**: See [README.md](README.md)
- **Troubleshooting**: [INSTALL.md Troubleshooting Section](INSTALL.md#troubleshooting)
- **Issues**: [GitHub Issues](https://github.com/index-tts/index-tts/issues)
- **Email**: indexspeech@bilibili.com

## Tips & Tricks

1. **Save Models Locally**: Download once, use offline
2. **GPU Acceleration**: Significantly speeds up synthesis
3. **Pre-compute Embeddings**: Cache speaker embeddings for repeated use
4. **Batch Processing**: Process multiple texts efficiently
5. **Mix Languages**: Blend English and Chinese naturally

## License

This project is licensed under the Bilibili IndexTTS License. See [LICENSE](LICENSE) for details.

## Citation

If you use IndexTTS2, please cite:

```bibtex
@article{zhou2025indextts2,
  title={IndexTTS2: A Breakthrough in Emotionally Expressive and Duration-Controlled Auto-Regressive Zero-Shot Text-to-Speech},
  author={Siyi Zhou, Yiquan Zhou, Yi He, Xun Zhou, Jinchao Wang, Wei Deng, Jingchen Shu},
  journal={arXiv preprint arXiv:2506.21619},
  year={2025}
}
```

---

**Happy Synthesizing! 🎉**

For detailed information, visit [https://github.com/index-tts/index-tts](https://github.com/index-tts/index-tts)
