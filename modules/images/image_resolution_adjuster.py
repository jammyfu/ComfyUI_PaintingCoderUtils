# -*- coding: utf-8 -*-
# Filename: image_resolution_adjuster.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🖼️Image

import torch
import numpy as np
from PIL import Image
from math import gcd
import torch.nn.functional as F


def resize_image(image, target_width, target_height, method='contain', background_color='#000000'):
    """Resize an image while maintaining aspect ratio.
       method: 'contain', 'cover', 'fill', 'inside', 'outside'
    """
    # 将ComfyUI的图像Tensor转换为PIL图像对象
    img = Image.fromarray(np.clip(255. * image.cpu().numpy(), 0, 255).astype(np.uint8))
    img_width, img_height = img.size

    if method == 'contain':
        # Contain: 缩放图像以适应目标尺寸，保持宽高比，可能出现背景
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height
        if img_ratio > target_ratio:
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * img_ratio)
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 解析背景颜色
        try:
            color = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            color = (0, 0, 0)  # 默认黑色
            
        padded_img = Image.new('RGB', (target_width, target_height), color)
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        padded_img.paste(resized_img, (x_offset, y_offset))
        
        # 生成mask
        mask = calculate_mask((img_width, img_height), (target_width, target_height), method, scale_factor=1.0)
        return np.array(padded_img).astype(np.float32)/255.0, mask, target_width, target_height

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
        
        # 生成mask
        mask = calculate_mask((img_width, img_height), (target_width, target_height), method, scale_factor=1.0)
        return np.array(cropped_img).astype(np.float32)/255.0, mask, target_width, target_height

    elif method == 'fill':
        # Fill: 拉伸图像以填充目标尺寸，忽略宽高比，可能变形
        resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        # 生成mask
        mask = calculate_mask((img_width, img_height), (target_width, target_height), method, scale_factor=1.0)
        return np.array(resized_img).astype(np.float32)/255.0, mask, target_width, target_height

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
        
        # 解析背景颜色
        try:
            color = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            color = (0, 0, 0)  # 默认黑色
            
        padded_img = Image.new('RGB', (target_width, target_height), color)
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        padded_img.paste(resized_img, (x_offset, y_offset))
        
        # 生成mask
        mask = calculate_mask((img_width, img_height), (target_width, target_height), method, scale_factor=1.0)
        return np.array(padded_img).astype(np.float32)/255.0, mask, target_width, target_height

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
        
        # 生成mask
        mask = calculate_mask((img_width, img_height), (target_width, target_height), method, scale_factor=1.0)
        return np.array(cropped_img).astype(np.float32)/255.0, mask, target_width, target_height

def pad_image(image, target_width, target_height, position='center', background_color='#000000'):
    """Pad an image to the target dimensions with specified background color."""
    # 将ComfyUI的图像Tensor转换为PIL图像对象
    img = Image.fromarray(np.clip(255. * image.cpu().numpy(), 0, 255).astype(np.uint8))
    img_width, img_height = img.size

    # 解析十六进制颜色
    try:
        color = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        print(f"Invalid color format: {background_color}, using black")
        color = (0, 0, 0)

    # 创建指定颜色的背景图像
    padded_img = Image.new('RGB', (target_width, target_height), color)

    # 计算粘贴位置
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

    # 将原图粘贴到背景上
    padded_img.paste(img, (x_offset, y_offset))
    
    # 生成mask
    mask = calculate_mask((img_width, img_height), (target_width, target_height), position, scale_factor=1.0)
    
    # 转换回ComfyUI需要的格式
    return np.array(padded_img).astype(np.float32) / 255.0, mask, target_width, target_height

def calculate_resolution(aspect_ratio, scale_factor, max_width, max_height, min_width, min_height):
    """Calculate the target resolution based on aspect ratio and scale factor."""
    
    # SDXL 最佳分辨率对照表
    base_resolutions = {
        "1:1": (1024, 1024),
        "9:7": (1152, 896),
        "7:9": (896, 1152),
        "3:2": (1216, 832),
        "2:3": (832, 1216),
        "7:4": (1344, 768),
        "4:7": (768, 1344),
        "12:5": (1536, 640),
        "5:12": (640, 1536),
    }
    
    # 从输入中提取比例部分
    ratio = aspect_ratio.split(" ")[0]
    
    # 查找对应的基础分辨率
    if ratio in base_resolutions:
        base_width, base_height = base_resolutions[ratio]
    else:
        raise ValueError(f"Invalid aspect ratio: {ratio}")

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
    """Get the aspect ratio string from width and height, maintaining standard ratios"""
    # SDXL 标准比例映射
    sdxl_ratios = {
        (1024, 1024): "1:1",
        (1152, 896): "9:7",
        (896, 1152): "7:9",
        (1216, 832): "3:2",
        (832, 1216): "2:3",
        (1344, 768): "7:4",
        (768, 1344): "4:7",
        (1536, 640): "12:5",
        (640, 1536): "5:12"
    }
    
    # Midjourney 标准比例映射
    midjourney_ratios = {
        (1024, 1024): "1:1",
        (1200, 992): "6:5",
        (1232, 928): "4:3",
        (1344, 896): "3:2",
        (1456, 816): "16:9",
        (1536, 768): "2:1",
        (768, 1536): "1:2",
        (816, 1456): "9:16",
        (896, 1344): "2:3",
        (928, 1232): "3:4",
        (992, 1200): "5:6"
    }
    
    # 合并所有标准比例
    standard_ratios = {**sdxl_ratios, **midjourney_ratios}
    
    # 如果是标准分辨率，直接返回对应的比例
    if (width, height) in standard_ratios:
        return standard_ratios[(width, height)]
    
    # 如果不是标准分辨率，则使用最大公约数计算
    common_divisor = gcd(width, height)
    aspect_width = width // common_divisor
    aspect_height = height // common_divisor
    return f"{aspect_width}:{aspect_height}"

def create_outline(image, background_color):
    """给图片添加1像素的描边，使用背景色的反色"""
    # 将背景色转换为RGB元组
    try:
        bg_color = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        bg_color = (0, 0, 0)
    
    # 计算反色
    outline_color = tuple(255 - c for c in bg_color)
    
    # 将图像转换为PIL图像
    img = Image.fromarray(np.clip(255. * image, 0, 255).astype(np.uint8))
    width, height = img.size
    
    # 创建新图像，比原图大2像素
    outlined = Image.new('RGB', (width + 2, height + 2), outline_color)
    # 将原图粘贴到中心
    outlined.paste(img, (1, 1))
    
    # 转换回tensor格式
    return np.array(outlined).astype(np.float32) / 255.0

def calculate_mask(original_size, target_size, extend_mode, feather=0, scale_factor=1.0):
    """计算填充区域的mask，只在有背景区域时添加羽化效果"""
    orig_w, orig_h = original_size
    target_w, target_h = target_size
    
    # 创建目标尺寸的mask（默认全白，表示背景）
    mask = torch.ones((target_h, target_w))
    
    if extend_mode in ["top", "bottom", "left", "right", "center"]:
        # 这些模式下原始图像尺寸不变，只有目标尺寸受scale_factor影响
        new_w = orig_w  # 不对原始尺寸应用scale_factor
        new_h = orig_h

        if extend_mode == "center":
            x_offset = max(0, (target_w - new_w) // 2)
            y_offset = max(0, (target_h - new_h) // 2)
        elif extend_mode == "top":
            x_offset = max(0, (target_w - new_w) // 2)
            y_offset = 0
        elif extend_mode == "bottom":
            x_offset = max(0, (target_w - new_w) // 2)
            y_offset = max(0, target_h - new_h)
        elif extend_mode == "left":
            x_offset = 0
            y_offset = max(0, (target_h - new_h) // 2)
        else:  # right
            x_offset = max(0, target_w - new_w)
            y_offset = max(0, (target_h - new_h) // 2)

        actual_w = min(new_w, target_w - x_offset)
        actual_h = min(new_h, target_h - y_offset)

        if actual_w > 0 and actual_h > 0:
            content_area = torch.zeros((actual_h, actual_w))
            mask[y_offset:y_offset + actual_h, x_offset:x_offset + actual_w] = content_area
            
            if feather > 0:
                scaled_feather = int(feather * scale_factor)
                
                # 判断哪些边需要羽化
                has_top = y_offset > 0
                has_bottom = y_offset + actual_h < target_h
                has_left = x_offset > 0
                has_right = x_offset + actual_w < target_w
                
                for i in range(target_h):
                    for j in range(target_w):
                        if i < y_offset or i >= y_offset + actual_h or j < x_offset or j >= x_offset + actual_w:
                            continue
                            
                        # 只计算需要羽化的边的距离
                        dt = i - y_offset if has_top and i - y_offset < scaled_feather else scaled_feather
                        db = (y_offset + actual_h - i - 1) if has_bottom and (y_offset + actual_h - i - 1) < scaled_feather else scaled_feather
                        dl = j - x_offset if has_left and j - x_offset < scaled_feather else scaled_feather
                        dr = (x_offset + actual_w - j - 1) if has_right and (x_offset + actual_w - j - 1) < scaled_feather else scaled_feather
                        
                        d = min(dt, db, dl, dr)
                        if d < scaled_feather:
                            v = 1.0 - (d / scaled_feather)
                            mask[i, j] = v * v
    
    elif extend_mode == "fill":
        mask.fill_(0.0)
        
    elif extend_mode in ["cover", "outside"]:
        mask.fill_(0.0)
        
    elif extend_mode in ["contain", "inside"]:
        ratio = min(target_w/orig_w, target_h/orig_h)
        new_w = int(orig_w * ratio)
        new_h = int(orig_h * ratio)
        
        x_offset = (target_w - new_w) // 2
        y_offset = (target_h - new_h) // 2
        
        # 创建基础mask
        base_mask = torch.zeros((new_h, new_w))
        
        # 只在有背景区域时添加羽化效果
        if feather > 0 and (x_offset > 0 or y_offset > 0):
            for i in range(new_h):
                for j in range(new_w):
                    # 只在边缘有背景时计算羽化
                    dt = i if y_offset > 0 else new_h
                    db = new_h - i - 1 if y_offset > 0 else new_h
                    dl = j if x_offset > 0 else new_w
                    dr = new_w - j - 1 if x_offset > 0 else new_w
                    
                    d = min(dt, db, dl, dr)
                    
                    if d >= feather:
                        continue
                        
                    v = (feather - d) / feather
                    base_mask[i, j] = v * v
        
        mask[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = base_mask

    return mask

class ImageResolutionAdjuster:
    def __init__(self):
        self.selected_color = "#000000"
    
    @classmethod
    def get_resolution_options(cls):
        """Generate resolution options for SDXL and Midjourney optimal resolutions"""
        # SDXL基础分辨率
        sdxl_resolutions = [
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
        
        # Midjourney基础分辨率
        midjourney_resolutions = [
            (1024, 1024),  # 1:1
            (1200, 992),   # 6:5
            (1232, 928),   # 4:3
            (1344, 896),   # 3:2
            (1456, 816),   # 16:9
            (1536, 768),   # 2:1
            (768, 1536),   # 1:2
            (816, 1456),   # 9:16
            (896, 1344),   # 2:3
            (928, 1232),   # 3:4
            (992, 1200),   # 5:6
        ]
        
        # 合并所有分辨率并去重
        all_resolutions = list(set(sdxl_resolutions + midjourney_resolutions))
        
        # 创建带有比例值的元组列表
        resolution_ratios = []
        for width, height in all_resolutions:
            ratio = width / height  # 计算实际比例值
            ratio_str = get_aspect_ratio_string(width, height)
            resolution_ratios.append((ratio, f"{ratio_str} ({width}x{height})"))
        
        # 按比例值排序（从小到大）
        resolution_ratios.sort(key=lambda x: x[0])
        
        # 只返回分辨率字符串
        return [item[1] for item in resolution_ratios]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "target_resolution": (s.get_resolution_options(),),
                "extend_mode": (["contain", "cover", "fill", "inside", "outside", "top", "bottom", "left", "right", "center"],),
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
                "max_width": ("INT", {"default": 2048, "min": 1, "max": 8192, "step": 1}),
                "max_height": ("INT", {"default": 2048, "min": 1, "max": 8192, "step": 1}),
                "min_width": ("INT", {"default": 640, "min": 1, "max": 8192, "step": 1}),
                "min_height": ("INT", {"default": 640, "min": 1, "max": 8192, "step": 1}),
                "background_color": ("STRING", {"default": "#000000", "multiline": False}),
                "feathering": ("INT", {"default": 40, "min": 0, "max": 512, "step": 1}),
                "invert_mask": ("BOOLEAN", {"default": False}),
                "add_outline": ("BOOLEAN", {"default": False}),
            },
            "hidden": {"color_widget": "COMBO"}
        }

    CATEGORY = "🎨Painting👓Coder/🖼️Image"
    RETURN_TYPES = ("IMAGE", "MASK", "INT", "INT")
    RETURN_NAMES = ("images", "mask", "width", "height")
    FUNCTION = "adjust_resolution"

    def adjust_resolution(self, images, target_resolution, extend_mode, background_color, scale_factor, max_width, max_height, min_width, min_height, invert_mask, add_outline, feathering=40):
        output_images = []
        output_masks = []
        
        # 从目标分辨率字符串中提取宽高比和尺寸
        import re
        match = re.search(r'(\d+:\d+)\s*\((\d+)x(\d+)\)', target_resolution)
        if not match:
            raise ValueError(f"Invalid resolution format: {target_resolution}")
        
        aspect_ratio = match.group(1)
        base_width = int(match.group(2))
        base_height = int(match.group(3))
        
        # 计算目标分辨率
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
        
        # 确保尺寸为8的倍数
        target_width = (target_width // 8) * 8
        target_height = (target_height // 8) * 8
        
        for image in images:
            if extend_mode in ["contain", "cover", "fill", "inside", "outside"]:
                scaled_image, mask, width, height = resize_image(image, target_width, target_height, method=extend_mode, background_color=background_color)
                mask = calculate_mask((image.shape[1], image.shape[0]), (width, height), extend_mode, feather=feathering, scale_factor=scale_factor)
            elif extend_mode in ["top", "bottom", "left", "right", "center"]:
                scaled_image, mask, width, height = pad_image(image, target_width, target_height, 
                                                      position=extend_mode, 
                                                      background_color=background_color)
                mask = calculate_mask((image.shape[1], image.shape[0]), (width, height), extend_mode, feather=feathering, scale_factor=scale_factor)
            else:
                raise ValueError(f"Invalid extend_mode: {extend_mode}")
            
            if add_outline:
                scaled_image = create_outline(scaled_image, background_color)
                mask = F.pad(mask, (1, 1, 1, 1), mode='constant', value=0)
                width += 2
                height += 2
            
            output_images.append(torch.from_numpy(scaled_image).unsqueeze(0))
            output_masks.append(mask.unsqueeze(0))
        
        output_images = torch.cat(output_images, dim=0)
        output_masks = torch.cat(output_masks, dim=0)
        
        if invert_mask:
            output_masks = 1.0 - output_masks
        
        return (output_images, output_masks, width, height)

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        if "background_color" in kwargs:
            color = kwargs["background_color"]
            # 验证颜色格式
            if not color.startswith('#') or len(color) != 7:
                return False
            try:
                # 尝试解析十六进制颜色
                int(color[1:], 16)
            except ValueError:
                return False
        return True

    # 添加 Widget 定义
    @classmethod
    def WIDGETS(s):
        return {"color_widget": {"widget_type": "color_picker", "target": "background_color"}}

# 更新节点映射
NODE_CLASS_MAPPINGS = {
    "PaintingCoder::ImageResolutionAdjuster": ImageResolutionAdjuster,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PaintingCoder::ImageResolutionAdjuster": "Image Resolution Adjuster 📐",
}
