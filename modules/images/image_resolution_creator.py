# -*- coding: utf-8 -*-
# Filename: image_latent_creator.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🖼️Image

import torch

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

class ImageSizeCreator:
    """创建图像尺寸"""
    
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
                "resolution": (s.get_resolution_options(),), 
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1}),
            },
        }

    RETURN_TYPES = (any, "INT", "INT")  # resolution, width, height
    RETURN_NAMES = ("resolution", "width", "height")
    FUNCTION = "create_size"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def parse_resolution(self, resolution_str):
        """解析分辨率字符串"""
        try:
            # 处理各种可能的输入类型
            if isinstance(resolution_str, (list, tuple)):
                # 如果是列表或元组，取第一个元素
                resolution_str = resolution_str[0]
            elif not isinstance(resolution_str, str):
                # 如果既不是字符串也不是列表/元组，转换为字符串
                resolution_str = str(resolution_str)
            
            # 检查是否包含预期的格式
            if "(" in resolution_str and ")" in resolution_str:
                # 从字符串中提取宽度和高度
                width_height = resolution_str.split(" ")[1].strip("()")
                width, height = map(int, width_height.split("x"))
            else:
                # 如果格式不对，返回默认值
                print(f"[ImageSizeCreator] Invalid resolution format: {resolution_str}, using default")
                return 1024, 1024
            
            return width, height
        except Exception as e:
            print(f"[ImageSizeCreator] Error parsing resolution: {str(e)}, using default")
            return 1024, 1024  # 默认分辨率

    def create_size(self, mode, resolution, scale_factor=1.0):
        try:
            print(f"[ImageSizeCreator] Input resolution type: {type(resolution)}, value: {resolution}")
            
            # 解析分辨率
            base_width, base_height = self.parse_resolution(resolution)
            
            # 应用缩放系数
            width = int(base_width * scale_factor)
            height = int(base_height * scale_factor)
            
            print(f"[ImageSizeCreator] Created size: {width}x{height}")
            
            # 确保返回的 resolution 是列表格式
            if isinstance(resolution, (list, tuple)):
                resolution_list = list(resolution)
            else:
                resolution_list = [str(resolution)]
            
            return (resolution_list[0], width, height)
            
        except Exception as e:
            print(f"[ImageSizeCreator] Error in create_size: {str(e)}")
            # 发生错误时返回默认值
            return ("1:1 (1024x1024)", 1024, 1024)

class ImageLatentCreator(ImageSizeCreator):
    """创建空的图像潜空间"""
    
    @classmethod
    def INPUT_TYPES(s):
        base_inputs = super().INPUT_TYPES()
        base_inputs["required"].update({
            "batch_size": ("INT", {"default": 1, "min": 1, "max": 64}),
        })
        base_inputs["hidden"] = {"extra_pnginfo": "EXTRA_PNGINFO"}
        return base_inputs

    RETURN_TYPES = ("LATENT", any, "INT", "INT", "INT")  # latent, resolution, width, height, batch_size
    RETURN_NAMES = ("latent", "resolution", "width", "height", "batch_size")
    FUNCTION = "create_latent"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def create_latent(self, mode, resolution, batch_size=1, scale_factor=1.0, extra_pnginfo=None):
        try:
            # 使用父类的 create_size 方法获取基本尺寸
            resolution_list, width, height = super().create_size(mode, resolution, scale_factor)
            
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
            
            return (latent, resolution_list, width, height, batch_size)
            
        except Exception as e:
            print(f"Error in ImageLatentCreator: {str(e)}")
            raise e

# 注册节点
NODE_CLASS_MAPPINGS = {
    "PaintingCoder::ImageSizeCreator": ImageSizeCreator,
    "PaintingCoder::ImageLatentCreator": ImageLatentCreator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PaintingCoder::ImageSizeCreator": "Image Size Creator 📏",
    "PaintingCoder::ImageLatentCreator": "Image Latent Creator 🎨",
} 