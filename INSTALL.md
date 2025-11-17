# Installation Guide for IndexTTS2

This guide will help you set up IndexTTS2 on your system.

## Prerequisites

- **Git**: Download from [https://git-scm.com/downloads](https://git-scm.com/downloads)
- **Git LFS**: Download from [https://git-lfs.com/](https://git-lfs.com/)
- **Python 3.10+**: Download from [https://www.python.org/](https://www.python.org/)
- **NVIDIA CUDA Toolkit 12.8+** (for GPU acceleration): Download from [https://developer.nvidia.com/cuda-toolkit](https://developer.nvidia.com/cuda-toolkit)

## Step 1: Install Git LFS

After installing Git LFS, enable it for your user account:

```bash
git lfs install
```

## Step 2: Clone the Repository

```bash
git clone https://github.com/index-tts/index-tts.git
cd index-tts
git lfs pull  # Download large model files
```

## Step 3: Install the `uv` Package Manager

`uv` is the recommended package manager for this project. Install it via:

```bash
pip install -U uv
```

Or see [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) for other options.

## Step 4: Install Dependencies

`uv` will automatically create a virtual environment and install all dependencies:

```bash
uv sync --all-extras
```

### Optional: Use a Mirror (for faster downloads in certain regions)

If you're in China or experience slow downloads, use a local mirror:

```bash
uv sync --all-extras --default-index "https://mirrors.aliyun.com/pypi/simple"
```

Or:

```bash
uv sync --all-extras --default-index "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
```

### Optional: Custom Installation

If you encounter issues with optional features (e.g., DeepSpeed on Windows), you can skip them:

```bash
uv sync  # Skip --all-extras for minimal installation
uv sync --extra webui  # Only install WebUI support
```

## Step 5: Download Model Checkpoints

You need to download the pre-trained model weights. Choose one method:

### Method A: Using Hugging Face (Recommended)

```bash
uv tool install "huggingface-hub[cli,hf_xet]"
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
```

### Method B: Using ModelScope

```bash
uv tool install "modelscope"
modelscope download --model IndexTeam/IndexTTS-2 --local_dir checkpoints
```

## Step 6: Verify GPU Support (Optional)

To check if your GPU is properly detected:

```bash
uv run tools/gpu_check.py
```

## Next Steps

- **Web UI Demo**: Run `uv run webui.py` and open http://127.0.0.1:7860
- **Python API**: See [README.md](README.md) for usage examples
- **Training**: See documentation for model training

## Troubleshooting

### CUDA Not Found
Ensure you have NVIDIA CUDA Toolkit 12.8+ installed. After installation, restart your terminal.

### ModuleNotFoundError or Missing Dependencies
Always run commands with `uv run` to ensure the correct environment is used:
```bash
uv run webui.py
```

### GPU Out of Memory
Enable FP16 inference for lower VRAM usage:
```bash
uv run webui.py --fp16
```

### Port 7860 Already in Use
Specify a different port:
```bash
uv run webui.py --listen 127.0.0.1 --server-port 7861
```

## Getting Help

- **GitHub Issues**: [https://github.com/index-tts/index-tts/issues](https://github.com/index-tts/index-tts/issues)
- **Discord Community**: [https://discord.gg/uT32E7KDmy](https://discord.gg/uT32E7KDmy)
- **QQ Groups**: 553460296 (No.1) or 663272642 (No.4)
- **Email**: indexspeech@bilibili.com
