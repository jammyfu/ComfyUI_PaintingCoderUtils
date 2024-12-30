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

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "MultilineTextInput": MultilineTextInput,
}
