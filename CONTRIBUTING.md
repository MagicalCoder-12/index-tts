# Contributing to IndexTTS2

Thank you for your interest in contributing to IndexTTS2! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful to all contributors and maintain professional communication.

## How to Contribute

### Reporting Issues

- **Check existing issues** before creating a new one
- Include a **clear description** of the problem
- Provide **reproduction steps** if applicable
- Share your **system information** (OS, Python version, CUDA version)
- Include **error messages** and logs

### Submitting Pull Requests

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and commit with clear messages:
   ```bash
   git commit -m "Add brief description of changes"
   ```
4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create a Pull Request** with:
   - Clear title and description
   - Reference to any related issues
   - Explanation of changes and their purpose
   - Testing notes if applicable

### Development Setup

```bash
git clone https://github.com/index-tts/index-tts.git
cd index-tts
git lfs pull
pip install -U uv
uv sync --all-extras
```

### Running Tests

```bash
# Run GPU checks
uv run tools/gpu_check.py

# Run inference test
uv run indextts/infer_v2.py
```

## Code Style

- **Python**: Follow PEP 8 standards
- **Naming**: Use descriptive variable and function names
- **Comments**: Add comments for complex logic
- **Type hints**: Use type annotations where applicable
- **Docstrings**: Add docstrings to functions and classes

### Example Function Style

```python
def process_audio(audio_path: str, sample_rate: int = 22050) -> np.ndarray:
    """
    Process audio file from the given path.
    
    Args:
        audio_path: Path to the audio file
        sample_rate: Target sample rate in Hz
        
    Returns:
        Processed audio waveform as numpy array
    """
    # Implementation here
    pass
```

## Project Structure

```
index-tts/
├── indextts/           # Core source code
│   ├── BigVGAN/        # Vocoder implementation
│   ├── gpt/            # Language model
│   ├── s2mel/          # Acoustic features
│   ├── vqvae/          # Discrete encoder
│   ├── utils/          # Utilities
│   ├── infer.py        # IndexTTS v1 inference
│   └── infer_v2.py     # IndexTTS2 inference
├── checkpoints/        # Model configurations
├── tools/              # Utility scripts
├── tests/              # Test files
├── webui.py            # Web interface
├── train.py            # Training script
└── pyproject.toml      # Project configuration
```

## Testing Changes

Before submitting a PR:

1. **Test locally**:
   ```bash
   uv run webui.py  # Test web UI
   ```

2. **Verify inference**:
   ```python
   from indextts.infer_v2 import IndexTTS2
   tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
   # Test your changes
   ```

3. **Check for regressions**: Ensure existing functionality still works

## Documentation

- Update `README.md` for major changes
- Add docstrings to new functions
- Update `RELEASE_NOTES.md` when making notable changes
- Include examples for new features

## Commit Messages

Write clear, descriptive commit messages:

```
[Category] Brief description

Detailed explanation of changes (if needed)

- Specific change 1
- Specific change 2
```

Categories:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation update
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Test additions/updates
- `ci`: CI/CD updates

## Areas for Contribution

### High-Priority

- **Bug fixes**: Help us improve stability
- **Documentation**: Improve clarity and examples
- **Performance optimization**: Make inference faster
- **Hardware support**: Test on different GPUs/platforms

### Medium-Priority

- **New features**: Emotion control enhancements
- **Model improvements**: Better voice cloning
- **WebUI enhancements**: Improved user experience
- **Multilingual support**: Add new languages

### Lower-Priority

- **Code cleanup**: Refactoring for readability
- **Type hints**: Adding type annotations
- **Test coverage**: Adding unit tests

## License

By contributing to IndexTTS2, you agree that your contributions will be licensed under the Bilibili IndexTTS License.

## Questions?

- **GitHub Discussions**: Post questions in issues
- **Discord**: [https://discord.gg/uT32E7KDmy](https://discord.gg/uT32E7KDmy)
- **Email**: indexspeech@bilibili.com

## Recognition

Contributors will be:
- Listed in the project README
- Credited in release notes
- Recognized in the community

Thank you for helping make IndexTTS2 better! 🎉
