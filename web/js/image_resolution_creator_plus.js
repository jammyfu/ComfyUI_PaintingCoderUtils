import { app } from "../../../scripts/app.js";
import { setupSizeNode } from "./image_size_base.js";

// SDXL分辨率选项
const sdxlResolutionOptions = {
    "Landscape": [
        "9:7 (1152x896)",   // 比例约 1.29
        "3:2 (1216x832)",   // 比例 1.50
        "7:4 (1344x768)",   // 比例 1.75
        "12:5 (1536x640)",  // 比例 2.40
    ],
    "Portrait": [
        "7:9 (896x1152)",   // 比例约 1.29
        "2:3 (832x1216)",   // 比例 1.50
        "4:7 (768x1344)",   // 比例 1.75
        "5:12 (640x1536)",  // 比例 2.40
    ],
    "Square": [
        "1:1 (1024x1024)",  // 比例 1.00
    ]
};

// Midjourney分辨率选项
const midjourneyResolutionOptions = {
    "Landscape": [
        "6:5 (1200x992)",   // 比例 1.21
        "4:3 (1232x928)",   // 比例 1.33
        "3:2 (1344x896)",   // 比例 1.50
        "16:9 (1456x816)",  // 比例 1.78
        "2:1 (1536x768)",   // 比例 2.00
    ],
    "Portrait": [
        "1:2 (768x1536)",   // 比例 0.50
        "9:16 (816x1456)",  // 比例 0.56
        "2:3 (896x1344)",   // 比例 0.67
        "3:4 (928x1232)",   // 比例 0.75
        "5:6 (992x1200)",   // 比例 0.83
    ],
    "Square": [
        "1:1 (1024x1024)",  // 比例 1.00
    ]
};

// 添加一个全局变量来跟踪对话框状态
let isDialogOpen = false;

// 获取默认分辨率
function getDefaultResolution(mode) {
    switch (mode) {
        case "Landscape":
            return "7:4 (1344x768)";  // SDXL默认横向
        case "Portrait":
            return "4:7 (768x1344)";  // SDXL默认纵向
        case "Square":
            return "1:1 (1024x1024)"; // 默认正方形
        default:
            return "1:1 (1024x1024)";
    }
}

// 更新自定义分辨率
function updateCustomResolution(node, width, height) {
    // 计算宽高比
    const gcd = (a, b) => b ? gcd(b, a % b) : a;
    const divisor = gcd(width, height);
    const ratio = `${width/divisor}:${height/divisor}`;
    
    // 更新分辨率选项
    const resolutionWidget = node.widgets.find(w => w.name === "resolution");
    const customOption = `${ratio} (${width}x${height})`;
    
    // 直接设置值，不更新选项列表
    resolutionWidget.value = customOption;
    
    // 触发更新
    if (resolutionWidget.callback) {
        resolutionWidget.callback(customOption);
    }
}

// 更新分辨率选项
function updatePlusResolutionOptions(node, mode, style, triggerUpdate = true) {
    console.log("[ImageSizeCreatorPlus] Updating resolution options for mode:", mode, "style:", style);
    
    // 找到分辨率widget
    const resolutionWidget = node.widgets?.find(w => w.name === "resolution");
    if (!resolutionWidget) {
        console.warn("[ImageSizeCreatorPlus] Resolution widget not found");
        return;
    }

    if (style === "Custom") {
        // Custom模式下保持当前值不变
        return;
    } else {
        // 根据风格选择对应的分辨率选项
        const resolutionOptions = style === "Midjourney" ? midjourneyResolutionOptions : sdxlResolutionOptions;
        const options = resolutionOptions[mode] || [];
        
        // 更新选项和值
        resolutionWidget.options = { values: options };
        resolutionWidget.value = options[0] || "";
    }

    // 触发widget的change事件
    if (resolutionWidget.callback) {
        resolutionWidget.callback(resolutionWidget.value);
    }

    // 只在需要时触发更新
    if (triggerUpdate) {
        requestAnimationFrame(() => {
            app.graph.setDirtyCanvas(true);
        });
    }
}

function showCustomResolutionDialog(node, onConfirm) {
    // 如果已经有对话框打开，则返回
    if (isDialogOpen) {
        console.log("[CustomDialog] Dialog already open, skipping");
        return;
    }
    
    isDialogOpen = true;
    console.log("[CustomDialog] Opening dialog");
    
    // 创建对话框
    const dialog = document.createElement("dialog");
    dialog.style.cssText = "padding: 20px; background: #333; color: white; border-radius: 8px; border: 1px solid #666;";
    
    const form = document.createElement("form");
    form.style.display = "flex";
    form.style.flexDirection = "column";
    form.style.gap = "10px";
    
    // 添加模式选择
    const modeLabel = document.createElement("label");
    modeLabel.textContent = "Mode:";
    const modeSelect = document.createElement("select");
    modeSelect.style.cssText = "padding: 5px; margin: 5px 0; background: #444; color: white; border: 1px solid #666; border-radius: 4px;";
    ["Landscape", "Portrait", "Square"].forEach(mode => {
        const option = document.createElement("option");
        option.value = option.textContent = mode;
        modeSelect.appendChild(option);
    });
    // 设置当前模式
    modeSelect.value = node.widgets.find(w => w.name === "mode").value;
    
    // 宽度输入
    const widthLabel = document.createElement("label");
    widthLabel.textContent = "Width (multiple of 8):";
    const widthInput = document.createElement("input");
    widthInput.type = "number";
    widthInput.min = "64";
    widthInput.max = "8192";
    widthInput.step = "8";
    widthInput.style.cssText = "padding: 5px; margin: 5px 0; background: #444; color: white; border: 1px solid #666; border-radius: 4px;";
    
    // 高度输入
    const heightLabel = document.createElement("label");
    heightLabel.textContent = "Height (multiple of 8):";
    const heightInput = document.createElement("input");
    heightInput.type = "number";
    heightInput.min = "64";
    heightInput.max = "8192";
    heightInput.step = "8";
    heightInput.style.cssText = "padding: 5px; margin: 5px 0; background: #444; color: white; border: 1px solid #666; border-radius: 4px;";
    
    // 获取当前分辨率的宽高
    const getCurrentDimensions = () => {
        const resolutionWidget = node.widgets.find(w => w.name === "resolution");
        const match = resolutionWidget.value.match(/\((\d+)x(\d+)\)/);
        if (match) {
            return {
                width: parseInt(match[1]),
                height: parseInt(match[2])
            };
        }
        return null;
    };
    
    // 根据模式获取默认尺寸
    function getDefaultDimensions(mode) {
        switch (mode) {
            case "Landscape":
                return { width: 1344, height: 768 };
            case "Portrait":
                return { width: 768, height: 1344 };
            case "Square":
                return { width: 1024, height: 1024 };
            default:
                return { width: 1024, height: 1024 };
        }
    }
    
    // 根据模式自动调整宽高
    function updateDimensionsByMode(mode, keepRatio = false) {
        let currentWidth = parseInt(widthInput.value) || 1024;
        let currentHeight = parseInt(heightInput.value) || 1024;
        
        if (mode === "Square") {
            // 正方形模式：使用较大的边长
            const size = Math.max(currentWidth, currentHeight);
            widthInput.value = heightInput.value = size;
        } else if (mode === "Landscape") {
            // 横向模式：确保宽度大于高度
            if (currentWidth <= currentHeight) {
                if (keepRatio) {
                    // 保持比例，交换宽高
                    [currentWidth, currentHeight] = [currentHeight, currentWidth];
                } else {
                    // 使用默认横向尺寸
                    const defaults = getDefaultDimensions("Landscape");
                    currentWidth = defaults.width;
                    currentHeight = defaults.height;
                }
            }
            widthInput.value = currentWidth;
            heightInput.value = currentHeight;
        } else if (mode === "Portrait") {
            // 纵向模式：确保高度大于宽度
            if (currentHeight <= currentWidth) {
                if (keepRatio) {
                    // 保持比例，交换宽高
                    [currentWidth, currentHeight] = [currentHeight, currentWidth];
                } else {
                    // 使用默认纵向尺寸
                    const defaults = getDefaultDimensions("Portrait");
                    currentWidth = defaults.width;
                    currentHeight = defaults.height;
                }
            }
            widthInput.value = currentWidth;
            heightInput.value = currentHeight;
        }
    }
    
    // 设置初始值
    const currentDimensions = getCurrentDimensions() || getDefaultDimensions(modeSelect.value);
    widthInput.value = currentDimensions.width;
    heightInput.value = currentDimensions.height;
    
    // 监听输入变化
    function validateAndAdjustDimensions() {
        let width = parseInt(widthInput.value);
        let height = parseInt(heightInput.value);
        
        // 确保在有效范围内
        width = Math.max(0, Math.min(8192, width));
        height = Math.max(0, Math.min(8192, height));
        
        const mode = modeSelect.value;
        if (mode === "Square") {
            // 正方形模式：使用最后修改的值
            const lastChanged = document.activeElement === widthInput ? width : height;
            widthInput.value = heightInput.value = lastChanged;
        } else if (mode === "Landscape" && width <= height) {
            // 横向模式：交换宽高
            [widthInput.value, heightInput.value] = [height, width];
        } else if (mode === "Portrait" && height <= width) {
            // 纵向模式：交换宽高
            [widthInput.value, heightInput.value] = [height, width];
        } else {
            widthInput.value = width;
            heightInput.value = height;
        }
    }
    
    widthInput.oninput = validateAndAdjustDimensions;
    heightInput.oninput = validateAndAdjustDimensions;
    
    // 监听模式变化
    modeSelect.onchange = () => {
        updateDimensionsByMode(modeSelect.value, true);
    };
    
    // 按钮容器
    const buttonContainer = document.createElement("div");
    buttonContainer.style.cssText = "display: flex; gap: 10px; justify-content: flex-end; margin-top: 10px;";
    
    // 确认按钮
    const confirmButton = document.createElement("button");
    confirmButton.textContent = "Confirm";
    confirmButton.style.cssText = "padding: 5px 15px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;";
    
    // 取消按钮
    const cancelButton = document.createElement("button");
    cancelButton.textContent = "Cancel";
    cancelButton.style.cssText = "padding: 5px 15px; background: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;";
    
    // 组装对话框
    buttonContainer.appendChild(cancelButton);
    buttonContainer.appendChild(confirmButton);
    form.appendChild(modeLabel);
    form.appendChild(modeSelect);
    form.appendChild(widthLabel);
    form.appendChild(widthInput);
    form.appendChild(heightLabel);
    form.appendChild(heightInput);
    form.appendChild(buttonContainer);
    dialog.appendChild(form);
    document.body.appendChild(dialog);
    
    // 修改关闭对话框函数
    const closeDialog = () => {
        console.log("[CustomDialog] Attempting to close dialog");
        try {
            dialog.remove();
            isDialogOpen = false;
            console.log("[CustomDialog] Dialog removed successfully");
        } catch (error) {
            console.error("[CustomDialog] Error closing dialog:", error);
        }
    };
    
    // 修改确认按钮逻辑
    confirmButton.onclick = async (e) => {
        console.log("[CustomDialog] Confirm button clicked");
        e.preventDefault();
        e.stopPropagation();
        
        let width = parseInt(widthInput.value);
        let height = parseInt(heightInput.value);
        const mode = modeSelect.value;
        
        console.log("[CustomDialog] Parsed dimensions:", { width, height, mode });
        
        // 验证输入
        if (isNaN(width) || isNaN(height) || 
            width < 64 || height < 64 || 
            width > 8192 || height > 8192) {
            console.warn("[CustomDialog] Invalid dimensions");
            alert("Please enter valid dimensions (64-8192)");
            return;
        }
        
        // 调整为最接近的8的倍数
        width = Math.round(width / 8) * 8;
        height = Math.round(height / 8) * 8;
        console.log("[CustomDialog] Adjusted dimensions:", { width, height });
        
        try {
            // 先更新模式
            const modeWidget = node.widgets.find(w => w.name === "mode");
            if (modeWidget && modeWidget.value !== mode) {
                console.log("[CustomDialog] Updating mode to:", mode);
                modeWidget.value = mode;
                await new Promise(resolve => {
                    if (modeWidget.callback) {
                        modeWidget.callback(mode);
                    }
                    resolve();
                });
            }
            
            // 调用回调并等待完成
            console.log("[CustomDialog] Calling onConfirm callback");
            await new Promise(resolve => {
                onConfirm(width, height);
                resolve();
            });
            
            // 等待一帧以确保所有更新完成
            await new Promise(resolve => requestAnimationFrame(resolve));
            
            // 最后关闭对话框
            console.log("[CustomDialog] Closing dialog");
            closeDialog();
        } catch (error) {
            console.error("[CustomDialog] Error in confirm button handler:", error);
            isDialogOpen = false;  // 确保错误时也重置状态
        }
        
        return false;
    };
    
    // 修改取消按钮逻辑
    cancelButton.onclick = (e) => {
        console.log("[CustomDialog] Cancel button clicked");
        e.preventDefault();
        e.stopPropagation();
        
        try {
            // 更新为当前mode的默认分辨率
            const modeWidget = node.widgets.find(w => w.name === "mode");
            const defaultRes = getDefaultResolution(modeWidget.value);
            const resolutionWidget = node.widgets.find(w => w.name === "resolution");
            resolutionWidget.options = { values: [defaultRes] };
            resolutionWidget.value = defaultRes;
            
            closeDialog();
            console.log("[CustomDialog] Dialog cancelled successfully");
        } catch (error) {
            console.error("[CustomDialog] Error in cancel button handler:", error);
            isDialogOpen = false;
        }
        
        return false;
    };
    
    // 显示对话框
    dialog.showModal();
    
    // 添加对话框关闭事件处理
    dialog.addEventListener('close', (e) => {
        console.log("[CustomDialog] Dialog close event triggered");
        e.preventDefault();
        e.stopPropagation();
        isDialogOpen = false;
    });
    
    // 添加表单提交处理
    form.onsubmit = (e) => {
        console.log("[CustomDialog] Form submit prevented");
        e.preventDefault();
        e.stopPropagation();
        return false;
    };
}

// 修改setupPlusSizeNode函数
function setupPlusSizeNode(nodeType, nodeData, app) {
    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function() {
        const result = onNodeCreated?.apply(this, arguments);
        
        const modeWidget = this.widgets.find(w => w.name === "mode");
        const styleWidget = this.widgets.find(w => w.name === "style");
        const resolutionWidget = this.widgets.find(w => w.name === "resolution");
        
        if (modeWidget) {
            const originalModeCallback = modeWidget.callback;
            modeWidget.callback = (value) => {
                const styleWidget = this.widgets.find(w => w.name === "style");
                if (styleWidget.value === "Custom") {
                    // 更新为新mode的默认分辨率
                    const defaultRes = getDefaultResolution(value);
                    const resolutionWidget = this.widgets.find(w => w.name === "resolution");
                    resolutionWidget.options = { values: [defaultRes] };
                    resolutionWidget.value = defaultRes;
                } else {
                    updatePlusResolutionOptions(this, value, styleWidget.value);
                }
                originalModeCallback?.call(this, value);
            };
        }
        
        if (styleWidget) {
            // 记录初始值，但不触发对话框
            styleWidget._last_value = styleWidget.value;
            
            const originalCallback = styleWidget.callback;
            styleWidget.callback = (value) => {
                if (value === "Custom") {
                    // 只在没有对话框打开时显示对话框
                    if (!isDialogOpen) {
                        showCustomResolutionDialog(this, (width, height) => {
                            updateCustomResolution(this, width, height);
                        });
                    }
                } else {
                    updatePlusResolutionOptions(this, this.widgets.find(w => w.name === "mode").value, value);
                }
                styleWidget._last_value = value;
                originalCallback?.call(this, value);
            };
        }
        
        if (resolutionWidget) {
            const originalCallback = resolutionWidget.callback;
            resolutionWidget.callback = (value) => {
                const styleWidget = this.widgets.find(w => w.name === "style");
                if (styleWidget.value === "Custom" && !isDialogOpen) {
                    showCustomResolutionDialog(this, (width, height) => {
                        updateCustomResolution(this, width, height);
                    });
                }
                originalCallback?.call(this, value);
            };
        }
        
        return result;
    };

    // 修改配置加载处理
    const onConfigure = nodeType.prototype.onConfigure;
    nodeType.prototype.onConfigure = function(config) {
        const result = onConfigure?.apply(this, arguments);
        
        const modeWidget = this.widgets?.find(w => w.name === "mode");
        const styleWidget = this.widgets?.find(w => w.name === "style");
        
        if (modeWidget && styleWidget) {
            // 记录初始值，但不触发对话框
            if (styleWidget) {
                styleWidget._last_value = styleWidget.value;
            }
            
            // 只更新分辨率选项，不显示对话框
            setTimeout(() => {
                if (styleWidget.value !== "Custom") {
                    updatePlusResolutionOptions(this, modeWidget.value, styleWidget.value, false);
                }
            }, 0);
        }

        return result;
    };

    // 添加widget更改处理
    const onPropertyChanged = nodeType.prototype.onPropertyChanged;
    nodeType.prototype.onPropertyChanged = function(property, value) {
        if (property === "mode" || property === "style") {
            const modeWidget = this.widgets?.find(w => w.name === "mode");
            const styleWidget = this.widgets?.find(w => w.name === "style");
            if (modeWidget && styleWidget) {
                updatePlusResolutionOptions(this, modeWidget.value, styleWidget.value);
            }
        }
        return onPropertyChanged?.apply(this, arguments);
    };
}

// 注册扩展
app.registerExtension({
    name: "PaintingCoder.ImageSizeCreatorPlus",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "PaintingCoder::ImageSizeCreatorPlus" || 
            nodeData.name === "PaintingCoder::ImageLatentCreatorPlus") {
            setupPlusSizeNode(nodeType, nodeData, app);
        }
    }
}); 