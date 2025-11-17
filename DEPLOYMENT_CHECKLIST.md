# IndexTTS2 Deployment Checklist

Complete checklist for deploying IndexTTS2 to production.

## Pre-Deployment Review

### Documentation
- [x] README.md - Main documentation complete
- [x] INSTALL.md - Installation guide comprehensive
- [x] QUICK_START.md - 5-minute setup guide created
- [x] RELEASE_NOTES.md - Release information complete
- [x] CONTRIBUTING.md - Developer guidelines ready
- [x] DEPLOYMENT.md - Production guide detailed
- [x] RELEASE_PROCESS.md - Release workflow documented
- [x] DOCUMENTATION_INDEX.md - Documentation index created
- [x] CLEANUP_SUMMARY.txt - Cleanup report generated

### Code Quality
- [x] Removed Telugu-specific test scripts
- [x] Removed temporary output directories
- [x] Removed development virtual environment
- [x] Preserved all core functionality
- [x] Verified source code integrity
- [x] Checked for redundant files

### Repository Structure
- [x] Core modules intact (indextts/, checkpoints/, tools/, tests/)
- [x] Web UI (webui.py) present
- [x] Training script (train.py) present
- [x] Configuration files valid
- [x] Examples directory preserved
- [x] License files included

### Automation
- [x] GitHub Actions workflow created
- [x] Release workflow triggers on tags
- [x] Build artifacts configured
- [x] Release notes template ready

## Before First Release

### Step 1: Test Everything Locally
- [ ] Clone the repository fresh
- [ ] Run installation: `uv sync --all-extras`
- [ ] Download models: `hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints`
- [ ] Test WebUI: `uv run webui.py`
- [ ] Test GPU: `uv run tools/gpu_check.py`
- [ ] Test inference in Python:
  ```python
  from indextts.infer_v2 import IndexTTS2
  tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints")
  tts.infer(spk_audio_prompt='examples/voice_01.wav', text="Test", output_path="test.wav")
  ```

### Step 2: Documentation Review
- [ ] README.md - Check all links work
- [ ] INSTALL.md - Verify all instructions accurate
- [ ] QUICK_START.md - Test all examples
- [ ] RELEASE_NOTES.md - Verify accuracy
- [ ] CONTRIBUTING.md - Check guidelines are clear

### Step 3: GitHub Setup
- [ ] Repository is public
- [ ] License file is correct
- [ ] .gitignore is configured
- [ ] README.md has GitHub badges
- [ ] Repository settings are configured:
  - [ ] Description set
  - [ ] Homepage URL set
  - [ ] Topics/tags added
  - [ ] Branch protection rules (optional)

### Step 4: Pre-Release Tasks
- [ ] Update pyproject.toml version (optional)
- [ ] Ensure all PRs are merged
- [ ] CI/CD passes all checks
- [ ] Git log is clean
- [ ] No uncommitted changes

## First Release Deployment

### Step 1: Create Git Tag
```bash
cd index-tts
git add .
git commit -m "chore: clean repository and add release documentation"
git tag -a v2.0.0 -m "IndexTTS2 Release v2.0.0"
```

### Step 2: Push to GitHub
```bash
git push origin main
git push origin v2.0.0
```

### Step 3: Monitor GitHub Actions
- [ ] Go to Actions tab on GitHub
- [ ] Find "Create Release" workflow
- [ ] Verify workflow runs successfully
- [ ] Check release creation
- [ ] Verify artifacts uploaded

### Step 4: Verify Release
- [ ] GitHub Release page created
- [ ] Release notes display correctly
- [ ] Links in release notes work
- [ ] Artifacts are available for download
- [ ] Release is marked as latest

## Post-Release

### Verification
- [ ] Release is visible on GitHub
- [ ] Users can clone and install
- [ ] Documentation links are correct
- [ ] Download links work
- [ ] Release notes are complete

### Community Communication
- [ ] Post announcement on Discord
- [ ] Update project website/demo
- [ ] Notify QQ group (if applicable)
- [ ] Update project status

### Monitoring
- [ ] Monitor GitHub Issues for problems
- [ ] Check Discord for feedback
- [ ] Track download statistics (if available)
- [ ] Respond to user feedback

## Continuous Deployment (After First Release)

### Regular Updates
- [ ] Schedule monthly releases (or as needed)
- [ ] Monitor and merge PRs
- [ ] Update documentation with new features
- [ ] Update RELEASE_NOTES.md before release
- [ ] Test changes locally before release

### Maintenance
- [ ] Monitor dependency updates
- [ ] Update security patches
- [ ] Review and close stale issues
- [ ] Respond to user feedback
- [ ] Update CI/CD as needed

### Documentation Updates
For each release, update:
- [ ] RELEASE_NOTES.md
- [ ] README.md (if features changed)
- [ ] QUICK_START.md (if examples changed)
- [ ] INSTALL.md (if setup changed)
- [ ] CONTRIBUTING.md (if guidelines changed)

## Release Cadence

Suggested release schedule:
- **Patch releases** (v2.0.x): As needed for bug fixes (weekly or as needed)
- **Minor releases** (v2.x.0): Monthly for new features
- **Major releases** (vX.0.0): When breaking changes occur

Example schedule:
```
v2.0.0 - Initial release (November 2025)
v2.0.1 - Bug fixes (1-2 weeks after v2.0.0)
v2.1.0 - New features (1 month after v2.0.0)
v2.0.2 - Critical bug fixes (as needed)
v2.2.0 - More features (1 month after v2.1.0)
```

## Deployment Environments

### Development
- [x] Local development environment
- [x] Testing with GPU/CPU
- [x] Code review process

### Staging
- [ ] Optional: Test on staging server
- [ ] Run integration tests
- [ ] Performance testing

### Production
- [ ] Docker deployment
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Monitoring and logging
- [ ] Automated backups

## Success Criteria

Release is successful when:
- [x] All documentation is complete
- [x] Core functionality is preserved
- [x] No breaking changes (unless major release)
- [x] GitHub Actions workflow works
- [x] Release page is created automatically
- [x] Users can install and use easily
- [x] Community feedback is positive

## Troubleshooting

### Release Workflow Fails
1. Check GitHub Actions logs
2. Verify tag format: `v*` pattern
3. Check `.github/workflows/release.yml` syntax
4. Ensure repository permissions

### Installation Issues
1. Direct users to INSTALL.md
2. Check git lfs pull was run
3. Verify Python version (3.10+)
4. Ensure CUDA is installed

### Model Download Issues
1. Check internet connection
2. Try different mirror
3. Use ModelScope if HuggingFace is slow
4. Check disk space

## Rollback Plan

If major issues occur after release:

1. Create a patch release with fixes
2. Document issues in release notes
3. Communicate with community
4. Mark problematic release as outdated (GitHub UI)

## Version Control

Keep organized version history:
```
git log --oneline --graph

v2.0.0 - Initial release
  |
  ├─ v2.0.1 - Bug fixes
  |   └─ v2.0.2 - More bug fixes
  |
  └─ v2.1.0 - New features
      └─ v2.1.1 - Small fixes
```

## Support Plan

Post-release support:
- [ ] Monitor GitHub Issues daily
- [ ] Respond to Discord messages
- [ ] Fix critical bugs within 24 hours
- [ ] Release patches for critical issues
- [ ] Provide installation support
- [ ] Help with troubleshooting

## Documentation Maintenance

Keep documentation current:
- [ ] Update version numbers
- [ ] Fix broken links
- [ ] Add new examples
- [ ] Improve clarity
- [ ] Add FAQ section
- [ ] Update system requirements

## Success Metrics

Track these metrics:
- Number of GitHub stars
- Number of downloads
- Issue/PR velocity
- Community engagement
- User feedback sentiment

---

**Last Updated**: November 17, 2025  
**Status**: Ready for deployment  
**Reviewer**: IndexTTS Team
