import torch

class ImageSwitch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "use_first": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
            },
            "_meta": {
                "preferred_width": 300,
                "maintain_dimensions": True
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "switch_image"
    CATEGORY = "🎨Painting👓Coder/🔄Switch"

    def switch_image(self, use_first, image_1=None, image_2=None):
        try:
            # 如果两个输入都为空，返回白色图像
            if image_1 is None and image_2 is None:
                return (torch.ones((1, 512, 512, 3)),)
            
            # 如果只有一个输入不为空，返回该输入
            if image_1 is None:
                return (image_2,)
            if image_2 is None:
                return (image_1,)
            
            # 根据use_first选择输出
            return (image_1,) if use_first else (image_2,)

        except Exception as e:
            print(f"Error in ImageSwitch: {str(e)}")
            # 发生错误时返回白色图像
            return (torch.ones((1, 512, 512, 3)),)

class TextSwitch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "use_first": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "text_1": ("STRING", {"multiline": True}),
                "text_2": ("STRING", {"multiline": True}),
            },
            "_meta": {
                "preferred_width": 300,
                "maintain_dimensions": True
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "switch_text"
    CATEGORY = "🎨Painting👓Coder/🔄Switch"

    def switch_text(self, use_first, text_1=None, text_2=None):
        try:
            # 如果两个输入都为空，返回空字符串
            if text_1 is None and text_2 is None:
                return ("",)
            
            # 如果只有一个输入不为空，返回该输入
            if text_1 is None:
                return (text_2 if text_2 is not None else "",)
            if text_2 is None:
                return (text_1 if text_1 is not None else "",)
            
            # 根据use_first选择输出
            return (text_1,) if use_first else (text_2,)

        except Exception as e:
            print(f"Error in TextSwitch: {str(e)}")
            # 发生错误时返回空字符串
            return ("",)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "ImageSwitch": ImageSwitch,
    "TextSwitch": TextSwitch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageSwitch": "Image Switch 🔄",
    "TextSwitch": "Text Switch 🔄"
} 