import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.ClickPopup",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // 检查是否为 ClickPopup 节点
        if (nodeData.name === "ClickPopup") {
            // 保存原始的 onNodeCreated 方法
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            // 重写 onNodeCreated 方法
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // 查找按钮组件
                const buttonWidget = this.widgets?.find(w => w.name === "button");
                if (buttonWidget) {
                    // 设置按钮点击回调
                    buttonWidget.callback = () => {
                        alert("Button clicked!");
                        // 重置按钮状态
                        buttonWidget.value = false;
                    };
                }
                return result;
            };
        }
    }
});