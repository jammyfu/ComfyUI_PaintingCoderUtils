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
                    "placeholder": I18n.get_text('text_combiner.separator_placeholder', "输入分隔符...", app_language=True),
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
            # 获取所有文本输入键
            text_inputs = sorted(
                [k for k in kwargs.keys() if k.startswith('text_')],
                key=lambda x: int(x.split('_')[1])
            )
            
            # 只处理非None的输入（已连接的输入）
            for key in text_inputs:
                input_text = kwargs.get(key)
                
                # 跳过未连接的输入（None值）
                if input_text is None:
                    continue
                    
                # 处理已连接的输入
                input_text = str(input_text).replace('\r\n', '\n').replace('\r', '\n')
                
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
                
                texts.extend(t for t in split_texts if t is not None)
            
            if not texts:  # 如果没有有效的文本输入
                return (I18n.get_text('text_combiner.waiting_input', "等待输入...", app_language=True),)
            
            # 根据分隔符类型选择合并方式
            if '\n' in (separator if not use_regex else bytes(separator, "utf-8").decode("unicode_escape")):
                combined_text = '\n'.join(texts)
            elif not separator.strip():
                combined_text = ' '.join(texts)
            else:
                combined_text = f"{separator}".join(texts)
            
            return (combined_text,)
            
        except Exception as e:
            return (I18n.get_text('text_combiner.error', f"错误: {str(e)}", app_language=True),)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "TextCombiner": TextCombiner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextCombiner": I18n.get_text('text_combiner.name', "文本合并器 📝", app_language=True),
}

NODE_CATEGORY_MAPPINGS = {
    "TextCombiner": "🎨Painting👓Coder/📝Text",
}

NODE_COLOR_MAPPINGS = {
    "TextCombiner": (13, 110, 253),  # Bootstrap 蓝色
}
