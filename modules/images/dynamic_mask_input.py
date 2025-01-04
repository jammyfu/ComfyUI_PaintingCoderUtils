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
            "required": {},  # 不需要默认输入
            "optional": {},
            "_meta": {
                "preferred_width": 300,  # 设置默认宽度为300
                "maintain_dimensions": True  # 保持刷新时的尺寸
            }
        }
    
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("masks",)
    OUTPUT_IS_LIST = (True,)  # 标记输出为列表
    FUNCTION = "combine_masks"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def combine_masks(self, **mask_inputs):
        try:
            # 收集所有非空掩码
            masks = []
            for i in range(1, len(mask_inputs) + 1):
                key = f"mask_{i}"
                if key in mask_inputs and mask_inputs[key] is not None:
                    if isinstance(mask_inputs[key], torch.Tensor):
                        masks.append(mask_inputs[key])

            # 如果没有掩码，返回一个包含空白掩码的列表
            if not masks:
                empty_mask = torch.zeros((1, 512, 512))
                return ([empty_mask],)

            # 直接返回掩码列表
            return (masks,)

        except Exception as e:
            print(f"Error in DynamicMaskCombiner: {str(e)}")
            # 发生错误时返回包含空白掩码的列表
            empty_mask = torch.zeros((1, 512, 512))
            return ([empty_mask],)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "DynamicMaskCombiner": DynamicMaskCombiner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DynamicMaskCombiner": I18n.get_text("dynamic_mask_input.name", "Dynamic Mask Input 🎭", app_language=True),
} 