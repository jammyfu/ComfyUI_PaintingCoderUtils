![Painting Coder Utilities Logo](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/paiting_coder_logo02.jpg)
# ComfyUI画画的程序员工具集节点

一个为 ComfyUI 设计的实用节点集合，旨在简化图像和文本处理工作流程。功能包括优化的分辨率调整、文本清理工具、动态图像/文本组合和蒙版预览工具。这个集合由一位喜欢绘画的程序员创建，非常适合希望提升 AI 艺术创作流程的艺术家和开发者。

[English](./README.md) | [简体中文](./README_CN.md)


# ⚠️ 重要更新说明

**版本0.3.0重大更新：**
- 修改了命名空间以提升兼容性
- 此更新会导致旧的工作流无法使用
- 请使用我们的工作流修复工具来修复现有工作流：

 ![工作流修复工具](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/workflow_fix_tools_cn.jpg)

  打开 [工作流修复工具](https://jammyfu.github.io/ComfyUI_PaintingCoderUtils/fix/workflow_fixer.html?lang=zh) 或者到目录 **ComfyUI_PaintingCoderUtils/docs/fix/** 寻找 **workflow_fixer.html** 并打开页面


- 新增功能：支持Windows与Unix(Linux/Mac)格式之间的路径分隔符转换
- 修复工具现在同时支持命名空间更新和路径格式转换


---


## 🎯 功能节点

### 📐图像分辨率调整器 (Image Resolution Adjuster)
一个用于按照 SDXL 最佳宽高比调整图像分辨率的实用节点。

![图像分辨率调整器设置](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/image_resolution_adjuster00.png)

图像分辨率调整，可自由设置填充背景颜色
![图像分辨率调整器设置](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/image_resolution_adjuster01.png)

图像按比例批量重绘
![图像按比例批量重绘](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/flux_batch_inpainting01.jpg)

### Flux图像按比例批量重绘工作流下载
<a href="https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/refs/heads/main/workflow/Flux_Image_Resolution_Adjuster_scale_up_batch_workflow.json" download="Flux_Image_Resolution_Adjuster_batch_workflow.json">⬇️ 下载工作流JSON（右键另存为）</a> 

特点：
- 支持所有 SDXL 最佳分辨率：
  - 1:1 (1024x1024)
  - 9:7 (1152x896)
  - 7:9 (896x1152)
  - 3:2 (1216x832)
  - 2:3 (832x1216)
  - 7:4 (1344x768)
  - 4:7 (768x1344)
  - 12:5 (1536x640)
  - 5:12 (640x1536)
- 多种延展模式：
  - contain: 保持比例缩放至目标尺寸内
  - cover: 保持比例缩放以覆盖目标尺寸
  - fill: 拉伸以填充目标尺寸
  - inside: 类似 contain，但只缩小不放大
  - outside: 类似 cover，但只放大不缩小
  - top/bottom/left/right/center: 在目标尺寸内定位图像
- 可调节的缩放系数
- 可配置的最大和最小分辨率限制
- 背景颜色选择器
- 调整时保持宽高比
### 图像描边功能 (Image Outline)
在图像分辨率调整器中新增了描边功能：
- 一键添加 1 像素宽的描边
- 描边颜色自动设置为背景色的反色
- 适用于所有延展模式
- 保持图像质量不变
- 自动调整输出尺寸（每边增加 1 像素）

使用方法：
1. 将节点添加到工作流
2. 从 SDXL 预设中选择目标分辨率
3. 根据需要选择延展模式
4. 使用颜色选择器设置背景颜色
5. 根据需要调整缩放系数和分辨率限制
6. 在图像分辨率调整器中找到 `add_outline` 选项
7. 设置为 `True` 启用描边
8. 描边颜色会自动根据 `background_color` 设置的背景色计算反色
9. 输出图像尺寸会自动调整（宽高各增加 2 像素）

### 🌐Web图像加载器 (Web Image Loader)
一个用于从网络加载图像的节点。

![Web图像加载器示例](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/web_image_loader01.png)
![Web图像加载器示例](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/web_image_loader02.png)

特点：
- 支持从URL加载图像,支持Base64格式
- 自动处理图像格式
- 支持批量图像加载
- 错误处理：
  - 无效URL时返回占位图像
  - 优雅处理异常，自动剔除错误图像

使用方法：
1. 将节点添加到工作流
2. 输入图像URL
3. 节点将自动加载并处理图像
4. 输出图像可连接到需要图像输入的其他节点

使用场景：
- 从网络资源加载图像
- 动态图像处理工作流
- 批量图像下载和处理

### 🖼️图像转Base64编码器 (Image to Base64 Encoder)
一个用于将图像转换为Base64编码的节点。

![图像转Base64编码器示例](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/image_to_base64.png)

特点：
- 支持多种图像格式（JPEG, PNG, BMP等）
- 自动处理图像大小和格式
- 支持批量图像编码
- 错误处理：
  - 无效图像时返回错误信息
  - 优雅处理异常，确保工作流不中断

使用方法：
1. 将节点添加到工作流
2. 输入图像文件或图像路径
3. 节点将自动将图像转换为Base64编码
4. 输出Base64编码字符串可连接到需要Base64输入的其他节点

使用场景：
- 图像数据传输
- 图像嵌入HTML或JSON
- 动态图像处理工作流
- 批量图像编码和处理

### 🔀 Switch节点（Image Switch,Text Switch）
Switch节点用于在工作流中动态切换不同的输入或输出路径。

![Switch节点](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/switch_nodes_01.png)

特点：
- 支持多种输入和输出类型
- 可配置的切换条件
- 自动处理输入输出连接

使用方法：
1. 将Switch节点添加到工作流
2. 配置切换条件（如布尔值、数值范围等）
3. 连接不同的输入和输出路径
4. 根据条件自动切换路径

使用场景：
- 动态调整工作流
- 条件分支处理
- 多路径选择


### 🖼️图像尺寸创建器 (Image Size Creator)
一个用于创建图像尺寸的节点。

![图像尺寸创建器](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/image_size_creator01.png)

特点：
- 支持所有SDXL最优分辨率：
  - 1:1 (1024x1024)
  - 9:7 (1152x896)
  - 7:9 (896x1152)
  - 3:2 (1216x832)
  - 2:3 (832x1216)
  - 7:4 (1344x768)
  - 4:7 (768x1344)
  - 12:5 (1536x640)
  - 5:12 (640x1536)
- 可调节的缩放因子
- 支持横向、纵向和方形模式
- 自动计算最佳分辨率

使用方法：
1. 将节点添加到工作流
2. 选择图像模式(横向/纵向/方形)
3. 选择目标分辨率
4. 调整缩放因子(可选)

使用场景：
- 创建特定尺寸的图像
- SDXL图像生成优化
- 批量图像处理工作流

### 🖼️图像潜空间创建器 (Image Latent Creator)
一个用于创建空的图像潜空间的节点。

![图像潜空间创建器](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/image_latent_creator01.png)
特点：
- 继承图像尺寸创建器的所有功能
- 支持批量大小设置
- 自动创建优化的潜空间尺寸
- 支持额外的PNG信息

使用方法：
1. 将节点添加到工作流
2. 设置所需的图像尺寸参数
3. 设置批量大小
4. 连接到需要潜空间输入的节点

使用场景：
- 创建空白潜空间
- SDXL工作流初始化
- 批量图像生成
- 自定义潜空间处理



### ✂️空行和前导空格清理器 (Remove Empty Lines And Leading Spaces)
一个用于清理文本中的空行和前导/尾随空格的文本处理节点。

![空行和前导空格清理器](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/rm_line_and_space_cn00.png)

特点：
- 移除文本中的空行
- 移除行首和行尾的空格
- 可选择保留段落之间的单个空行
- 可选择保留缩进
- 支持批量文本处理

使用示例：
```
输入文本：
    你好世界    
  
     这是一个测试    
  
  
    上面有多个空行    

输出文本（使用默认设置）：
你好世界
这是一个测试
上面有多个空行
```

参数说明：
- `output type`：输出类型(文本、列表)
- `remove empty line option`：移除空行
- `remove loading space option`：移除空格

使用场景：
- 清理提示词文本
- 格式化 LoRA 训练文本
- 准备文生图的输入文本
- 标准化文本输入格式

清除多余的空行及空格生成文本：
![清除多余的空行及空格生成文本](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/rm_line_and_space_cn01.png)

清除空行保留空格生成文本：
![清除空行保留空格生成文本](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/rm_line_and_space_cn02.png)

清除空格保留空号生成文本：
![清除空格保留空号生成文本](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/rm_line_and_space_cn03.png)

清除空行、空格生成列表：
![清除空行、空格生成列表](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/rm_line_and_space_cn04.png)



### 🔗文本组合器（TextCombiner）✨
新增文本组合器节点，可以将多个文本输入组合成一个文本输出。
![新增文本组合器节点，可以将多个文本输入组合成一个文本输出。](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/text_combiner01.png)

功能特点：
- 支持动态输入：连接输入时自动增加新的输入点
- 灵活的分隔符：
  - 支持正则表达式
  - 支持转义字符（如 \n, \r）
  - 留空则使用空格连接
- 智能换行：当分隔符包含换行符时，自动按行分割输出
- 自动过滤：移除空行，保留纯空格内容

使用示例：
1. 基本用法：
   - 使用逗号分隔：`,`
   - 输出：text1, text2, text3

2. 换行分隔：
   - 使用换行符：`\n`
   - 输出：
     ```
     text1
     text2
     text3
     ```

3. 混合分隔：
   - 使用逗号或换行：`,|\n`
   - 支持两种分隔方式

4. 空分隔符：
   - 留空
   - 直接用空格连接文本


### 🖼️动态图像输入组合器 (Dynamic Image Input)
一个用于动态组合多个图像输入的节点。
![一个用于动态组合多个图像输入的节点](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/dynamic_image_combiner01.png)

特点：
- 动态输入端口：连接时自动增加新的图像输入点
- 智能图像处理：
  - 自动过滤空输入
  - 保持图像格式和质量
  - 支持批量图像处理
- 错误处理：
  - 当没有有效输入时返回空白图像
  - 优雅处理异常情况
- 输出格式：返回图像列表，便于后续处理

使用方法：
1. 将节点添加到工作流
2. 连接图像输入（会自动创建新的输入端口）
3. 节点将自动组合所有非空图像输入
4. 输出可以连接到需要图像列表的其他节点

使用场景：
- 批量图像处理
- 图像集合管理
- 动态工作流构建
- 图像列表生成



### 📝文本显示增强器 (Show Text Plus)
一个增强型的文本显示节点，提供更多文本格式化和显示选项。

![文本显示增强器示例](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/muti_text_and_show_text_plus01.jpg)

特点：
- 关闭显示模式：
  - 普通模式：直接显示文本
- 文本统计功能：
  - 字符数统计
  - 单词数统计
  - 行数统计
- 支持长文本自动换行
- 支持多语言文本

使用方法：
1. 将节点添加到工作流
2. 连接文本输入
3. 选择显示模式

### 📝多行文本输入器 (Multiline Text)
一个支持多行文本输入的节点，方便输入和编辑长文本内容。

![多行文本输入器示例](docs/images/muti_text_and_show_text_plus01.jpg)

特点：
- 支持多行文本输入和编辑
- 保留文本格式和换行
- 兼容中英文输入
- 方便的文本编辑界面
- 支持复制粘贴操作

使用方法：
1. 将节点添加到工作流
2. 双击文本框进行编辑
3. 支持直接粘贴多行文本
4. 编辑完成后点击其他区域保存

使用场景：
- 输入长篇提示词
- 编辑多行描述文本
- 批量文本处理
- LoRA 训练文本准备



### 🎭蒙版预览器 (Mask Preview)
一个用于预览和检查图像蒙版的实用节点。

![蒙版预览器示例](https://raw.githubusercontent.com/jammyfu/ComfyUI_PaintingCoderUtils/main/docs/images/mask_preview01.png)

特点：
- 直观显示蒙版区域
- 支持多种预览模式：
  - 原始蒙版
  - 轮廓高亮
- 支持批量蒙版预览
- 实时更新预览效果

使用方法：
1. 将节点添加到工作流
2. 连接蒙版输入
3. 选择预览模式
4. 调整显示参数

## 📦 安装方法

1. 进入 ComfyUI 的 `custom_nodes` 目录
2. 克隆仓库：
   ```bash
   cd custom_nodes
   git clone https://github.com/jammyfu/ComfyUI_PaintingCoderUtils.git
   ```
3. 重启 ComfyUI


## 📝 许可证

MIT License

## 🤝 更新说明
### v0.3.2 (2025-01-22)
- **改进:**
  - 完善了工作流修复工具，增加了更多的错误处理和提示信息
  - 优化了用户界面，使操作更加直观
  - 增加了对更多节点类型的支持
  - 提升了路径分隔符转换功能的稳定性
  - 修复了在某些情况下无法正确加载 JSON 文件的问题

### v0.3.1 (2025-01-22)
- **Bug修复:**
  - 修复了文本组合器在处理特殊字符时的崩溃问题
  - 修复了动态图像输入节点在某些情况下未正确处理输入的问题
  - 修复了蒙版预览器在批量预览时的显示错误
  - 修复了路径分隔符转换功能在某些系统上的兼容性问题
  - 修复了图像分辨率调整器在特定分辨率下的处理错误


### v0.3.0 (2025-01-21)
- **重大变更:**
  - 修改了命名空间结构以提高兼容性
  - 添加了工作流修复工具以便迁移
  - 增加了路径分隔符转换功能
  - 增强了错误处理和用户反馈
  - 改善了跨平台兼容性

### v0.2.2 (2024-01-09)
- 新增 Mask Switch 节点
  - 支持根据条件在两个蒙版之间切换
  - 提供默认空白蒙版处理
  - 优化异常处理机制
  - 保持蒙版格式和质量

### v0.2.1 (2024-01-07)
- 新增 Web图像加载器 节点
  - 支持从 URL 和 Base64 加载图像
  - 自动处理图像格式
  - 支持批量图像加载
  - 错误处理：无效 URL 时返回占位图像，优雅处理异常
  - 支持缓存功能，提升加载效率
  - 预览功能：生成预览图像并保存

### v0.2.0 (2024-01-06)
- 新增图像切换器节点
  - 支持根据条件在两个图像之间切换
  - 提供默认空白图像处理
  - 优化异常处理机制
  - 保持图像格式和质量

- 新增文本切换器节点
  - 支持根据条件在两个文本之间切换
  - 提供默认空白文本处理
  - 优化异常处理机制
  - 保持文本格式和内容

### v0.1.9 (2024-01-05)
- 优化图像分辨率调整器
  - 新增蒙版羽化(feather)功能
  - 改进蒙版边缘处理算法
  - 提升蒙版处理性能
  - 优化边缘平滑效果

### v0.1.8 (2024-01-04)
- 优化文本组合器
  - 改进文本拼接逻辑
  - 提升处理大量文本的性能
  - 修复特殊字符处理问题
  - 优化内存占用

### v0.1.7 (2024-01-03)
- 优化图像分辨率调整器
  - 改进延展模式算法
  - 提升图像处理性能
  - 修复边缘处理问题
  - 优化内存使用

### v0.1.6 (2024-01-02)
- 新增多行文本输入器节点
  - 支持多行文本输入和编辑
  - 保留文本格式和换行
  - 兼容中英文输入
  - 方便的文本编辑界面
  - 支持复制粘贴操作


### v0.1.5 (2024-12-28)
- 新增 Mask Preview 蒙版预览器节点
  - 实现实时预览功能
  - 支持批量蒙版处理


### v0.1.4 (2024-12-27)
- 新增 Show Text Plus 节点
  - 添加多种显示模式
  - 优化长文本显示效果


### v0.1.3 (2024-12-26)
- 新增动态图像输入组合器
  - 实现动态输入端口
  - 添加智能图像处理
  - 优化错误处理机制
  - 支持图像列表输出 


### v0.1.2 (2024-12-25)
- 新增图像描边功能
- 新增文本组合器节点 


### v0.1.1 (2024-12-25)
- 新增 TextCombiner 节点
  - 实现动态输入连接点
  - 支持正则表达式分隔符
  - 支持换行符和转义字符
  - 添加空分隔符处理
  - 优化文本拼接逻辑

### v0.1.0 (2024-12-23)
- 首次发布
- 添加图像分辨率调整器：
  - 支持 SDXL 最佳分辨率
  - 多种延展模式
  - 背景颜色选择器
  - 缩放系数调整
  - 分辨率限制
- 添加空行和前导空格清理器：
  - 文本清理功能
  - 可配置的保留选项
  - 批量处理支持

### 计划功能
- 动态图像输入组合
- 文本模板系统
- 更多图像处理工具

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 🙏 致谢

- ComfyUI 团队
- Impact-Pack 项目
