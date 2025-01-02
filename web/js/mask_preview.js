import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.MaskPreview",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // 检查是否为 MaskPreview 节点
        if (nodeData.name === "MaskPreview") {
            // 保存原始的 onNodeCreated 方法
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // 重写 onNodeCreated 方法
            nodeType.prototype.onNodeCreated = function() {
                // 调用原始方法
                onNodeCreated?.apply(this, arguments);
                
                // 查找预览开关组件
                const previewEnabled = this.widgets.find(w => w.name === "preview_enabled");
                if (previewEnabled) {
                    // 设置预览开关的回调函数
                    previewEnabled.callback = (value) => {
                        // 当预览状态改变时，触发节点重新执行
                        if (this.graph) {
                            app.queuePrompt();
                        }
                    };
                }
            };
        }
    }
});