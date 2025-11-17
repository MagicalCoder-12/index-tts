# Coqui XTTS Upgrade - Dependency and File Cleanup

## Overview

This design document outlines the strategy for removing old IndexTTS2 dependencies and files that will conflict with the Coqui XTTS integration. The cleanup ensures a smooth transition from the custom IndexTTS2 architecture to Coqui XTTS while maintaining project integrity.

## Objectives

- Remove IndexTTS2-specific model components and dependencies
- Clean up conflicting inference modules
- Eliminate unused model checkpoints and configurations
- Preserve essential utilities and infrastructure
- Maintain Telugu language support capabilities
- Ensure clean migration path for existing users

## Scope Analysis

### Current Architecture Components

IndexTTS2 uses a custom three-stage pipeline:

1. **GPT Language Model**: Custom autoregressive sequence-to-sequence generation
   - Located in: `indextts/gpt/`
   - Model files: `gpt.pth`
   - Two versions: `model.py` (v1) and `model_v2.py` (v2)

2. **S2Mel Acoustic Encoder**: DAC-based codec for audio representation
   - Located in: `indextts/s2mel/`
   - Model files: `s2mel.pth`
   - Includes semantic codec, length regulator, and flow matching modules

3. **BigVGAN Vocoder**: NVIDIA BigVGAN implementation
   - Located in: `indextts/BigVGAN/` and `indextts/s2mel/modules/bigvgan/`
   - Model files: `bigvgan_generator.pth`, `bigvgan_discriminator.pth`
   - Includes ECAPA-TDNN speaker encoder

4. **VQVAE Discrete Encoder**: XTTS-derived discrete VAE (commented out in current codebase)
   - Located in: `indextts/vqvae/xtts_dvae.py`
   - Currently unused but kept for reference

### Coqui XTTS Architecture

Coqui XTTS provides an integrated TTS solution with:
- Built-in multilingual support
- Speaker cloning capabilities
- End-to-end inference pipeline
- Pre-trained models and configuration

### Conflict Zones

| Component | IndexTTS2 Location | Conflict Risk | Action |
|-----------|-------------------|---------------|--------|
| Inference modules | `indextts/infer.py`, `indextts/infer_v2.py` | High | Remove |
| GPT models | `indextts/gpt/` | High | Remove |
| S2Mel modules | `indextts/s2mel/` | High | Remove |
| BigVGAN vocoder | `indextts/BigVGAN/` | Medium | Remove custom, keep if Coqui compatible |
| VQVAE | `indextts/vqvae/` | Low | Remove |
| CLI interface | `indextts/cli.py` | High | Rewrite for Coqui XTTS |
| WebUI | `webui.py` | High | Rewrite for Coqui XTTS |
| Config files | `checkpoints/config.yaml` | Medium | Replace with Coqui config |

## Cleanup Strategy

### Phase 1: Dependency Analysis

#### Dependencies to Remove

From `pyproject.toml`, the following IndexTTS2-specific dependencies will be evaluated:

| Dependency | Purpose | Action | Reason |
|------------|---------|--------|--------|
| `descript-audiotools==0.7.2` | DAC codec for S2Mel | Remove | Coqui XTTS uses different codec |
| `keras==2.9.0` | Legacy deep learning (unused) | Remove | Not used by Coqui XTTS |
| `tensorboard==2.9.1` | Training monitoring | Evaluate | Keep if training needed |
| `modelscope==1.27.0` | Chinese model hub | Evaluate | May not be needed |
| `munch==4.0.0` | Config management | Evaluate | Check if used by remaining code |
| `numba==0.58.1` | JIT compilation | Evaluate | Check if used by utils |
| `opencv-python==4.9.0.80` | Image processing | Remove | Not needed for TTS |
| `sentencepiece>=0.2.1` | Tokenization | Evaluate | Coqui XTTS may use different tokenizer |

#### Dependencies to Retain

| Dependency | Purpose | Reason to Keep |
|------------|---------|----------------|
| `torch==2.8.*` | Deep learning framework | Core requirement |
| `torchaudio==2.8.*` | Audio processing | Core requirement |
| `transformers==4.52.1` | Hugging Face models | May be used by Coqui XTTS |
| `librosa==0.10.2.post1` | Audio analysis | General utility |
| `accelerate==1.8.1` | Model acceleration | Performance optimization |
| `safetensors==0.5.2` | Model serialization | Modern standard |
| `gradio==5.45.0` | WebUI framework | UI requirement |

#### New Dependencies to Add

| Dependency | Purpose | Version |
|------------|---------|---------|
| `TTS` | Coqui TTS library | Latest stable |
| Additional dependencies as required by Coqui XTTS |

### Phase 2: Source Code Cleanup

#### Files to Remove

```
Core Model Components:
├── indextts/gpt/
│   ├── conformer/ (entire directory)
│   ├── conformer_encoder.py
│   ├── model.py (v1 inference)
│   ├── model_v2.py (v2 inference)
│   ├── perceiver.py
│   ├── transformers_beam_search.py
│   ├── transformers_generation_utils.py
│   ├── transformers_gpt2.py
│   └── transformers_modeling_utils.py
├── indextts/s2mel/ (entire directory with subdirectories)
│   ├── dac/
│   ├── modules/
│   ├── hf_utils.py
│   ├── optimizers.py
│   └── wav2vecbert_extract.py
├── indextts/vqvae/
│   └── xtts_dvae.py
├── indextts/BigVGAN/ (evaluate - may keep if compatible)
│   └── (entire directory)

Inference and Interface:
├── indextts/infer.py (v1 inference)
├── indextts/infer_v2.py (v2 inference)
├── indextts/cli.py (old CLI)
├── webui.py (old WebUI)
├── train.py (IndexTTS2 training)

Telugu Fine-tuning Scripts (evaluate based on need):
├── finetune_telugu.py
├── prepare_telugu_finetuning.py
├── evaluate_telugu_finetuning.py
├── quickstart_telugu_finetuning.py
├── test_telugu_finetuning_setup.py
├── telugu_tts_mms.py
├── telugu_tts_xtts.py
├── use_telugu_tts.py
```

#### Files to Preserve

```
Essential Utilities:
├── indextts/utils/
│   ├── common.py (general utilities)
│   ├── text_utils.py (text processing)
│   ├── front.py (text normalization)
│   └── webui_utils.py (UI helpers - adapt for new WebUI)

Infrastructure:
├── tools/ (keep all)
│   ├── i18n/ (internationalization)
│   └── gpu_check.py
├── tests/ (keep all test data)
│   └── te/ (Telugu dataset)

Configuration:
├── pyproject.toml (update dependencies)
├── start scripts (.bat, .sh, .ps1) (update for new entry points)
```

#### Files to Modify

| File | Modification Type | Description |
|------|------------------|-------------|
| `indextts/utils/front.py` | Adapt | Update TextNormalizer and TextTokenizer if needed for Coqui XTTS |
| `indextts/utils/webui_utils.py` | Adapt | Update UI utilities for new Gradio interface |
| `indextts/__init__.py` | Rewrite | Update module exports for Coqui XTTS |
| `tools/i18n/locale/*.json` | Update | Revise UI strings for new interface |

### Phase 3: Configuration Cleanup

#### Checkpoint Files to Remove

```
checkpoints/
├── gpt.pth (IndexTTS2 GPT model)
├── s2mel.pth (S2Mel acoustic model)
├── bigvgan_generator.pth (custom BigVGAN)
├── bigvgan_discriminator.pth (discriminator)
├── dvae.pth (if present, VQVAE model)
├── wav2vec2bert_stats.pt (W2V-BERT statistics)
├── feat1.pt (speaker matrix)
├── feat2.pt (emotion matrix)
├── qwen0.6bemo4-merge/ (emotion instruction model)
├── bpe.model (BPE tokenizer)
├── te_bpe.model (Telugu BPE tokenizer)
├── unigram_12000.vocab (vocabulary)
├── config.yaml (IndexTTS2 config)
├── config_telugu_finetuning.yaml (Telugu config)
```

#### New Configuration Structure

Coqui XTTS configuration will replace the existing structure:

```
checkpoints/
├── coqui_xtts/ (new directory for Coqui models)
│   ├── config.json (Coqui XTTS configuration)
│   ├── model.pth (Coqui XTTS model weights)
│   ├── vocab.json (tokenizer vocabulary)
│   └── speakers.json (speaker embeddings if applicable)
```

### Phase 4: Utility Preservation Strategy

#### Text Processing Utilities

Components from `indextts/utils/front.py` that may be reusable:

- **TextNormalizer**: Language-specific text normalization
  - Chinese text normalization (cn2an, jieba)
  - English text normalization (g2p-en)
  - Telugu text support
  - Strategy: Evaluate if Coqui XTTS handles this internally; if not, preserve and adapt

- **TextTokenizer**: BPE and unigram tokenization
  - Strategy: Likely replaced by Coqui tokenizer; archive as reference

#### Audio Processing Utilities

Components from `indextts/utils/`:

- **common.py**: General audio utilities
  - Strategy: Preserve, evaluate each function for relevance
  
- **feature_extractors.py**: Mel spectrogram extraction
  - Strategy: Preserve if Coqui XTTS requires custom preprocessing

#### WebUI Utilities

Components from `indextts/utils/webui_utils.py`:

- Gradio interface helpers
- Audio format conversion
- File management
- Strategy: Adapt for new Coqui XTTS Gradio interface

### Phase 5: Migration Path

#### Backward Compatibility Considerations

For users with existing IndexTTS2 installations:

1. **Deprecation Notice**: Add clear documentation explaining the transition
2. **Legacy Branch**: Create a `legacy-indextts2` branch preserving old codebase
3. **Migration Guide**: Document how to transition inference scripts
4. **Data Migration**: Preserve Telugu dataset and metadata

#### Migration Checklist

```
Pre-Migration:
☐ Backup existing checkpoints directory
☐ Document current working configurations
☐ Archive custom fine-tuned models
☐ Export any custom voice embeddings

Migration:
☐ Remove IndexTTS2 source files per cleanup list
☐ Update pyproject.toml dependencies
☐ Install Coqui TTS library
☐ Download Coqui XTTS models
☐ Rewrite CLI interface for Coqui XTTS
☐ Rebuild WebUI for Coqui XTTS

Post-Migration:
☐ Test basic inference with English text
☐ Test Telugu language support
☐ Verify voice cloning functionality
☐ Update documentation and README
☐ Update start scripts
☐ Run regression tests
```

## Implementation Guidelines

### Step 1: Create Backup

Before any deletion:

- Create a backup branch: `git checkout -b backup-indextts2`
- Tag current state: `git tag -a v2.0.0-indextts2 -m "Last IndexTTS2 version"`
- Document checkpoint locations and sizes

### Step 2: Dependency Update

Update `pyproject.toml`:

```
Remove IndexTTS2-specific dependencies
Add Coqui TTS dependency
Update version to 3.0.0 (major version for breaking changes)
Update description to reflect Coqui XTTS integration
```

Execute: `uv lock --upgrade` to regenerate lock file

### Step 3: Source Code Removal

Execute removal in this order:

1. Remove inference files: `indextts/infer.py`, `indextts/infer_v2.py`
2. Remove model directories: `indextts/gpt/`, `indextts/s2mel/`, `indextts/vqvae/`
3. Evaluate and remove/keep: `indextts/BigVGAN/`
4. Remove training script: `train.py`
5. Remove old CLI and WebUI: `indextts/cli.py`, `webui.py`

### Step 4: Checkpoint Cleanup

Move old checkpoints to archive:

```
Create: checkpoints/archive_indextts2/
Move all IndexTTS2 checkpoints to archive
Keep directory structure for reference
Update .gitignore to exclude archived checkpoints from tracking
```

### Step 5: Utility Adaptation

For preserved utilities:

1. Review each function in `indextts/utils/front.py`
2. Test compatibility with Coqui XTTS tokenization
3. Adapt or remove incompatible functions
4. Update imports in remaining code

### Step 6: Configuration Migration

Create new configuration structure:

- Define Coqui XTTS config schema
- Map Telugu language support settings
- Preserve i18n configurations
- Update startup scripts with new paths

### Step 7: Documentation Update

Update all documentation files:

| File | Update Required |
|------|----------------|
| `README.md` | Complete rewrite for Coqui XTTS |
| `INSTALL.md` | Update installation instructions |
| `QUICK_START.md` | New quick start guide |
| `TELUGU_FINETUNING_GUIDE.md` | Adapt for Coqui XTTS Telugu support |
| `RELEASE_NOTES.md` | Add v3.0.0 breaking changes note |

## Risk Assessment

### High Risk Areas

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Loss of Telugu fine-tuning capability | High | Verify Coqui XTTS Telugu support before removing scripts |
| Breaking existing user workflows | High | Provide comprehensive migration guide and legacy branch |
| Dependency conflicts | Medium | Test on clean environment, document minimum versions |
| Loss of custom emotion control | Medium | Evaluate Coqui XTTS emotion capabilities |

### Rollback Strategy

If migration fails:

1. Restore from `backup-indextts2` branch
2. Reinstall IndexTTS2 dependencies from uv.lock
3. Restore archived checkpoints
4. Document issues for future retry

## Testing Strategy

### Unit Tests

- Text normalization for English, Chinese, Telugu
- Audio preprocessing utilities
- Configuration loading
- File I/O operations

### Integration Tests

- End-to-end inference with English text
- Voice cloning with reference audio
- Telugu language synthesis
- Multi-language support
- WebUI functionality

### Performance Tests

- Inference speed comparison (IndexTTS2 vs Coqui XTTS)
- Memory usage monitoring
- GPU utilization metrics
- Audio quality assessment (MOS scores)

## Success Criteria

Migration is considered successful when:

1. ✓ All IndexTTS2-specific code removed without breaking project structure
2. ✓ Coqui XTTS successfully performs basic inference
3. ✓ Telugu language support functional
4. ✓ Voice cloning operational
5. ✓ WebUI accessible and functional
6. ✓ Documentation updated and accurate
7. ✓ No dependency conflicts
8. ✓ All tests passing

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Backup and preparation | 1 hour | None |
| Dependency analysis and update | 2 hours | Backup complete |
| Source code removal | 3 hours | Dependencies updated |
| Checkpoint cleanup | 1 hour | Source removal complete |
| Utility adaptation | 4 hours | Source removal complete |
| Configuration migration | 2 hours | Utility adaptation complete |
| Testing | 4 hours | All previous phases complete |
| Documentation | 3 hours | Testing complete |
| **Total** | **20 hours** | Sequential execution |

## Open Questions

1. **Telugu Support**: Does Coqui XTTS natively support Telugu, or will custom fine-tuning be required?
2. **BigVGAN Compatibility**: Can the existing BigVGAN implementation be reused with Coqui XTTS?
3. **Emotion Control**: How does Coqui XTTS handle emotion control compared to IndexTTS2?
4. **Model Size**: What are the storage requirements for Coqui XTTS vs IndexTTS2?
5. **Custom Training**: Will users still be able to fine-tune on custom datasets?
6. **License Compatibility**: Are there any licensing conflicts between IndexTTS2 components and Coqui XTTS?

## References

- IndexTTS2 Architecture: Current codebase analysis
- Coqui XTTS Documentation: To be reviewed for migration specifics
- Project Dependencies: `pyproject.toml` and `uv.lock`
- Configuration Schema: `checkpoints/config.yaml`
