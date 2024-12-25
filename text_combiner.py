# -*- coding: utf-8 -*-
# Filename: text_combiner.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/📝Text

import comfy

class TextCombiner:
    def __init__(self):
        self.input_count = 1  # 初始输入节点数量

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_1": ("STRING", {"multiline": True}),
                "refresh": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "text_2": ("STRING", {"multiline": True}),  # 只保留一个可选输入
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "combine_text"
    CATEGORY = "🎨Painting👓Coder/📝Text"

    CONTEXT_MENU = {
        "refresh_node": ["Refresh Node", "refresh_node"],
        "add_input": ["Add Input", "add_input"],
    }
    
    def combine_text(self, text_1, refresh=False, **kwargs):
        # 检查是否需要添加新的输入
        if kwargs.get(f"text_{self.input_count + 1}"):
            self.add_input()

        # 组合所有非空文本
        texts = [text_1] + [v for k, v in kwargs.items() if v and v.strip()]
        combined_text = ", ".join(t.strip() for t in texts if t.strip())
        return (combined_text,)

    def add_input(self):
        self.input_count += 1
        # 动态更新 INPUT_TYPES
        self.INPUT_TYPES = lambda s: {
            "required": {
                "text_1": ("STRING", {"multiline": True}),
                "refresh": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                f"text_{i}": ("STRING", {"multiline": True}) 
                for i in range(2, self.input_count + 2)  # +2 是为了总是多一个空输入
            },
        }
        return {"refresh": True}

    def refresh_node(self):
        return {"refresh": True}

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "TextCombiner": TextCombiner,
}
