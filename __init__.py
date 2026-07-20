from .nodes.aspect_ratio_advanced_v2 import AspectRatioAdvancedV2

NODE_CLASS_MAPPINGS = {
    # Gamle workflows laster fortsatt koden, men brukeren blir varslet
    "AspectRatioAdvanced": AspectRatioAdvancedV2,      
    
    # Det nye offisielle flaggskipet ditt
    "dehypnotic_AspectRatio": AspectRatioAdvancedV2  
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # Tydelig beskjed i grensesnittet om å bytte ut noden
    "AspectRatioAdvanced": "AspectRatioAdvanced - DEPRECATED - REPLACE",
    "dehypnotic_AspectRatio": "🧘AspectRatio (Dehypnotic)"
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

