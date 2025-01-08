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
            # 创建空白图像作为默认值
            empty_image = torch.ones((1, 1024, 1024, 3))
            
            # 如果两个输入都为空，返回空白图像
            if image_1 is None and image_2 is None:
                return (empty_image,)
            
            # 根据use_first选择输出
            if use_first:
                return (image_1,) if image_1 is not None else (empty_image,)
            else:
                return (image_2,) if image_2 is not None else (empty_image,)

        except Exception as e:
            print(f"Error in ImageSwitch: {str(e)}")
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
            
            # 根据use_first选择输出
            if use_first:
                return (text_1,) if text_1 is not None else ("",)
            else:
                return (text_2,) if text_2 is not None else ("",)

        except Exception as e:
            print(f"Error in TextSwitch: {str(e)}")
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