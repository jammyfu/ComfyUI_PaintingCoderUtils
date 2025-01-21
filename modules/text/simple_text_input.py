# -*- coding: utf-8 -*-
# Filename: simple_text_input.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/📝Text

from ..text.i18n import I18n

class SimpleTextInput:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "",
                    "placeholder": I18n.get_text("simple_text_input.placeholder", "在此输入文本..."),
                }),
            },
            "_meta": {
                "preferred_width": 300,
                "maintain_dimensions": True
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "process"
    CATEGORY = "🎨Painting👓Coder/📝Text"

    def process(self, text):
        return (text,)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "PaintingCoder::SimpleTextInput": SimpleTextInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PaintingCoder::SimpleTextInput": "Simple Text Input 📝",
} 