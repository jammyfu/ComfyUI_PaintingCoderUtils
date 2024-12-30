# -*- coding: utf-8 -*-
# Filename: __init__.py
# Developer: jammyfu

import os

# 获取当前文件所在目录
EXTENSION_FOLDER = os.path.dirname(os.path.realpath(__file__))

# 导入所有非测试节点类
from .modules.images.mask_preview import MaskPreview
from .modules.images.dynamic_image_input import DynamicImageCombiner
from .modules.images.image_resolution_adjuster import ImageResolutionAdjuster
from .modules.text.text_combiner import TextCombiner
from .modules.text.show_text_plus import ShowTextPlus
from .modules.text.multiline_text_input import MultilineTextInput
from .modules.text.remove_empty_lines import RemoveEmptyLinesAndLeadingSpaces


# 节点类映射
NODE_CLASS_MAPPINGS = {
    "MaskPreview": MaskPreview,
    "DynamicImageCombiner": DynamicImageCombiner,
    "ImageResolutionAdjuster": ImageResolutionAdjuster,
    "TextCombiner": TextCombiner,
    "ShowTextPlus": ShowTextPlus,
    "MultilineTextInput": MultilineTextInput,
    "RemoveEmptyLinesAndLeadingSpaces": RemoveEmptyLinesAndLeadingSpaces,
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskPreview": "Mask Preview 🖼️",
    "DynamicImageCombiner": "Dynamic Image Input 🖼️",
    "ImageResolutionAdjuster": "Image Resolution Adjuster 📐",
    "TextCombiner": "Text Combiner ✍️",
    "ShowTextPlus": "Show Text Plus 📝",
    "MultilineTextInput": "Multiline Text Input 📝",
    "RemoveEmptyLinesAndLeadingSpaces": "Remove Empty Lines And Leading Spaces 📝",
}

# Web 目录配置
WEB_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "web")
print(f"Loading web directory from: {WEB_DIRECTORY}")

# 导出必要的变量
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 添加 Web 目录到 ComfyUI
def get_web_dirs():
    return [WEB_DIRECTORY]

# 打印调试信息
print(f"Initialized PaintingCoderUtils from: {EXTENSION_FOLDER}")
print(f"Available nodes: {list(NODE_CLASS_MAPPINGS.keys())}")
print(f"Web directory: {WEB_DIRECTORY}")
