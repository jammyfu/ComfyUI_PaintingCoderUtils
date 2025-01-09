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

class MaskSwitch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "use_first": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "mask_1": ("MASK",),
                "mask_2": ("MASK",),
            },
            "_meta": {
                "preferred_width": 300,
                "maintain_dimensions": True
            }
        }
    
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    FUNCTION = "switch_mask"
    CATEGORY = "🎨Painting👓Coder/🔄Switch"

    def switch_mask(self, use_first, mask_1=None, mask_2=None):
        try:
            # 创建空白掩码作为默认值
            empty_mask = torch.zeros((1, 1024, 1024))
            
            # 如果两个输入都为空，返回空白掩码
            if mask_1 is None and mask_2 is None:
                return (empty_mask,)
            
            # 根据use_first选择输出
            if use_first:
                return (mask_1,) if mask_1 is not None else (empty_mask,)
            else:
                return (mask_2,) if mask_2 is not None else (empty_mask,)

        except Exception as e:
            print(f"Error in MaskSwitch: {str(e)}")
            return (torch.zeros((1, 512, 512)),)

class LatentSwitch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "use_first": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "latent_1": ("LATENT",),
                "latent_2": ("LATENT",),
            },
            "_meta": {
                "preferred_width": 300,
                "maintain_dimensions": True
            }
        }
    
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    FUNCTION = "switch_latent"
    CATEGORY = "🎨Painting👓Coder/🔄Switch"

    def switch_latent(self, use_first, latent_1=None, latent_2=None):
        try:
            # 创建空白latent作为默认值
            empty_latent = {
                "samples": torch.zeros((1, 4, 64, 64)),
                "batch_size": 1
            }
            
            # 如果两个输入都为空，返回空白latent
            if latent_1 is None and latent_2 is None:
                return (empty_latent,)
            
            # 根据use_first选择输出
            if use_first:
                return (latent_1,) if latent_1 is not None else (empty_latent,)
            else:
                return (latent_2,) if latent_2 is not None else (empty_latent,)

        except Exception as e:
            print(f"Error in LatentSwitch: {str(e)}")
            return (empty_latent,)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "ImageSwitch": ImageSwitch,
    "TextSwitch": TextSwitch,
    "MaskSwitch": MaskSwitch,
    "LatentSwitch": LatentSwitch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageSwitch": "Image Switch 🔄",
    "TextSwitch": "Text Switch 🔄",
    "MaskSwitch": "Mask Switch 🔄",
    "LatentSwitch": "Latent Switch 🔄"
} 