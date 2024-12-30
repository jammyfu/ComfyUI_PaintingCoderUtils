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

    def show_text(self, input_text, unique_id=None, extra_pnginfo=None):
        try:
            print(f"[ShowTextPlus] Input text: {input_text}")  # 调试日志

            # 处理输入文本
            if isinstance(input_text, list):
                # 将列表内容拼接成字符串，每项一行
                display_text = "\n".join(str(item) for item in input_text)
            else:
                display_text = str(input_text)

            print(f"[ShowTextPlus] Processed text: {display_text}")  # 调试日志

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
                            # 更新节点的显示值
                            node["widgets_values"] = [display_text]
                            print(f"[ShowTextPlus] Updated widget values: {display_text}")  # 调试日志

            return {"ui": {"text": [display_text]}, "result": (input_text,)}

        except Exception as e:
            print(f"[ShowTextPlus] Error: {str(e)}")  # 错误日志
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