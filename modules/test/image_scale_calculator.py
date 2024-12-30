# -*- coding: utf-8 -*-
# Filename: image_scale_calculator.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🖼️Image

import torch
import numpy as np
from PIL import Image

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
        padded_img = Image.new('RGB', (target_width, target_height), 'black') # 创建黑色背景
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        padded_img.paste(resized_img, (x_offset, y_offset))  # 将缩放后的图片贴到中心
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
        cropped_img = resized_img.crop((x_offset, y_offset, x_offset + target_width, y_offset + target_height)) # 裁剪中心部分
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
         return np.array(padded_img).astype(np.float32)/255.0, new_width, new_height

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

def crop_image(image, target_width, target_height, position='center'):
    """Crop an image to the target dimensions.
         position: 'center' (居中),
                  'top-left' (左上角),
                  'top-right' (右上角),
                  'bottom-left' (左下角),
                  'bottom-right' (右下角).
    """
    img = Image.fromarray(np.clip(255. * image.cpu().numpy(), 0, 255).astype(np.uint8))
    img_width, img_height = img.size

    if img_width < target_width or img_height < target_height:
          raise ValueError(f"image size is less than target size, current width={img_width}, height={img_height}, target_width={target_width}, target_height={target_height}")

    if position == 'center':
        x_offset = (img_width - target_width) // 2
        y_offset = (img_height - target_height) // 2
    elif position == 'top-left':
        x_offset = 0
        y_offset = 0
    elif position == 'top-right':
        x_offset = img_width - target_width
        y_offset = 0
    elif position == 'bottom-left':
         x_offset = 0
         y_offset = img_height - target_height
    elif position == 'bottom-right':
         x_offset = img_width - target_width
         y_offset = img_height - target_height
    else:
        raise ValueError(f"Invalid crop position: {position}")

    cropped_img = img.crop((x_offset, y_offset, x_offset + target_width, y_offset + target_height))
    return np.array(cropped_img).astype(np.float32) / 255.0, target_width, target_height


class ImageScaleCalculator:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),  # Input image
                "scale_type": (["ratio", "max_width", "max_height", "force_size", "crop"],),  # Scale type
                "scale_ratio": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 100.0, "step": 0.01}),  # Scale ratio
                "max_width": ("INT", {"default": 512, "min": 1, "max": 8192, "step": 1}),  # Max width
                "max_height": ("INT", {"default": 512, "min": 1, "max": 8192, "step": 1}),  # Max height
                "target_width": ("INT", {"default": 512, "min": 1, "max": 8192, "step": 1}),  # Target width
                "target_height": ("INT", {"default": 512, "min": 1, "max": 8192, "step": 1}),  # Target height
                "crop_position": (["center", "top-left", "top-right", "bottom-left", "bottom-right"],),  # Crop position
                "method": (["contain", "cover", "fill", "inside", "outside"],),  # Resize method
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT")
    RETURN_NAMES = ("image", "width", "height")
    FUNCTION = "scale_image"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"  # Node category

    def scale_image(self, image, scale_type, scale_ratio, max_width, max_height, target_width, target_height, crop_position, method):
        img = image[0]  # Get the image
        img_width = img.shape[1]
        img_height = img.shape[0]

        if scale_type == "ratio":
            target_width = int(img_width * scale_ratio)
            target_height = int(img_height * scale_ratio)

            # 应用最大尺寸限制
            target_width = min(target_width, max_width)
            target_height = min(target_height, max_height)

            scaled_image, width, height = resize_image(img, target_width, target_height, method=method)  # Scale by ratio with limits

        elif scale_type == "max_width":
             target_width = max_width
             target_height = int(img_height * (max_width / img_width))

            # 应用最大尺寸限制
             target_height = min(target_height, max_height)

             scaled_image, width, height = resize_image(img, target_width, target_height, method="contain")  # Scale by max width with limits

        elif scale_type == "max_height":
             target_height = max_height
             target_width = int(img_width * (max_height / img_height))

            # 应用最大尺寸限制
             target_width = min(target_width, max_width)
             scaled_image, width, height = resize_image(img, target_width, target_height, method="contain")  # Scale by max height with limits

        elif scale_type == "force_size":
             scaled_image, width, height = resize_image(img, target_width, target_height, method="fill")  # Force target width and height

        elif scale_type == "crop":
              scaled_image, width, height = crop_image(img, target_width, target_height, crop_position)  # Crop image


        return (torch.from_numpy(scaled_image).unsqueeze(0), width, height)
