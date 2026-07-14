from .nodes.aspect_ratio_advanced import AspectRatioAdvanced
from .nodes.aspect_ratio_advanced_v2 import AspectRatioAdvancedV2

NODE_CLASS_MAPPINGS = {
    "AspectRatioAdvanced": AspectRatioAdvanced,
    "AspectRatioAdvancedV2": AspectRatioAdvancedV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectRatioAdvanced": "AspectRatio V1 (Dehypnotic)",
    "AspectRatioAdvancedV2": "AspectRatio V2 (Dehypnotic)"
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
