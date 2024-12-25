# -*- coding: utf-8 -*-
# Filename: dynamic_image_input.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🖼️Image

import torch

class DynamicImageCombiner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},  # 不需要默认输入
            "optional": {},
            "_meta": {
                "preferred_width": 300,  # 设置默认宽度为300
                "maintain_dimensions": True  # 保持刷新时的尺寸
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    OUTPUT_IS_LIST = (True,)  # 标记输出为列表
    FUNCTION = "combine_images"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def combine_images(self, **image_inputs):
        try:
            # 收集所有非空图像
            images = []
            for i in range(1, len(image_inputs) + 1):
                key = f"image_{i}"
                if key in image_inputs and image_inputs[key] is not None:
                    if isinstance(image_inputs[key], torch.Tensor):
                        images.append(image_inputs[key])

            # 如果没有图像，返回一个包含空白图像的列表
            if not images:
                empty_image = torch.zeros((1, 512, 512, 3))
                return ([empty_image],)

            # 直接返回图像列表
            return (images,)

        except Exception as e:
            print(f"Error in DynamicImageCombiner: {str(e)}")
            # 发生错误时返回包含空白图像的列表
            empty_image = torch.zeros((1, 512, 512, 3))
            return ([empty_image],)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "DynamicImageCombiner": DynamicImageCombiner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicImageCombiner": "Dynamic Image Input 🖼️",
}