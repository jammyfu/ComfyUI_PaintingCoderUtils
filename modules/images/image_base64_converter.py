import base64
import io
from PIL import Image
import numpy as np
import traceback

class ImageToBase64:
    """将图片转换为 base64 格式的节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),  # ComfyUI 的图片格式
            },
            "optional": {
                "add_data_uri": ("BOOLEAN", {"default": True}),  # 控制是否添加 data URI 前缀
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("base64_images",)
    FUNCTION = "convert_to_base64"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def convert_to_base64(self, images, add_data_uri=True):
        try:
            # 转换图片格式
            if len(images.shape) == 3:
                # 单张图片，增加批次维度
                images = images[None, ...]
            
            base64_list = []
            
            # 处理每张图片
            for img in images:
                # 将 PyTorch Tensor 转换为 numpy 数组
                img_np = img.cpu().numpy()
                
                # 将 numpy 数组转换为 PIL Image
                img_np = (img_np * 255).astype(np.uint8)
                pil_image = Image.fromarray(img_np)
                
                # 将图片转换为 base64
                buffered = io.BytesIO()
                pil_image.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                # 根据参数决定是否添加 data URI 前缀
                if add_data_uri:
                    img_base64 = f"data:image/png;base64,{img_base64}"
                    
                base64_list.append(img_base64)
            
            # 如果只有一张图片，返回字符串；否则返回列表
            result = base64_list[0] if len(base64_list) == 1 else base64_list
            
            # 确保返回的是元组
            return (result,)
            
        except Exception as e:
            return ("",)  # 发生错误时返回空字符串