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

// 更新分辨率选项
function updateLatentResolutionOptions(node, mode, triggerUpdate = true) {
    console.log("[ImageLatentCreator] Updating resolution options for mode:", mode);
    
    // 找到分辨率widget
    const resolutionWidget = node.widgets?.find(w => w.name === "resolution");
    if (!resolutionWidget) {
        console.warn("[ImageLatentCreator] Resolution widget not found");
        return;
    }

    // 获取对应模式的分辨率选项
    const options = sdxlResolutionOptions[mode] || [];
    
    // 如果选项没有变化，不进行更新
    if (JSON.stringify(resolutionWidget.options?.values) === JSON.stringify(options)) {
        return;
    }

    // 保存当前值
    const currentValue = resolutionWidget.value;

    // 更新选项
    resolutionWidget.options = { values: options };
    
    // 如果当前值在新选项中存在，保持不变
    if (options.includes(currentValue)) {
        resolutionWidget.value = currentValue;
    } else {
        resolutionWidget.value = options[0] || "";
    }

    // 只在需要时触发更新
    if (triggerUpdate) {
        requestAnimationFrame(() => {
            app.graph.setDirtyCanvas(true);
        });
    }
}

app.registerExtension({
    name: "PaintingCoder.ImageLatentCreator",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ImageLatentCreator"|| nodeData.name === "PaintingCoder::ImageLatentCreator") {
            setupSizeNode(nodeType, nodeData, app);
            
            // 创建节点时的处理
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated?.apply(this, arguments);

                // 初始化时更新分辨率选项
                const modeWidget = this.widgets?.find(w => w.name === "mode");
                
                if (modeWidget) {
                    // 初始更新，但不触发画布更新
                    updateLatentResolutionOptions(this, modeWidget.value, false);

                    // 监听模式变化
                    modeWidget.callback = (value) => {
                        console.log("[ImageLatentCreator] Mode changed to:", value);
                        updateLatentResolutionOptions(this, value);
                    };
                }

                return result;
            };

            // 加载配置时的处理
            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function(config) {
                const result = onConfigure?.apply(this, arguments);
                
                // 恢复时更新分辨率选项
                const modeWidget = this.widgets?.find(w => w.name === "mode");
                
                if (modeWidget) {
                    console.log("[ImageLatentCreator] Restoring configuration with mode:", modeWidget.value);
                    // 延迟更新以确保连接稳定
                    setTimeout(() => {
                        updateLatentResolutionOptions(this, modeWidget.value, false);
                    }, 0);
                }

                return result;
            };
            
            // 添加连接处理
            const onConnectionsChange = nodeType.prototype.onConnectionsChange;
            nodeType.prototype.onConnectionsChange = function(type, index, connected, link_info) {
                const result = onConnectionsChange?.apply(this, arguments);
                
                // 如果是 resolution 输出端口的连接变化
                if (index === 4) {
                    console.log("[ImageLatentCreator] Resolution connection changed:", {type, connected, link_info});
                }
                
                return result;
            };
        }
    }
}); 