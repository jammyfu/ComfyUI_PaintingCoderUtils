import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.ClickPopup",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ClickPopup") {
            // 添加按钮点击事件处理
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                // 获取按钮部件
                const buttonWidget = this.widgets?.find(w => w.name === "button");
                if (buttonWidget) {
                    buttonWidget.callback = () => {
                        alert("Button clicked!");
                        // 触发按钮点击后重置状态
                        buttonWidget.value = false;
                    };
                }

                return result;
            };
        }
    }
});