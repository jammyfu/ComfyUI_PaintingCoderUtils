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
import random
import folder_paths
from nodes import PreviewImage
import traceback

class WebImageLoader(PreviewImage):
    cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "cache")
    image_cache = {}
    
    def __init__(self):
        super().__init__()
        # 确保缓存目录存在
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_source": ("STRING", {"default": "", "multiline": True}),
                "use_cache": ("BOOLEAN", {"default": True}),
                "preview_enabled": ("BOOLEAN", {"default": True}),  # 重命名为 preview_enabled
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

    def get_filename(self):
        """生成临时文件名"""
        random_num = str(random.randint(0, 0xffffffff))
        return f"web_image_{random_num}.png"

    def get_subfolder(self):
        """获取子文件夹路径"""
        return self.output_dir

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

    def process_single_source(self, source: str, use_cache: bool) -> Union[Image.Image, None]:
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
                return None

            if use_cache and image is not None:
                self.save_to_cache(image, cache_path)

            return image

        except Exception as e:
            print(f"Error processing source: {str(e)}")
            return None

    def load_image(self, image_source: str, use_cache: bool, preview_enabled: bool = True):
        try:
            # 如果输入为空，返回空列表
            if not image_source.strip():
                empty_result = torch.ones((1, 1024, 1024, 3))
                return {"ui": {"images": []}, "result": (empty_result,)}

            # 分割多行输入
            sources = [s.strip() for s in image_source.split('\n') if s.strip()]
            if not sources:
                empty_result = torch.ones((1, 1024, 1024, 3))
                return {"ui": {"images": []}, "result": (empty_result,)}
            
            # 处理所有图像源
            tensors = []  # 存储最终的tensor列表
            preview_results = []
            
            for i, source in enumerate(sources):
                current_image = None
                current_tensor = None
                
                try:
                    # 尝试处理单个图像
                    image = self.process_single_source(source, use_cache)
                    if image is None:  # 如果处理结果为空
                        raise Exception("Failed to load image")
                    
                    # 直接使用 PIL Image 对象
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    # 转换为 numpy 数组并创建 tensor
                    img_array = np.array(image)
                    current_tensor = torch.from_numpy(img_array).float() / 255.0
                    current_image = image
                    
                except Exception as e:
                    print(f"Error loading image {i+1}: {str(e)}")
                    # 创建错误提示图像
                    error_image = self.create_error_image()
                    img_array = np.array(error_image)
                    current_tensor = torch.from_numpy(img_array).float() / 255.0
                    current_image = error_image
                
                # 添加到tensor列表，确保维度正确
                if len(current_tensor.shape) == 2:
                    current_tensor = current_tensor.unsqueeze(-1).repeat(1, 1, 3)
                elif len(current_tensor.shape) == 3 and current_tensor.shape[-1] != 3:
                    current_tensor = current_tensor[..., :3]
                
                # 添加batch维度
                current_tensor = current_tensor.unsqueeze(0)
                
                # 只添加成功的图像到 tensors 列表
                if current_image is not None and not isinstance(current_image, Image.Image) or current_image != self.create_error_image():
                    tensors.append(current_tensor)
                
                # 生成预览图像
                if preview_enabled:
                    filename = self.get_filename()
                    subfolder = self.get_subfolder()
                    preview_path = f"{subfolder}/{filename}"
                    
                    # 保存预览图像
                    if current_image is not None:
                        current_image.save(preview_path)
                    else:
                        Image.fromarray((current_tensor.squeeze(0).numpy() * 255).astype(np.uint8)).save(preview_path)
                    
                    preview_results.append({
                        "filename": filename,
                        "subfolder": subfolder,
                        "type": self.type
                    })
            
            # 创建最终输出
            if tensors:
                # 将所有 tensor 沿 batch 维度拼接
                output_tensor = torch.cat(tensors, dim=0)
                return {"ui": {"images": preview_results}, "result": (output_tensor,)}
            else:
                empty_result = torch.ones((1, 1024, 1024, 3))
                return {"ui": {"images": []}, "result": (empty_result,)}

        except Exception as e:
            print(f"Critical error in WebImageLoader: {str(e)}")
            traceback.print_exc()
            error_image = self.create_error_image()
            error_tensor = torch.from_numpy(np.array(error_image)).float() / 255.0
            return {"ui": {"images": []}, "result": (error_tensor.unsqueeze(0),)}

    @classmethod
    def IS_CHANGED(s, image_source: str, use_cache: bool, preview_enabled: bool) -> float:
        # 更新参数名为 preview_enabled
        return float(hash(f"{image_source}_{use_cache}_{preview_enabled}"))

    @classmethod
    def VALIDATE_INPUTS(s, image_source: str, use_cache: bool, preview_enabled: bool) -> bool:
        # 更新参数名为 preview_enabled
        return True

# 添加到 ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "WebImageLoader": WebImageLoader,
    "PaintingCoder::WebImageLoader": WebImageLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WebImageLoader": "Web Image Loader 🌐（URL Or Base64）",
    "PaintingCoder::WebImageLoader": "Web Image Loader 🌐（URL Or Base64）"
}
