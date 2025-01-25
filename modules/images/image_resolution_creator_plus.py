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
        return {
            "required": {
                "mode": (["Landscape", "Portrait", "Square"],),
                "style": (["SDXL", "Midjourney"],),
                "resolution": (s.get_resolution_options(),),
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
            },
        }

    @classmethod
    def get_resolution_options(cls):
        """根据选择的风格返回对应的分辨率选项"""
        return cls.get_sdxl_resolutions()  # 默认返回SDXL的分辨率

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
        return [(w, h) for w, h in mj_resolutions]

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

    def create_size(self, mode, style, resolution, scale_factor=1.0):
        """创建图像尺寸，支持不同风格"""
        try:
            print(f"[ImageSizeCreatorPlus] Creating size with style: {style}")
            return super().create_size(mode, resolution, scale_factor)
        except Exception as e:
            print(f"Error in ImageSizeCreatorPlus: {str(e)}")
            return ("1:1 (1024x1024)", 1024, 1024)

class ImageLatentCreatorPlus(ImageLatentCreator, ImageSizeCreatorPlus):
    """增强版图像潜空间创建器"""
    
    @classmethod
    def INPUT_TYPES(s):
        base_inputs = super().INPUT_TYPES()
        base_inputs["required"]["style"] = (["SDXL", "Midjourney"],)
        return base_inputs

    def create_latent(self, mode, style, resolution, batch_size=1, scale_factor=1.0, extra_pnginfo=None):
        """创建潜空间，支持不同风格"""
        try:
            print(f"[ImageLatentCreatorPlus] Creating latent with style: {style}")
            resolution_list, width, height = self.create_size(mode, style, resolution, scale_factor)
            
            batch_size = max(1, int(batch_size))
            samples = torch.zeros([batch_size, 4, height // 8, width // 8])
            
            latent = {
                "samples": samples,
                "batch_size": batch_size,
                "batch_index": list(range(batch_size))
            }
            
            return (latent, resolution_list, width, height, batch_size)
            
        except Exception as e:
            print(f"Error in ImageLatentCreatorPlus: {str(e)}")
            raise e

# 注册节点
NODE_CLASS_MAPPINGS = {
    "PaintingCoder::ImageSizeCreatorPlus": ImageSizeCreatorPlus,
    "PaintingCoder::ImageLatentCreatorPlus": ImageLatentCreatorPlus,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PaintingCoder::ImageSizeCreatorPlus": "Image Size Creator Plus ✨",
    "PaintingCoder::ImageLatentCreatorPlus": "Image Latent Creator Plus ✨",
} 