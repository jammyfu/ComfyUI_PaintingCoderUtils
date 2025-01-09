# -*- coding: utf-8 -*-
# Filename: dynamic_image_input.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🖼️Image

import torch

class DynamicImageCombiner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {},
            "_meta": {
                "preferred_width": 300,
                "maintain_dimensions": True
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "combine_images"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def combine_images(self, **kwargs):
        try:
            images = []
            # 获取所有图像输入键
            image_inputs = sorted(
                [k for k in kwargs.keys() if k.startswith('image_')],
                key=lambda x: int(x.split('_')[1])
            )
            
            # 只处理非None的输入（已连接的输入）
            for key in image_inputs:
                input_image = kwargs.get(key)
                
                # 跳过未连接的输入（None值）
                if input_image is None:
                    continue
                    
                # 处理已连接的输入
                if isinstance(input_image, torch.Tensor):
                    images.append(input_image)

            # 如果没有有效的图像输入，返回空图像
            if not images:
                empty_image = torch.zeros((1, 512, 512, 3))
                return ([empty_image],)

            return (images,)

        except Exception as e:
            print(f"Error in DynamicImageCombiner: {str(e)}")
            empty_image = torch.zeros((1, 512, 512, 3))
            return ([empty_image],)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "DynamicImageCombiner": DynamicImageCombiner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicImageCombiner": "Dynamic Image Input 🖼️"
}