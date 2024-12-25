# 首先导入安装模块并执行安装
from .install import setup
setup()

import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# 设置 web 目录
WEB_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "web")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

try:
    from .image_resolution_adjuster import ImageResolutionAdjuster
    from .color_picker import ColorPicker
    from .remove_empty_lines import RemoveEmptyLinesAndLeadingSpaces
    from .text_combiner import TextCombiner
    from .multiline_text_input import MultilineTextInput
    from .click_popup import ClickPopup
    
    
    # 节点映射
    NODE_CLASS_MAPPINGS = {
        "ImageResolutionAdjuster": ImageResolutionAdjuster,
        "ColorPicker": ColorPicker,
        "RemoveEmptyLinesAndLeadingSpaces": RemoveEmptyLinesAndLeadingSpaces,
        "TextCombiner": TextCombiner,
        "MultilineTextInput": MultilineTextInput,
        "ClickPopup": ClickPopup,
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "ImageResolutionAdjuster": "Image Resolution Adjuster",
        "ColorPicker": "Color Picker",
        "RemoveEmptyLinesAndLeadingSpaces": "Remove Empty Lines And Leading Spaces",
        "TextCombiner": "Text Combiner",
        "MultilineTextInput": "Multiline Text Input",
        "ClickPopup": "Click Popup"
    }
    

    

except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please restart ComfyUI after the installation is complete.")
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}
    
