# -*- coding: utf-8 -*-
# Filename: show_text_plus.py
# Developer: jammyfu
# Category: 🎨Painting👓Coder/📝Text

class ShowTextPlus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "show_text"
    CATEGORY = "🎨Painting👓Coder/📝Text"
    OUTPUT_NODE = True

    def __init__(self):
        # 初始化时设置默认值
        self.widget_value = ""

    def show_text(self, input_text, unique_id=None, extra_pnginfo=None):
        try:
            # 处理输入文本
            if isinstance(input_text, list):
                display_text = "\n".join(str(item) for item in input_text)
            else:
                display_text = str(input_text)

            # 更新节点UI显示
            if unique_id is not None and extra_pnginfo is not None:
                if isinstance(extra_pnginfo, list) and len(extra_pnginfo) > 0:
                    if isinstance(extra_pnginfo[0], dict) and "workflow" in extra_pnginfo[0]:
                        workflow = extra_pnginfo[0]["workflow"]
                        node = next(
                            (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                            None,
                        )
                        if node:
                            # 只在值发生变化时更新
                            if "widgets_values" not in node or node["widgets_values"] != [display_text]:
                                node["widgets_values"] = [display_text]
                                self.widget_value = display_text

            # 如果没有存储的值，使用当前显示文本
            if not hasattr(self, 'widget_value') or self.widget_value != display_text:
                self.widget_value = display_text

            return {"ui": {"text": [self.widget_value]}, "result": (input_text,)}

        except Exception as e:
            print(f"[ShowTextPlus] Error: {str(e)}")
            return {
                "ui": {"text": ["Error occurred"]},
                "result": ("Error occurred",)
            }

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "ShowTextPlus": ShowTextPlus,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShowTextPlus": "Show Text Plus 📝",
}