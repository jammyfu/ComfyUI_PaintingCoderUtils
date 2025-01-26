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
from .modules.images.image_resolution_creator import ImageSizeCreator
from .modules.images.image_resolution_creator import ImageLatentCreator
from .modules.images.image_resolution_creator_plus import ImageSizeCreatorPlus
from .modules.images.image_resolution_creator_plus import ImageLatentCreatorPlus
from .modules.images.dynamic_image_input import DynamicImageCombiner
from .modules.images.dynamic_mask_input import DynamicMaskCombiner
from .modules.images.image_resolution_adjuster import ImageResolutionAdjuster
from .modules.text.text_combiner import TextCombiner
from .modules.text.show_text_plus import ShowTextPlus
from .modules.text.simple_text_input import SimpleTextInput
from .modules.text.multiline_text_input import MultilineTextInput
from .modules.text.remove_empty_lines import RemoveEmptyLinesAndLeadingSpaces
from .modules.switch.switch_node import TextSwitch
from .modules.switch.switch_node import ImageSwitch
from .modules.switch.switch_node import MaskSwitch
from .modules.switch.switch_node import LatentSwitch
from .modules.web.web_image_loader import WebImageLoader
from .modules.images.image_base64_converter import ImageToBase64
from .modules.utils.output_converter import OutputToTextConverter




# 节点类映射
NODE_CLASS_MAPPINGS = {
    "PaintingCoder::MaskPreview": MaskPreview,
    "PaintingCoder::ImageSizeCreator": ImageSizeCreator,
    "PaintingCoder::ImageSizeCreatorPlus": ImageSizeCreatorPlus,
    "PaintingCoder::ImageToBase64": ImageToBase64,
    "PaintingCoder::ImageLatentCreator": ImageLatentCreator,
    "PaintingCoder::ImageLatentCreatorPlus": ImageLatentCreatorPlus,
    "PaintingCoder::DynamicImageCombiner": DynamicImageCombiner,
    "PaintingCoder::DynamicMaskCombiner": DynamicMaskCombiner,
    "PaintingCoder::ImageResolutionAdjuster": ImageResolutionAdjuster,
    "PaintingCoder::TextCombiner": TextCombiner,
    "PaintingCoder::ShowTextPlus": ShowTextPlus,
    "PaintingCoder::SimpleTextInput": SimpleTextInput,
    "PaintingCoder::MultilineTextInput": MultilineTextInput,
    "PaintingCoder::RemoveEmptyLinesAndLeadingSpaces": RemoveEmptyLinesAndLeadingSpaces,
    "PaintingCoder::TextSwitch": TextSwitch, 
    "PaintingCoder::MaskSwitch": MaskSwitch,
    "PaintingCoder::LatentSwitch": LatentSwitch,
    "PaintingCoder::WebImageLoader": WebImageLoader,
    "PaintingCoder::OutputToTextConverter": OutputToTextConverter,
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "PaintingCoder::MaskPreview": "Mask Preview 🎭",
    "PaintingCoder::ImageSizeCreator": "Image Size Creator 📏",
    "PaintingCoder::ImageSizeCreatorPlus": "Image Size Creator Plus ✨",
    "PaintingCoder::ImageLatentCreator": "Image Latent Creator 🎨",
    "PaintingCoder::ImageLatentCreatorPlus": "Image Latent Creator Plus ✨",
    "PaintingCoder::ImageToBase64": "Image To Base64 🎨", 
    "PaintingCoder::DynamicImageCombiner": "Dynamic Image Input 🖼️",
    "PaintingCoder::DynamicMaskCombiner": "Dynamic Mask Input 🎭",
    "PaintingCoder::ImageResolutionAdjuster": "Image Resolution Adjuster 📐",
    "PaintingCoder::TextCombiner": "Text Combiner ✍️",
    "PaintingCoder::ShowTextPlus": "Show Text Plus 📝",
    "PaintingCoder::SimpleTextInput": "Simple Text Input 📝",
    "PaintingCoder::MultilineTextInput": "Multiline Text Input 📝",
    "PaintingCoder::RemoveEmptyLinesAndLeadingSpaces": "Remove Empty Lines And Leading Spaces 📝",
    "PaintingCoder::TextSwitch": "Text Switch 🔄",
    "PaintingCoder::ImageSwitch": "Image Switch 🔄",
    "PaintingCoder::MaskSwitch": "Mask Switch 🔄",
    "PaintingCoder::LatentSwitch": "Latent Switch 🔄",
    "PaintingCoder::WebImageLoader": "Web Image Loader 🌐（URL Or Base64）",
    "PaintingCoder::OutputToTextConverter": "Output To Text Converter 📝",
}

# Web 目录配置
WEB_DIRECTORY = "./web"
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
