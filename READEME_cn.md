# ComfyUI PaintingCoderUtils Nodes

一个为 ComfyUI 设计的实用节点集合，提供了一系列便捷的图像处理工具。

## 🌟 特点

- 💡 简单易用
- 🛠️ 实用功能
- 🔌 完全兼容 ComfyUI
- 🎨 专注图像处理

## 📦 安装方法

1. 进入 ComfyUI 的 `custom_nodes` 目录
2. 下载 `ComfyUI_LaofuUtil` 文件夹
3. 重启 ComfyUI

## 📚 使用文档

请参考 `ComfyUI_LaofuUtil` 文件夹中的 `README.md` 文件。

bash
cd custom_nodes
git clone https://github.com/laofu-dev/ComfyUI_LaofuUtil.git


3. 重启 ComfyUI

## 🎯 功能节点

### 动态图片输入 (Dynamic Image Inputs)
将多个图片输入合并为一个列表输出的工具节点。

特点：
- 支持动态增减图片输入端口
- 自动忽略未连接的输入端口
- 输出统一的图片列表格式

使用场景：
- 批量处理多张图片
- 合并多个图片源
- 为需要图片列表输入的节点提供数据

### 移除空行 (Remove Empty Lines)
文本处理工具，用于清理文本中的空行。

特点：
- 支持移除空行
- 支持移除首尾空格
- 灵活的输出格式选项

## 🎨 使用示例

### 动态图片输入节点
1. 将节点添加到工作流
2. 连接图片到输入端口
3. 输出的图片列表可用于后续处理

### 移除空行节点
1. 输入需要处理的文本
2. 选择处理选项
3. 获取处理后的文本

## 🔧 开发说明

### 项目结构


├── __init__.py
├── dynamic_image_input.py
├── remove_empty_lines.py
├── README.md
└── LICENSE

### 添加新节点
1. 在项目目录创建新的 Python 文件
2. 实现节点类
3. 在 `__init__.py` 中注册节点

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

- GitHub: [你的GitHub主页]
- Email: [你的邮箱]

## 🙏 致谢

- ComfyUI 团队
- Impact-Pack 项目



这个 README：
