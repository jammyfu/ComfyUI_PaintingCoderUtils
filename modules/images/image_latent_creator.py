# -*- coding: utf-8 -*-
# Filename: image_latent_creator.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🖼️Image

import torch

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

class ImageLatentCreator:
    """创建空的图像潜空间"""
    
    @classmethod
    def get_resolution_options(cls):
        """Generate resolution options for SDXL optimal resolutions"""
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
        
        options = []
        for width, height in base_resolutions:
            ratio = cls.get_aspect_ratio_string(width, height)
            options.append(f"{ratio} ({width}x{height})")
        
        return options

    @staticmethod
    def get_aspect_ratio_string(width, height):
        """Get the aspect ratio string from width and height"""
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
        return sdxl_ratios.get((width, height), "1:1")

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["Landscape", "Portrait", "Square"],),
                "resolution": (s.get_resolution_options(),),  # combo 格式
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64}),
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
            },
            "hidden": {"extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("LATENT", any, "INT", "INT", "INT")
    RETURN_NAMES = ("latent", "resolution", "width", "height", "batch_size")
    OUTPUT_IS_LIST = (False, False, False, False, False)
    FUNCTION = "create_latent"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def parse_resolution(self, resolution_str):
        """解析分辨率字符串"""
        try:
            # 从字符串中提取宽度和高度
            width_height = resolution_str.split(" ")[1].strip("()")
            width, height = map(int, width_height.split("x"))
            return width, height
        except:
            return 1024, 1024  # 默认分辨率

    def create_latent(self, mode, resolution, batch_size=1, scale_factor=1.0, extra_pnginfo=None):
        try:
            # resolution 已经是格式化的字符串，如 "9:7 (1152x896)"
            print(f"[ImageLatentCreator] Using resolution: {resolution}")
            
            # 解析分辨率
            base_width, base_height = self.parse_resolution(resolution)
            
            # 应用缩放系数
            width = int(base_width * scale_factor)
            height = int(base_height * scale_factor)
            
            # 确保 batch_size 是整数且至少为 1
            batch_size = max(1, int(batch_size))
            
            # 直接创建正确 batch_size 的 tensor
            samples = torch.zeros([batch_size, 4, height // 8, width // 8])
            
            # 创建正确格式的 latent 字典
            latent = {
                "samples": samples,
                "batch_size": batch_size,
                "batch_index": list(range(batch_size))
            }
            
            print(f"[ImageLatentCreator] Created latent with shape: {samples.shape}, batch_size: {batch_size}")
            
            
            return (latent,resolution,width, height, batch_size)
            
        except Exception as e:
            print(f"Error in ImageLatentCreator: {str(e)}")
            raise e

# 注册节点
NODE_CLASS_MAPPINGS = {
    "ImageLatentCreator": ImageLatentCreator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageLatentCreator": "Image Latent Creator 🎨"
} 