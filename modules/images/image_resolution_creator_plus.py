# -*- coding: utf-8 -*-
# Filename: image_resolution_creator_plus.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🖼️Image

import torch
from .image_resolution_creator import ImageSizeCreator, any, ImageLatentCreator

class ImageSizeCreatorPlus(ImageSizeCreator):
    """增强版图像尺寸创建器，支持SDXL和Midjourney尺寸"""
    
    @classmethod
    def INPUT_TYPES(s):
        """动态获取输入类型"""
        return {
            "required": {
                "mode": (["Landscape", "Portrait", "Square"],),
                "style": (["SDXL", "Midjourney"],),
                "resolution": (s.get_resolution_options(),),  # 使用动态方法获取选项
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
            },
        }

    RETURN_TYPES = (any, "INT", "INT")
    RETURN_NAMES = ("resolution", "width", "height")
    FUNCTION = "create_size"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    @classmethod
    def get_sdxl_resolution_options(cls):
        """获取SDXL的分辨率选项"""
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
        return [f"{cls.get_aspect_ratio_string(w, h)} ({w}x{h})" for w, h in sdxl_resolutions]

    @classmethod
    def get_midjourney_resolution_options(cls):
        """获取Midjourney的分辨率选项"""
        mj_resolutions = [
            (768, 1536),   # 1:2
            (816, 1456),   # 9:16
            (896, 1344),   # 2:3
            (928, 1232),   # 3:4
            (992, 1200),   # 5:6
            (1024, 1024),  # 1:1
            (1200, 992),   # 6:5
            (1232, 928),   # 4:3
            (1344, 896),   # 3:2
            (1456, 816),   # 16:9
            (1536, 768),   # 2:1
        ]
        return [f"{cls.get_aspect_ratio_string(w, h)} ({w}x{h})" for w, h in mj_resolutions]

    @classmethod
    def get_resolution_options(cls):
        """获取所有可用的分辨率选项"""
        # 合并SDXL和Midjourney的所有选项
        sdxl_options = cls.get_sdxl_resolution_options()
        mj_options = cls.get_midjourney_resolution_options()
        return list(set(sdxl_options + mj_options))  # 使用set去重

    @staticmethod
    def get_sdxl_resolutions():
        """获取SDXL的标准分辨率"""
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
        return [(w, h) for w, h in sdxl_resolutions]

    @staticmethod
    def get_midjourney_resolutions():
        """获取Midjourney的标准分辨率"""
        mj_resolutions = [
            (768, 1536),   # 1:2
            (816, 1456),   # 9:16
            (896, 1344),   # 2:3
            (928, 1232),   # 3:4
            (992, 1200),   # 5:6
            (1024, 1024),  # 1:1
            (1200, 992),   # 6:5
            (1232, 928),   # 4:3
            (1344, 896),   # 3:2
            (1456, 816),   # 16:9
            (1536, 768),   # 2:1
        ]
        return [f"{cls.get_aspect_ratio_string(w, h)} ({w}x{h})" for w, h in mj_resolutions]

    @staticmethod
    def get_aspect_ratio_string(width, height):
        """获取宽高比字符串"""
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
        mj_ratios = {
            (768, 1536): "1:2",
            (816, 1456): "9:16",
            (896, 1344): "2:3",
            (928, 1232): "3:4",
            (992, 1200): "5:6",
            (1024, 1024): "1:1",
            (1200, 992): "6:5",
            (1232, 928): "4:3",
            (1344, 896): "3:2",
            (1456, 816): "16:9",
            (1536, 768): "2:1"
        }
        
        # 合并两个比例映射
        all_ratios = {**sdxl_ratios, **mj_ratios}
        return all_ratios.get((width, height), "1:1")

    def get_valid_resolutions(self, style):
        """根据风格获取有效的分辨率选项"""
        if style == "Midjourney":
            return self.get_midjourney_resolution_options()
        return self.get_sdxl_resolution_options()

    def create_size(self, mode, style, resolution, scale_factor=1.0):
        """创建图像尺寸，支持不同风格"""
        try:
            print(f"[ImageSizeCreatorPlus] Creating size with style: {style}")
            
            # 获取当前风格的有效分辨率选项
            valid_resolutions = self.get_valid_resolutions(style)
            
            # 检查分辨率是否在有效选项中
            if resolution not in valid_resolutions:
                # 如果不在有效选项中，使用默认分辨率
                resolution = valid_resolutions[0]
                print(f"[ImageSizeCreatorPlus] Invalid resolution for {style}, using default: {resolution}")
            
            # 从分辨率字符串中提取宽度和高度
            import re
            match = re.search(r'\((\d+)x(\d+)\)', resolution)
            if not match:
                raise ValueError(f"Invalid resolution format: {resolution}")
            
            width = int(match.group(1))
            height = int(match.group(2))
            
            # 应用缩放因子
            width = int(width * scale_factor)
            height = int(height * scale_factor)
            
            # 确保宽高为8的倍数
            width = (width // 8) * 8
            height = (height // 8) * 8
            
            return (resolution, width, height)
            
        except Exception as e:
            print(f"Error in ImageSizeCreatorPlus: {str(e)}")
            return ("1:1 (1024x1024)", 1024, 1024)

    def validate_inputs(self, **kwargs):
        """验证输入参数"""
        style = kwargs.get("style", "SDXL")
        resolution = kwargs.get("resolution", "")
        valid_resolutions = self.get_valid_resolutions(style)
        
        if resolution not in valid_resolutions:
            return {"resolution": valid_resolutions[0]}
        return {}

class ImageLatentCreatorPlus(ImageLatentCreator, ImageSizeCreatorPlus):
    """增强版图像潜空间创建器"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["Landscape", "Portrait", "Square"],),
                "style": (["SDXL", "Midjourney"],),
                "resolution": (s.get_resolution_options(),),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64}),
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
            },
        }

    RETURN_TYPES = ("LATENT", any, "INT", "INT", "INT")
    RETURN_NAMES = ("latent", "resolution", "width", "height", "batch_size")
    
    def create_latent(self, mode, style, resolution, batch_size=1, scale_factor=1.0):
        """创建潜空间，忽略style参数"""
        # 调用父类的create_size方法获取尺寸
        resolution, width, height = self.create_size(mode, style, resolution, scale_factor)
        
        # 创建标准格式的latent字典
        latent = {
            "samples": torch.zeros([batch_size, 4, height // 8, width // 8]),
            "batch_size": batch_size,
            "batch_index": list(range(batch_size))
        }
        
        return (latent, resolution, width, height, batch_size)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "PaintingCoder::ImageSizeCreatorPlus": ImageSizeCreatorPlus,
    "PaintingCoder::ImageLatentCreatorPlus": ImageLatentCreatorPlus,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PaintingCoder::ImageSizeCreatorPlus": "Image Size Creator Plus ✨",
    "PaintingCoder::ImageLatentCreatorPlus": "Image Latent Creator Plus ✨",
} 