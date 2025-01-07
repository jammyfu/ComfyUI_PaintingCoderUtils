# -*- coding: utf-8 -*-
# Filename: __init__.py
# Developer: jammyfu

import os
import locale
from .modules.text.i18n import I18n

# 获取当前文件所在目录
EXTENSION_FOLDER = os.path.dirname(os.path.realpath(__file__))

# 导入所有非测试节点类
from .modules.images.mask_preview import MaskPreview
from .modules.images.dynamic_image_input import DynamicImageCombiner
from .modules.images.dynamic_mask_input import DynamicMaskCombiner
from .modules.images.image_resolution_adjuster import ImageResolutionAdjuster
from .modules.text.text_combiner import TextCombiner
from .modules.text.show_text_plus import ShowTextPlus
from .modules.text.simple_text_input import SimpleTextInput
from .modules.text.multiline_text_input import MultilineTextInput
from .modules.text.remove_empty_lines import RemoveEmptyLinesAndLeadingSpaces
from .modules.images.image_latent_creator import ImageLatentCreator



# 节点类映射
NODE_CLASS_MAPPINGS = {
    "MaskPreview": MaskPreview,
    "ImageLatentCreator": ImageLatentCreator,
    "DynamicImageCombiner": DynamicImageCombiner,
    "DynamicMaskCombiner": DynamicMaskCombiner,
    "ImageResolutionAdjuster": ImageResolutionAdjuster,
    "TextCombiner": TextCombiner,
    "ShowTextPlus": ShowTextPlus,
    "SimpleTextInput": SimpleTextInput,
    "MultilineTextInput": MultilineTextInput,
    "RemoveEmptyLinesAndLeadingSpaces": RemoveEmptyLinesAndLeadingSpaces,
    
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskPreview": "Mask Preview 🎭",
    "ImageLatentCreator": "Image Latent Creator 🎨",
    "DynamicImageCombiner": "Dynamic Image Input 🖼️",
    "DynamicMaskCombiner": "Dynamic Mask Input 🎭",
    "ImageResolutionAdjuster": "Image Resolution Adjuster 📐",
    "TextCombiner": "Text Combiner ✍️",
    "ShowTextPlus": "Show Text Plus 📝",
    "SimpleTextInput": "Simple Text Input 📝",
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

def init():
    try:
        # 获取系统语言设置
        system_lang = locale.getdefaultlocale()[0]
        if system_lang:
            lang_code = system_lang.split('_')[0].lower()
            I18n.set_language(lang_code)
    except:
        # 如果获取失败，默认使用英文
        I18n.set_language('en')
