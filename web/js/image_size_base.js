import { app } from "../../../scripts/app.js";

// 共享的分辨率选项
export const resolutionOptions = {
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

// 共享的更新分辨率选项函数
export function updateResolutionOptions(node, mode, triggerUpdate = true) {
    console.log("[ImageSizeBase] Updating resolution options for mode:", mode);
    
    // 找到分辨率widget
    const resolutionWidget = node.widgets?.find(w => w.name === "resolution");
    if (!resolutionWidget) {
        console.warn("[ImageSizeBase] Resolution widget not found");
        return;
    }

    // 获取新选项
    const options = resolutionOptions[mode] || [];
    
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

// 共享的节点初始化函数
export function setupSizeNode(nodeType, nodeData, app) {
    // 创建节点时的处理
    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function() {
        const result = onNodeCreated?.apply(this, arguments);

        // 初始化时更新分辨率选项
        const modeWidget = this.widgets?.find(w => w.name === "mode");
        if (modeWidget) {
            // 初始更新，但不触发画布更新
            updateResolutionOptions(this, modeWidget.value, false);

            // 监听模式变化
            modeWidget.callback = (value) => {
                console.log("[ImageSizeBase] Mode changed to:", value);
                const node = this;
                // 延迟更新以确保连接稳定
                setTimeout(() => {
                    updateResolutionOptions(node, value);
                }, 0);
            };
        }

        return result;
    };

    // 加载配置时的处理
    const onConfigure = nodeType.prototype.onConfigure;
    nodeType.prototype.onConfigure = function(config) {
        const result = onConfigure?.apply(this, arguments);
        
        // 恢复时更新分辨率选项，但不触发画布更新
        const modeWidget = this.widgets?.find(w => w.name === "mode");
        if (modeWidget) {
            console.log("[ImageSizeBase] Restoring configuration with mode:", modeWidget.value);
            const node = this;
            // 延迟更新以确保连接稳定
            setTimeout(() => {
                updateResolutionOptions(node, modeWidget.value, false);
            }, 0);
        }

        return result;
    };
} 