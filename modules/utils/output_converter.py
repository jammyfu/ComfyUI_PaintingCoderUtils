# -*- coding: utf-8 -*-
# Filename: output_converter.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🛠️Utils

import json
import torch
import numpy as np
from PIL import Image

class AnyType(str):
    """自定义任意类型"""
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

class OutputToTextConverter:
    """通用输出转文本转换器"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "any_input": (any_type,),  # 使用自定义的any_type
                "format": (["Auto", "JSON", "Plain Text", "Raw"],),
                "indent": ("INT", {"default": 2, "min": 0, "max": 8, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "convert"
    CATEGORY = "🎨Painting👓Coder/🛠️Utils"

    def convert(self, any_input, format="Auto", indent=2):
        """将任何输入转换为文本"""
        try:
            # 如果输入为None
            if any_input is None:
                return ("None",)

            # 如果输入已经是字符串
            if isinstance(any_input, str):
                return (any_input,)

            # 根据不同类型进行转换
            if format == "Auto":
                text = self._auto_convert(any_input, indent)
            elif format == "JSON":
                text = self._to_json(any_input, indent)
            elif format == "Plain Text":
                text = str(any_input)
            else:  # Raw
                text = repr(any_input)

            print(f"[OutputConverter] Converted {type(any_input).__name__} to text")
            return (text,)

        except Exception as e:
            print(f"[OutputConverter] Error converting output: {str(e)}")
            return (f"Error: {str(e)}",)

    def _auto_convert(self, obj, indent):
        """自动选择最合适的转换方式"""
        # 处理常见的数据类型
        if isinstance(obj, (dict, list, tuple, set)):
            return self._to_json(obj, indent)
        elif isinstance(obj, (int, float, bool)):
            return str(obj)
        elif isinstance(obj, (torch.Tensor, np.ndarray)):
            return self._tensor_to_text(obj)
        elif isinstance(obj, Image.Image):
            return self._image_to_text(obj)
        else:
            # 尝试JSON序列化，如果失败则使用str
            try:
                return self._to_json(obj, indent)
            except:
                return str(obj)

    def _to_json(self, obj, indent):
        """转换为JSON格式"""
        def default_converter(o):
            if isinstance(o, (torch.Tensor, np.ndarray)):
                return self._tensor_to_text(o)
            elif isinstance(o, Image.Image):
                return self._image_to_text(o)
            elif hasattr(o, '__dict__'):
                return o.__dict__
            return str(o)

        return json.dumps(obj, indent=indent, default=default_converter)

    def _tensor_to_text(self, tensor):
        """转换张量为文本描述"""
        if isinstance(tensor, np.ndarray):
            shape = tensor.shape
            dtype = str(tensor.dtype)
        else:  # torch.Tensor
            shape = tuple(tensor.size())
            dtype = str(tensor.dtype)

        return f"Tensor(shape={shape}, dtype={dtype})"

    def _image_to_text(self, image):
        """转换图像为文本描述"""
        return f"Image(size={image.size}, mode={image.mode})"

# 注册节点
NODE_CLASS_MAPPINGS = {
    "PaintingCoder::OutputToTextConverter": OutputToTextConverter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PaintingCoder::OutputToTextConverter": "Output To Text 📝",
} 