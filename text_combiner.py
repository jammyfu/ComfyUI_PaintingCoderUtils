# -*- coding: utf-8 -*-
# Filename: text_combiner.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/📝Text

import re

class TextCombiner:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "separator": ("STRING", {
                    "default": ",", 
                    "multiline": False,
                    "placeholder": "支持正则表达式和转义字符，如: ,|\\n。使用特殊字符请关闭正则开关"
                }),
                "use_regex": ("BOOLEAN", {"default": False}),
            },
            "optional": {}
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
                    # 标准化输入文本的换行符
                    input_text = input_text.replace('\r\n', '\n').replace('\r', '\n')
                    
                    if use_regex:
                        # 正则模式：处理转义字符并使用正则分割
                        try:
                            separator_escaped = bytes(separator, "utf-8").decode("unicode_escape")
                            split_texts = re.split(separator_escaped, input_text)
                        except Exception as e:
                            return (f"正则表达式错误: {str(e)}",)
                    else:
                        # 普通模式：直接使用字符分割
                        if separator.strip():
                            split_texts = input_text.split(separator)
                        else:
                            split_texts = [input_text]
                    
                    # 过滤空字符串并添加到结果列表，保留纯空格字符串
                    texts.extend(t for t in split_texts if t is not None)
            
            # 根据分隔符是否包含换行来决定输出格式
            if '\n' in (separator if not use_regex else bytes(separator, "utf-8").decode("unicode_escape")):
                combined_text = '\n'.join(t if t.strip() else '""' for t in texts) if texts else "等待输入文本"
            elif not separator.strip():
                combined_text = ' '.join(t if t.strip() else '""' for t in texts) if texts else "等待输入文本"
            else:
                combined_text = f"{separator}".join(t if t.strip() else '""' for t in texts) if texts else "等待输入文本"
            
            return (combined_text,)
            
        except Exception as e:
            # 处理可能的错误
            return (f"Error: {str(e)}",)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "TextCombiner": TextCombiner,
}
