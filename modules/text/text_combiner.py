# -*- coding: utf-8 -*-
# Filename: text_combiner.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/📝Text

import re
from .i18n import I18n

class TextCombiner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "separator": ("STRING", {
                    "default": ",", 
                    "multiline": False,
                    "placeholder": I18n.get_text('separator_placeholder')
                }),
                "use_regex": ("BOOLEAN", {"default": False}),
            },
            "optional": {},
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "combine_text"
    CATEGORY = "🎨Painting👓Coder/📝Text"

    def combine_text(self, separator=",", use_regex=False, **kwargs):
        try:
            texts = []
            for i in range(1, len(kwargs) + 1):
                key = f"text_{i}"
                if key in kwargs and kwargs[key] is not None:
                    input_text = kwargs[key]
                    input_text = input_text.replace('\r\n', '\n').replace('\r', '\n')
                    
                    if use_regex:
                        try:
                            separator_escaped = bytes(separator, "utf-8").decode("unicode_escape")
                            split_texts = re.split(separator_escaped, input_text)
                        except Exception as e:
                            return (I18n.get_text('regex_error', str(e)),)
                    else:
                        if separator.strip():
                            split_texts = input_text.split(separator)
                        else:
                            split_texts = [input_text]
                    
                    texts.extend(t for t in split_texts if t is not None and t != '')
            
            if not texts:
                return (I18n.get_text('waiting_input'),)
            
            if '\n' in (separator if not use_regex else bytes(separator, "utf-8").decode("unicode_escape")):
                combined_text = '\n'.join(texts)
            elif not separator.strip():
                combined_text = ' '.join(texts)
            else:
                combined_text = f"{separator}".join(texts)
            
            return (combined_text,)
            
        except Exception as e:
            return (f"Error: {str(e)}",)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "TextCombiner": TextCombiner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextCombiner": "Text Combiner 📝",
}

NODE_CATEGORY_MAPPINGS = {
    "TextCombiner": "🎨Painting👓Coder/📝Text",
}

NODE_COLOR_MAPPINGS = {
    "TextCombiner": (13, 110, 253),  # Bootstrap 蓝色
}
