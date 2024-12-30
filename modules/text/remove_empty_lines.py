# 创建者: jammyfu
import re

class RemoveEmptyLinesAndLeadingSpaces:
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
                "text": ("STRING", {"multiline": True})  # 文本输入，支持多行
            },
            "optional": {
                "output_type": (["String", "List"], {"default": "String"}),  # 输出类型，可选择 "String" 或 "List"，默认为 "String"
                "remove_empty_lines_option": ("BOOLEAN", {"default": True}),  # 控制是否移除空行的布尔值，默认为 True
                "remove_leading_spaces_option": ("BOOLEAN", {"default": True}),  # 控制是否移除行首空格的布尔值，默认为 True
            }
        }
    
    RETURN_TYPES = ("STRING",)  # 返回类型为字符串
    RETURN_NAMES = ("output",)  # 返回值的名称为 "output"
    OUTPUT_IS_LIST = (False,)  # 初始时输出不是列表
    FUNCTION = "process_text"  # 节点执行的函数名
    CATEGORY = "🎨Painting👓Coder/📝Text"  # 节点在 ComfyUI 中的类别，这里修改了
    
    def process_text(self, text, output_type, remove_empty_lines_option, remove_leading_spaces_option):
        """
        处理文本的函数，根据按钮值移除空行和行首空格。

        Args:
            text (str): 输入的文本字符串。
            output_type (str): 输出类型，"String" 或 "List"。
            remove_empty_lines_option (bool): 是否移除空行的标志。
            remove_leading_spaces_option (bool): 是否移除行首空格的标志。
        Returns:
            tuple: 包含处理后的文本（字符串或字符串列表）。
        """
        processed_text = text  # 初始时，处理后的文本和原始文本相同
        
        if remove_empty_lines_option or remove_leading_spaces_option:
            
            # 根据 remove_empty_lines_option 控制是否移除空行
            if remove_empty_lines_option:
                processed_text = re.sub(r"^\n+", "", processed_text)  # 去除开头的空行
                processed_text = re.sub(r"\n{2,}", "\n", processed_text)  # 将多个空行替换为单个
                processed_text = re.sub(r"\n+$", "", processed_text)  # 去除末尾的空行

            # 根据 remove_leading_spaces_option 控制是否移除行首空格
            if remove_leading_spaces_option:
                processed_text = re.sub(r"^ +", "", processed_text, flags=re.MULTILINE)

            # 将文本按行分割
            lines = processed_text.split('\n')
            if remove_leading_spaces_option:
                lines = [line.strip() for line in lines]  # 去除每行首尾的空格
            
            if remove_empty_lines_option:
                lines = [line for line in lines if line.strip()]  # 修改：使用 strip() 检查是否为空行
            
            # 根据输出类型设置 OUTPUT_IS_LIST
            self.OUTPUT_IS_LIST = (output_type == "List",)
            
            # 根据输出类型返回结果，如果是列表则返回列表，否则将列表用换行符连接成字符串
            return (lines if output_type == "List" else "\n".join(lines),)
        else:
            # 如果按钮都是False,直接返回原始输入文本，根据 output_type 返回
            self.OUTPUT_IS_LIST = (output_type == "List",)
            return (text.splitlines() if output_type == "List" else text, )

# 节点类映射，用于 ComfyUI 注册
NODE_CLASS_MAPPINGS = {
    "RemoveEmptyLinesAndLeadingSpaces": RemoveEmptyLinesAndLeadingSpaces
}

# 节点显示名称映射，用于 ComfyUI 显示
NODE_DISPLAY_NAME_MAPPINGS = {
    "RemoveEmptyLinesAndLeadingSpaces": "Remove Empty Lines & Leading Spaces"
}

# # 测试代码
# if __name__ == "__main__":
#     # 创建测试实例
#     processor = RemoveEmptyLinesAndLeadingSpaces()
    
#     # 测试文本，包含各种情况
#     test_text = """第今晚的星空✨

#     像极了我们的回忆💭
            
#       你在那边🌌 我在这边🌙

# 生活总是充满惊喜🎉

#    有时候觉得自己是一颗

#      🌟✨闪耀的小星星💫

# 音乐流淌🎶

#      让我暂时忘记烦恼😌

#    感受这一刻 的快乐💖"""
    
#     # 测试不同组合
#     test_cases = [
#         (True, True, "String"),
#         (True, False, "String"),
#         (False, False, "String"),
#     ]
    
#     for remove_empty, remove_spaces, output_type in test_cases:
#         print(f"\n测试配置：")
#         print(f"移除空行: {remove_empty}")
#         print(f"移除首尾空格: {remove_spaces}")
#         print(f"输出类型: {output_type}")
#         print("-" * 30)
        
#         result = processor.process_text(
#             test_text,
#             output_type,
#             remove_empty,
#             remove_spaces
#         )
        
#         print("处理结果：")
#         print(result[0])  # result是元组，取第一个元素
