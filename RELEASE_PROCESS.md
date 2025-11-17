# IndexTTS2 Release Process

This document outlines the process for creating and publishing releases on GitHub.

## Automated Release Workflow

The repository includes a GitHub Actions workflow that automates the release creation process.

### Files Involved

- **Workflow File**: `.github/workflows/release.yml`
- **Documentation**: `RELEASE_NOTES.md`, `INSTALL.md`, `CHANGELOG.md` (if applicable)

## How to Create a Release

### Method 1: Using Git Tags (Automatic)

When you push a tag matching the pattern `v*`, the workflow automatically triggers:

```bash
# Make your changes and commit them
git add .
git commit -m "Release preparation changes"

# Create a tag
git tag -a v2.0.1 -m "IndexTTS2 Release v2.0.1"

# Push tag to trigger workflow
git push origin v2.0.1

# Monitor the workflow
# GitHub will automatically:
# 1. Create a GitHub Release
# 2. Build source distributions
# 3. Upload to PyPI (if configured)
```

### Method 2: Manual Trigger (Workflow Dispatch)

Trigger the workflow manually via GitHub Actions:

1. Go to **Actions** tab on GitHub
2. Select **"Create Release"** workflow
3. Click **"Run workflow"**
4. Enter release tag (e.g., `v2.0.1`)
5. Click **"Run workflow"**

### Method 3: Manual Release

Create a release directly on GitHub:

1. Go to **Releases** > **Draft a new release**
2. **Tag version**: `v2.0.1`
3. **Target**: `main` branch
4. **Title**: `IndexTTS2 Release v2.0.1`
5. **Description**: Use the template below
6. Click **"Publish release"**

## Release Notes Template

Use this template for the release description:

```markdown
# IndexTTS2 v2.0.1

## Installation

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

Quick start:
\`\`\`bash
git clone https://github.com/index-tts/index-tts.git
cd index-tts
git lfs pull
pip install -U uv
uv sync --all-extras
\`\`\`

## What's New

- **Feature 1**: Description
- **Feature 2**: Description
- **Bug Fix**: Description

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for complete details.

## Resources

- **Documentation**: [README.md](README.md)
- **Installation Guide**: [INSTALL.md](INSTALL.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Paper**: [https://arxiv.org/abs/2506.21619](https://arxiv.org/abs/2506.21619)
- **Model Hub**: [IndexTeam/IndexTTS-2](https://huggingface.co/IndexTeam/IndexTTS-2)

## Requirements

- Python 3.10+
- Git LFS
- NVIDIA CUDA 12.8+ (for GPU)
- 8GB+ RAM, 10GB+ disk space

## Support

- **Discord**: [https://discord.gg/uT32E7KDmy](https://discord.gg/uT32E7KDmy)
- **GitHub Issues**: [Report bugs](https://github.com/index-tts/index-tts/issues)
- **Email**: indexspeech@bilibili.com
```

## Pre-Release Checklist

Before creating a release:

- [ ] Update `RELEASE_NOTES.md` with new features and fixes
- [ ] Update `INSTALL.md` if installation instructions changed
- [ ] Update `pyproject.toml` version number (optional)
- [ ] Run tests locally: `uv run tools/gpu_check.py`
- [ ] Test WebUI: `uv run webui.py`
- [ ] Review all changes in `git log`
- [ ] Ensure all PRs are merged and CI passes

## Version Numbering

Follow Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes (e.g., v1.0.0 → v2.0.0)
- **MINOR**: New features, backward compatible (e.g., v2.0.0 → v2.1.0)
- **PATCH**: Bug fixes (e.g., v2.0.0 → v2.0.1)

Examples:
- `v2.0.0` - Major release with new features
- `v2.0.1` - Patch release with bug fixes
- `v2.1.0` - Minor release with new features

## Release Artifacts

The GitHub workflow generates:

1. **Source Distribution** (`*.tar.gz`)
   - Contains full source code
   - Includes all necessary files
   - Excludes venv and build artifacts

2. **Wheel Distribution** (`*.whl`)
   - Binary package for pip installation
   - Platform-specific

## Installation After Release

Users can install released versions via:

```bash
# From source
git clone https://github.com/index-tts/index-tts.git
cd index-tts
git checkout v2.0.1
git lfs pull

# From PyPI (when available)
pip install indextts
```

## Troubleshooting

### Workflow Fails

1. Check GitHub Actions logs for errors
2. Verify tag format: `v*` (e.g., `v2.0.1`)
3. Ensure `.github/workflows/release.yml` is correct
4. Verify repository has write permissions

### Missing Release Notes

- Always update `RELEASE_NOTES.md` before creating a release
- Ensure the file is in the root directory
- Check for formatting errors in markdown

### Build Artifacts Missing

- Verify `pyproject.toml` is present and valid
- Check that all dependencies are listed
- Ensure no syntax errors in build configuration

## Maintenance

- Keep release notes up to date
- Regularly update installation instructions
- Monitor for security updates in dependencies
- Test releases on multiple platforms

## Support

For questions about the release process:

- **GitHub Issues**: [https://github.com/index-tts/index-tts/issues](https://github.com/index-tts/index-tts/issues)
- **Discord**: [https://discord.gg/uT32E7KDmy](https://discord.gg/uT32E7KDmy)
- **Email**: indexspeech@bilibili.com
