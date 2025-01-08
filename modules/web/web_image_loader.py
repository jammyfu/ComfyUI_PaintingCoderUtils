import torch
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import os
import hashlib
import base64
import re
import numpy as np
from typing import Tuple, Union, List

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

    def create_error_image(self) -> Image.Image:
        """创建错误提示图像"""
        # 创建白色背景图像
        img = Image.new('RGB', (512, 512), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            # 尝试加载系统字体
            font_size = 40
            try:
                # 尝试加载微软雅黑（Windows）
                font = ImageFont.truetype("msyh.ttc", font_size)
            except:
                try:
                    # 尝试加载PingFang（MacOS）
                    font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
                except:
                    # 使用默认字体
                    font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()

        # 错误信息
        error_message = "Load Image Error"
        text_color = (255, 0, 0)  # 红色
        
        # 计算文本大小以居中显示
        try:
            text_bbox = draw.textbbox((0, 0), error_message, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except:
            # 如果无法获取文本大小，使用估计值
            text_width = len(error_message) * font_size * 0.6
            text_height = font_size

        # 计算居中位置
        x = (512 - text_width) / 2
        y = (512 - text_height) / 2
        
        # 绘制文本
        draw.text((x, y), error_message, fill=text_color, font=font)
        
        # 绘制红色边框
        draw.rectangle([(0, 0), (511, 511)], outline=text_color, width=2)
        
        return img

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
            print(f"Error loading URL: {str(e)}")
            return self.create_error_image()

    def decode_base64(self, base64_str: str) -> Image.Image:
        """解码base64图像"""
        try:
            # 移除header
            base64_data = re.sub(r'^data:image/[a-zA-Z]+;base64,', '', base64_str)
            # 解码
            image_data = base64.b64decode(base64_data)
            return Image.open(io.BytesIO(image_data)).convert('RGB')
        except Exception as e:
            print(f"Error decoding Base64: {str(e)}")
            return self.create_error_image()

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

    def process_single_source(self, source: str, use_cache: bool) -> Image.Image:
        """处理单个图像源"""
        try:
            cache_path = self.get_cache_path(source)
            image = None

            # 尝试从缓存加载
            if use_cache:
                cache_exists, cached_image = self.load_from_cache(cache_path)
                if cache_exists:
                    return cached_image

            # 如果没有缓存或不使用缓存，根据输入类型加载
            if self.is_url(source):
                image = self.download_image(source)
            elif self.is_base64(source):
                image = self.decode_base64(source)
            else:
                print(f"Invalid image source format: {source}")
                return self.create_error_image()

            if use_cache and image is not None:
                self.save_to_cache(image, cache_path)

            return image

        except Exception as e:
            print(f"Error processing source: {str(e)}")
            return self.create_error_image()

    def load_image(self, image_source: str, use_cache: bool) -> Tuple[torch.Tensor]:
        """主要加载函数"""
        try:
            # 如果输入为空，返回1024x1024的白色图像
            if not image_source.strip():
                return (torch.ones((1, 1024, 1024, 3)),)

            # 分割多行输入
            sources = [s.strip() for s in image_source.split('\n') if s.strip()]
            
            # 处理所有图像源
            images = []
            for source in sources:
                image = self.process_single_source(source, use_cache)
                images.append(np.array(image))

            # 转换为tensor
            if not images:
                return (torch.ones((1, 1024, 1024, 3)),)
            
            image_tensors = [torch.from_numpy(img).float() / 255.0 for img in images]
            # 堆叠所有图像
            stacked_tensor = torch.stack(image_tensors)
            
            return (stacked_tensor,)

        except Exception as e:
            print(f"Error in WebImageLoader: {str(e)}")
            error_image = self.create_error_image()
            image_tensor = torch.from_numpy(np.array(error_image)).float() / 255.0
            return (image_tensor.unsqueeze(0),)

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "WebImageLoader": WebImageLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WebImageLoader": "Web Image Loader 🌐（URL Or Base64）"
} 