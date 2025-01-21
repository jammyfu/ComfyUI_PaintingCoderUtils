import torch
import numpy as np
from PIL import Image
import random
import folder_paths
from nodes import PreviewImage

class MaskPreview(PreviewImage):
    """预览mask的节点"""
    
    def __init__(self):
        super().__init__()
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "masks": ("MASK",),  # 改为复数形式，表示支持列表
                "preview_enabled": ("BOOLEAN", {"default": True}),  # 添加预览开关
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("MASK", "IMAGE",)  # 同时返回mask和image
    RETURN_NAMES = ("masks", "images",)  # 指定返回值名称
    OUTPUT_IS_LIST = (True, True)  # 标记输出为列表
    FUNCTION = "preview_mask"
    CATEGORY = "🎨Painting👓Coder/🖼️Image"

    def get_filename(self):
        """生成临时文件名"""
        random_num = str(random.randint(0, 0xffffffff))
        return f"mask_preview_{random_num}.png"

    def get_subfolder(self):
        """获取子文件夹路径"""
        return self.output_dir

    def preview_mask(self, masks, preview_enabled=True, prompt=None, extra_pnginfo=None):
        # 确保masks是列表或批次格式
        if len(masks.shape) == 2:
            masks = masks.unsqueeze(0)
        
        preview_results = []
        converted_images = []
        converted_masks = []
        
        # 处理每个mask
        for i in range(masks.shape[0]):
            mask = masks[i]
            
            mask_tensor = mask.unsqueeze(0)
            mask_tensor = torch.clamp(mask_tensor, 0, 1)
            converted_images.append(mask_tensor)
            converted_masks.append(mask)
            
            # 只在启用预览时生成预览图像
            if preview_enabled:
                preview_img = (mask.cpu().numpy() * 255).astype(np.uint8)
                pil_image = Image.fromarray(preview_img, mode='L')
                filename = self.get_filename()
                subfolder = self.get_subfolder()
                preview_path = f"{subfolder}/{filename}"
                pil_image.save(preview_path)
                preview_results.append({
                    "filename": filename,
                    "subfolder": subfolder,
                    "type": self.type
                })
        
        # 返回结果
        return {"ui": {"images": preview_results}, 
                "result": (converted_masks, converted_images,)} 