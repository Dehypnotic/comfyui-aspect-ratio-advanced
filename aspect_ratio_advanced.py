import torch
import torch.nn.functional as F
import math

class AspectRatioAdvanced:
    """
    Advanced Aspect Ratio Node v0.2.0 - Simplified UX with combined scaling field
    No more confusion between aspect_ratio and scaling_mode!
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        # Kombinert scaling field - logisk rekkefølge: fleksible moduser først, så presets
        scaling_options = [
            "custom dimensions",
            "target megapixels", 
            "min side",
            "max side",
            "1:1 square", 
            "4:3 standard",
            "3:2 classic",
            "16:9 widescreen",
            "21:9 ultrawide",
            "3:4 portrait",
            "2:3 photo",
            "9:16 mobile",
            "9:21 vertical",
            "4:5 social",
            "5:7 print"
        ]
        
        return {
            "required": {
                "custom_width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 8}),
                "custom_height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 8}),
                "scaling": (scaling_options,),
                "use_image_ratio": (["No", "Yes"], {"default": "Yes", "tooltip": "Use connected image's aspect ratio when available. Set to No to use scaling preset even with image connected."}),
                "target_megapixels": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 16.0, "step": 0.1}),
                "min_side": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 8}),
                "max_side": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 8}),
                "flip_dimensions": (["No", "Yes"],),
                "batch_count": ("INT", {"default": 1, "min": 1, "max": 64})
            },
            "optional": {
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("INT", "INT", "INT", "LATENT", "IMAGE", "STRING")
    RETURN_NAMES = ("width", "height", "batch_count", "empty_latent", "scaled_image", "resolution_info")
    FUNCTION = "calculate_resolution"
    CATEGORY = "CustomNodes/Resolution"
    
    def calculate_resolution(self, custom_width, custom_height, scaling, use_image_ratio, target_megapixels, min_side, max_side, flip_dimensions, batch_count, image=None):
        
        ratio_map = {
            "1:1 square": (1, 1),
            "4:3 standard": (4, 3), 
            "3:2 classic": (3, 2),
            "16:9 widescreen": (16, 9),
            "21:9 ultrawide": (21, 9),
            "3:4 portrait": (3, 4),
            "2:3 photo": (2, 3),
            "9:16 mobile": (9, 16),
            "9:21 vertical": (9, 21),
            "4:5 social": (4, 5),
            "5:7 print": (5, 7)
        }
        
        def make_divisible_by_8(value):
            return max(64, (value // 8) * 8)
        
        scaled_image = None
        
        # 🖼️ Image ratio har prioritet når toggle er på
        if image is not None and use_image_ratio == "Yes":
            img_height = image.shape[1]
            img_width = image.shape[2]
            image_ratio = img_width / img_height
            
            # Bruk scaling mode på image ratio
            if scaling == "target megapixels":
                total_pixels = target_megapixels * 1_000_000
                k = math.sqrt(total_pixels / (img_width * img_height))
                width = int(img_width * k)
                height = int(img_height * k)
            elif scaling == "min side":
                if img_width <= img_height:
                    width = min_side
                    height = int(min_side / image_ratio)
                else:
                    height = min_side
                    width = int(min_side * image_ratio)
            elif scaling == "max side":
                if img_width >= img_height:
                    width = max_side
                    height = int(max_side / image_ratio)
                else:
                    height = max_side
                    width = int(max_side * image_ratio)
            else:
                # Andre scaling modes når image er tilkoblet - bruk image ratio
                width = img_width
                height = img_height
            
            width = make_divisible_by_8(width)
            height = make_divisible_by_8(height)
            
            # Skaler image
            image_permuted = image.permute(0, 3, 1, 2)
            scaled_image_permuted = F.interpolate(
                image_permuted, 
                size=(height, width), 
                mode='bilinear', 
                align_corners=False
            )
            scaled_image = scaled_image_permuted.permute(0, 2, 3, 1)
        
        # 📐 Bruk scaling preset (enten uten image, eller med use_image_ratio = No)
        elif scaling == "custom dimensions":
            width = make_divisible_by_8(custom_width)
            height = make_divisible_by_8(custom_height)
            
            # Skaler image til custom dimensjoner hvis tilgjengelig
            if image is not None:
                image_permuted = image.permute(0, 3, 1, 2)
                scaled_image_permuted = F.interpolate(
                    image_permuted, 
                    size=(height, width), 
                    mode='bilinear', 
                    align_corners=False
                )
                scaled_image = scaled_image_permuted.permute(0, 2, 3, 1)
        
        elif scaling in ratio_map:
            ratio_w, ratio_h = ratio_map[scaling]
            
            # Kan ikke bruke megapixels/min/max scaling på preset ratios direkt
            # Bruk ratio med standard 1024 base for nå
            if scaling in ["target megapixels", "min side", "max side"]:
                # Dette bør ikke skje med den nye strukturen, men fallback
                width = 1024
                height = 1024
            else:
                # Beregn dimensjoner basert på preset ratio
                base_pixels = target_megapixels * 1_000_000
                k = math.sqrt(base_pixels / (ratio_w * ratio_h))
                width = int(ratio_w * k)
                height = int(ratio_h * k)
            
            width = make_divisible_by_8(width)
            height = make_divisible_by_8(height)
            
            # Skaler image til preset ratio hvis tilgjengelig
            if image is not None:
                image_permuted = image.permute(0, 3, 1, 2)
                scaled_image_permuted = F.interpolate(
                    image_permuted, 
                    size=(height, width), 
                    mode='bilinear', 
                    align_corners=False
                )
                scaled_image = scaled_image_permuted.permute(0, 2, 3, 1)
        
        else:
            # Fallback
            width = make_divisible_by_8(custom_width)
            height = make_divisible_by_8(custom_height)
        
        # 🔄 Flip hvis ønsket
        if flip_dimensions == "Yes":
            width, height = height, width
            if scaled_image is not None:
                scaled_image_permuted = scaled_image.permute(0, 3, 1, 2)
                scaled_image_permuted = F.interpolate(
                    scaled_image_permuted, 
                    size=(height, width), 
                    mode='bilinear', 
                    align_corners=False
                )
                scaled_image = scaled_image_permuted.permute(0, 2, 3, 1)
        
        # Opprett latent
        latent_width = width // 8
        latent_height = height // 8
        latent = torch.zeros([batch_count, 4, latent_height, latent_width])
        
        # Info
        actual_mp = (width * height) / 1_000_000
        actual_min = min(width, height)
        actual_max = max(width, height)
        
        if image is not None and use_image_ratio == "Yes":
            source_info = "from image"
        elif scaling == "custom dimensions":
            source_info = "custom dimensions"
        else:
            source_info = f"{scaling}"
        
        resolution_info = f"{width}x{height} ({actual_mp:.2f}MP, {width/height:.2f}:1, {source_info})"
        
        return (width, height, batch_count, {"samples": latent}, scaled_image, resolution_info)

# Node mapping
NODE_CLASS_MAPPINGS = {
    "AspectRatioAdvanced": AspectRatioAdvanced
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectRatioAdvanced": "🎯 Aspect Ratio Advanced"
}
