# 首先导入安装模块并执行安装
from .install import setup
setup()

try:
    from .image_resolution_adjuster import ImageResolutionAdjuster
    from .color_picker import ColorPicker
    from .remove_empty_lines import RemoveEmptyLinesAndLeadingSpaces

    # 节点映射
    NODE_CLASS_MAPPINGS = {
        "ImageResolutionAdjuster": ImageResolutionAdjuster,
        "ColorPicker": ColorPicker,
        "RemoveEmptyLinesAndLeadingSpaces": RemoveEmptyLinesAndLeadingSpaces
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "ImageResolutionAdjuster": "Image Resolution Adjuster",
        "ColorPicker": "Color Picker",
        "RemoveEmptyLinesAndLeadingSpaces": "Remove Empty Lines And Leading Spaces"
    }
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please restart ComfyUI after the installation is complete.")
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}
