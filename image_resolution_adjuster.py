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
    
    # 从目标分辨率中提取实际的宽高比和尺寸
    if "(" in aspect_ratio:
        # 如果输入格式是 "9:7 (1152x896)" 这样的格式
        dimensions = aspect_ratio.split("(")[1].strip(")").split("x")
        base_width = int(dimensions[0])
        base_height = int(dimensions[1])
    else:
        # 如果找不到对应的预设值，返回错误
        raise ValueError(f"Unable to parse resolution from: {aspect_ratio}")

    # 计算初始目标尺寸
    target_width = int(base_width * scale_factor)
    target_height = int(base_height * scale_factor)
    
    # 应用最大分辨率约束
    current_max = max(target_width, target_height)
    if current_max > max_width or current_max > max_height:
        scale = min(max_width / current_max, max_height / current_max)
        target_width = int(target_width * scale)
        target_height = int(target_height * scale)
    
    # 应用最小分辨率约束
    current_min = min(target_width, target_height)
    if current_min < min_width or current_min < min_height:
        scale = max(min_width / current_min, min_height / current_min)
        target_width = int(target_width * scale)
        target_height = int(target_height * scale)
    
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
        # 只保留 SDXL 最佳分辨率
        base_resolutions = [
            (1024, 1024),  # 1:1
            (1152, 896),   # 9:7
            (896, 1152),   # 7:9
            (1216, 832),   # 3:2
            (832, 1216),   # 2:3
            (1344, 768),   # 7:4
            (768, 1344),   # 4:7
            (1536, 640),   # 12:5
            (640, 1536),   # 5:12
        ]
        
        # 生成分辨率选项列表
        resolutions = []
        for width, height in base_resolutions:
            aspect_ratio = get_aspect_ratio_string(width, height)
            resolutions.append(f"{aspect_ratio} ({width}x{height})")
        
        return {
            "required": {
                "images": ("IMAGE",),
                "target_resolution": (resolutions,),
                "extend_mode": (["contain", "cover", "fill", "inside", "outside", "top", "bottom", "left", "right", "center"],),
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
                "max_width": ("INT", {"default": 2048, "min": 1, "max": 8192, "step": 1}),
                "max_height": ("INT", {"default": 2048, "min": 1, "max": 8192, "step": 1}),
                "min_width": ("INT", {"default": 640, "min": 1, "max": 8192, "step": 1}),
                "min_height": ("INT", {"default": 640, "min": 1, "max": 8192, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("images", "width", "height")
    FUNCTION = "adjust_resolution"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def adjust_resolution(self, images, target_resolution, extend_mode, scale_factor, max_width, max_height, min_width, min_height):
        output_images = []
        
        # 从目标分辨率字符串中提取宽高比
        aspect_ratio = target_resolution.split(" ")[0]
        
        # 计算目标分辨率
        target_width, target_height, base_width, base_height = calculate_resolution(
            aspect_ratio, scale_factor, max_width, max_height, min_width, min_height
        )
        
        for image in images:
            if extend_mode in ["contain", "cover", "fill", "inside", "outside"]:
                scaled_image, width, height = resize_image(image, target_width, target_height, method=extend_mode)
            elif extend_mode in ["top", "bottom", "left", "right", "center"]:
                scaled_image, width, height = pad_image(image, target_width, target_height, position=extend_mode)
            else:
                raise ValueError(f"Invalid extend_mode: {extend_mode}")
            
            output_images.append(torch.from_numpy(scaled_image).unsqueeze(0))
        
        return (torch.cat(output_images, dim=0), target_width, target_height)
