# -*- coding: utf-8 -*-
# Filename: click_popup.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/🔧Utils

class ClickPopup:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "button": ("BOOLEAN", {"default": False}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("message",)
    FUNCTION = "show_popup"
    CATEGORY = "🎨Painting👓Coder/🔧Utils"
    
    def show_popup(self, button):
        return ("Button clicked!",)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "ClickPopup": ClickPopup,
} 