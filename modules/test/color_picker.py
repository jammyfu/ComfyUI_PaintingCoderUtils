import torch
import numpy as np
from PIL import Image

class ColorPicker:
    """
    颜色选择器节点，使用 jscolor 实现颜色选择和吸管工具
    """
    
    def __init__(self):
        self.color = "#000000"
    
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}}  # 不需要输入项
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("color",)
    FUNCTION = "pick_color"
    CATEGORY = "🎨Painting👓Coder/🎨Color"

    def pick_color(self):
        return (self.color,)

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    def widget_value_updated(self, widget, value):
        if widget.name == "color_picker":
            self.color = value

    @classmethod
    def WIDGETS(s):
        return {"color_picker": ("color", {"default": "#000000"})}

# 在 __init__.py 中添加节点注册
NODE_CLASS_MAPPINGS = {
    "ColorPicker": ColorPicker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ColorPicker": "Color Picker"
} 