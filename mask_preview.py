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
        
        # 处理每个mask
        for i in range(masks.shape[0]):
            mask = masks[i]
            
            # 将mask转换为3通道图像
            mask_np = mask.cpu().numpy()
            mask_rgb = np.stack([mask_np, mask_np, mask_np], axis=2)  # 改为HWC格式
            
            # 确保值在0-255范围内
            mask_rgb = (mask_rgb * 255).astype(np.uint8)
            
            # 创建PIL图像
            pil_image = Image.fromarray(mask_rgb)
            
            # 转换回tensor格式（CHW格式）
            mask_tensor = torch.from_numpy(np.array(pil_image)).float() / 255.0
            mask_tensor = mask_tensor.permute(2, 0, 1)
            converted_images.append(mask_tensor)
            
            # 如果启用预览，则生成预览图像
            if preview_enabled:
                # 生成预览
                filename = self.get_filename()
                subfolder = self.get_subfolder()
                
                # 保存图像
                preview_path = f"{subfolder}/{filename}"
                pil_image.save(preview_path)
                
                # 添加到预览结果
                preview_results.append({
                    "filename": filename,
                    "subfolder": subfolder,
                    "type": self.type
                })
        
        # 将转换后的图像堆叠为批次
        converted_images = torch.stack(converted_images) if converted_images else None
        
        # 根据预览开关返回不同的结果
        if preview_enabled:
            return {"ui": {"images": preview_results}, 
                    "result": (masks, converted_images,)}
        else:
            return {"result": (masks, converted_images,)} 