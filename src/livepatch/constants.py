from typing import Dict, Any

# Central place to maintain viewport presets
DEFAULT_VIEWPORTS: Dict[str, Dict[str, Any]] = {
    "desktop_hd": {"width": 1920, "height": 1080, "device_scale_factor": 1, "is_mobile": False},
    "mobile_modern": {"width": 390, "height": 844, "device_scale_factor": 3, "is_mobile": True},
}

HASH_ATTR = "data-el-hash"
