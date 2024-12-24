class DynamicImageInputs:
    """动态图片输入节点
    
    这个节点允许动态添加多个图片输入端口，并将所有输入的图片合并成一个列表输出。
    
    特点：
    1. 支持动态增减图片输入端口
    2. 自动忽略未连接的输入端口
    3. 输出一个包含所有输入图片的列表
    
    使用方法：
    1. 将节点添加到工作流中
    2. 连接图片到输入端口
    3. 使用 get_input 方法动态增加更多输入端口
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义节点的输入类型
        
        Returns:
            dict: 包含默认的单个图片输入端口
        """
        return {"required": {"image_1": ("IMAGE",)}}

    RETURN_TYPES = ("IMAGE",)    # 返回图片类型
    RETURN_NAMES = ("images",)   # 输出端口名称
    OUTPUT_IS_LIST = (True,)     # 标记输出为列表类型
    FUNCTION = "process_images"   # 处理函数名称
    CATEGORY = "🎨Painting👓Coder/🖼️Image"  # 节点分类

    def process_images(self, **kwargs):
        """处理所有输入的图片
        
        Args:
            **kwargs: 包含所有输入图片的字典，键名格式为 "image_1", "image_2" 等
            
        Returns:
            tuple: 包含所有输入图片的列表
        """
        images = []
        for k, v in kwargs.items():
            if k.startswith("image_") and v is not None:
                images.append(v)
        return (images,)