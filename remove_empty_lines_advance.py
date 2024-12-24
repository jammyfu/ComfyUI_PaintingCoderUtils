# 创建者: jammyfu
import re

class RemoveEmptyLinesAndLeadingSpacesAdvance:
    """
    一个 ComfyUI 自定义节点，用于移除文本中多余的空行和行首空格。
    """
    @classmethod
    def INPUT_TYPES(s):
        """
        定义节点的输入类型。

        Returns:
            dict: 包含 'required' 和 'optional' 输入定义的字典。
        """
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "output_type": (["String", "List"], {"default": "String"}),
            },
            "optional": {
                "remove_empty_lines_option": ("BOOLEAN", {"default": True}),
                "remove_leading_spaces_option": ("BOOLEAN", {"default": True}),
                "preview": ("BOOLEAN", {"default": False}),
                "output_preview": ("STRING", {"multiline": True, "readonly": True, "default": "", "display": "none"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)
    OUTPUT_NODE = True
    FUNCTION = "process_text"
    CATEGORY = "🎨Painting👓Coder/📝Text"
    
    # 定义 OUTPUT_IS_LIST
    OUTPUT_IS_LIST = [False]
    
    @classmethod
    def IS_CHANGED(s, **kwargs):
        preview = kwargs.get("preview", False)
        if preview:
            return float("nan")
        return False
    
    def process_text(self, text, output_type, remove_empty_lines_option, remove_leading_spaces_option, preview, output_preview):
        """
        处理文本的函数，根据按钮值移除空行和行首空格。

        Args:
            text (str): 输入的文本字符串。
            output_type (str): 输出类型，"String" 或 "List"。
            remove_empty_lines_option (bool): 是否移除空行的标志。
            remove_leading_spaces_option (bool): 是否移除行首空格的标志。
            preview (bool): 是否显示预览窗口。
            output_preview (str): 输出预览文本。
        Returns:
            tuple: 包含处理后的文本（字符串或字符串列表）和预览UI。
        """
        processed_text = text
        
        if remove_empty_lines_option or remove_leading_spaces_option:
            lines = processed_text.split('\n')
            
            if remove_leading_spaces_option:
                lines = [line.strip() for line in lines]
                
            if remove_empty_lines_option:
                lines = [line for line in lines if line.strip()]
            
            result = lines if output_type == "List" else "\n".join(lines)
        else:
            result = text.splitlines() if output_type == "List" else text

        if preview:
            return {
                "ui": {
                    "output_preview": [result, {"multiline": True, "readonly": True, "height": 300}]
                },
                "result": (result,)
            }
        else:
            return (result,)

# 节点类映射，用于 ComfyUI 注册
NODE_CLASS_MAPPINGS = {
    "RemoveEmptyLinesAndLeadingSpacesAdvance": RemoveEmptyLinesAndLeadingSpacesAdvance
}

# 节点显示名称映射，用于 ComfyUI 显示
NODE_DISPLAY_NAME_MAPPINGS = {
    "RemoveEmptyLinesAndLeadingSpacesAdv": "Remove Empty Lines & Leading Spaces Advance"
}
