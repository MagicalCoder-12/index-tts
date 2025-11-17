# IndexTTS2 Documentation Index

Complete guide to all available documentation in this repository.

## Getting Started (Start Here!)

### 👤 **New Users**
1. **[QUICK_START.md](QUICK_START.md)** - Get up and running in 5 minutes
   - Prerequisites and installation
   - Web UI quick start
   - Python API examples
   - Troubleshooting

2. **[INSTALL.md](INSTALL.md)** - Detailed installation guide
   - System requirements
   - Step-by-step setup
   - Optional features (DeepSpeed, FP16)
   - Mirror options for slow networks
   - Comprehensive troubleshooting

### 🚀 **Developers & Contributors**
1. **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
   - Development setup
   - Code style guidelines
   - Testing requirements
   - PR submission process
   - Project structure

2. **[README.md](README.md)** - Main project documentation
   - Project overview
   - Features and capabilities
   - API usage examples
   - Model downloads
   - Community and support

## Feature Guides

### 🎤 **Voice Cloning**
See [README.md](README.md) - Section "📝 Using IndexTTS2 in Python"
- Zero-shot voice cloning with high fidelity
- Reference audio input
- Example code provided

### 😊 **Emotion Control**
See [README.md](README.md) and [QUICK_START.md](QUICK_START.md)
- Emotion vectors (8 dimensions)
- Emotional reference audio
- Text-based emotion descriptions
- Multiple emotion control methods

### 🗣️ **Multilingual Support**
See [README.md](README.md)
- English, Chinese (Traditional & Simplified)
- Pinyin-annotated text for precise pronunciation
- BPE tokenization
- Language mixing examples

### 🎯 **Duration Control** (Advanced)
See [README.md](README.md) and [RELEASE_NOTES.md](RELEASE_NOTES.md)
- Precise synthesis duration control
- Controlled vs. free generation modes
- Autoregressive features

## Production & Deployment

### 🐳 **Docker & Containers**
See [DEPLOYMENT.md](DEPLOYMENT.md)
- Docker image building
- Docker Compose for multi-service setup
- Container best practices

### ☁️ **Cloud Deployment**
See [DEPLOYMENT.md](DEPLOYMENT.md)
- AWS SageMaker setup
- Google Cloud Platform (Vertex AI)
- Azure Container Instances
- Environment variables and secrets

### 🔄 **API Servers**
See [DEPLOYMENT.md](DEPLOYMENT.md)
- FastAPI inference server setup
- REST API endpoints
- Batch processing
- Request/response examples

### 📊 **Performance & Optimization**
See [DEPLOYMENT.md](DEPLOYMENT.md)
- GPU memory management
- FP16 quantization
- Model optimization
- Batch processing
- Caching strategies

### 🔍 **Monitoring & Logging**
See [DEPLOYMENT.md](DEPLOYMENT.md)
- Health check endpoints
- Prometheus metrics
- Logging configuration
- Error handling

## Release & Distribution

### 🔖 **Release Notes**
See [RELEASE_NOTES.md](RELEASE_NOTES.md)
- Version 2.0.0 features
- Breaking changes from v1.5
- Known limitations
- Performance metrics
- System requirements

### 📦 **Release Process**
See [RELEASE_PROCESS.md](RELEASE_PROCESS.md)
- How to create releases
- GitHub Actions workflow
- Version numbering (Semantic Versioning)
- Pre-release checklist
- Release artifacts

### 📋 **Cleanup Summary**
See [CLEANUP_SUMMARY.txt](CLEANUP_SUMMARY.txt)
- What was removed
- What was added
- Project statistics
- Quality assurance notes

## Project Structure

```
├── README.md                      ← Main documentation
├── QUICK_START.md                 ← 5-minute setup
├── INSTALL.md                     ← Detailed installation
├── RELEASE_NOTES.md               ← What's new
├── CONTRIBUTING.md                ← How to contribute
├── DEPLOYMENT.md                  ← Production deployment
├── RELEASE_PROCESS.md             ← Release workflow
├── DOCUMENTATION_INDEX.md         ← This file
├── CLEANUP_SUMMARY.txt            ← Cleanup report
│
├── indextts/                      ← Source code
│   ├── infer_v2.py               ← Main inference
│   ├── infer.py                  ← Legacy inference
│   ├── cli.py                    ← Command-line interface
│   ├── gpt/                      ← Language model
│   ├── BigVGAN/                  ← Vocoder
│   ├── s2mel/                    ← Acoustic features
│   ├── vqvae/                    ← Encoder
│   └── utils/                    ← Utilities
│
├── webui.py                       ← Web interface
├── train.py                       ← Training script
├── checkpoints/                   ← Models & config
├── examples/                      ← Reference audio
├── tools/                         ← Utilities
└── tests/                         ← Test data
```

## Common Tasks

### Installation
→ [QUICK_START.md](QUICK_START.md) or [INSTALL.md](INSTALL.md)

### Basic Voice Cloning
→ [QUICK_START.md](QUICK_START.md#using-the-web-ui)

### Advanced Python API
→ [README.md](README.md#-using-indextts2-in-python)

### Production Deployment
→ [DEPLOYMENT.md](DEPLOYMENT.md)

### Contributing Code
→ [CONTRIBUTING.md](CONTRIBUTING.md)

### Creating a Release
→ [RELEASE_PROCESS.md](RELEASE_PROCESS.md)

### Troubleshooting
→ [INSTALL.md#troubleshooting](INSTALL.md#troubleshooting) or [QUICK_START.md#troubleshooting](QUICK_START.md#troubleshooting)

### Understanding Architecture
→ [README.md#-neural-network-architecture](README.md#--neural-network-architecture)

### Citation & References
→ [README.md#-citation](README.md#-citation) or [RELEASE_NOTES.md](RELEASE_NOTES.md#license)

## Feature Matrix

| Feature | Documentation | Difficulty |
|---------|---------------|-----------|
| Installation | [INSTALL.md](INSTALL.md) | Easy |
| Web UI | [QUICK_START.md](QUICK_START.md) | Easy |
| Voice Cloning | [README.md](README.md) | Easy |
| Emotion Control | [README.md](README.md) | Medium |
| Pinyin Control | [README.md](README.md) | Medium |
| Python API | [README.md](README.md) | Medium |
| Batch Processing | [DEPLOYMENT.md](DEPLOYMENT.md) | Hard |
| Docker Deployment | [DEPLOYMENT.md](DEPLOYMENT.md) | Medium |
| Cloud Deployment | [DEPLOYMENT.md](DEPLOYMENT.md) | Hard |
| Performance Optimization | [DEPLOYMENT.md](DEPLOYMENT.md) | Hard |

## Quick Reference

### Commands

```bash
# Installation
pip install -U uv
uv sync --all-extras

# Download models
uv tool install "huggingface-hub[cli,hf_xet]"
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints

# Run WebUI
uv run webui.py

# Check GPU
uv run tools/gpu_check.py

# Training
uv run train.py

# Create release
git tag -a v2.0.0 -m "Release"
git push origin v2.0.0
```

### File Formats

| Format | Description | Example |
|--------|-------------|---------|
| `.wav` | Audio files | Input/output audio |
| `.yaml` | Configuration | `checkpoints/config.yaml` |
| `.json` | Metadata | Model configs |
| `.py` | Python code | Source code |
| `.md` | Documentation | This file |

### Environment Variables

```bash
# Model paths
export INDEXTTS_MODEL_DIR=/path/to/models
export INDEXTTS_CONFIG_PATH=/path/to/config.yaml

# Performance
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Features
export GRADIO_ANALYTICS_ENABLED=False
```

## Resources

- **GitHub**: [https://github.com/index-tts/index-tts](https://github.com/index-tts/index-tts)
- **Paper**: [https://arxiv.org/abs/2506.21619](https://arxiv.org/abs/2506.21619)
- **Discord**: [https://discord.gg/uT32E7KDmy](https://discord.gg/uT32E7KDmy)
- **Model Hub**: [https://huggingface.co/IndexTeam/IndexTTS-2](https://huggingface.co/IndexTeam/IndexTTS-2)
- **Demo**: [https://index-tts.github.io/index-tts2.github.io/](https://index-tts.github.io/index-tts2.github.io/)

## Support

| Channel | Use For |
|---------|---------|
| **Issues** | Bug reports, feature requests |
| **Discussions** | Questions, suggestions |
| **Discord** | Community, quick help |
| **Email** | Commercial inquiries |

## Document Status

| Document | Lines | Last Updated | Status |
|----------|-------|--------------|--------|
| README.md | 511 | 2025-02-12 | ✓ Current |
| QUICK_START.md | 257 | 2025-11-17 | ✓ New |
| INSTALL.md | 130 | 2025-11-17 | ✓ New |
| RELEASE_NOTES.md | 177 | 2025-11-17 | ✓ New |
| CONTRIBUTING.md | 193 | 2025-11-17 | ✓ New |
| DEPLOYMENT.md | 347 | 2025-11-17 | ✓ New |
| RELEASE_PROCESS.md | 198 | 2025-11-17 | ✓ New |
| CLEANUP_SUMMARY.txt | 320 | 2025-11-17 | ✓ New |

---

**Last Updated**: November 17, 2025  
**Maintained By**: IndexTTS Team  
**License**: Bilibili IndexTTS License
