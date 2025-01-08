import torch
import requests
from PIL import Image
import io
import os
import hashlib
import time
from typing import Tuple

class WebImageLoader:
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "cache")
    image_cache = {}
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING", {"default": "", "multiline": False}),
                "use_cache": ("BOOLEAN", {"default": True}),
            },
            "_meta": {
                "preferred_width": 300,
                "maintain_dimensions": True
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "load_image"
    CATEGORY = "🎨Painting👓Coder/🌐Web"

    def __init__(self):
        # 确保缓存目录存在
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_cache_path(self, url: str) -> str:
        """生成缓存文件路径"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{url_hash}.png")

    def download_image(self, url: str) -> Image.Image:
        """从URL下载图像"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content)).convert('RGB')
        except Exception as e:
            print(f"Error downloading image from {url}: {str(e)}")
            # 返回1x1的红色图像作为错误提示
            return Image.new('RGB', (1, 1), color='red')

    def save_to_cache(self, image: Image.Image, cache_path: str):
        """保存图像到缓存"""
        try:
            image.save(cache_path, "PNG")
        except Exception as e:
            print(f"Error saving cache: {str(e)}")

    def load_from_cache(self, cache_path: str) -> Tuple[bool, Image.Image]:
        """从缓存加载图像"""
        try:
            if os.path.exists(cache_path):
                return True, Image.open(cache_path).convert('RGB')
        except Exception as e:
            print(f"Error loading cache: {str(e)}")
        return False, None

    def load_image(self, url: str, use_cache: bool) -> Tuple[torch.Tensor]:
        """主要加载函数"""
        try:
            if not url.strip():
                # 返回1x1的灰色图像作为空URL提示
                return (torch.ones((1, 1, 1, 3)) * 0.5,)

            cache_path = self.get_cache_path(url)
            image = None

            # 尝试从缓存加载
            if use_cache:
                cache_exists, cached_image = self.load_from_cache(cache_path)
                if cache_exists:
                    image = cached_image

            # 如果没有缓存或不使用缓存，从URL下载
            if image is None:
                image = self.download_image(url)
                if use_cache:
                    self.save_to_cache(image, cache_path)

            # 转换为tensor
            image_tensor = torch.from_numpy(np.array(image)).float() / 255.0
            image_tensor = image_tensor.unsqueeze(0)
            
            return (image_tensor,)

        except Exception as e:
            print(f"Error in WebImageLoader: {str(e)}")
            # 返回1x1的红色图像作为错误提示
            return (torch.tensor([[[[1.0, 0.0, 0.0]]]]),)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "WebImageLoader": WebImageLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WebImageLoader": "Web Image Loader 🌐"
} 