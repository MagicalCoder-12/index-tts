"""
IndexTTS - Voice Cloning and Text-to-Speech powered by Coqui XTTS

This package provides a simplified interface for voice cloning and text-to-speech
synthesis with Telugu language support, powered by Coqui XTTS.

Migration Notice:
-----------------
Version 3.0.0 represents a major architectural change from IndexTTS2 to Coqui XTTS.
The old IndexTTS2 inference code has been removed. For legacy support, please use
the backup-indextts2 branch or the v2.0.0-indextts2 tag.

Features:
---------
- Multi-language text-to-speech synthesis
- Zero-shot voice cloning
- Telugu language support
- High-quality audio generation
- Web UI for easy interaction

Usage:
------
The new implementation will use Coqui XTTS. Stay tuned for updated API documentation.

For the previous IndexTTS2 implementation, refer to:
- Branch: backup-indextts2
- Tag: v2.0.0-indextts2
"""

__version__ = "3.0.0"
__author__ = "Voice Cloner Project"

# Utilities that are preserved from IndexTTS2
# These will be evaluated for compatibility with Coqui XTTS
from . import utils

__all__ = [
    "__version__",
    "__author__",
    "utils",
]
