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
                    "placeholder": "支持正则表达式和转义字符，如: ,|\\n。使用特殊字符请加\\转义"
                }),
            },
            "optional": {}
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "combine_text"
    CATEGORY = "🎨Painting👓Coder/📝Text"

    def combine_text(self, separator=",", **kwargs):
        try:
            # 如果分隔符不是正则表达式，对特殊字符进行转义
            if not any(c in separator for c in "[](){}?*+|^$\\"):
                separator = re.escape(separator)
            
            # 处理转义字符
            separator = bytes(separator, "utf-8").decode("unicode_escape")
            
            # 检查分隔符是否包含换行相关字符
            is_newline_separator = bool(re.search(r'\\[rn]|[\r\n]', separator))
            
            # 收集所有非空文本
            texts = []
            for i in range(1, len(kwargs) + 1):
                key = f"text_{i}"
                if key in kwargs and kwargs[key] is not None:
                    input_text = kwargs[key]
                    # 标准化输入文本的换行符
                    input_text = input_text.replace('\r\n', '\n').replace('\r', '\n')
                    
                    # 使用正则表达式分割输入文本
                    split_texts = re.split(separator, input_text) if separator != " " else [input_text]
                    # 过滤空字符串并添加到结果列表，保留纯空格字符串
                    texts.extend(t.rstrip('\n').rstrip('\r') for t in split_texts if t is not None)
            
            # 根据分隔符类型选择拼接方式
            if is_newline_separator:
                # 如果分隔符包含换行，使用换行符拼接
                combined_text = '\n'.join(t if t.strip() else '""' for t in texts) if texts else "等待输入文本"
            elif not separator.strip():
                # 如果分隔符为空，使用单个空格拼接
                combined_text = ' '.join(t if t.strip() else '""' for t in texts) if texts else "等待输入文本"
            else:
                # 否则使用逗号和空格拼接
                combined_text = ", ".join(t if t.strip() else '""' for t in texts) if texts else "等待输入文本"
            
            return (combined_text,)
            
        except re.error as e:
            # 如果正则表达式无效，返回错误信息
            return (f"Regular expression error: {str(e)}",)
        except Exception as e:
            # 处理其他可能的错误
            return (f"Error: {str(e)}",)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "TextCombiner": TextCombiner,
}
