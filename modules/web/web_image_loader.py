import torch
import requests
from PIL import Image
import io
import os
import hashlib
import base64
import re
import numpy as np
from typing import Tuple, Union

class WebImageLoader:
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "cache")
    image_cache = {}
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_source": ("STRING", {"default": "", "multiline": True}),
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

    def is_url(self, text: str) -> bool:
        """判断是否为URL"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(text))

    def is_base64(self, text: str) -> bool:
        """判断是否为base64图像"""
        pattern = r'^data:image/[a-zA-Z]+;base64,'
        return bool(re.match(pattern, text))

    def get_cache_path(self, source: str) -> str:
        """生成缓存文件路径"""
        source_hash = hashlib.md5(source.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{source_hash}.png")

    def download_image(self, url: str) -> Image.Image:
        """从URL下载图像"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content)).convert('RGB')
        except Exception as e:
            print(f"Error downloading image from {url}: {str(e)}")
            return Image.new('RGB', (1, 1), color='red')

    def decode_base64(self, base64_str: str) -> Image.Image:
        """解码base64图像"""
        try:
            # 移除header
            base64_data = re.sub(r'^data:image/[a-zA-Z]+;base64,', '', base64_str)
            # 解码
            image_data = base64.b64decode(base64_data)
            return Image.open(io.BytesIO(image_data)).convert('RGB')
        except Exception as e:
            print(f"Error decoding base64 image: {str(e)}")
            return Image.new('RGB', (1, 1), color='red')

    def save_to_cache(self, image: Image.Image, cache_path: str):
        """保存图像到缓存"""
        try:
            image.save(cache_path, "PNG")
        except Exception as e:
            print(f"Error saving cache: {str(e)}")

    def load_from_cache(self, cache_path: str) -> Tuple[bool, Union[Image.Image, None]]:
        """从缓存加载图像"""
        try:
            if os.path.exists(cache_path):
                return True, Image.open(cache_path).convert('RGB')
        except Exception as e:
            print(f"Error loading cache: {str(e)}")
        return False, None

    def load_image(self, image_source: str, use_cache: bool) -> Tuple[torch.Tensor]:
        """主要加载函数"""
        try:
            # 如果输入为空，返回1024x1024的白色图像
            if not image_source.strip():
                return (torch.ones((1, 1024, 1024, 3)),)

            cache_path = self.get_cache_path(image_source)
            image = None

            # 尝试从缓存加载
            if use_cache:
                cache_exists, cached_image = self.load_from_cache(cache_path)
                if cache_exists:
                    image = cached_image

            # 如果没有缓存或不使用缓存，根据输入类型加载
            if image is None:
                if self.is_url(image_source):
                    image = self.download_image(image_source)
                elif self.is_base64(image_source):
                    image = self.decode_base64(image_source)
                else:
                    print("Invalid image source format")
                    return (torch.ones((1, 1024, 1024, 3)),)  # 返回白色图像

                if use_cache:
                    self.save_to_cache(image, cache_path)

            # 转换为tensor
            image_tensor = torch.from_numpy(np.array(image)).float() / 255.0
            image_tensor = image_tensor.unsqueeze(0)
            
            return (image_tensor,)

        except Exception as e:
            print(f"Error in WebImageLoader: {str(e)}")
            # 返回1024x1024的白色图像作为错误提示
            return (torch.ones((1, 1024, 1024, 3)),)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "WebImageLoader": WebImageLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WebImageLoader": "Web Image Loader 🌐"
} 