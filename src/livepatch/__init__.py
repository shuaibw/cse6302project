"""Live patch & before/after capture package.

High-level usage:

from livepatch.api import capture_with_patches, run_capture_with_patches

See cli: python -m livepatch --url ...
"""
from .api import capture_with_patches, run_capture_with_patches, DEFAULT_VIEWPORTS
__all__ = [
    'capture_with_patches',
    'run_capture_with_patches',
    'DEFAULT_VIEWPORTS'
]
