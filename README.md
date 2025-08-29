# AspectRatioAdvanced - ComfyUI Node

An advanced aspect ratio calculator and image scaler for ComfyUI with flexible scaling modes and intelligent image handling.

<img width="401" height="598" alt="image" src="https://github.com/user-attachments/assets/472ac2a9-4687-464d-87e0-f0a35027c58b" />

## Features

🎯 **Smart Aspect Ratio Calculation**
- 12 preset aspect ratios (square, portrait, landscape, social media formats)
- Custom dimensions support
- Automatic megapixel-based scaling

📐 **Flexible Scaling Modes**
- **Target Megapixels**: Scale to achieve specific resolution
- **Min Side**: Set shortest dimension, maintain aspect ratio  
- **Max Side**: Set longest dimension, maintain aspect ratio

🖼️ **Intelligent Image Processing**
- Optional image input automatically detects aspect ratio
- Real-time image scaling to calculated dimensions
- Toggle control for using image ratio vs presets

⚡ **Advanced Controls**
- Dimension flipping (portrait ↔ landscape)
- Batch processing support
- 8-divisible dimensions (latent space compatible)

## Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```bashcd
   cd ComfyUI/custom_nodes/
   ```
2. Clone this repository:
   ```bashcd
   git clone https://github.com/Dehypnotic/comfyui-aspect-ratio-advanced.git
   ```
3. Restart ComfyUI

## Usage

### Aspect Ratio Calculation

1. Add the **🎯 Aspect Ratio Advanced** node to your workflow
2. Select desired `aspect_ratio` preset
3. Choose `scaling_mode` (target megapixels, min side, or max side)
4. Adjust the corresponding value (megapixels, min_side, or max_side)

### With Image Input

1. Connect an image node to the optional `image` input
2. Set `use_image_ratio` to **Yes** to use the image's aspect ratio
3. Set `use_image_ratio` to **No** to scale image to selected preset ratio

### Custom Dimensions

1. Select `aspect_ratio: custom`
2. Set `custom_width` and `custom_height` to desired values
3. Connected images will be scaled to these exact dimensions

## Node Inputs

| Input | Type | Description |
|-------|------|-------------|
| `custom_width` | INT | Width when using custom aspect ratio |
| `custom_height` | INT | Height when using custom aspect ratio |
| `aspect_ratio` | COMBO | Preset aspect ratios or custom |
| `scaling_mode` | COMBO | How to scale dimensions (megapixels/min/max side) |
| `use_image_ratio` | COMBO | Use connected image's ratio (Yes/No) |
| `target_megapixels` | FLOAT | Target resolution in megapixels |
| `min_side` | INT | Shortest dimension in pixels |
| `max_side` | INT | Longest dimension in pixels |
| `flip_dimensions` | COMBO | Swap width/height (No/Yes) |
| `batch_count` | INT | Number of latent batches to generate |
| `image` | IMAGE | Optional: Image to analyze/scale |

## Node Outputs

| Output | Type | Description |
|--------|------|-------------|
| `width` | INT | Calculated width |
| `height` | INT | Calculated height |  
| `batch_count` | INT | Batch count passthrough |
| `empty_latent` | LATENT | Empty latent tensor |
| `scaled_image` | IMAGE | Scaled input image (if provided) |
| `resolution_info` | STRING | Human-readable resolution summary |

## Supported Aspect Ratios

- **1:1 square** - Perfect square format
- **4:3 standard** - Classic monitor/photo ratio
- **3:2 classic** - 35mm film ratio
- **16:9 widescreen** - Modern video/monitor standard
- **21:9 ultrawide** - Cinematic widescreen
- **3:4 portrait** - Vertical standard format
- **2:3 photo** - Vertical photo ratio
- **9:16 mobile** - Vertical video (TikTok, Instagram Stories)
- **9:21 vertical** - Extended vertical format
- **4:5 social** - Instagram post format
- **5:7 print** - Standard print ratio

## Technical Notes

- All output dimensions are automatically rounded to multiples of 8 (required for latent space)
- Minimum dimension is 64 pixels
- Uses bilinear interpolation for high-quality image scaling
- Compatible with all ComfyUI image processing workflows

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Pull requests welcome! Please:
1. Test your changes thoroughly
2. Update documentation for new features
3. Follow the existing code style

## Changelog

### v0.1.0
- Initial release
- Support for 12 aspect ratio presets
- Three scaling modes (megapixels, min/max side)
- Optional image input with intelligent ratio detection
- Real-time image scaling output

---

**Created for the ComfyUI community** 💙



