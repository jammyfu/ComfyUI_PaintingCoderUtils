# -*- coding: utf-8 -*-
# Filename: multiline_text_input.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/📝Text

class MultilineTextInput:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "get_text"
    CATEGORY = "🎨Painting👓Coder/📝Text"

    def get_text(self, text):
        return (text,)

# 更新节点映射
NODE_CLASS_MAPPINGS = {
    "PaintingCoder::MultilineTextInput": MultilineTextInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PaintingCoder::MultilineTextInput": "Multiline Text Input 📝",
}
