# 首先导入安装模块并执行安装
from .install import setup
setup()

try:
    from .image_resolution_adjuster import ImageResolutionAdjuster
    # 暂时注释掉未实现的节点
    # from .dynamic_image_input import DynamicImageInputs
    from .remove_empty_lines import RemoveEmptyLinesAndLeadingSpaces

    # 节点映射
    NODE_CLASS_MAPPINGS = {
        "ImageResolutionAdjuster": ImageResolutionAdjuster,
        # "DynamicImageInputs": DynamicImageInputs,
        "RemoveEmptyLinesAndLeadingSpaces": RemoveEmptyLinesAndLeadingSpaces,
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "ImageResolutionAdjuster": "Image Resolution Adjuster",
        # "DynamicImageInputs": "Dynamic Image Inputs",
        "RemoveEmptyLinesAndLeadingSpaces": "Remove Empty Lines And LeadingSpaces",
    }
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please restart ComfyUI after the installation is complete.")
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}
