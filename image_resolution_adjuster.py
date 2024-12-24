# -*- coding: utf-8 -*-
# Filename: image_resolution_adjuster.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🖼️Image

import torch
import numpy as np
from PIL import Image, ImageOps
from math import gcd

def resize_image(image, target_width, target_height, method='contain'):
    """Resize an image while maintaining aspect ratio.
       method: 'contain' (保持宽高比，缩放图像以完全适应容器),
             'cover' (保持宽高比，缩放图像以覆盖整个容器),
             'fill' (忽略宽高比，缩放图像以完全填充容器),
             'inside' (保持宽高比，缩小或不改变图像使其完全适合容器),
             'outside' (保持宽高比，放大或不改变图像使其完全覆盖容器).
       """
    # 将ComfyUI的图像Tensor转换为PIL图像对象
    img = Image.fromarray(np.clip(255. * image.cpu().numpy(), 0, 255).astype(np.uint8))
    img_width, img_height = img.size

    if method == 'contain':
        # Contain: 缩放图像以适应目标尺寸，保持宽高比，可能出现黑边
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height
        if img_ratio > target_ratio:
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * img_ratio)
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        padded_img = Image.new('RGB', (target_width, target_height), 'black')
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        padded_img.paste(resized_img, (x_offset, y_offset))
        return np.array(padded_img).astype(np.float32)/255.0, new_width, new_height

    elif method == 'cover':
        # Cover: 缩放图像以覆盖目标尺寸，保持宽高比，可能裁剪
         img_ratio = img_width / img_height
         target_ratio = target_width / target_height
         if img_ratio > target_ratio:
            new_height = target_height
            new_width = int(target_height * img_ratio)
         else:
            new_width = target_width
            new_height = int(target_width / img_ratio)
         resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
         x_offset = (new_width - target_width) // 2
         y_offset = (new_height - target_height) // 2
         cropped_img = resized_img.crop((x_offset, y_offset, x_offset + target_width, y_offset + target_height))
         return np.array(cropped_img).astype(np.float32)/255.0 , target_width, target_height

    elif method == 'fill':
        # Fill: 拉伸图像以填充目标尺寸，忽略宽高比，可能变形
        resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return np.array(resized_img).astype(np.float32)/255.0, target_width, target_height

    elif method == 'inside':
       # Inside: 和 contain 相同，保持宽高比，缩小或不改变图像使其完全适合容器
         img_ratio = img_width / img_height
         target_ratio = target_width / target_height
         if img_ratio > target_ratio:
            new_width = target_width
            new_height = int(target_width / img_ratio)
         else:
            new_height = target_height
            new_width = int(target_height * img_ratio)
         resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
         padded_img = Image.new('RGB', (target_width, target_height), 'black')
         x_offset = (target_width - new_width) // 2
         y_offset = (target_height - new_height) // 2
         padded_img.paste(resized_img, (x_offset, y_offset))
         return np.array(padded_img).astype(np.float32)/255.0, target_width, target_height

    elif method == 'outside':
         # Outside: 和 cover 相同，保持宽高比，放大或不改变图像使其完全覆盖容器
         img_ratio = img_width / img_height
         target_ratio = target_width / target_height
         if img_ratio > target_ratio:
             new_height = target_height
             new_width = int(target_height * img_ratio)
         else:
             new_width = target_width
             new_height = int(target_width / img_ratio)
         resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
         x_offset = (new_width - target_width) // 2
         y_offset = (new_height - target_height) // 2
         cropped_img = resized_img.crop((x_offset, y_offset, x_offset + target_width, y_offset + target_height))
         return np.array(cropped_img).astype(np.float32)/255.0 , target_width, target_height

def pad_image(image, target_width, target_height, position='center'):
    """Pad an image to the target dimensions.
       position: 'center' (居中), 'top' (顶部), 'bottom' (底部), 'left' (左边), 'right' (右边)
    """
    img = Image.fromarray(np.clip(255. * image.cpu().numpy(), 0, 255).astype(np.uint8))
    img_width, img_height = img.size

    padded_img = Image.new('RGB', (target_width, target_height), 'black') # 创建黑色背景

    if position == 'center':
        x_offset = (target_width - img_width) // 2
        y_offset = (target_height - img_height) // 2
    elif position == 'top':
         x_offset = (target_width - img_width) // 2
         y_offset = 0
    elif position == 'bottom':
        x_offset = (target_width - img_width) // 2
        y_offset = target_height - img_height
    elif position == 'left':
         x_offset = 0
         y_offset = (target_height - img_height) // 2
    elif position == 'right':
         x_offset = target_width - img_width
         y_offset = (target_height - img_height) // 2
    else:
         raise ValueError(f"Invalid pad position: {position}")

    padded_img.paste(img, (x_offset, y_offset))
    return np.array(padded_img).astype(np.float32) / 255.0, target_width, target_height

def calculate_resolution(aspect_ratio, scale_factor, max_width, max_height, min_width, min_height):
    """Calculate the target resolution based on aspect ratio and scale factor."""
    
    base_resolutions = {
        "1:1": (1024, 1024),
        "1152x896": (1152, 896),
        "896x1152": (896, 1152),
        "1216x832": (1216, 832),
        "832x1216": (832, 1216),
        "1344x768": (1344, 768),
        "768x1344": (768, 1344),
        "1536x640": (1536, 640),
        "640x1536": (640, 1536),
    }
    
    if aspect_ratio in base_resolutions:
       base_width, base_height = base_resolutions[aspect_ratio]
    else: # default to 1:1
        base_width = 1024
        base_height = 1024
    
    target_width = int(base_width * scale_factor)
    target_height = int(base_height * scale_factor)

    
    return target_width, target_height, base_width, base_height

def get_aspect_ratio_string(width, height):
    """Get the aspect ratio string from width and height"""
    common_divisor = gcd(width, height)
    aspect_width = width // common_divisor
    aspect_height = height // common_divisor
    return f"{aspect_width}:{aspect_height}"

class ImageResolutionAdjuster:
    @classmethod
    def INPUT_TYPES(s):
         
        resolutions = ["1:1 (1024x1024)",
                        f"{get_aspect_ratio_string(1152,896)} (1152x896)",
                        f"{get_aspect_ratio_string(896,1152)} (896x1152)",
                        f"{get_aspect_ratio_string(1216,832)} (1216x832)",
                        f"{get_aspect_ratio_string(832,1216)} (832x1216)",
                        f"{get_aspect_ratio_string(1344,768)} (1344x768)",
                        f"{get_aspect_ratio_string(768,1344)} (768x1344)",
                         f"{get_aspect_ratio_string(1536,640)} (1536x640)",
                        f"{get_aspect_ratio_string(640,1536)} (640x1536)"]
        return {
            "required": {
                "images": ("IMAGE",),
                 "target_resolution": (resolutions,),
                "extend_mode": (["contain", "cover", "fill", "inside", "outside", "top", "bottom", "left", "right", "center"],),
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}), # scale_factor 最小值保留小数点后1位
                "max_width": ("INT", {"default": 2048, "min": 1, "max": 8192, "step": 1}),
                "max_height": ("INT", {"default": 2048, "min": 1, "max": 8192, "step": 1}),
                "min_width": ("INT", {"default": 640, "min": 1, "max": 8192, "step": 1}),  # 默认最小宽度
                "min_height": ("INT", {"default": 640, "min": 1, "max": 8192, "step": 1}), # 默认最小高度
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("images", "width", "height")
    FUNCTION = "adjust_resolution"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def adjust_resolution(self, images, target_resolution, extend_mode, scale_factor, max_width, max_height, min_width, min_height):
        
        output_images = []
        output_width = 0
        output_height = 0
        
        # Extract aspect ratio from the target_resolution string
        aspect_ratio = target_resolution.split(" ")[0]
        
        target_width, target_height, base_width, base_height = calculate_resolution(aspect_ratio, scale_factor, max_width, max_height, min_width, min_height)
       
        for image in images:
            img = image

            # Calculate the initial target dimensions based on scale_factor
            
            
            # Apply maximum resolution constraint
            current_max = max(target_width, target_height)
            if current_max > max_width or current_max > max_height:
                scale = min(max_width / current_max, max_height / current_max)
                target_width = int(target_width * scale)
                target_height = int(target_height * scale)
                

            # Apply minimum resolution constraint
            current_min = min(target_width, target_height)
            if current_min < min_width or current_min < min_height:
                 scale = max(min_width / current_min, min_height / current_min)
                 target_width = int(target_width * scale)
                 target_height = int(target_height * scale)

            if extend_mode in ["contain", "cover", "fill", "inside", "outside"]:
                scaled_image, width, height = resize_image(img, target_width, target_height, method=extend_mode)
            elif extend_mode in ["top", "bottom", "left", "right", "center"]:
                 scaled_image, width, height = pad_image(img, target_width, target_height, position=extend_mode)
            else:
                 raise ValueError(f"Invalid extend_mode: {extend_mode}")

            output_images.append(torch.from_numpy(scaled_image).unsqueeze(0))
            output_width = width
            output_height = height

        return (torch.cat(output_images, dim=0), output_width, output_height)
