import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.PaintingCoder.TextCombiner",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TextCombiner") {
            // 添加 CSS 样式 - 使用更深的莫兰迪蓝
            const style = document.createElement('style');
            style.textContent = `
                .comfy-node[data-type="TextCombiner"] {
                    background-color: rgb(63, 77, 85) !important;
                    color: rgb(255, 255, 255) !important;
                }

                .comfy-node[data-type="TextCombiner"] .title-box {
                    background-color: rgb(45, 55, 65) !important;
                    color: rgb(33, 37, 41) !important;
                }

                .comfy-node[data-type="TextCombiner"]:hover {
                    background-color: rgba(63, 77, 85, 0.9) !important;
                }
            `;
            document.head.appendChild(style);

            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // 初始化状态
                this.lastConnectedCount = 0;
                this.addInput("text_1", "STRING");
                
                // 直接设置节点颜色 - 使用更深的莫兰迪蓝
                if (this.constructor.nodeData?.name === "TextCombiner") {
                    this.bgcolor = "#2e414a";  //（面板）
                    this.color = "#132832"; 
                    if (this.title_box) {
                        this.title_box.style.backgroundColor = "rgb(45, 55, 65)";  // 更深的标题栏颜色
                        this.title_box.style.color = "#212529";  // 黑色文字
                    }
                }
                
                return result;
            };

            nodeType.prototype.onConnectionsChange = function(connectionType, slot, isConnected) {
                if (connectionType === 1) {  // 输入连接
                    const connectedCount = this.inputs.reduce((count, input) => 
                        count + (input.link ? 1 : 0), 0);

                    if (connectedCount !== this.lastConnectedCount) {
                        this.lastConnectedCount = connectedCount;
                        const targetCount = connectedCount + 1;

                        while (this.inputs.length < targetCount) {
                            const newIndex = this.inputs.length + 1;
                            this.addInput(`text_${newIndex}`, "STRING");
                        }

                        while (this.inputs.length > Math.max(targetCount, 1)) {
                            const lastInput = this.inputs[this.inputs.length - 1];
                            if (!lastInput.link) {
                                this.removeInput(this.inputs.length - 1);
                            }
                        }

                        this.setSize(this.computeSize());
                        app.graph.setDirtyCanvas(true);
                    }
                }
            };
        }
    }
});