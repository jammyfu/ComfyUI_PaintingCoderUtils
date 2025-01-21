# -*- coding: utf-8 -*-
# Filename: dynamic_mask_input.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🖼️Image

import torch
from ..text.i18n import I18n

class DynamicMaskCombiner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask_1": ("MASK",),  # 添加一个初始掩码输入
            },
            "optional": {},
            "_meta": {
                "preferred_width": 300,
                "maintain_dimensions": True
            }
        }
    
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("masks",)
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "combine_masks"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def combine_masks(self, **kwargs):
        try:
            masks = []
            # 获取所有掩码输入键
            mask_inputs = sorted(
                [k for k in kwargs.keys() if k.startswith('mask_')],
                key=lambda x: int(x.split('_')[1])
            )
            
            # 只处理非None的输入（已连接的输入）
            for key in mask_inputs:
                input_mask = kwargs.get(key)
                
                # 跳过未连接的输入（None值）
                if input_mask is None:
                    continue
                    
                # 处理已连接的输入
                if isinstance(input_mask, torch.Tensor):
                    masks.append(input_mask)

            # 如果没有有效的掩码输入，返回空掩码
            if not masks:
                empty_mask = torch.zeros((1, 512, 512))
                return ([empty_mask],)

            return (masks,)

        except Exception as e:
            print(f"Error in DynamicMaskCombiner: {str(e)}")
            empty_mask = torch.zeros((1, 512, 512))
            return ([empty_mask],)

# 更新节点映射
NODE_CLASS_MAPPINGS = {
    "PaintingCoder::DynamicMaskCombiner": DynamicMaskCombiner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PaintingCoder::DynamicMaskCombiner": "Dynamic Mask Input 🎭",
} 