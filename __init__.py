from .image_scale_calculator import ImageScaleCalculator
from .remove_empty_lines import RemoveEmptyLinesAndLeadingSpaces
from .remove_empty_lines_advance import RemoveEmptyLinesAndLeadingSpacesAdvance
from .dynamic_image_input import DynamicImageInputs

# 可以在此处添加任何初始化代码

# 节点类映射
NODE_CLASS_MAPPINGS = {
    "ImageScaleCalculator": ImageScaleCalculator,
    "RemoveEmptyLinesAndLeadingSpaces": RemoveEmptyLinesAndLeadingSpaces,
    "RemoveEmptyLinesAndLeadingSpacesAdvance": RemoveEmptyLinesAndLeadingSpacesAdvance,
    "DynamicImageInputs": DynamicImageInputs
}

# 友好/人类可读的节点标题映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageScaleCalculator": "Image Scale Calculator Node",
    "RemoveEmptyLinesAndLeadingSpaces": "Remove Empty Lines & Leading Spaces",
    "RemoveEmptyLinesAndLeadingSpacesAdvance": "Remove Empty Lines & Leading Spaces Advance",
    "DynamicImageInputs": "Dynamic Image Inputs"
}

# 你可以在此处添加更多的配置或注册逻辑
